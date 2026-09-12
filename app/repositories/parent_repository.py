from typing import List, Optional

from pydantic import BaseModel
from pymongo import (
    MongoClient,
    ASCENDING,
    UpdateOne,
)
from pymongo.collection import Collection
from pymongo.database import Database

from app.config.settings import ChunkingConfig
from app.models.parent_chunk import ParentChunk

# ============================================================
# SYNC RESULT
# ============================================================


class ParentSyncResult(BaseModel):

    incoming_count: int

    existing_count_before: int

    inserted_count: int

    unchanged_count: int

    deleted_stale_count: int

    final_count: int


# ============================================================
# PARENT REPOSITORY
# ============================================================


class ParentRepository:
    """
    MongoDB repository for ParentChunk persistence.

    Responsibilities
    ----------------
    - Persist ParentChunk objects
    - Retrieve ParentChunk objects
    - Provide idempotent ingestion
    - Synchronize stored parents with the current document
    """

    def __init__(
        self,
        config: ChunkingConfig,
    ):

        self.config = config

        self.client = MongoClient(config.mongodb_uri)

        self.database: Database = self.client[config.mongodb_database]

        self.collection: Collection = self.database[config.mongodb_parent_collection]

        self._create_indexes()

    # ========================================================
    # INDEXES
    # ========================================================

    def _create_indexes(
        self,
    ) -> None:

        # ----------------------------------------------------
        # Efficient retrieval of a document's parents
        # in document order.
        # ----------------------------------------------------

        self.collection.create_index(
            [
                ("document_id", ASCENDING),
                ("parent_index", ASCENDING),
            ],
        )

        # ----------------------------------------------------
        # Current idempotency rule.
        #
        # Same document + same parent content
        # should not be stored twice.
        # ----------------------------------------------------

        self.collection.create_index(
            [
                ("document_id", ASCENDING),
                ("content_hash", ASCENDING),
            ],
            unique=True,
        )

    # ========================================================
    # SERIALIZATION
    # ========================================================

    @staticmethod
    def _to_document(
        parent: ParentChunk,
    ) -> dict:

        document = parent.model_dump(mode="python")

        document["_id"] = parent.parent_id

        return document

    # ========================================================
    # DESERIALIZATION
    # ========================================================

    @staticmethod
    def _from_document(
        document: dict,
    ) -> ParentChunk:

        document = document.copy()

        document.pop(
            "_id",
            None,
        )

        return ParentChunk.model_validate(document)

    # ========================================================
    # UPSERT ONE
    # ========================================================

    def upsert_parent(
        self,
        parent: ParentChunk,
    ) -> bool:

        document = self._to_document(parent)

        result = self.collection.update_one(
            {
                "document_id": parent.document_id,
                "content_hash": parent.content_hash,
            },
            {"$setOnInsert": document},
            upsert=True,
        )

        return result.upserted_id is not None

    # ========================================================
    # UPSERT MANY
    # ========================================================

    def upsert_parents(
        self,
        parents: List[ParentChunk],
    ) -> int:

        if not parents:
            return 0

        operations = []

        for parent in parents:

            document = self._to_document(parent)

            operations.append(
                UpdateOne(
                    {
                        "document_id": parent.document_id,
                        "content_hash": parent.content_hash,
                    },
                    {"$setOnInsert": document},
                    upsert=True,
                )
            )

        result = self.collection.bulk_write(operations)

        return result.upserted_count

    # ========================================================
    # SYNCHRONIZE DOCUMENT PARENTS
    # ========================================================

    def sync_parents(
        self,
        document_id: str,
        parents: List[ParentChunk],
    ) -> ParentSyncResult:

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        for parent in parents:

            if parent.document_id != document_id:

                raise ValueError(
                    "All ParentChunks must belong " "to the supplied document_id."
                )

        # ----------------------------------------------------
        # READ CURRENT DATABASE STATE
        # ----------------------------------------------------

        existing_documents = list(
            self.collection.find(
                {
                    "document_id": document_id,
                }
            )
        )

        existing_count_before = len(existing_documents)

        # ----------------------------------------------------
        # EXISTING HASHES
        # ----------------------------------------------------

        existing_hashes = {document["content_hash"] for document in existing_documents}

        # ----------------------------------------------------
        # INCOMING HASHES
        # ----------------------------------------------------

        incoming_by_hash = {parent.content_hash: parent for parent in parents}

        incoming_hashes = set(incoming_by_hash.keys())

        # ----------------------------------------------------
        # CLASSIFY
        # ----------------------------------------------------

        new_hashes = incoming_hashes - existing_hashes

        unchanged_hashes = incoming_hashes & existing_hashes

        stale_hashes = existing_hashes - incoming_hashes

        # ----------------------------------------------------
        # INSERT NEW PARENTS
        # ----------------------------------------------------

        operations = []

        for content_hash in new_hashes:

            parent = incoming_by_hash[content_hash]

            document = self._to_document(parent)

            operations.append(
                UpdateOne(
                    {
                        "document_id": document_id,
                        "content_hash": content_hash,
                    },
                    {"$setOnInsert": document},
                    upsert=True,
                )
            )

        inserted_count = 0

        if operations:

            result = self.collection.bulk_write(operations)

            inserted_count = result.upserted_count

        # ----------------------------------------------------
        # DELETE STALE PARENTS
        # ----------------------------------------------------
        #
        # We intentionally insert new records BEFORE deleting
        # stale ones.
        #
        # If insertion fails, the old data still exists.
        # ----------------------------------------------------

        deleted_stale_count = 0

        if stale_hashes:

            delete_result = self.collection.delete_many(
                {
                    "document_id": document_id,
                    "content_hash": {"$in": list(stale_hashes)},
                }
            )

            deleted_stale_count = delete_result.deleted_count

        # ----------------------------------------------------
        # FINAL COUNT
        # ----------------------------------------------------

        final_count = self.count_by_document_id(document_id)

        return ParentSyncResult(
            incoming_count=len(parents),
            existing_count_before=(existing_count_before),
            inserted_count=(inserted_count),
            unchanged_count=len(unchanged_hashes),
            deleted_stale_count=(deleted_stale_count),
            final_count=final_count,
        )

    # ========================================================
    # GET BY PARENT ID
    # ========================================================

    def get_by_id(
        self,
        parent_id: str,
    ) -> Optional[ParentChunk]:

        document = self.collection.find_one(
            {
                "_id": parent_id,
            }
        )

        if document is None:
            return None

        return self._from_document(document)

    # ========================================================
    # GET BY DOCUMENT ID
    # ========================================================

    def get_by_document_id(
        self,
        document_id: str,
    ) -> List[ParentChunk]:

        cursor = self.collection.find(
            {
                "document_id": document_id,
            }
        ).sort(
            "parent_index",
            ASCENDING,
        )

        return [self._from_document(document) for document in cursor]

    # ========================================================
    # COUNT
    # ========================================================

    def count(
        self,
    ) -> int:

        return self.collection.count_documents({})

    def count_by_document_id(
        self,
        document_id: str,
    ) -> int:

        return self.collection.count_documents(
            {
                "document_id": document_id,
            }
        )

    # ========================================================
    # DELETE
    # ========================================================

    def delete_by_document_id(
        self,
        document_id: str,
    ) -> int:

        result = self.collection.delete_many(
            {
                "document_id": document_id,
            }
        )

        return result.deleted_count

    # ========================================================
    # CONNECTION TEST
    # ========================================================

    def ping(
        self,
    ) -> bool:

        self.client.admin.command("ping")

        return True

    # ========================================================
    # CLOSE
    # ========================================================

    def close(
        self,
    ) -> None:

        self.client.close()
