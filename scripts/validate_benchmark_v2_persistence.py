import hashlib
import json
import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.models import Filter

from app.config.settings import (
    ChunkingConfig,
    HybridSearchConfig,
)
from app.repositories.parent_repository import (
    ParentRepository,
)
from app.utils.document_id import extract_document_id
from app.utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIRECTORY = PROJECT_ROOT / "data" / "documents"
MANIFEST_PATH = PROJECT_ROOT / "data" / "benchmark" / "manifest.json"


# ============================================================
# BENCHMARK EXPECTATIONS
# ============================================================

EXPECTED_DOCUMENT_COUNT = 24
EXPECTED_PARENT_COUNT = 120
EXPECTED_CHILD_COUNT = 196
EXPECTED_CORPUS_SHA256 = (
    "16c01b5dfb1753d0b55dafdf6164d977" "383c0419c4ebfe8b376189aaf7ef9e62"
)

SMOKE_TEST_DOCUMENT_ID = "DOC-TEST-001"


# ============================================================
# VALIDATION RESULT
# ============================================================


class PersistenceValidationResult(BaseModel):
    """
    Summary of the Benchmark V2 persistence validation.

    This gives us one structured object that can later be:
        - logged
        - serialized
        - persisted into benchmark reports
        - consumed by CI
    """

    mongo_document_count: int
    qdrant_document_count: int

    mongo_parent_count: int
    qdrant_child_count: int

    unique_parent_keys: int
    unique_child_keys: int

    child_parent_id_failures: int
    child_parent_key_failures: int

    corpus_sha256: str

    passed: bool


# ============================================================
# BENCHMARK V2 PERSISTENCE VALIDATOR
# ============================================================


