"""Subsets Noto Sans CJK JP Bold down to just the characters used in sections.py.

    python generator/subset_jp.py [path/to/NotoSansCJK-Bold.ttc]

Only needed if you change the Japanese text; the resulting file is committed in fonts/.
"""
import os
import re
import sys

from fontTools import subset
from fontTools.ttLib import TTCollection

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
OUT = os.path.join(HERE, "fonts", "NotoSansJP-Bold-subset.otf")

font = next(f for f in TTCollection(SRC).fonts if "JP" in (f["name"].getDebugName(1) or ""))
src = open(os.path.join(HERE, "sections.py"), encoding="utf-8").read()
chars = "".join(sorted(set(re.findall(r"[\u3000-\u30ff\u4e00-\u9fff\uff00-\uffef]", src)) | set(map(chr, range(0x20, 0x7f)))))
opts = subset.Options()
opts.layout_features = []
opts.name_IDs = [0, 1, 2, 3, 4, 5, 6]
opts.notdef_outline = True
sub = subset.Subsetter(opts)
sub.populate(text=chars + " ")
sub.subset(font)
font.save(OUT)
print(f"{len(chars)} characters -> {os.path.getsize(OUT) / 1024:.1f} KB: {chars}")
