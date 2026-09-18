import logging
from typing import List, Optional

from pydantic import BaseModel
from pymongo import (
    ASCENDING,
    MongoClient,
    UpdateOne,
)
from pymongo.collection import Collection
from pymongo.database import Database

from app.config.settings import ChunkingConfig
from app.models.parent_chunk import ParentChunk

logger = logging.getLogger(__name__)


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

    Identity model
    --------------

    parent_id
        Runtime/database identity.
        Used by ChildChunk.parent_id.

    parent_key
        Stable deterministic identity.
        Used for synchronization, evaluation, diagnostics,
        and benchmark reproducibility.

    Important
    ---------
    content_hash alone is NOT the identity of a ParentChunk.

    Two different parents may legitimately contain identical
    text and therefore have the same content_hash.
    """

    def __init__(self, config: ChunkingConfig) -> None:

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
        # Runtime parent ID.
        #
        # Mongo _id is already unique, so no additional
        # parent_id index is necessary because _id contains
        # parent_id in our serialization.
        # ----------------------------------------------------

        # ----------------------------------------------------
        # Stable benchmark/persistence identity.
        # ----------------------------------------------------

        self.collection.create_index(
            [
                ("parent_key", ASCENDING),
            ],
            unique=True,
            name="uq_parent_key",
        )

        # ----------------------------------------------------
        # Efficient ordered lookup for a document.
        #
        # Deliberately NOT unique.
        #
        # During synchronization, a changed parent may
        # temporarily coexist with its stale predecessor
        # before stale deletion occurs.
        # ----------------------------------------------------

        self.collection.create_index(
            [
                ("document_id", ASCENDING),
                ("parent_index", ASCENDING),
            ],
            name="ix_document_parent_index",
        )

        # ----------------------------------------------------
        # Useful for diagnostics / versioning / integrity.
        #
        # NOT unique because identical content may appear
        # legitimately in multiple parents.
        # ----------------------------------------------------

        self.collection.create_index(
            [
                ("document_id", ASCENDING),
                ("content_hash", ASCENDING),
            ],
            name="ix_document_content_hash",
        )

        logger.debug(
            "MongoDB indexes ready for collection=%s",
            self.collection.name,
        )

    # ========================================================
    # SERIALIZATION
    # ========================================================

    @staticmethod
    def _to_document(
        parent: ParentChunk,
    ) -> dict:

        document = parent.model_dump(mode="python")

        # Mongo _id stores the runtime parent ID.
        document["_id"] = parent.parent_id

        return document

    # ========================================================
    # DESERIALIZATION
    # ========================================================

    @staticmethod
    def _from_document(document: dict) -> ParentChunk:
        document = document.copy()
        document.pop(
            "_id",
            None,
        )

        return ParentChunk.model_validate(document)

    # ========================================================
    # UPSERT ONE
    # ========================================================

    def upsert_parent(self, parent: ParentChunk) -> bool:

        document = self._to_document(parent)
        result = self.collection.update_one(
            {
                "parent_key": parent.parent_key,
            },
            {
                "$setOnInsert": document,
            },
            upsert=True,
        )

        inserted = result.upserted_id is not None

        logger.debug(
            "Parent upsert: parent_key=%s inserted=%s",
            parent.parent_key,
            inserted,
        )

        return inserted

    # ========================================================
    # UPSERT MANY
    # ========================================================

    def upsert_parents(
        self,
        parents: List[ParentChunk],
    ) -> int:

        if not parents:
            return 0

        self._validate_unique_parent_keys(parents)
        operations = []

        for parent in parents:
            document = self._to_document(parent)
            operations.append(
                UpdateOne(
                    {
                        "parent_key": (parent.parent_key),
                    },
                    {
                        "$setOnInsert": document,
                    },
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

        self._validate_document_membership(
            document_id=document_id,
            parents=parents,
        )

        self._validate_unique_parent_keys(parents)

        # ----------------------------------------------------
        # READ CURRENT STATE
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
        # EXISTING STABLE KEYS
        # ----------------------------------------------------

        existing_keys = {document["parent_key"] for document in existing_documents}

        # ----------------------------------------------------
        # INCOMING STABLE KEYS
        # ----------------------------------------------------

        incoming_by_key = {parent.parent_key: parent for parent in parents}

        incoming_keys = set(incoming_by_key.keys())

        # ----------------------------------------------------
        # CLASSIFY
        # ----------------------------------------------------

        new_keys = incoming_keys - existing_keys
        unchanged_keys = incoming_keys & existing_keys
        stale_keys = existing_keys - incoming_keys

        # ----------------------------------------------------
        # INSERT NEW PARENTS
        # ----------------------------------------------------
        #
        # New records are inserted BEFORE stale records are
        # deleted.
        #
        # Therefore a failed insertion leaves the previous
        # valid state intact.
        # ----------------------------------------------------

        operations = []

        for parent_key in new_keys:
            parent = incoming_by_key[parent_key]
            document = self._to_document(parent)

            operations.append(
                UpdateOne(
                    {
                        "parent_key": parent_key,
                    },
                    {
                        "$setOnInsert": document,
                    },
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

        deleted_stale_count = 0

        if stale_keys:
            delete_result = self.collection.delete_many(
                {
                    "document_id": (document_id),
                    "parent_key": {"$in": list(stale_keys)},
                }
            )

            deleted_stale_count = delete_result.deleted_count

        # ----------------------------------------------------
        # FINAL COUNT
        # ----------------------------------------------------

        final_count = self.count_by_document_id(document_id)

        sync_result = ParentSyncResult(
            incoming_count=len(parents),
            existing_count_before=(existing_count_before),
            inserted_count=(inserted_count),
            unchanged_count=len(unchanged_keys),
            deleted_stale_count=(deleted_stale_count),
            final_count=final_count,
        )

        logger.info(
            (
                "Parent sync document_id=%s "
                "incoming=%d existing=%d "
                "inserted=%d unchanged=%d "
                "deleted_stale=%d final=%d"
            ),
            document_id,
            sync_result.incoming_count,
            sync_result.existing_count_before,
            sync_result.inserted_count,
            sync_result.unchanged_count,
            sync_result.deleted_stale_count,
            sync_result.final_count,
        )

        return sync_result

    # ========================================================
    # GET BY RUNTIME PARENT ID
    # ========================================================

    def get_by_id(self, parent_id: str) -> Optional[ParentChunk]:

        document = self.collection.find_one(
            {
                "_id": parent_id,
            }
        )

        if document is None:
            return None

        return self._from_document(document)

    # ========================================================
    # GET BY STABLE PARENT KEY
    # ========================================================

    def get_by_key(
        self,
        parent_key: str,
    ) -> Optional[ParentChunk]:

        document = self.collection.find_one(
            {
                "parent_key": parent_key,
            }
        )

        if document is None:
            return None

        return self._from_document(document)

    # ========================================================
    # GET BY DOCUMENT ID
    # ========================================================

    def get_by_document_id(self, document_id: str) -> List[ParentChunk]:

        cursor = self.collection.find(
            {
                "document_id": (document_id),
            }
        ).sort(
            "parent_index",
            ASCENDING,
        )

        return [self._from_document(document) for document in cursor]

    # ========================================================
    # COUNT
    # ========================================================

    def count(self) -> int:
        return self.collection.count_documents({})

    def count_by_document_id(self, document_id: str) -> int:
        return self.collection.count_documents(
            {
                "document_id": document_id,
            }
        )

    # ========================================================
    # DELETE
    # ========================================================

    def delete_by_document_id(self, document_id: str) -> int:
        result = self.collection.delete_many(
            {
                "document_id": document_id,
            }
        )

        return result.deleted_count

    # ========================================================
    # VALIDATION
    # ========================================================

    @staticmethod
    def _validate_document_membership(
        document_id: str,
        parents: List[ParentChunk],
    ) -> None:

        for parent in parents:
            if parent.document_id != document_id:
                raise ValueError(
                    "All ParentChunks must belong " "to the supplied document_id."
                )

    @staticmethod
    def _validate_unique_parent_keys(parents: List[ParentChunk]) -> None:

        parent_keys = [parent.parent_key for parent in parents]
        if len(parent_keys) != len(set(parent_keys)):
            raise ValueError(
                "Duplicate parent_key values " "detected in incoming parents."
            )

    # ========================================================
    # CONNECTION TEST
    # ========================================================

    def ping(self) -> bool:
        self.client.admin.command("ping")
        return True

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self) -> None:
        self.client.close()
