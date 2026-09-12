import re
from typing import List
from app.models.elements import StructuralElement
from app.models.document import Document
from app.models.metadata import HeadingContext

# ============================================================
# STRUCTURE DETECTOR
# ============================================================


class StructureDetector:

    HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$")

    BULLET_PATTERN = re.compile(r"^\s*[-*+]\s+")

    NUMBERED_PATTERN = re.compile(r"^\s*\d+\.\s+")

    TABLE_PATTERN = re.compile(r"^\s*\|.*\|\s*$")

    CODE_FENCE_PATTERN = re.compile(r"^\s*```")

    def detect(
        self,
        document: Document,
    ) -> List[StructuralElement]:

        lines = document.text.splitlines()

        elements = []

        heading_context = HeadingContext()

        paragraph_buffer: List[str] = []
        list_buffer: List[str] = []
        code_buffer: List[str] = []

        inside_code = False

        element_counter = 0

        # ----------------------------------------------------
        # Helper functions
        # ----------------------------------------------------

        def flush_paragraph():

            nonlocal element_counter

            if not paragraph_buffer:
                return

            content = "\n".join(paragraph_buffer).strip()

            if content:

                elements.append(
                    StructuralElement(
                        element_id=(f"element-{element_counter}"),
                        element_type="paragraph",
                        content=content,
                        heading_context=(heading_context.copy()),
                    )
                )

                element_counter += 1

            paragraph_buffer.clear()

        def flush_list():

            nonlocal element_counter

            if not list_buffer:
                return

            content = "\n".join(list_buffer).strip()

            if content:

                elements.append(
                    StructuralElement(
                        element_id=(f"element-{element_counter}"),
                        element_type="list",
                        content=content,
                        heading_context=(heading_context.copy()),
                    )
                )

                element_counter += 1

            list_buffer.clear()

        def flush_code():

            nonlocal element_counter

            if not code_buffer:
                return

            content = "\n".join(code_buffer).strip()

            if content:

                elements.append(
                    StructuralElement(
                        element_id=(f"element-{element_counter}"),
                        element_type="code",
                        content=content,
                        heading_context=(heading_context.copy()),
                    )
                )

                element_counter += 1

            code_buffer.clear()

        # ----------------------------------------------------
        # Main parser
        # ----------------------------------------------------

        for line in lines:

            stripped = line.strip()

            # ------------------------------------------------
            # CODE BLOCK
            # ------------------------------------------------

            if self.CODE_FENCE_PATTERN.match(line):

                if inside_code:

                    code_buffer.append(line)

                    flush_code()

                    inside_code = False

                else:

                    flush_paragraph()
                    flush_list()

                    inside_code = True

                    code_buffer.append(line)

                continue

            if inside_code:

                code_buffer.append(line)

                continue

            # ------------------------------------------------
            # HEADING
            # ------------------------------------------------

            heading_match = self.HEADING_PATTERN.match(stripped)

            if heading_match:

                flush_paragraph()
                flush_list()

                level = len(heading_match.group(1))

                heading = heading_match.group(2).strip()

                heading_context.update(
                    level,
                    heading,
                )

                elements.append(
                    StructuralElement(
                        element_id=(f"element-{element_counter}"),
                        element_type="heading",
                        content=heading,
                        heading_context=(heading_context.copy()),
                        heading_level=level,
                    )
                )

                element_counter += 1

                continue

            # ------------------------------------------------
            # EMPTY LINE
            # ------------------------------------------------

            if not stripped:

                flush_paragraph()
                flush_list()

                continue

            # ------------------------------------------------
            # LIST / TABLE
            # ------------------------------------------------

            is_list = self.BULLET_PATTERN.match(line) or self.NUMBERED_PATTERN.match(
                line
            )

            is_table = self.TABLE_PATTERN.match(line)

            if is_list or is_table:

                flush_paragraph()

                list_buffer.append(line)

                continue

            # ------------------------------------------------
            # NORMAL PARAGRAPH
            # ------------------------------------------------

            flush_list()

            paragraph_buffer.append(line)

        # ----------------------------------------------------
        # Flush remaining content
        # ----------------------------------------------------

        flush_paragraph()
        flush_list()

        if inside_code:

            flush_code()

        return elements
