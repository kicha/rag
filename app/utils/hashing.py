import re
import uuid
from hashlib import sha256
from typing import Iterable

# ============================================================
# CONTENT HASH
# ============================================================


def generate_content_hash(
    content: str,
) -> str:

    normalized = content.strip()

    return sha256(normalized.encode("utf-8")).hexdigest()


# ============================================================
# LEGACY CHUNK ID GENERATOR
# ============================================================


class ChunkIdGenerator:

    @staticmethod
    def generate(
        document_id: str,
        chunk_index: int,
    ) -> str:

        return str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{document_id}:chunk:{chunk_index}",
            )
        )


# ============================================================
# BENCHMARK KEY GENERATOR
# ============================================================


class ChunkKeyGenerator:
    """
    Generates deterministic benchmark identities.

    These are NOT database primary keys.

    Runtime IDs:
        parent_id
        child_id

    Stable evaluation identities:
        parent_key
        child_key
    """

    HASH_PREFIX_LENGTH = 12

    @classmethod
    def generate_parent_key(
        cls,
        document_id: str,
        parent_index: int,
        section_path: Iterable[str],
        content_hash: str,
    ) -> str:

        normalized_path = cls._normalize_section_path(section_path)

        hash_prefix = content_hash[: cls.HASH_PREFIX_LENGTH]

        return (
            f"{document_id}"
            f"::P{parent_index:03d}"
            f"::{normalized_path}"
            f"::{hash_prefix}"
        )

    @classmethod
    def generate_child_key(
        cls,
        parent_key: str,
        child_index: int,
        content_hash: str,
    ) -> str:

        hash_prefix = content_hash[: cls.HASH_PREFIX_LENGTH]

        return f"{parent_key}" f"::C{child_index:03d}" f"::{hash_prefix}"

    @staticmethod
    def _normalize_section_path(
        section_path: Iterable[str],
    ) -> str:

        normalized_parts = []

        for part in section_path:

            normalized = re.sub(
                r"\s+",
                " ",
                part.strip(),
            )

            normalized = normalized.replace(
                "::",
                ":",
            )

            normalized = normalized.replace(
                "/",
                "-",
            )

            if normalized:
                normalized_parts.append(normalized)

        if not normalized_parts:
            return "_root"

        return "/".join(normalized_parts)
