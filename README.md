# GME Sentiment Analysis Dashboard
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![D3.js](https://img.shields.io/badge/D3.js-v7-orange.svg)](https://d3js.org/)
[![Plotly](https://img.shields.io/badge/Plotly-v2.35-green.svg)](https://plotly.com/)

> **An interactive visualization dashboard exploring the relationship between Reddit sentiment and GME stock volatility during the 2021 short squeeze event.**

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Live%20Demo-blue)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Background](#background)
- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [Visualizations](#visualizations)
  - [Vis 1: Emotional Candlestick](#vis-1-emotional-candlestick)
  - [Vis 2: Market Spiral Trajectory](#vis-2-market-spiral-trajectory)
  - [Vis 3: Sentiment Flow](#vis-3-sentiment-flow)
  - [Vis 4: Risk Correlation Matrix](#vis-4-risk-correlation-matrix)
  - [Vis 5: Predictive Aligner](#vis-5-predictive-aligner)
- [The Story](#the-story)
- [Technical Architecture](#technical-architecture)
- [Project Structure](#project-structure)
- [Research Papers](#research-papers)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## 🎯 Overview

This project presents a comprehensive analysis of the GameStop (GME) stock phenomenon that occurred in early 2021, combining **social media sentiment analysis** from Reddit's WallStreetBets (WSB) community with **financial market data**. Through five interconnected visualizations, we reveal how collective emotions—fear, hype, and anger—drove one of the most dramatic market events in recent history.

### Key Features

- 🎨 **High-contrast, accessible design** with pure white backgrounds and bold color differentiation
- 📊 **Five interactive visualizations** telling a complete story from multiple angles
- 🖱️ **Cross-chart interactivity**: Hover over any chart to see corresponding Reddit comments
- 🎬 **Animated timeline** showing the evolution of market sentiment
- 🔍 **Zoom and brush capabilities** for detailed exploration
- 📱 **Responsive layout** with sticky comment panel

---

## 📖 Background

### The GME Short Squeeze: A Perfect Storm

In January 2021, GameStop (GME), a struggling video game retailer, became the epicenter of a financial revolution. A coordinated buying effort by retail investors—primarily organized through Reddit's r/WallStreetBets community—triggered a massive short squeeze, sending the stock price from under $20 to over $480 in a matter of days.

This event represented:
- **A clash between retail and institutional investors**
- **The power of social media in financial markets**
- **An unprecedented demonstration of collective sentiment driving price action**

Our dashboard captures this narrative by analyzing:
- **58,000+ Reddit comments** from WSB during the peak period
- **Daily stock prices, volumes, and volatility metrics**
- **Emotion classification** (Hype, Fear, Anger, Noise) using NLP techniques

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lizzy-g54/GME-sentiment-analysis.git
   cd GME-sentiment-analysis
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install pandas plotly numpy
   ```

4. **Launch the dashboard**
   
   Simply open `index.html` in your browser:
   ```bash
   # On macOS
   open index.html
   
   # On Linux
   xdg-open index.html
   
   # On Windows
   start index.html
   ```
   
   Or use a local server for better performance:
   ```bash
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

---

## 💡 Usage

### Dashboard Navigation

1. **Main View**: The left side contains five visualization cards
2. **Comment Panel**: The right sidebar shows top Reddit comments for the selected date
3. **Interactivity**: Hover over any chart to update the comment panel

### Tips for Exploration

- **Use the brush** in Vis 1 (Candlestick) to zoom into specific time periods
- **Click Play** in Vis 2 (Market Spiral) to watch the bubble cycle unfold
- **Hover over streams** in Vis 3 to see daily sentiment breakdowns
- **Drag the slider** in Vis 5 to explore lead-lag relationships

---

## 📊 Data Sources

### Primary Dataset: `final_dataset_for_vis.csv`

| Column | Description | Type |
|--------|-------------|------|
| `date` | Trading date | Date |
| `count_Anger` | Number of "Anger" classified comments | Integer |
| `count_Fear` | Number of "Fear" classified comments | Integer |
| `count_Hype` | Number of "Hype" classified comments | Integer |
| `count_Noise` | Number of "Noise" (neutral) comments | Integer |
| `total_comments` | Total Reddit comments for the day | Integer |
| `fear_ratio` | Proportion of fear comments (0-1) | Float |
| `close` | GME closing price (USD) | Float |
| `volume` | Trading volume (shares) | Integer |
| `high` | Daily high price (USD) | Float |
| `low` | Daily low price (USD) | Float |
| `volatility` | Price volatility metric | Float |

### Supporting Datasets

- **`top_comments.csv`**: Curated top-voted comments with sentiment labels
- **`reddit_wsb.csv`**: Raw Reddit submissions and comments
- **`gme_sentiment_labeled.csv`**: Full labeled dataset for model training
- **`train_stockemo.csv` / `val_stockemo.csv` / `test_stockemo.csv`**: Train/validation/test splits

### Data Collection Period

**January 28, 2021 - February 26, 2021** (30 trading days)

This period captures:
- The initial squeeze peak (Jan 28)
- The decline phase
- The secondary pump (Feb 24-25)

---

## 📈 Visualizations

### Vis 1: Emotional Candlestick

**File**: `main.js` (function `renderVis1`)

![Candlestick Chart](https://via.placeholder.com/800x350/ffffff/007bff?text=Emotional+Candlestick+Chart)

#### What It Shows

This visualization combines traditional **OHLC (Open-High-Low-Close) candlestick charts** with **sentiment heatmapping**. Each candle represents one trading day, with its color intensity indicating the level of fear in the Reddit community.

#### How to Read It

- **Candle Body**: Shows the opening and closing prices
  - Top of body = Higher of (Open, Close)
  - Bottom of body = Lower of (Open, Close)
- **Wicks (Shadows)**: Show the high and low prices for the day
- **Color Intensity**: Represents `fear_ratio` (light pink = low fear, deep red = high fear)

#### Interactive Features

- **Brush/Zoom**: Drag the bottom slider to focus on specific date ranges
- **Dynamic Y-axis**: Automatically rescales when zooming
- **Tooltip**: Hover to see:
  - Date
  - Price change (▲ Up / ▼ Down)
  - Total Reddit posts
  - Fear ratio percentage

#### Key Insights

> **January 28, 2021**: The peak fear day (54.9% fear ratio) coincided with the highest volatility (3.30) and extreme price swings ($28.06 - $120.75). This was the day trading restrictions were imposed by Robinhood.

---

### Vis 2: Market Spiral Trajectory

**File**: `vis2_market_spiral_perfect.html` (generated by `vis2.py`)

![Market Spiral](https://via.placeholder.com/800x650/ffffff/ff9f1c?text=Market+Spiral+Animation)

#### What It Shows

An **animated scatter plot** that visualizes GME's journey through the "emotional landscape" of the market over time. This is the centerpiece narrative visualization.

#### How to Read It

- **X-axis (Sentiment Balance)**: 
  - Negative values (left) = Fear dominates
  - Positive values (right) = Hype dominates
  - Formula: `(count_Hype - count_Fear) / total_comments`
  
- **Y-axis (Community Engagement)**: 
  - Total Reddit comments (log scale)
  - Higher = More social media attention
  
- **Bubble Size**: Trading volume (larger = more shares traded)

- **Color**: Fear intensity (white/light pink = calm, deep red = panic)

- **Dashed Line**: Historical trajectory showing the path taken

#### Interactive Features

- **Play/Pause Button**: Animate through the timeline
- **Date Slider**: Manually scrub through dates
- **Animation Speed**: 800ms per frame with smooth transitions

#### Key Insights

> **The Cycle**: Watch how GME moves from the **Hype Phase** (top right, high engagement, positive sentiment) through the **Panic Phase** (top left, high engagement, negative sentiment) and finally to the **Exhaustion Phase** (bottom, low engagement).

> **Extreme Fear Day**: February 19, 2021 shows the highest fear ratio (79.5%) but surprisingly low engagement—indicating isolated panic among remaining holders.

---

### Vis 3: Sentiment Flow

**File**: `main.js` (function `renderVis3`)

![Sentiment Flow](https://via.placeholder.com/800x300/ffffff/2ca02c?text=Sentiment+Streamgraph)

#### What It Shows

A **streamgraph (flowing area chart)** displaying the absolute volume of three primary emotions over time: **Hype** (blue), **Fear** (orange), and **Anger** (red).

#### How to Read It

- **Layer Height**: Number of comments for that emotion on a given day
- **Stacked Height**: Total community engagement
- **Color Coding**:
  - 🔵 Blue (`#007bff`) = Hype / Optimism
  - 🟠 Orange (`#ff9f1c`) = Fear / Anxiety
  - 🔴 Red (`#d63031`) = Anger / Frustration

#### Interactive Features

- **Hover Line**: Vertical dashed line follows cursor
- **Tooltip**: Shows exact counts for all three emotions plus total
- **Date Update**: Automatically updates the comment panel

#### Key Insights

> **January 29, 2021**: The highest total engagement day (2,527 comments) with fear (1,211) slightly dominating hype (1,179)—the community was divided.

> **February 24, 2021**: A secondary spike in engagement (332M volume day) shows fear (224) and hype (129) coexisting during the second pump.

---

### Vis 4: Risk Correlation Matrix (SPLOM)

**File**: `vis4_splom_final.html` (generated by `vis4_s.py`)

![SPLOM Matrix](https://via.placeholder.com/900x900/ffffff/9467bd?text=Risk+Correlation+Matrix)

#### What It Shows

A **Scatter Plot Matrix (SPLOM)** that reveals correlations between five key dimensions: Fear Sentiment, Hype Posts, Social Attention, Trading Volume, and Market Risk (Volatility).

#### How to Read It

The matrix displays all pairwise relationships:

| Dimension | Description |
|-----------|-------------|
| **Fear Sentiment** | `fear_ratio` (0-1 scale) |
| **Hype Posts** | `count_Hype` (raw count) |
| **Social Attention** | `total_comments` (engagement) |
| **Trading Volume** | `volume` (shares traded) |
| **Market Risk** | `volatility` (price variance) |

- **Each Subplot**: One scatter plot showing X vs Y
- **Point Color**: Market volatility (red intensity)
- **Point Size**: Fixed at 7px with 70% opacity
- **Diagonal**: Hidden (self-correlation is trivial)

#### Interactive Features

- **Hover**: Shows exact date and coordinate values
- **Zoom**: Box-select to zoom into dense regions
- **Pan**: Drag to explore after zooming

#### Key Insights

> **Volume ↔ Volatility**: Strong positive correlation—high trading volume almost always accompanies high volatility.

> **Fear Ratio ↔ Volatility**: The color gradient (red = high volatility) shows that extreme fear often precedes or coincides with high volatility.

> **Social Attention Clustering**: Most high-volatility days cluster in the upper-right quadrant (high engagement + high fear).

---

### Vis 5: Predictive Aligner

**File**: `main.js` (function `renderVis5`)

![Predictive Aligner](https://via.placeholder.com/800x300/ffffff/d63031?text=Predictive+Aligner)

#### What It Shows

A **dual-axis time series chart** exploring the temporal relationship between **fear sentiment** (leading indicator?) and **market volatility** (outcome).

#### How to Read It

- **Left Y-axis (Red)**: Fear Posts Volume (`count_Fear`)
- **Right Y-axis (Gray)**: Market Volatility (`volatility`)
- **X-axis**: Timeline (Jan 28 - Feb 26, 2021)
- **Red Line**: Fear sentiment trajectory
- **Gray Area**: Volatility background

#### Interactive Features

- **Time Offset Slider**: Drag from -5 to +5 days
  - **Negative values**: Fear leads volatility (predictive)
  - **Zero**: Synchronous movement
  - **Positive values**: Fear lags volatility (reactive)
  
- **Visual Feedback**: Red line shifts horizontally as you drag

#### Key Insights

> **Lead-Lag Analysis**: By shifting the fear line backward (-1 to -3 days), you may observe better alignment with volatility spikes—suggesting that Reddit fear could be a **leading indicator** for market turbulence.

> **January 28 Peak**: The fear spike precedes the volatility explosion, supporting the predictive hypothesis.

---

## 📖 The Story

### Chapter 1: The Spark (January 25-27, 2021)

Before our data begins, Keith Gill (known as "DeepFuckingValue" on Reddit) had been advocating for GME for months. By late January, the WSB community had grown to millions, and the short interest in GME exceeded 100% of the float. The powder keg was ready.

### Chapter 2: The Explosion (January 28, 2021)

Our story begins on the most volatile day in GME's history. The stock opened at $120.75, crashed to $28.06, and closed at $48.40. The fear ratio hit 54.9%—the highest in our dataset. 

**What happened?** Trading restrictions. Robinhood and other brokers halted buy orders, triggering a massive sell-off. The community's reaction was immediate and furious—2,257 comments that day, with fear dominating.

*Visual Evidence*: Vis 1 shows the deepest red candle. Vis 2 places this day in the "Panic Zone" (left side). Vis 3 reveals the fear spike.

### Chapter 3: The Aftermath (January 29 - February 5, 2021)

The following week saw extreme volatility as the battle between retail buyers and short sellers continued. January 29 recorded the highest engagement (2,527 comments) with fear (1,211) and hype (1,179) nearly balanced—the community was split between panic and hope.

Prices swung wildly:
- Jan 29: $62.50 - $103.50 (closed at $81.25)
- Feb 2: Crashed to $18.56 (closed at $22.50)
- Feb 5: Recovered to $15.94

*Visual Evidence*: Vis 2's spiral shows the chaotic movement between quadrants. Vis 4's scatter plots reveal the extreme volatility cluster.

### Chapter 4: The Quiet Desperation (February 8-22, 2021)

As prices stabilized in the $10-15 range, engagement plummeted. The community was exhausted. Fear remained elevated (often 60-70%), but the volume of comments dried up—from thousands to dozens.

February 19 stands out: 79.5% fear ratio, but only 39 total comments. The remaining holders were fearful, but the crowd had moved on.

*Visual Evidence*: Vis 3 shows the stream narrowing dramatically. Vis 2's spiral moves to the bottom (low engagement).

### Chapter 5: The Dead Cat Bounce (February 24-26, 2021)

On February 24, GME suddenly spiked from $11.18 to $22.93—a 105% gain. Volume exploded to 332 million shares. The community roared back to life with 362 comments.

But this wasn't the same energy. The fear ratio remained high (64.3%), suggesting skepticism about the sustainability of the move. By February 26, prices had retreated to $25.43, and engagement faded again.

*Visual Evidence*: Vis 1 shows a small red candle on Feb 24. Vis 2's spiral makes a brief excursion back to high engagement. Vis 5 shows the fear line aligning with the volatility spike.

### The Meta-Narrative: Sentiment as a Leading Indicator

Our analysis suggests a provocative hypothesis: **Reddit fear predicts volatility**. 

When we shift the fear line backward by 1-2 days in Vis 5, the alignment with volatility improves. This implies that the emotional state of the WSB community—measurable through NLP analysis of comments—may precede price movements.

**Why would this happen?**
1. **Information asymmetry**: Retail investors may react to news faster than algorithms
2. **Sentiment contagion**: Fear spreads through social networks before affecting trading decisions
3. **Self-fulfilling prophecy**: If enough believers act on sentiment, it becomes reality

### Conclusion: The Anatomy of a Bubble

The GME saga follows a classic bubble pattern, visible in Vis 2's spiral:

1. **Stealth Phase**: Early believers accumulate (pre-January)
2. **Awareness Phase**: Price rises attract attention (early January)
3. **Mania Phase**: FOMO drives parabolic price action (late January)
4. **Blow-off Phase**: Restrictions and profit-taking trigger collapse (late January)
5. **Despair Phase**: Engagement fades, prices stabilize at lower levels (February)
6. **Echo Bubble**: A brief revival fails to regain momentum (late February)

The WSB community didn't just observe this bubble—they created it. Our dashboard captures the emotional heartbeat of a financial revolution.

---

## 🏗️ Technical Architecture

### Frontend Stack

- **D3.js v7**: Core visualization library for Vis 1, 3, and 5
- **Plotly.js**: Interactive 3D and SPLOM charts for Vis 2 and 4
- **Bootstrap 5**: Responsive grid and component styling
- **Custom CSS**: High-contrast design system

### Data Processing Stack

- **Python 3.8+**: Data processing and visualization generation
- **Pandas**: Data manipulation and cleaning
- **Plotly Express**: Python interface for generating HTML visualizations
- **NumPy**: Numerical computations

### Design Philosophy

- **High Contrast**: Pure white backgrounds (#ffffff) with bold, saturated colors
- **Accessibility**: Clear typography, sufficient color contrast, intuitive interactions
- **Performance**: Lightweight D3 code, optimized rendering, smooth animations

---

## 📁 Project Structure

```
GME-sentiment-analysis/
│
├── index.html                          # Main dashboard entry point
├── main.js                             # D3.js visualizations (Vis 1, 3, 5)
│
├── vis2.py                             # Market Spiral generator
├── vis2_market_spiral_perfect.html     # Animated spiral visualization
│
├── vis4_s.py                           # SPLOM generator
├── vis4_splom_final.html               # Risk correlation matrix
│
├── vis4_risk_fingerprint.py            # Alternative risk visualization
├── vis4_risk_fingerprint.html          # Risk fingerprint output
│
├── process_data.py                     # Data cleaning pipeline
│
├── dataset/                            # Data directory
│   ├── final_dataset_for_vis.csv       # Main dataset (30 days)
│   ├── top_comments.csv                # Curated comments for display
│   ├── reddit_wsb.csv                  # Raw Reddit data
│   ├── gme_sentiment_labeled.csv       # Full labeled dataset
│   ├── train_stockemo.csv              # Training split
│   ├── val_stockemo.csv                # Validation split
│   └── test_stockemo.csv               # Test split
│
├── 2301.09279v2.pdf                    # Research paper: "The GameStop Episode..."
├── 2512.20027v1.pdf                    # Research paper: "Social Media and Market Manipulation"
├── STATS401_6_Gao_Ning_Yu_Date.docx    # Academic report
│
└── README.md                           # This file
```

---

## 📚 Research Papers

This project references two academic papers included in the repository:

### 1. "The GameStop Episode: A Behavioral Finance Perspective" (2301.09279v2)

Analyzes the GME short squeeze through the lens of behavioral finance, examining:
- Herding behavior in retail investors
- The role of social media in information dissemination
- Regulatory implications of coordinated buying

### 2. "Social Media and Market Manipulation: Detection and Prevention" (2512.20027v1)

Explores:
- NLP techniques for sentiment analysis in financial contexts
- Machine learning models for detecting market manipulation
- The intersection of free speech and market integrity


### Data Usage

The Reddit data is used for academic and educational purposes under fair use. The stock data is publicly available market information.

---

## 🔮 Future Work

1. **Expand Temporal Scope**: Include data from 2020 and 2022-2023
2. **Multi-Ticker Analysis**: Compare GME with AMC, BB, and other "meme stocks"
3. **Machine Learning**: Predict volatility from sentiment features
4. **Real-Time Dashboard**: Live streaming of Reddit sentiment and price action
5. **Network Analysis**: Map user influence and information flow


*"Power to the Players"*