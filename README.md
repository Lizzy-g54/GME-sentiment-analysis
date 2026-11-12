# GME Sentiment Analysis Dashboard

An interactive course project exploring how discussion on Reddit's r/WallStreetBets and GameStop (GME) market activity changed during the 2021 short squeeze. It combines sentiment summaries with linked visualizations so readers can inspect patterns across time. The dashboard is an exploratory analysis; visual alignment alone does not establish causation or predictive performance.

## What to explore

- **Emotional Candlestick:** GME price movements alongside the share of comments labeled as fear.
- **Market Spiral:** An animated view of sentiment balance, discussion volume, and trading volume.
- **Sentiment Flow:** Changes in counts of comments labeled hype, fear, and anger.
- **Risk Correlation Matrix:** Pairwise views of sentiment, attention, volume, and volatility.
- **Predictive Aligner:** A movable time offset for comparing fear and volatility series. This is a visual exploration of timing, not a validated forecast.

The project uses D3.js and Plotly for the interactive views, with Python scripts for data preparation and chart generation.

## Run locally

1. Clone this repository.
2. From the repository root, start a local web server: `python -m http.server 8000`.
3. Open `http://localhost:8000/` in a modern browser.

The dashboard reads files from `dataset/`. A local server helps the browser load those files consistently.

## Repository guide

| Path | Purpose |
| --- | --- |
| `index.html`, `main.js` | Dashboard layout and D3 visualizations |
| `vis2.py`, `vis4_s.py` | Scripts for generated Plotly views |
| `process_data.py` | Data preparation |
| `dataset/` | Data used by the dashboard |
| `notebooks/` | Analysis notebooks |

## Reading the results

The charts show relationships within the selected period and data. A shift of one line relative to another can suggest a question for further analysis, but it does not by itself test whether sentiment predicts later market behavior. Any predictive claim would require a stated target, a time-respecting evaluation, an appropriate baseline, and results on held-out data.

This repository contains a team course project. For an account of my individual contribution, see the [research and projects section of my portfolio](https://lizzy-g54.github.io/#research).

## Data and reuse

The repository includes derived tables and source data under `dataset/`. Before reusing or redistributing those files, check the original source terms and any applicable privacy requirements. The included papers and course report are background material; their presence does not imply that their content is licensed for reuse.