class BenchmarkV2PersistenceValidator:
    """
    Validates the persisted Benchmark V2 universe.

    Benchmark V2 consists of two persistence layers:

        MongoDB
            authoritative ParentChunk store

        Qdrant
            ChildChunk retrieval/search store

    The validator checks both stores independently and then
    verifies the referential relationship between them.

    Important architectural invariant:

        Qdrant ChildChunk.parent_id
                ->
        Mongo ParentChunk.parent_id

    and:

        Qdrant ChildChunk.parent_key
                ->
        Mongo ParentChunk.parent_key

    Both relationships must agree.
    """

    def __init__(
        self,
        chunking_config: ChunkingConfig,
        hybrid_config: HybridSearchConfig,
    ) -> None:

        self.chunking_config = chunking_config
        self.hybrid_config = hybrid_config

        # MongoDB is accessed through the repository abstraction
        # rather than bypassing the project persistence layer.
        self.parent_repository = ParentRepository(chunking_config)

        qdrant_url = (
            f"http://{chunking_config.qdrant_host}:" f"{chunking_config.qdrant_port}"
        )

        self.qdrant_client = QdrantClient(url=qdrant_url)

    # ========================================================
    # PUBLIC VALIDATION ENTRY POINT
    # ========================================================

    def validate(
        self,
    ) -> PersistenceValidationResult:
        """
        Run every Benchmark V2 persistence invariant.

        Any failed invariant raises RuntimeError immediately.

        A successful return therefore means the persisted
        ParentChunk/ChildChunk universe is safe to freeze.
        """

        logger.info("Starting Benchmark V2 persistence validation.")

        expected_document_ids = self._build_expected_document_ids()

        # ----------------------------------------------------
        # MongoDB state
        # ----------------------------------------------------

        mongo_parents = self._load_all_mongo_parents()
        mongo_document_ids = {parent.document_id for parent in mongo_parents}
        parent_ids = {parent.parent_id for parent in mongo_parents}
        parent_keys = {parent.parent_key for parent in mongo_parents}
        parent_key_by_id = {
            parent.parent_id: parent.parent_key for parent in mongo_parents
        }

        # ----------------------------------------------------
        # Qdrant state
        # ----------------------------------------------------

        qdrant_children = self._load_all_qdrant_children()
        qdrant_document_ids = {child["document_id"] for child in qdrant_children}
        child_keys = {child["child_key"] for child in qdrant_children}

        # ----------------------------------------------------
        # Validate document universe
        # ----------------------------------------------------

        self._validate_document_ids(
            source_name="MongoDB",
            actual_document_ids=mongo_document_ids,
            expected_document_ids=expected_document_ids,
        )

        self._validate_document_ids(
            source_name="Qdrant",
            actual_document_ids=qdrant_document_ids,
            expected_document_ids=expected_document_ids,
        )

        # ----------------------------------------------------
        # Validate smoke-test contamination is gone
        # ----------------------------------------------------

        self._validate_no_smoke_test_data(
            mongo_document_ids=mongo_document_ids,
            qdrant_document_ids=qdrant_document_ids,
        )

        # ----------------------------------------------------
        # Validate expected persistence counts
        # ----------------------------------------------------

        self._validate_count(
            name="Mongo parent count",
            actual=len(mongo_parents),
            expected=EXPECTED_PARENT_COUNT,
        )

        self._validate_count(
            name="Qdrant child count",
            actual=len(qdrant_children),
            expected=EXPECTED_CHILD_COUNT,
        )

        # ----------------------------------------------------
        # Validate stable-key uniqueness
        # ----------------------------------------------------

        self._validate_parent_key_uniqueness(
            mongo_parents=mongo_parents,
            unique_parent_keys=parent_keys,
        )

        self._validate_child_key_uniqueness(
            qdrant_children=qdrant_children,
            unique_child_keys=child_keys,
        )

        # ----------------------------------------------------
        # Validate cross-store referential integrity
        # ----------------------------------------------------

        (
            child_parent_id_failures,
            child_parent_key_failures,
        ) = self._validate_child_parent_references(
            qdrant_children=qdrant_children,
            parent_ids=parent_ids,
            parent_key_by_id=parent_key_by_id,
        )

        # ----------------------------------------------------
        # Validate corpus fingerprint
        # ----------------------------------------------------

        corpus_sha256 = self._calculate_corpus_sha256()

        self._validate_manifest_fingerprint(corpus_sha256)

        result = PersistenceValidationResult(
            mongo_document_count=len(mongo_document_ids),
            qdrant_document_count=len(qdrant_document_ids),
            mongo_parent_count=len(mongo_parents),
            qdrant_child_count=len(qdrant_children),
            unique_parent_keys=len(parent_keys),
            unique_child_keys=len(child_keys),
            child_parent_id_failures=(child_parent_id_failures),
            child_parent_key_failures=(child_parent_key_failures),
            corpus_sha256=corpus_sha256,
            passed=True,
        )

        self._log_summary(result)

        return result

    # ========================================================
    # EXPECTED DOCUMENT IDS
    # ========================================================

    @staticmethod
    def _build_expected_document_ids() -> set[str]:
        """
        Benchmark V2 currently contains DOC-001 through DOC-024.
        """

        return {
            f"DOC-{index:03d}"
            for index in range(
                1,
                EXPECTED_DOCUMENT_COUNT + 1,
            )
        }

    # ========================================================
    # MONGODB LOAD
    # ========================================================

    def _load_all_mongo_parents(
        self,
    ) -> list[Any]:
        """
        Load all Benchmark V2 parents through the repository's
        Mongo collection.

        ParentRepository currently provides document-scoped
        retrieval, so we use the collection for the global
        validation pass while still relying on the repository
        for configuration and serialization conventions.
        """

        documents = list(self.parent_repository.collection.find({}))

        parents = [
            self.parent_repository._from_document(document) for document in documents
        ]

        logger.info(f"mongo_parent_count={len(parents)}")

        return parents

    # ========================================================
    # QDRANT LOAD
    # ========================================================

    def _load_all_qdrant_children(
        self,
    ) -> list[dict[str, Any]]:
        """
        Scroll through every child payload in the Benchmark V2
        Qdrant collection.

        Qdrant scroll pagination is used because retrieval query
        limits must not determine validation completeness.
        """

        collection_name = self.hybrid_config.collection_name
        children: list[dict[str, Any]] = []
        next_offset = None

        while True:

            points, next_offset = self.qdrant_client.scroll(
                collection_name=collection_name,
                scroll_filter=Filter(),
                limit=100,
                offset=next_offset,
                with_payload=True,
                with_vectors=False,
            )

            for point in points:

                if point.payload is None:
                    raise RuntimeError(
                        f"Qdrant point has no payload: " f"point_id={point.id}"
                    )

                payload = dict(point.payload)

                self._validate_required_child_payload(
                    point_id=str(point.id),
                    payload=payload,
                )

                children.append(payload)

            if next_offset is None:
                break

        logger.info(f"qdrant_child_count=" f"{len(children)}")

        return children

    # ========================================================
    # REQUIRED QDRANT PAYLOAD
    # ========================================================

    @staticmethod
    def _validate_required_child_payload(
        point_id: str,
        payload: dict[str, Any],
    ) -> None:
        """
        Every Qdrant child must expose these identifiers.

        These fields form the persistence/evaluation contract
        introduced in Benchmark V2.
        """

        required_fields = {
            "document_id",
            "parent_id",
            "parent_key",
            "child_id",
            "child_key",
        }

        missing_fields = required_fields - payload.keys()

        if missing_fields:
            raise RuntimeError(
                f"Qdrant child payload is missing "
                f"required fields. "
                f"point_id={point_id} "
                f"missing_fields="
                f"{sorted(missing_fields)}"
            )

    # ========================================================
    # DOCUMENT ID VALIDATION
    # ========================================================

    @staticmethod
    def _validate_document_ids(
        source_name: str,
        actual_document_ids: set[str],
        expected_document_ids: set[str],
    ) -> None:

        missing_document_ids = expected_document_ids - actual_document_ids

        unexpected_document_ids = actual_document_ids - expected_document_ids

        if missing_document_ids or unexpected_document_ids:
            raise RuntimeError(
                f"{source_name} document universe mismatch. "
                f"missing_document_ids="
                f"{sorted(missing_document_ids)} "
                f"unexpected_document_ids="
                f"{sorted(unexpected_document_ids)}"
            )

        logger.info(
            f"{source_name.lower()}_document_count=" f"{len(actual_document_ids)}"
        )

    # ========================================================
    # SMOKE DATA VALIDATION
    # ========================================================

    @staticmethod
    def _validate_no_smoke_test_data(
        mongo_document_ids: set[str],
        qdrant_document_ids: set[str],
    ) -> None:

        if SMOKE_TEST_DOCUMENT_ID in mongo_document_ids:
            raise RuntimeError(
                f"Smoke-test document remains in MongoDB: " f"{SMOKE_TEST_DOCUMENT_ID}"
            )

        if SMOKE_TEST_DOCUMENT_ID in qdrant_document_ids:
            raise RuntimeError(
                f"Smoke-test document remains in Qdrant: " f"{SMOKE_TEST_DOCUMENT_ID}"
            )

        logger.info("smoke_test_data_present=False")

    # ========================================================
    # COUNT VALIDATION
    # ========================================================

    @staticmethod
    def _validate_count(
        name: str,
        actual: int,
        expected: int,
    ) -> None:

        if actual != expected:
            raise RuntimeError(
                f"{name} mismatch. " f"expected={expected} " f"actual={actual}"
            )

    # ========================================================
    # PARENT KEY UNIQUENESS
    # ========================================================

    @staticmethod
    def _validate_parent_key_uniqueness(
        mongo_parents: list[Any],
        unique_parent_keys: set[str],
    ) -> None:

        if len(mongo_parents) != len(unique_parent_keys):
            raise RuntimeError("Duplicate parent_key values detected " "in MongoDB.")

        logger.info(f"unique_parent_keys=" f"{len(unique_parent_keys)}")

    # ========================================================
    # CHILD KEY UNIQUENESS
    # ========================================================

    @staticmethod
    def _validate_child_key_uniqueness(
        qdrant_children: list[dict[str, Any]],
        unique_child_keys: set[str],
    ) -> None:

        if len(qdrant_children) != len(unique_child_keys):
            raise RuntimeError("Duplicate child_key values detected " "in Qdrant.")

        logger.info(f"unique_child_keys=" f"{len(unique_child_keys)}")

    # ========================================================
    # CROSS-STORE REFERENTIAL INTEGRITY
    # ========================================================

    @staticmethod
    def _validate_child_parent_references(
        qdrant_children: list[dict[str, Any]],
        parent_ids: set[str],
        parent_key_by_id: dict[
            str,
            str,
        ],
    ) -> tuple[int, int]:
        """
        Verify both child -> parent relationships.

        Check 1:
            child.parent_id must exist in MongoDB.

        Check 2:
            the child.parent_key must equal the parent_key
            belonging to that exact parent_id.

        The second check is stronger than independently checking
        whether the parent_key merely exists somewhere.
        """

        parent_id_failures = 0
        parent_key_failures = 0

        for child in qdrant_children:
            parent_id = child["parent_id"]
            parent_key = child["parent_key"]

            if parent_id not in parent_ids:
                parent_id_failures += 1
                logger.error(
                    f"Missing Mongo parent "
                    f"child_id={child['child_id']} "
                    f"parent_id={parent_id}"
                )

                # If parent_id does not exist, there is no valid
                # parent_key pair to compare against.
                continue

            expected_parent_key = parent_key_by_id[parent_id]

            if parent_key != expected_parent_key:

                parent_key_failures += 1

                logger.error(
                    f"Parent reference mismatch "
                    f"child_id={child['child_id']} "
                    f"parent_id={parent_id} "
                    f"child_parent_key="
                    f"{parent_key} "
                    f"mongo_parent_key="
                    f"{expected_parent_key}"
                )

        if parent_id_failures:
            raise RuntimeError(
                f"Found {parent_id_failures} " f"child parent_id failures."
            )

        if parent_key_failures:
            raise RuntimeError(
                f"Found {parent_key_failures} " f"child parent_key failures."
            )

        logger.info("child_parent_id_failures=0")
        logger.info("child_parent_key_failures=0")

        return (
            parent_id_failures,
            parent_key_failures,
        )

    # ========================================================
    # CORPUS FINGERPRINT
    # ========================================================

    @staticmethod
    def _calculate_corpus_sha256() -> str:
        """
        Reproduce the exact corpus hashing strategy used by
        build_benchmark_manifest.py.

        Hash input order is deterministic because filenames are
        sorted before hashing.
        """

        markdown_files = sorted(DOCUMENTS_DIRECTORY.glob("DOC-*.md"))

        corpus_hasher = hashlib.sha256()

        for file_path in markdown_files:
            document_id = extract_document_id(file_path)
            text = file_path.read_text(encoding="utf-8")
            corpus_hasher.update(document_id.encode("utf-8"))
            corpus_hasher.update(b"\0")
            corpus_hasher.update(text.encode("utf-8"))
            corpus_hasher.update(b"\0")

        return corpus_hasher.hexdigest()

    # ========================================================
    # MANIFEST VALIDATION
    # ========================================================

    @staticmethod
    def _validate_manifest_fingerprint(
        calculated_corpus_sha256: str,
    ) -> None:

        if not MANIFEST_PATH.exists():
            raise FileNotFoundError(
                f"Benchmark manifest not found: " f"{MANIFEST_PATH}"
            )

        with MANIFEST_PATH.open(
            "r",
            encoding="utf-8",
        ) as file:

            manifest = json.load(file)

        manifest_sha256 = manifest.get("corpus_sha256")

        benchmark_version = manifest.get("benchmark_version")

        if benchmark_version != "2.0":
            raise RuntimeError(
                f"Unexpected benchmark_version. "
                f"expected=2.0 "
                f"actual={benchmark_version}"
            )

        if calculated_corpus_sha256 != manifest_sha256:
            raise RuntimeError(
                f"Corpus fingerprint does not match "
                f"manifest. "
                f"calculated="
                f"{calculated_corpus_sha256} "
                f"manifest={manifest_sha256}"
            )

        if calculated_corpus_sha256 != EXPECTED_CORPUS_SHA256:
            raise RuntimeError(
                f"Corpus fingerprint differs from "
                f"the canonical Benchmark V2 "
                f"fingerprint. "
                f"expected="
                f"{EXPECTED_CORPUS_SHA256} "
                f"actual="
                f"{calculated_corpus_sha256}"
            )

        logger.info(f"benchmark_version=" f"{benchmark_version}")

        logger.info(f"corpus_sha256=" f"{calculated_corpus_sha256}")

    # ========================================================
    # SUMMARY
    # ========================================================

    @staticmethod
    def _log_summary(
        result: PersistenceValidationResult,
    ) -> None:

        logger.info("Benchmark V2 persistence validation summary")
        logger.info(f"mongo_document_count=" f"{result.mongo_document_count}")
        logger.info(f"qdrant_document_count=" f"{result.qdrant_document_count}")
        logger.info(f"mongo_parent_count=" f"{result.mongo_parent_count}")
        logger.info(f"qdrant_child_count=" f"{result.qdrant_child_count}")
        logger.info(f"unique_parent_keys=" f"{result.unique_parent_keys}")
        logger.info(f"unique_child_keys=" f"{result.unique_child_keys}")
        logger.info(f"child_parent_id_failures=" f"{result.child_parent_id_failures}")
        logger.info(f"child_parent_key_failures=" f"{result.child_parent_key_failures}")
        logger.info(f"corpus_sha256=" f"{result.corpus_sha256}")
        logger.info("Benchmark V2 persistence validation PASSED.")

    # ========================================================
    # CLEANUP
    # ========================================================

    def close(
        self,
    ) -> None:
        self.parent_repository.close()


# ============================================================
# MAIN
# ============================================================


def main() -> None:

    chunking_config = ChunkingConfig()
    hybrid_config = HybridSearchConfig()

    logger.info(f"mongodb_collection=" f"{chunking_config.mongodb_parent_collection}")

    logger.info(f"qdrant_collection=" f"{hybrid_config.collection_name}")

    validator = BenchmarkV2PersistenceValidator(
        chunking_config=chunking_config,
        hybrid_config=hybrid_config,
    )

    try:
        validator.validate()
    finally:
        validator.close()


if __name__ == "__main__":
    configure_logging()
    main()
