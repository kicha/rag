import uuid
from hashlib import sha256


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


def generate_content_hash(content: str) -> str:
    return sha256(content.encode("utf-8")).hexdigest()
