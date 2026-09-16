from pydantic import BaseModel, Field
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage


class HyDEResult(BaseModel):
    original_query: str
    hypothetical_document: str


class HyDEGenerator:

    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def generate(self, query: str) -> HyDEResult:
        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        system_prompt = """
You generate hypothetical documents for semantic retrieval.

Given a user query, write a concise passage that could plausibly
appear in a high-quality technical document answering that query.

Rules:
- Write declarative document-style prose.
- Do not mention that this is hypothetical.
- Do not mention the user or the question.
- Preserve important technical terminology from the query.
- Prefer approximately 2-4 sentences.
- Do not add unnecessary examples.
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query),
        ]

        response = self.llm.invoke(messages)

        hypothetical_document = response.content.strip()

        if not hypothetical_document:
            raise RuntimeError("HyDE generation returned an empty document.")

        return HyDEResult(
            original_query=query,
            hypothetical_document=hypothetical_document,
        )
