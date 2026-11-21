#!/usr/bin/env python3
"""Sample news data for the make.fun news-image template (19 Nov 2026).

This is the data that filled the template for the submitted 19 Nov 2026
entry. To use the template for a new day, copy this file, replace PAGE
and STORIES with the new day's verified stories, and run draw_template.py.
Only change the data — the layout geometry stays fixed.

Story fields:
  n       -- number badge on the panel and dot on the map (1-20 drawn;
             21+ are text-only in the ALSO line)
  tag     -- "REGION · TOPIC" label under the picture
  headline-- bold headline, 2 lines max in the panel
  sub     -- one-line summary under the headline
  figure  -- key into FIGURE in draw_template.py (the picture library)
  row     -- hero / row1 / mid / row3 / row4 (fixed geometry per row)
"""

PAGE = {
    "date_title": "Thursday 19 November 2026",
    "date_short": "19 NOV",
    "standfirst": ("Trump, Xi & Putin meet in Shenzhen  •  ICJ rules Myanmar "
                   "guilty  •  GTA VI launches"),
    "masthead_left": "THE DAY IN WORLD NEWS",
    "masthead_right": "ALL STORIES FROM ONE DAY",
    # region bar: (name, count) — counts must add up to the story total
    "regions": [("ASIA", "7"), ("EUROPE", "2"), ("MIDDLE EAST", "3"),
                ("AMERICAS", "4"), ("AFRICA", "3"), ("OCEANIA", "1"),
                ("GLOBAL", "2")],
    "numbers_title": "THE DAY IN NUMBERS  ·  22 STORIES · 7 REGIONS · 20 DRAWN",
    # numbers strip: 6 verified numbers, (value, label)
    "numbers": [("90 MIN", "Shenzhen talks"), ("9-6", "ICJ vote"),
                ("~10,000", "Rohingya killed"), ("109-0", "Denmark vote"),
                ("$83", "Anthropic IPO"), ("99", "GTA Metacritic")],
    "also": ("ALSO ON THURSDAY 19 NOVEMBER:  21. DR Congo: Ebola response "
             "hampered.   22. Haiti pastor convicted in Miami."),
    "date_check": ("Van Gogh $190.4m was 18 Nov; Cyclone Akvan landfall is "
                   "20 Nov; no Shenzhen breakthrough claimed."),
    "sources": ("Sources: Reuters · AP · AFP · Al Jazeera · Nikkei · IAEA · "
                "IMD · All stories from Thursday 19 November 2026."),
    "credit": "make.fun / @inl-xin",
}

# Provenance for every value on the numbers strip: each number must have
# a documented source fact in the day's brief. Check 9 verifies this.
NUMBER_FACTS = {
    "90 MIN": "Shenzhen trilateral lasted ~90 minutes (brief story 1).",
    "9-6": "ICJ genocide ruling was a 9-6 decision (brief story 2).",
    "~10,000": "~10,000 Rohingya killed, per the ICJ ruling (brief story 2).",
    "109-0": "Denmark ratified the Greenland pact 109-0 (brief story 6).",
    "$83": "Anthropic IPO priced at $83/share (brief story 5).",
    "99": "GTA VI scored 99 on Metacritic (brief story 4).",
}

