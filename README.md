# Deep Reinforcement Learning for Dynamic Multi-Asset Portfolio Optimization

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![Gymnasium](https://img.shields.io/badge/Gymnasium-v0.29+-darkgreen.svg)](https://gymnasium.farama.org/)
[![Stable-Baselines3](https://img.shields.io/badge/Stable--Baselines3-v2.2+-brightgreen.svg)](https://stable-baselines3.readthedocs.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end quantitative trading and deep reinforcement learning framework that autonomously optimizes dynamic capital allocations across international equity indices (**S&P 500**, **Dow Jones Industrial Average**, and **Hang Seng Index**). 

The system benchmarks value-based (**DQN**) versus continuous policy-gradient (**A2C** and **PPO**) architectures evaluated over 34 years of daily market and macroeconomic history under realistic transaction costs ($0.10\%$ fee per turnover). Results are visualized through an interactive Streamlit web application.

---

## 📈 Empirical Performance & Out-of-Sample Benchmark

All models were evaluated on the **unseen forward test period (281 consecutive trading days)** starting with **$100,000.00** initial capital:

| Algorithm / Strategy | Action Space | Final Value | **Total Return (%)** | Annualized Return (CAGR) | **Sharpe Ratio** | **Max Drawdown** | Directional F1 Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 **A2C (Advantage Actor-Critic)** | Continuous | **$116,105.37** | **+16.11%** | **+14.33%** | **1.26** | **-9.02%** | **0.57** |
| 📊 *Equal-Weight Baseline (1/3 each)* | Passive | $108,655.61 | **+8.66%** | +7.67% | 0.70 | -10.87% | Benchmark |
| 🥈 **PPO (Proximal Policy Optimization)** | Continuous | **$106,595.01** | **+6.60%** | **+5.89%** | **0.56** | **-10.87%** | 0.57 |
| 🥉 **DQN (Deep Q-Network)** | Discrete (27 bins) | **$101,846.41** | **+1.85%** | **+1.65%** | **0.19** | **-12.40%** | 0.56 |

### 💡 Core Insights
1. **Continuous Action Superiority**: Continuous actor-critic agents substantially outperformed discrete DQN. Continuous action spaces allow smooth, micro-weight rebalancing without jumping between coarse discrete buckets.
2. **Transaction Cost Drag**: DQN suffered from frequent discrete state flips, accumulating heavy friction from the $0.10\%$ transaction fee penalty. A2C maintained steady momentum exposure, reducing turnover drag.
3. **Institutional Risk-Adjusted Alpha**: **A2C generated nearly 2x the passive market return (+16.11% vs +8.66%)** with an institutional-grade **Sharpe Ratio of 1.26** and the lowest maximum drawdown (**-9.02%**).

---

## 🔬 Mathematical Formulation (MDP Framework)

The portfolio optimization problem is framed as a discrete-time, finite-horizon Markov Decision Process $(S, A, P, R, \gamma)$:

### 1. State Space ($S_t \in \mathbb{R}^{d}$)
* Stationarized daily percentage returns for the S&P 500, DJIA, and Hang Seng Index.
* Macroeconomic indicators and technical context:
  * **VIX**: Chicago Board Options Exchange Volatility Index.
  * **ADS Index**: Aruoba-Diebold-Scotti business conditions index.
  * **US 3-Month T-Bill Rate**: Risk-free benchmark.
  * **EPU**: Economic Policy Uncertainty Index.
  * **GPRD**: Geopolitical Risk Daily Index.
  * Moving averages, 10-day rolling volatilities, and trading volumes.

### 2. Action Space ($A_t$)
* **Continuous (A2C, PPO)**: A 3-dimensional allocation vector $w_t = [w_{\text{sp500}}, w_{\text{djia}}, w_{\text{hsi}}]$ projected onto the probability simplex:
  $$\sum_{i=1}^{3} w_{i,t} = 1, \quad w_{i,t} \ge 0 \quad \forall i$$
* **Discrete (DQN)**: 27 discrete allocation weight combinations spanning $\{0.0, 0.5, 1.0\}$.

### 3. Reward Function with Realistic Friction ($R_t$)
$$\mathcal{R}_t = \ln\left(\frac{V_t}{V_{t-1}}\right) - \kappa \sum_{i=1}^{3} |w_{i,t} - w_{i,t-1}| - \lambda \cdot \sigma_t$$
* $\ln(V_t / V_{t-1})$: Logarithmic growth of net portfolio value.
* $\kappa = 0.001$: **10 basis points (0.10%)** transaction fee deducted per unit of portfolio turnover.
* $\lambda \cdot \sigma_t$: Risk penalty discouraging excessive localized variance.
* $\gamma = 0.99$: Discount factor prioritizing multi-month compounding wealth over myopic day-trading.

---

## 🏛️ System Architecture & Project Structure

```
.
├── data_prepared/              # 34 years of preprocessed daily financial data
│   ├── train.csv               # 7,812 trading days (~1987 to 2018)
│   ├── val.csv                 # Out-of-sample hyperparameter tuning set
│   └── test.csv                # 281-day untouched forward evaluation set
├── models/                     # Trained RL model weights
│   ├── A2C_portfolio.zip       # Advantage Actor-Critic policy weights
│   ├── DQN_portfolio.zip       # Deep Q-Network weights
│   └── PPO_portfolio.zip       # Proximal Policy Optimization weights
├── slides_assets/              # High-resolution benchmark charts & visual figures
│   ├── correlation_matrix.png  # Asset cross-correlation heatmap
│   ├── drawdown_chart.png      # Underwater drawdown dynamics
│   ├── metrics_bars.png        # Comparative return % & Sharpe ratio bars
│   └── portfolio_growth.png    # Cumulative trajectory comparison
├── app.py                      # Production Streamlit visual dashboard
├── portfolio_env.py            # Custom Gymnasium trading environments
├── train_rl.py                 # Multi-agent automated GPU training pipeline
├── tuning_results.json         # Hyperparameter grid search records
├── create_presentation.py      # Automated PPTX slide generator
├── Deep_RL_Portfolio_Optimization_Presentation.pptx # 12-slide presentation deck
├── PRESENTATION_GUIDE.md       # Full slide script & presenter notes
├── requirements.txt            # Python environment dependencies
└── README.md                   # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository & Set Up Environment

```bash
git clone https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
cd <YOUR-REPO-NAME>

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch the Interactive Dashboard

Pre-trained model weights are included in `models/`. Run the dashboard immediately:

```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser. The dashboard includes:
* **Exploratory Data Analysis (EDA)**: Interactive price series, return distributions, and correlation matrices.
* **Single Model Simulation**: Trajectory step-by-step simulations, Sharpe ratios, and max drawdown.
* **Compare All Engine**: Direct side-by-side benchmarking of all agents against the market baseline.

### 3. Re-train Models (Optional)

To retrain all 3 algorithms from scratch using GPU acceleration:

```bash
python train_rl.py
```

---

## 📊 Presentation Materials

This repository includes a 12-slide presentation for academic or professional defense:
* 📑 **PowerPoint Deck**: [`Deep_RL_Portfolio_Optimization_Presentation.pptx`](Deep_RL_Portfolio_Optimization_Presentation.pptx) (Widescreen 16:9, modern financial dark-theme, embedded charts, and speaker notes).
* 📝 **Speaker Script & Guide**: [`PRESENTATION_GUIDE.md`](PRESENTATION_GUIDE.md) (Slide-by-slide word-for-word presenter scripts).

---

## 🛠️ Technology Stack

* **Core Framework**: Python 3.10+, PyTorch, Gymnasium
* **Reinforcement Learning**: Stable-Baselines3 (DQN, A2C, PPO)
* **Data Processing & Analytics**: Pandas, NumPy, Scikit-Learn
* **Visualization & UI**: Streamlit, Matplotlib
* **Presentation Automation**: Python-pptx

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
