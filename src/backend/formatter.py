from backend.formats.json_format import format_json
from backend.formats.markdown_format import format_markdown
from backend.formats.raw_format import format_raw


def format_output(content: str, *, output_format: str) -> str:
    if output_format == "raw":
        return format_raw(content)
    if output_format == "json":
        return format_json(content)
    return format_markdown(content)
