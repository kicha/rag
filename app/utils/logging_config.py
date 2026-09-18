import logging


def configure_logging() -> None:
    """
    Configure project-wide logging.

    Application logs remain at INFO level.
    Noisy third-party libraries are reduced to WARNING.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s | " "%(levelname)-8s | " "%(name)s | " "%(message)s"),
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
    logging.getLogger("huggingface_hub").setLevel(logging.WARNING)
