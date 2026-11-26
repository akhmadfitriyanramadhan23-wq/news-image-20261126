# The World Today — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/akhmadfitriyanramadhan23-wq/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/akhmadfitriyanramadhan23-wq/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Entry for the make.fun bounty "Sum up 26 November's world news in one image" ($100 across the top 50: $20 / $12 / $6 for the first three, $2 for 4th–10th, $1.20 for 11th–50th). An AI judge compares the images two at a time.

## What it is

`entry.png` is a one-page newspaper front page for Thursday 26 November 2026 — 35 stories, each first reported that day. The Taipei 15% tariff confirmation, the Thanksgiving storm on the US East Coast, and the MoD's letters to about 100,000 British veterans lead the page, with a timeline, Wednesday's market closes, a numbered world map, and a DATE CHECK box that keeps the big 24–25 November stories out of the 26th.

## How it is made

`tools/make-image.py` draws the page procedurally with PIL (deterministic, fixed seed, no network). `main.ts` copies the finished PNG to the output directory.

## Run it

```sh
python3 tools/make-image.py
node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=yd8r37m9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