STORIES = [
    # ---- heroes (3 big panels) ----
    {"n": 1, "tag": "ASIA · DIPLOMACY",
     "headline": "TRUMP, XI & PUTIN MEET IN SHENZHEN",
     "sub": "First-ever trilateral, 'peace declaration', no breakthrough yet.",
     "figure": "summit", "row": "hero"},
    {"n": 2, "tag": "CULTURE · TECH",
     "headline": "GTA VI IS OUT AFTER 13 YEARS",
     "sub": "Vice City returns, 99 Metacritic, PS5 and Xbox only.",
     "figure": "gta", "row": "hero"},
    {"n": 3, "tag": "GLOBAL · BUSINESS",
     "headline": "ANTHROPIC DEBUTS ON NASDAQ",
     "sub": "$83 IPO, biggest ever, ANT starts trading.",
     "figure": "anthropic", "row": "hero"},
    # ---- row 1: north band (5 panels) ----
    {"n": 4, "tag": "ASIA · LAW",
     "headline": "ICJ: MYANMAR GUILTY OF GENOCIDE",
     "sub": "First-ever state genocide ruling, ~10,000 killed.",
     "figure": "icj", "row": "row1"},
    {"n": 5, "tag": "GLOBAL · CLIMATE",
     "headline": "COP31 FINAL STRETCH",
     "sub": "Fossil-fuel wording unresolved; Fiji drought.",
     "figure": "cop31", "row": "row1"},
    {"n": 7, "tag": "EUROPE · WAR",
     "headline": "KERCH BRIDGE HIT AGAIN",
     "sub": "Rail disrupted; Odesa strike kills 4.",
     "figure": "kerch", "row": "row1"},
    {"n": 10, "tag": "EUROPE · ARCTIC",
     "headline": "DENMARK RATIFIES GREENLAND PACT",
     "sub": "109-0, two US bases, sovereignty kept.",
     "figure": "greenland", "row": "row1"},
    {"n": 11, "tag": "ASIA · SECURITY",
     "headline": "N. KOREA EXPANDS ENRICHMENT",
     "sub": "IAEA warns on Yongbyon.",
     "figure": "nkorea", "row": "row1"},
    # ---- middle band: 4 tall flank panels around the central map ----
    {"n": 13, "tag": "AMERICAS · DIPLOMACY",
     "headline": "VENEZUELA DEAL SIGNED",
     "sub": "US restores military ties; signed Wed 18 Nov.",
     "figure": "venezuela", "row": "mid"},
    {"n": 15, "tag": "AFRICA · MIGRATION",
     "headline": "SENEGAL BOAT SINKS",
     "sub": "Boat with ~100 migrants reported sunk.",
     "figure": "senegal", "row": "mid"},
    {"n": 8, "tag": "MIDDLE EAST · SECURITY",
     "headline": "MISSILE HITS RIYADH TOWER",
     "sub": "PIF HQ damaged, no injuries.",
     "figure": "riyadh", "row": "mid"},
    {"n": 14, "tag": "MIDDLE EAST · ENERGY",
     "headline": "HORMUZ: 3 TANKERS ON FIRE",
     "sub": "Iranian reports only; cause unconfirmed.",
     "figure": "hormuz", "row": "mid"},
    # ---- row 3: south band (5 panels) ----
    {"n": 9, "tag": "MIDDLE EAST · WAR",
     "headline": "GAZA: NEW OPERATION",
     "sub": "Central Gaza; Arab League condemns.",
     "figure": "gaza", "row": "row3"},
    {"n": 20, "tag": "AFRICA · POLITICS",
     "headline": "SUDAN: RSF COMMANDER DEFECTS",
     "sub": "RSF commander reported to defect.",
     "figure": "sudan", "row": "row3"},
    {"n": 6, "tag": "ASIA · WEATHER",
     "headline": "CYCLONE AKVAN NEARS INDIA",
     "sub": "~50,000 evacuated, landfall due Friday.",
     "figure": "cyclone", "row": "row3"},
    {"n": 12, "tag": "ASIA · POLITICS",
     "headline": "BANGLADESH SHUTDOWN",
     "sub": "Yunus family home torched in unrest.",
     "figure": "bangladesh", "row": "row3"},
    {"n": 16, "tag": "OCEANIA · NATURE",
     "headline": "RED CRABS BEGIN ANNUAL MIGRATION",
     "sub": "Millions head to the sea, Christmas Is.",
     "figure": "redcrab", "row": "row3"},
    # ---- row 4: bottom band (3 wide panels) ----
    {"n": 17, "tag": "EUROPE · SEA",
     "headline": "GAS HUSKY: ALL 19 CREW SAFE",
     "sub": "LPG tanker sank off Bulgaria Tue; rescue confirmed Thu.",
     "figure": "gashusky", "row": "row4"},
    {"n": 18, "tag": "AMERICAS · SECURITY",
     "headline": "TRUMP ON IRAN: 'SEE WHAT HAPPENS'",
     "sub": "US would 'see what happens' after 1 Jan 2027.",
     "figure": "trumpiran", "row": "row4"},
    {"n": 19, "tag": "ASIA · BUSINESS",
     "headline": "JAPAN TOBACCO HIT BY $8.9BN CHARGE",
     "sub": "Charge on its Russia seizure.",
     "figure": "japantobacco", "row": "row4"},
]
