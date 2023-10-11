import re
import itertools
import unicodedata
from typing import Any
from exception import GetChapterFailed

CCHARS = ''.join(map(chr, itertools.chain(range(0x00,0x20), range(0x7f,0xa0))))
CCHARS_RE = re.compile('[%s]' % re.escape(CCHARS))

def sanitize_text(s: str):
    return unicodedata.normalize("NFKD", CCHARS_RE.sub('', s)).strip()

def ddir(d: dict[Any, Any], dir: str, de: Any={}) -> Any:
    """
    Retrieve dictionary value using recursive indexing with a string.
    ex.:
        `ddir({"data": {"attr": {"ch": 1}}}, "data/attr/ch")`
        will return `1`


    Args:
        dict (dict): Dictionary to retrieve the value from.
        dir (str): Directory of the value to be retrieved.

    Returns:
        op (Any): Retrieved value.
    """
    op = d
    for a in dir.split("/"):
        try: op = op[a]
        except: raise GetChapterFailed('Chapter not purchased')
    return op or de