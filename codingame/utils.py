import re

__all__ = (
    "CODINGAMER_HANDLE_REGEX",
    "CLASH_OF_CODE_HANDLE_REGEX",
)

CODINGAMER_HANDLE_REGEX = re.compile(r"[0-9a-f]{32}[0-9]{7}")
CLASH_OF_CODE_HANDLE_REGEX = re.compile(r"[0-9]{7}[0-9a-f]{32}")
