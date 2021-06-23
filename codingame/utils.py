import re

CODINGAMER_HANDLE_REGEX = re.compile(r"[0-9a-f]{32}[0-9]{7}")
CLASH_OF_CODE_HANDLE_REGEX = re.compile(r"[0-9]{7}[0-9a-f]{32}")
