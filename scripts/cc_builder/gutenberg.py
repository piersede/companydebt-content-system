"""Low-level Gutenberg block primitives.

Each function returns a block string. The PageBuilder class accumulates
blocks and joins them for final output.
"""



class PageBuilder:
    """Accumulates Gutenberg blocks and produces final HTML content."""

    def __init__(self):
        self._blocks: list[str] = []

    def add(self, text: str):
        self._blocks.append(text)

    def para(self, text: str):
        self.add(
            f'<!-- wp:paragraph -->\n<p>{text.strip()}</p>\n<!-- /wp:paragraph -->'
        )

    def heading(self, level: int, text: str):
        self.add(
            f'<!-- wp:heading {{"level":{level}}} -->\n'
            f'<h{level} class="wp-block-heading">{text.strip()}</h{level}>\n'
            f'<!-- /wp:heading -->'
        )

    def raw_html(self, markup: str):
        self.add(
            f'<!-- wp:html -->\n{markup.strip()}\n<!-- /wp:html -->'
        )

    def list_block(self, lhtml: str):
        ordered = '<ol' in lhtml.strip()[:10]
        self.add(
            f'<!-- wp:list {{"ordered":{str(ordered).lower()}}} -->\n{lhtml.strip()}\n<!-- /wp:list -->'
        )

    def table_block(self, thtml: str):
        self.add(
            f'<!-- wp:table {{"className":"is-style-stripes"}} -->\n'
            f'<figure class="wp-block-table is-style-stripes">{thtml.strip()}</figure>\n'
            f'<!-- /wp:table -->'
        )

    def group_start(self, cls: str, style: str):
        self.add(
            f'<!-- wp:group {{"className":"{cls}"}} -->\n'
            f'<div class="wp-block-group {cls}" style="{style}">'
        )

    def group_end(self):
        self.add('</div>\n<!-- /wp:group -->')

    def build(self) -> str:
        """Join all blocks into final content string."""
        return '\n\n'.join(self._blocks)

    @property
    def block_count(self) -> int:
        return len(self._blocks)
