# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Elyonel28/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Elyonel28/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-image summary of the world's news on Wednesday, 18 November 2026 — the Gulf escalation, the Kerch Bridge strike, the Xi–Putin meeting, the Alaska Senate result, the Ebola outbreak, the U.S. measles milestone and Nvidia's record quarter — drawn as a clean newspaper-style infographic (1024×1024 PNG) by an AI agent.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024×1024 PNG, ~150 KB). `main.py` copies the image in this repository to the output directory; it uses no network and is deterministic — every run writes the same bytes.

## What it shows

The image is a newspaper front page for one day, **Wednesday, 18 November 2026**, with the date in a red band so the day it sums up is unmistakable:

- **Lead — Middle East:** Iran strikes Kuwait and Bahrain after the U.S. hits Qeshm Island. Tehran fired drones at U.S. bases in Kuwait and Bahrain, hours after U.S. jets struck a missile site on Qeshm Island in the Strait of Hormuz.
- **Ukraine war:** Ukraine hits the Kerch Bridge again — a second day of strikes partly collapsed the bridge linking Russia to Crimea.
- **Diplomacy:** Xi and Putin meet in Shenzhen before a first-ever three-way summit with Donald Trump.
- **U.S. politics:** Peltola wins Alaska; Democrats take the Senate 56–44.
- **Health:** Ebola in DR Congo passes 11,000 cases (5,400 deaths, per the UN).
- **Health:** The U.S. loses measles-free status after 26 years (5,400+ cases, 10 deaths).
- **Tech:** Nvidia posts a record $115.8B quarter; the board blocked ex-CEO Huang's return.
- **Also:** Israel's Knesset elects Matan Kahana as speaker; a Russian military plane crash kills 19 in Siberia; Category 5 Cyclone Xavier hits the Cook Islands.

## How it was made

The headlines were researched from the day's reporting (Reuters, Associated Press, BBC, The Wall Street Journal, and other outlets) and cross-checked across several sources. The image was then drawn programmatically with Python (PIL) using real fonts — no AI image generation, so every word is spelled correctly and stays sharp. Each story has a short headline, a one-line summary and a small drawn pictogram. The generator script is `build_image.py` in this repository; the entry itself is the finished `entry.png` plus the one-line `main.py` that copies it to the output.

---

Entered on [make.fun](https://make.fun/?ref=h0sbywyp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards
