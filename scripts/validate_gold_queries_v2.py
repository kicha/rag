import json
import logging
from pathlib import Path
from typing import Any

from app.evaluation.gold_models import (
    AnnotationStatus,
    Answerability,
    GoldDatasetV2,
)
from app.utils.logging_config import (
    configure_logging,
)

logger = logging.getLogger(__name__)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

BENCHMARK_DIRECTORY = PROJECT_ROOT / "data" / "benchmark"

GOLD_PATH = BENCHMARK_DIRECTORY / "gold_queries_v2_draft.json"

UNITS_PATH = BENCHMARK_DIRECTORY / "benchmark_v2_units.json"

MANIFEST_PATH = BENCHMARK_DIRECTORY / "manifest.json"


# ============================================================
# JSON LOADING
# ============================================================


def load_json(
    path: Path,
) -> Any:

    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


# ============================================================
# VALIDATOR
# ============================================================


class GoldDatasetV2Validator:
    """
    Validate the gold dataset against the frozen Benchmark V2
    document/parent/child universe.
    """

    def __init__(
        self,
        dataset: GoldDatasetV2,
        units_data: dict[str, Any],
        manifest: dict[str, Any],
    ) -> None:

        self.dataset = dataset
        self.units_data = units_data
        self.manifest = manifest

        self.document_ids: set[str] = set()

        self.parent_keys: set[str] = set()

        self.child_keys: set[str] = set()

        self.parent_document_by_key: dict[
            str,
            str,
        ] = {}

        self.child_parent_by_key: dict[
            str,
            str,
        ] = {}

        self._build_unit_indexes()

    # --------------------------------------------------------
    # BUILD LOOKUP INDEXES
    # --------------------------------------------------------

    def _build_unit_indexes(
        self,
    ) -> None:

        for parent in self.units_data["parents"]:

            document_id = parent["document_id"]

            parent_key = parent["parent_key"]

            self.document_ids.add(document_id)

            self.parent_keys.add(parent_key)

            self.parent_document_by_key[parent_key] = document_id

            for child in parent["children"]:

                child_key = child["child_key"]

                self.child_keys.add(child_key)

                self.child_parent_by_key[child_key] = parent_key

    # --------------------------------------------------------
    # PUBLIC VALIDATION
    # --------------------------------------------------------

    def validate(
        self,
    ) -> None:

        self._validate_dataset_identity()

        self._validate_unit_counts()

        for query in self.dataset.queries:

            self._validate_query(query)

        logger.info(f"query_count=" f"{self.dataset.query_count}")

        logger.info(f"curated_query_count=" f"{self.dataset.curated_query_count}")

        logger.info("Benchmark V2 gold validation PASSED.")

    # --------------------------------------------------------
    # BENCHMARK IDENTITY
    # --------------------------------------------------------

    def _validate_dataset_identity(
        self,
    ) -> None:

        if self.dataset.benchmark_version != self.manifest["benchmark_version"]:
            raise RuntimeError("Gold benchmark_version does not " "match manifest.")

        if self.dataset.corpus_sha256 != self.manifest["corpus_sha256"]:
            raise RuntimeError("Gold corpus_sha256 does not " "match manifest.")

    # --------------------------------------------------------
    # UNIT COUNTS
    # --------------------------------------------------------

    def _validate_unit_counts(
        self,
    ) -> None:

        if len(self.parent_keys) != 120:
            raise RuntimeError(
                f"Expected 120 parents, " f"found {len(self.parent_keys)}."
            )

        if len(self.child_keys) != 196:
            raise RuntimeError(
                f"Expected 196 children, " f"found {len(self.child_keys)}."
            )

    # --------------------------------------------------------
    # QUERY VALIDATION
    # --------------------------------------------------------

    def _validate_query(
        self,
        query,
    ) -> None:

        # ----------------------------------------------------
        # Document references must exist.
        # ----------------------------------------------------

        for judgment in query.document_judgments:

            if judgment.document_id not in self.document_ids:
                raise RuntimeError(
                    f"query_id={query.query_id} "
                    f"references unknown document_id="
                    f"{judgment.document_id}"
                )

        # ----------------------------------------------------
        # Parent references must exist.
        # ----------------------------------------------------

        for judgment in query.parent_judgments:

            if judgment.parent_key not in self.parent_keys:
                raise RuntimeError(
                    f"query_id={query.query_id} "
                    f"references unknown parent_key="
                    f"{judgment.parent_key}"
                )

        # ----------------------------------------------------
        # Child references must exist.
        # ----------------------------------------------------

        for judgment in query.child_judgments:

            if judgment.child_key not in self.child_keys:
                raise RuntimeError(
                    f"query_id={query.query_id} "
                    f"references unknown child_key="
                    f"{judgment.child_key}"
                )

        # ----------------------------------------------------
        # Unanswerable queries must not contain positive gold
        # judgments once curated.
        # ----------------------------------------------------

        if query.answerability == Answerability.UNANSWERABLE:

            if (
                query.document_judgments
                or query.parent_judgments
                or query.child_judgments
            ):
                raise RuntimeError(
                    f"Unanswerable query "
                    f"{query.query_id} contains "
                    f"relevance judgments."
                )

        # ----------------------------------------------------
        # A CURATED answerable query must have parent and child
        # judgments. Migrated queries are intentionally allowed
        # to remain incomplete.
        # ----------------------------------------------------

        if (
            query.annotation_status == AnnotationStatus.CURATED
            and query.answerability == Answerability.ANSWERABLE
        ):

            if not query.parent_judgments:
                raise RuntimeError(
                    f"Curated answerable query "
                    f"{query.query_id} has no "
                    f"parent judgments."
                )

            if not query.child_judgments:
                raise RuntimeError(
                    f"Curated answerable query "
                    f"{query.query_id} has no "
                    f"child judgments."
                )

            unresolved_documents = [
                judgment.document_id
                for judgment in query.document_judgments
                if judgment.relevance is None
            ]

            if unresolved_documents:
                raise RuntimeError(
                    f"Curated query "
                    f"{query.query_id} still has "
                    f"ungraded documents: "
                    f"{unresolved_documents}"
                )


# ============================================================
# MAIN
# ============================================================


def main() -> None:

    gold_data = load_json(GOLD_PATH)

    units_data = load_json(UNITS_PATH)

    manifest = load_json(MANIFEST_PATH)

    dataset = GoldDatasetV2.model_validate(gold_data)

    validator = GoldDatasetV2Validator(
        dataset=dataset,
        units_data=units_data,
        manifest=manifest,
    )

    validator.validate()


if __name__ == "__main__":

    configure_logging()
    main()
