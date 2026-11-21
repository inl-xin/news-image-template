# make.fun 新闻图模板包

把 18、19 日跑通的新闻图做法存成模板：下次给新闻，直接填数据、出图、自检。

## 里面有什么

| 文件 | 作用 |
|---|---|
| `draw_template.py` | 画图程序（PIL）。版式固定，内容全从数据文件读 |
| `sample_news.py` | 示例新闻数据（19 Nov 2026，22 条）+ 数字条出处 |
| `main.py` | 提交入口：只把 `entry.png` 拷到输出目录（只用标准库） |
| `entry.png` | 用示例数据生成的样张（1024×1024，162 KB） |
| `check_template.py` | 14 项提交前自检，跑一遍就知道能不能交 |
| `LICENSE` | MIT |
| `styles/ink_wash_draw.py` | 另一套定稿版式：18 日中国水墨风（备用风格） |

## 定稿版式（默认：中央地图报纸版，19 日终版）

1024×1024，奶油纸底 `#F7F1E3`，只做平涂，不做写实插画。

- **报头**：左上 `THE DAY IN WORLD NEWS`，右上 `ALL STORIES FROM ONE DAY`，大号衬线日期（如 Thursday 19 November 2026），下面一行红色导语（3 条主新闻）。
- **地区条**：7 段色块，ASIA / EUROPE / MIDDLE EAST / AMERICAS / AFRICA / OCEANIA / GLOBAL + 各区条数，总和 = 新闻总数。
- **数字条**：`THE DAY IN NUMBERS · 22 STORIES · 7 REGIONS · 20 DRAWN` + 6 个核实过的数字（值 + 标签）。
- **Hero 行**：3 块大画板（330×180）。
- **北带**：5 块画板（195×118）。
- **中带**：中央世界地图（304×176，20 个编号红点）+ 左右各 2 块高画板（170×176），地图圆点用细线连到对应画板。
- **南带**：5 块画板（195×118）。
- **底带**：3 块宽画板（330×118）。
- **ALSO 行**：文字版短新闻（21、22 号）。
- **DATE CHECK 红框**：写清“不是当天新闻、所以没放进来”的东西。
- **脚注**：来源（Reuters · AP · AFP …）+ `make.fun / @inl-xin`。

每块画板固定结构：配图 + 右上红色编号徽章 + `地区 · 话题` 红标签 + 粗体标题（最多 2 行）+ 一句话说明。

备用风格（`styles/ink_wash_draw.py`）：18 日水墨版——红印章、毛笔分隔线、竖排书法、水墨山水配图；结构相同（报头 / 地区条 / 数字条 / 3+4+5 画板 / 地图+ALSO / DATE CHECK / 脚注），画板数 12 幅。

## 下次怎么用（填空结构）

1. 核实当天新闻，写一份简报：只留当天发生或当天首次报道的，数字逐个标出处。
2. 复制 `sample_news.py`，只改数据，不改代码：
   - `PAGE`：日期（大标题 + 短日期）、导语、地区条计数、数字条（6 个 + 每个数字的 `NUMBER_FACTS` 出处）、ALSO 行、DATE CHECK 文案、来源。
   - `STORIES`：20 条画出来的（`n` 1–20、`tag`、`headline`、`sub`、`figure`、`row`）+ ALSO 行里的 2 条文字新闻。
   - `figure` 是配图库的键（`draw_template.py` 里的 `FIGURE`）：summit、gta、anthropic、icj、cop31、kerch、greenland、nkorea、venezuela、senegal、riyadh、hormuz、gaza、sudan、cyclone、bangladesh、redcrab、gashusky、trumpiran、japantobacco。没有现成配图的新闻，先加一个画图函数再填。
3. 出图：`python3 draw_template.py`（默认写 `entry.png`）。
4. 自检：`python3 check_template.py`，14 项全过才能交。
5. 提交前先给人确认，不自动提交。

## 14 项提交前自检

| # | 检查 | 标准 |
|---|---|---|
| 1 | 格式 PNG，图片完整可打开 | 首字节正确，能打开 |
| 2 | 文件大小 ≤ 1 MiB | ≤ 1,048,576 字节 |
| 3 | 尺寸 ≤ 1024×1024 | 1024×1024 |
| 4 | 两次运行字节相同 | sha256 一致 |
| 5 | 日期写在图上且是真实日期 | 星期和日期对得上 |
| 6 | 新闻条数 ≥ 20 条 | 20 画 + 2 文字 = 22 |
| 7 | 覆盖 ≥ 5 个地区 | 多地区多领域 |
| 8 | 每块画板结构完整 | 编号、标签、标题、说明、配图齐全 |
| 9 | 数字条的每个数字都有简报出处 | `NUMBER_FACTS` 逐个有来源 |
| 10 | DATE CHECK 框在位，写清排除项 | 框 + 排除文案 |
| 11 | 来源脚注在位 | 列出通讯社 |
| 12 | 缩到 300px 宽时报头仍可读 | 报头区有深色文字像素 |
| 13 | LICENSE（OSI 批准）在仓库根目录 | MIT |
| 14 | 入口 main.py 在根目录、只用标准库、仓库 ≤ 1 MiB | import 只有 os、shutil |

## 重要提醒：复用时别直接复制

make.fun 的 transcript gate 要求提交的代码至少 30% 是 agent 在当次会话里亲手写的行，且入口文件至少有一行是亲手写的。直接复制这个模板一字不改去提交，`thinking_reproduces` 会挂。

正确做法：每次用模板时，让 agent 在当次会话里按当天新闻改写——换数据文件、调配图、改标题文案——并保留完整会话记录再打包提交。模板是起点，不是成品。
