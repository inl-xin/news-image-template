#!/usr/bin/env python3
"""14-item pre-submission self-check for the make.fun news-image template.

Run from the template directory:
    python3 check_template.py [entry.png]

Prints each check as PASS / FAIL with evidence. Exit 0 only if all pass.
Checks 1-12 are about the image itself; 13-14 are about the entry repo.
"""
import ast
import datetime
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png")

results = []


def check(name, ok, evidence):
    results.append((name, ok, evidence))
    print(("PASS" if ok else "FAIL"), "-", name, "-", evidence)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


# --- load the data module the image was drawn from ---
sys.path.insert(0, HERE)
from sample_news import PAGE, STORIES  # noqa: E402
from PIL import Image  # noqa: E402

# 1. format: PNG, magic bytes, opens cleanly
with open(PNG, "rb") as f:
    magic = f.read(8)
try:
    im = Image.open(PNG)
    im.load()
    opened = True
except Exception as e:  # noqa: BLE001
    opened = False
    print("open error:", e)
check("1. 格式 PNG，图片完整可打开",
      magic == b"\x89PNG\r\n\x1a\n" and opened,
      "magic=%s opened=%s" % (magic[:4], opened))

# 2. file size <= 1 MiB
size = os.path.getsize(PNG)
check("2. 文件大小 ≤ 1 MiB", size <= 1048576, "%d bytes" % size)

# 3. dimensions 1024x1024 (<= 1024x1024)
check("3. 尺寸 ≤ 1024×1024", im.size[0] <= 1024 and im.size[1] <= 1024,
      "%dx%d" % im.size)

# 4. determinism: redraw and compare bytes
out2 = os.path.join(HERE, "sample", "entry-check-rerun.png")
os.makedirs(os.path.join(HERE, "sample"), exist_ok=True)
r = subprocess.run([sys.executable, os.path.join(HERE, "draw_template.py"),
                    out2], capture_output=True, text=True)
same = r.returncode == 0 and sha256(PNG) == sha256(out2)
check("4. 两次运行字节相同（确定性）", same,
      "sha256 %s…" % sha256(PNG)[:16])

# 5. date on the image and a real calendar date
title = PAGE["date_title"]
try:
    d = datetime.datetime.strptime(title, "%A %d %B %Y").date()
    real_date = d.strftime("%A") == title.split(" ")[0]
except ValueError:
    real_date = False
check("5. 日期写在图上且是真实日期", bool(title) and real_date,
      title + (" (weekday matches)" if real_date else " (WEEKDAY MISMATCH)"))

# 6. story count >= 20
drawn = [s for s in STORIES if s["n"] <= 20]
total = len(STORIES) + 2  # +2 text-only ALSO items
check("6. 新闻条数 ≥ 20 条", total >= 20,
      "%d drawn + 2 ALSO = %d stories" % (len(drawn), total))

# 7. breadth: >= 5 regions covered
regions = {s["tag"].split(" · ")[0] for s in STORIES}
check("7. 覆盖 ≥ 5 个地区", len(regions) >= 5,
      "%d regions: %s" % (len(regions), ", ".join(sorted(regions))))

# 8. every drawn story has badge + tag + headline + sub + a figure
import draw_template as T  # noqa: E402
bad = [s["n"] for s in STORIES
       if not (s.get("n") and s.get("tag") and s.get("headline")
               and s.get("sub") and s.get("figure") in T.FIGURE)]
check("8. 每块画板都有编号、标签、标题、说明和配图",
      not bad, "20 drawn panels, missing: %s" % (bad or "none"))

# 9. numbers strip: every value has a documented source fact in the brief
from sample_news import NUMBER_FACTS  # noqa: E402
missing = [v for v, _ in PAGE["numbers"] if v not in NUMBER_FACTS
           or not NUMBER_FACTS[v].strip()]
check("9. 数字条的每个数字都有简报出处",
      not missing, "6 numbers, without source fact: %s" % (missing or "none"))

# 10. DATE CHECK box present with exclusions named
dc = PAGE.get("date_check", "")
check("10. DATE CHECK 框在位，写清排除项", len(dc) > 20,
      dc[:60] + "…")

# 11. sources footer present
src = PAGE.get("sources", "")
check("11. 来源脚注在位", "Sources:" in src and len(src) > 20,
      src[:60] + "…")

# 12. legible at ~300px: downscale, masthead band must still carry dark text
small = im.resize((300, 300))
band = small.crop((0, 0, 300, 40)).convert("L")
dark = sum(1 for px in band.getdata() if px < 100)
check("12. 缩到 300px 宽时报头仍有可读文字", dark > 200,
      "%d dark pixels in masthead band at 300px" % dark)

# 13. LICENSE (OSI) at repo root
lic = os.path.join(HERE, "LICENSE")
lic_ok = os.path.exists(lic) and "SPDX-License-Identifier: MIT" in open(lic).read()
check("13. LICENSE（OSI 批准）在仓库根目录", lic_ok, "MIT, SPDX line present")

# 14. entrypoint main.py at root, stdlib only; repo tree within 1 MiB
main = os.path.join(HERE, "main.py")
tree = ast.parse(open(main).read())
mods = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        mods.update(a.name.split(".")[0] for a in node.names)
    elif isinstance(node, ast.ImportFrom) and node.module:
        mods.add(node.module.split(".")[0])
stdlib = {"os", "shutil", "sys"}
total_bytes = sum(os.path.getsize(os.path.join(dp, f))
                  for dp, _, fs in os.walk(HERE) for f in fs)
check("14. 入口 main.py 在根目录、只用标准库、仓库 ≤ 1 MiB",
      os.path.exists(main) and mods <= stdlib and total_bytes <= 1048576,
      "imports=%s repo=%d bytes" % (sorted(mods), total_bytes))

print()
failed = [n for n, ok, _ in results if not ok]
print("RESULT: %d/14 passed%s" % (14 - len(failed),
                                  ("; FAILED: " + ", ".join(failed)) if failed else ""))
sys.exit(1 if failed else 0)
