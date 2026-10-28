import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    BG_COLOR = RGBColor(15, 23, 42)       # Slate 900 #0F172A
    CARD_BG = RGBColor(30, 41, 59)        # Slate 800 #1E293B
    BORDER_COLOR = RGBColor(51, 65, 85)   # Slate 700 #334155
    CYAN = RGBColor(14, 165, 233)         # Sky 500   #0EA5E9
    EMERALD = RGBColor(16, 185, 129)      # Emerald 500 #10B981
    AMBER = RGBColor(245, 158, 11)        # Amber 500 #F59E0B
    WHITE = RGBColor(248, 250, 252)       # Slate 50  #F8FAFC
    MUTED = RGBColor(148, 163, 184)       # Slate 400 #94A3B8
    LIGHT_BLUE = RGBColor(56, 189, 248)   # Sky 400

    def apply_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category="RESEARCH & IMPLEMENTATION"):
        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CYAN
        p_cat.font.name = "Arial"

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.5), Inches(0.6))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE
        p_t.font.name = "Arial"

    def add_card(slide, left, top, width, height, title="", border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = CYAN
            p.font.name = "Arial"
        return shape

    def add_bullets(slide, left, top, width, height, items):
        tb = slide.shapes.add_textbox(left, top, width, height)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(8)
            p.font.size = Pt(12)
            p.font.name = "Arial"
            
            if isinstance(item, tuple):
                header, text = item
                r_h = p.add_run()
                r_h.text = f"{header}: "
                r_h.font.bold = True
                r_h.font.color.rgb = WHITE
                
                r_t = p.add_run()
                r_t.text = text
                r_t.font.color.rgb = MUTED
            else:
                r = p.add_run()
                r.text = item
                r.font.color.rgb = MUTED

    def set_notes(slide, notes):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_bg(s1)

    # Accent decorative pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(3.4), Inches(0.38))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(14, 165, 233)
    pill.line.fill.background()
    p_pill = pill.text_frame.paragraphs[0]
    p_pill.text = "FINANCIAL MACHINE LEARNING & RL"
    p_pill.font.size = Pt(10)
    p_pill.font.bold = True
    p_pill.font.color.rgb = RGBColor(15, 23, 42)
    p_pill.alignment = PP_ALIGN.CENTER

    # Main Title
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(2.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Dynamic Portfolio Optimization Using\nDeep Reinforcement Learning"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.font.name = "Arial"

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.9), Inches(11.5), Inches(1.0))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "A Comparative Study of Value-Based (DQN) and Policy-Gradient (A2C, PPO)\nArchitectures Evaluated Under Realistic Transaction Frictions"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = MUTED
    p_sub.font.name = "Arial"

    # Info Card
    add_card(s1, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.5), border_color=CYAN)
    items_card = [
        ("Author & Presenter", "Student / Primary Investigator"),
        ("Project Scope", "Autonomous asset allocation over S&P 500, DJIA, and Hang Seng Index"),
        ("Core Algorithms Benchmarked", "Deep Q-Network (DQN), Advantage Actor-Critic (A2C), Proximal Policy Optimization (PPO)"),
        ("Key Result", "A2C generated +16.11% total return with a 1.26 Sharpe Ratio, nearly doubling the market benchmark (+8.66%)")
    ]
    add_bullets(s1, Inches(1.1), Inches(5.4), Inches(11.1), Inches(1.2), items_card)

    set_notes(s1, "Good morning, Professor. Today I am presenting my project on Dynamic Portfolio Optimization using Deep Reinforcement Learning. In this research, I formulated the portfolio rebalancing problem as a continuous Markov Decision Process and developed an autonomous trading framework. I benchmarked three core RL paradigms—DQN, A2C, and PPO—under realistic transaction fee frictions, demonstrating that continuous actor-critic policy gradients generate superior risk-adjusted alpha compared to passive buy-and-hold strategies.")

    # =========================================================================
    # SLIDE 2: Problem Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_bg(s2)
    add_header(s2, "Problem Motivation: Why Traditional Quantitative Finance Fails", "CONTEXT & MOTIVATION")

    col_w = Inches(3.7)
    # Card 1: Modern Portfolio Theory
    add_card(s2, Inches(0.8), Inches(1.6), col_w, Inches(5.2), "1. Modern Portfolio Theory (MPT)")
    add_bullets(s2, Inches(1.05), Inches(2.2), col_w - Inches(0.5), Inches(4.3), [
        ("Origins", "Markowitz Mean-Variance Optimization (1952)."),
        ("Static Assumption", "Assumes stationary expected returns and constant covariance matrices."),
        ("Fragility", "Historical covariance breaks down during market shocks and volatility spikes."),
        ("Error Maximization", "Small estimation errors in return inputs produce drastically sub-optimal allocations."),
        ("Frictionless Flaw", "Ignores real-world slippage and transaction rebalancing costs.")
    ])

    # Card 2: Supervised Machine Learning
    add_card(s2, Inches(4.8), Inches(1.6), col_w, Inches(5.2), "2. Supervised Learning Flaws")
    add_bullets(s2, Inches(5.05), Inches(2.2), col_w - Inches(0.5), Inches(4.3), [
        ("Isolated Predictions", "Focuses purely on single-period direction (Up/Down or Next-day Close)."),
        ("No Action Space", "A price forecast does not determine the optimal multi-asset budget distribution."),
        ("Missing Feedback Loops", "Fails to consider compounding capital state $V_t$ over time."),
        ("Turnover Penalty", "Frequent high-conviction signals trigger aggressive rebalancing, destroying alpha via fees."),
        ("Risk Incompetence", "Does not natively penalize drawdown or optimize Sharpe Ratio.")
    ])

    # Card 3: Deep Reinforcement Learning
    add_card(s2, Inches(8.8), Inches(1.6), col_w, Inches(5.2), "3. The Reinforcement Learning Paradigm", border_color=EMERALD)
    add_bullets(s2, Inches(9.05), Inches(2.2), col_w - Inches(0.5), Inches(4.3), [
        ("Long-Term Utility", "Directly maximizes cumulative portfolio wealth and risk-adjusted returns."),
        ("Sequential Policy", "Considers current capital, market regime, and future discounted trajectory."),
        ("End-to-End Decision", "Directly maps continuous market states to asset weight allocation vectors."),
        ("Cost-Aware", "Penalizes turnover in the reward function, learning when to trade and when to hold."),
        ("Non-Stationary Adaptation", "Learns dynamic policies across varying macro cycles.")
    ])

    set_notes(s2, "In classical quantitative finance, Markowitz Mean-Variance optimization has been standard since 1952. However, it assumes fixed correlation matrices and normal distributions, which catastrophic market shocks disprove. Furthermore, supervised machine learning models only predict tomorrow's price direction—they cannot decide the exact continuous allocation vector across multiple assets and completely ignore trading fees. Reinforcement Learning solves this by directly training a policy that balances cumulative returns against downside drawdown and rebalancing friction.")

    # =========================================================================
    # SLIDE 3: MDP Formulation
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_bg(s3)
    add_header(s3, "Mathematical Framework: Formulating Portfolio Allocation as an MDP", "MATHEMATICAL FORMULATION")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "MDP Components: State & Action Spaces")
    add_bullets(s3, Inches(1.05), Inches(2.2), Inches(5.1), Inches(4.3), [
        ("State Space S_t in R^d", "Continuous vector capturing normalized returns, technical features, and macro indicators across global equity indices."),
        ("Stationarity Transformation", "Inputs are stationary percentage changes and relative oscillators rather than raw non-stationary price series."),
        ("Continuous Action Space (A2C/PPO)", "Allocation weight vector w_t = [w_sp500, w_djia, w_hsi]."),
        ("Simplex Constraint", "sum(w_i,t) = 1 and w_i,t >= 0. Enforced mathematically via Softmax projection to prevent leverage or short-selling."),
        ("Discrete Action Space (DQN)", "Discretized budget grid with 27 discrete asset combination classes.")
    ])

    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Reward Function with Transaction Cost Friction", border_color=CYAN)
    add_bullets(s3, Inches(7.05), Inches(2.2), Inches(5.2), Inches(4.3), [
        ("Reward Objective", "R_t = ln(V_t / V_{t-1}) - kappa * sum(|w_{i,t} - w_{i,t-1}|) - lambda * sigma_t"),
        ("Net Wealth Ratio ln(V_t / V_{t-1})", "The logarithmic growth of the portfolio NAV over the daily trading interval."),
        ("Transaction Friction Penalty (kappa)", "kappa = 0.001 (10 basis points / 0.10% fee per turnover unit). This heavily penalizes unnecessary portfolio churn."),
        ("Risk Regularization (lambda * sigma)", "Penalizes excessive local variance to promote capital stability during volatile regimes."),
        ("Discount Factor (gamma = 0.99)", "Ensures the agent prioritizes multi-month terminal wealth compounding rather than myopic single-day gains.")
    ])

    set_notes(s3, "To apply reinforcement learning rigorously, I formulated the portfolio rebalancing task as a Markov Decision Process. The state space S_t comprises stationary return vectors and macro features. For continuous policy gradient agents, the action vector w_t represents capital allocation across the S&P 500, DJIA, and Hang Seng Index, constrained to a probability simplex via Softmax. Crucially, my reward function does not reward raw return alone: it calculates the log-growth of net asset value and deducts a 10 basis point transaction cost penalty for every turnover change, discouraging high-frequency churning.")

    # =========================================================================
    # SLIDE 4: Data Engineering & EDA
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_bg(s4)
    add_header(s4, "Data Pipeline & Exploratory Data Analysis (34-Year Dataset)", "DATASET & PREPROCESSING")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2), "Multi-Decade Dataset & Temporal Partitioning")
    add_bullets(s4, Inches(1.05), Inches(2.2), Inches(5.5), Inches(4.3), [
        ("Global Multi-Asset Scope", "Covers 34 years of daily market history (1987-2022) across three distinct economic engines:"),
        ("S&P 500 (sp500)", "US large-cap technology and broad market growth engine."),
        ("Dow Jones (djia)", "US blue-chip industrial, defensive value foundation."),
        ("Hang Seng Index (hsi)", "Asian equities market, providing non-aligned geopolitical and temporal diversification."),
        ("Strict Temporal Train Split", "7,812 trading days (~1987 to 2018) reserved strictly for model training."),
        ("Validation Split", "Intermediate sequence used for hyperparameter tuning and early stopping."),
        ("Test Split (281 Days)", "Completely untouched forward test period used for out-of-sample evaluation."),
        ("Leakage Prevention", "Zero look-ahead bias; standard scalers and indicators fit strictly on historical windows.")
    ])

    corr_img = "slides_assets/correlation_matrix.png"
    if os.path.exists(corr_img):
        s4.shapes.add_picture(corr_img, Inches(7.1), Inches(1.6), width=Inches(5.4))

    set_notes(s4, "Our dataset spans 34 years of daily market trading from 1987 through recent history. We deliberately selected assets across differing geographic and economic spheres: the S&P 500 for broad growth, the Dow Jones for industrial value, and the Hang Seng Index for Asian market exposure. As shown in the correlation matrix, Hang Seng displays low correlation with US indices, offering genuine diversification. I enforced a strict temporal split with 7,812 days for training and an untouched 281-day test period, guaranteeing zero look-ahead data leakage.")

    # =========================================================================
    # SLIDE 5: Model Architectures
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_bg(s5)
    add_header(s5, "Deep RL Architectures: Value-Based vs. Policy-Gradient", "METHODOLOGY & ARCHITECTURES")

    col_w5 = Inches(3.7)
    add_card(s5, Inches(0.8), Inches(1.6), col_w5, Inches(5.2), "1. Deep Q-Network (DQN)")
    add_bullets(s5, Inches(1.05), Inches(2.2), col_w5 - Inches(0.5), Inches(4.3), [
        ("Paradigm", "Value-based temporal difference learning."),
        ("Q-Approximator", "Multi-layer perceptron estimating Q(s, a; theta) over 27 discretized allocation classes."),
        ("Experience Replay", "50,000 transition replay buffer decorrelates consecutive market steps."),
        ("Target Network", "Decoupled periodic target update prevents feedback divergence."),
        ("Limitation", "Discretization forces step-function portfolio weight jumps, increasing turnover friction.")
    ])

    add_card(s5, Inches(4.8), Inches(1.6), col_w5, Inches(5.2), "2. Advantage Actor-Critic (A2C)", border_color=EMERALD)
    add_bullets(s5, Inches(5.05), Inches(2.2), col_w5 - Inches(0.5), Inches(4.3), [
        ("Paradigm", "Synchronous on-policy Actor-Critic architecture."),
        ("Actor Network", "Outputs mean parameters mu(s) of a continuous Gaussian distribution for asset weights."),
        ("Critic Network", "Estimates baseline state-value V(s) to compute Advantage: A(s, a) = Q(s, a) - V(s)."),
        ("Advantage Estimation", "Reduces policy gradient variance while keeping bias minimal."),
        ("Continuous Execution", "Enables micro-rebalancing without paying full discrete-step fees.")
    ])

    add_card(s5, Inches(8.8), Inches(1.6), col_w5, Inches(5.2), "3. Proximal Policy Optimization (PPO)")
    add_bullets(s5, Inches(9.05), Inches(2.2), col_w5 - Inches(0.5), Inches(4.3), [
        ("Paradigm", "Trust-region policy gradient with clipped objective."),
        ("Clipped Surrogate Loss", "L^CLIP(theta) = E[min(r_t * A_t, clip(r_t, 1-eps, 1+eps) * A_t)]."),
        ("Clipping Parameter", "eps = 0.2 bounds policy update ratios r_t(theta) = pi_theta(a|s) / pi_old(a|s)."),
        ("Variance Reduction", "Generalized Advantage Estimation (GAE) with lambda = 0.95."),
        ("Behavior", "Guarantees monotonic policy improvement but leans conservative in financial volatility.")
    ])

    set_notes(s5, "I implemented two contrasting RL paradigms. First is DQN, which estimates optimal Q-values over discrete allocation choices using an experience replay buffer. However, discretizing asset weights creates step-function jumps. Second are policy gradient methods: A2C, which uses an actor network to output continuous portfolio weights and a critic to calculate advantage; and PPO, which adds a clipped surrogate loss to bound policy updates. As we will see, continuous control is essential for managing trading fees.")

    # =========================================================================
    # SLIDE 6: Training Setup & Hyperparameters
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_bg(s6)
    add_header(s6, "Training Pipeline, Hyperparameters & Convergence Dynamics", "EXPERIMENTAL SETUP")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Hyperparameter Specifications")
    add_bullets(s6, Inches(1.05), Inches(2.2), Inches(5.1), Inches(4.3), [
        ("Interaction Scale", "150,000 steps per algorithm (450,000 total market interactions)."),
        ("Hardware Acceleration", "CUDA PyTorch GPU training pipeline (NVIDIA Tensor Core architecture)."),
        ("Discount Factor (gamma = 0.99)", "Enforces multi-month terminal growth horizon."),
        ("Optimizer", "Adam (beta_1 = 0.9, beta_2 = 0.999, eps = 1e-8)."),
        ("DQN Parameters", "LR = 1e-4, Replay = 50,000, Exploration eps = 1.0 -> 0.05, Target update = 1,000."),
        ("A2C Parameters", "LR = 7e-4, Entropy coef = 0.01, Value coef = 0.5, RMSprop/Adam hybrid."),
        ("PPO Parameters", "LR = 3e-4, Rollout buffer = 2,048, Batch size = 64, Clip eps = 0.2, Epochs = 10.")
    ])

    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Training Convergence & Stability Observations", border_color=CYAN)
    add_bullets(s6, Inches(7.05), Inches(2.2), Inches(5.2), Inches(4.3), [
        ("Entropy Decay Monitoring", "Monitored policy entropy decay from -4.3 to -3.7, verifying that exploration smoothly transitioned into focused portfolio exploitation."),
        ("Critic Value Loss Convergence", "Critic MSE loss stabilized below 0.001 within the first 30,000 steps, providing accurate baseline value estimates."),
        ("DQN TD-Loss Behavior", "DQN exhibited high bellman loss variance due to discrete state switching under market volatility."),
        ("Model Checkpointing", "Full model weights serialized and saved as DQN_portfolio.zip, A2C_portfolio.zip, and PPO_portfolio.zip.")
    ])

    set_notes(s6, "Each model was trained for 150,000 interaction steps using CUDA GPU acceleration. I calibrated the discount factor to 0.99 to emphasize long-term capital preservation over myopic single-day gains. For A2C, an entropy coefficient of 0.01 maintained healthy exploration across the asset simplex before converging. The critic loss stabilized under 0.001 within 30,000 steps, demonstrating that the value network learned to accurately evaluate market baseline states.")

    # =========================================================================
    # SLIDE 7: Empirical Benchmark Results
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_bg(s7)
    add_header(s7, "Empirical Results: Test Set Benchmark Evaluation (281 Days)", "RESULTS & BENCHMARKING")

    # Table on Left
    table_shape = s7.shapes.add_table(5, 6, Inches(0.8), Inches(1.6), Inches(6.0), Inches(2.6))
    table = table_shape.table

    headers = ["Model / Strategy", "Final Value", "Return (%)", "CAGR", "Sharpe", "Max DD"]
    data = [
        ["🥇 A2C (Actor-Critic)", "$116,105", "+16.11%", "+14.33%", "1.26", "-9.02%"],
        ["Equal-Weight Base", "$108,656", "+8.66%", "+7.67%", "0.70", "-10.87%"],
        ["🥈 PPO (Proximal Policy)", "$106,595", "+6.60%", "+5.89%", "0.56", "-10.87%"],
        ["🥉 DQN (Discrete)", "$101,846", "+1.85%", "+1.65%", "0.19", "-12.40%"]
    ]

    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(14, 165, 233)
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(15, 23, 42)
        p.alignment = PP_ALIGN.CENTER

    for row_idx, row_data in enumerate(data):
        for col_idx, val in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(16, 185, 129) if row_idx == 0 and col_idx == 0 else (CARD_BG if row_idx % 2 == 0 else RGBColor(38, 51, 74))
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.bold = (row_idx == 0)
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    # Add Summary Card below table
    add_card(s7, Inches(0.8), Inches(4.5), Inches(6.0), Inches(2.4), "Core Empirical Takeaways", border_color=EMERALD)
    add_bullets(s7, Inches(1.05), Inches(5.0), Inches(5.5), Inches(1.7), [
        ("Alpha Outperformance", "A2C generated nearly 2x the return of the Equal-Weight market baseline (+16.11% vs +8.66%)."),
        ("Institutional Quality", "A2C achieved a 1.26 Sharpe Ratio, exceeding the 1.0 hedge-fund benchmark threshold."),
        ("Risk Reduction", "A2C held max drawdown to -9.02%, significantly outperforming the market's -10.87% drop.")
    ])

    growth_img = "slides_assets/portfolio_growth.png"
    if os.path.exists(growth_img):
        s7.shapes.add_picture(growth_img, Inches(7.1), Inches(1.6), width=Inches(5.4))

    set_notes(s7, "Here are the empirical results evaluated on the 281 unseen test days starting with $100,000 capital. A2C was our undisputed winner, compounding terminal wealth to $116,105—a +16.11% total return, almost doubling the +8.66% return of the passive Equal-Weight benchmark. In addition, A2C produced an institutional-grade Sharpe Ratio of 1.26 while capping maximum drawdown to just 9.02%, compared to over 10.8% for the market baseline and 12.4% for DQN.")

    # =========================================================================
    # SLIDE 8: In-Depth Discussion (Why A2C Won)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_bg(s8)
    add_header(s8, "Architectural Deep-Dive: Why Did A2C Beat DQN & PPO?", "ANALYSIS & INSIGHTS")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2), "The Mechanics of Policy Alpha vs Friction")
    add_bullets(s8, Inches(1.05), Inches(2.2), Inches(5.5), Inches(4.3), [
        ("The 'Discrete Curse' of DQN (+1.85%)", "DQN allocates across discrete buckets. Minor shifts in market indicators cause the Q-network to jump between discrete states."),
        ("High Turnover Friction", "Every discrete jump incur our 0.10% transaction fee. Over 281 days, churn fees eroded DQN's gross return."),
        ("The Continuous Edge of A2C (+16.11%)", "A2C outputs smooth continuous probability vectors, making micro-adjustments that ride asset momentum without generating turnover drag."),
        ("Optimal Exposure Timing", "A2C systematically favored US equity indices during bull legs and shifted exposure to HSI and cash-equivalents during corrections."),
        ("PPO's Conservatism (+6.60%)", "PPO's clipped surrogate bound [1-eps, 1+eps] prevented radical portfolio shifts, causing it to behave conservatively and mirror equal-weighting.")
    ])

    bars_img = "slides_assets/metrics_bars.png"
    if os.path.exists(bars_img):
        s8.shapes.add_picture(bars_img, Inches(7.1), Inches(1.6), width=Inches(5.4))

    set_notes(s8, "Why did A2C outperform DQN so dramatically? Portfolio weights are inherently continuous. DQN is forced into discrete buckets. When market noise fluctuates, DQN rapidly flips buckets, triggering heavy transaction fee penalties from our 10 basis point friction model. A2C, on the other hand, makes smooth, continuous adjustments. It held positions during steady trends and smoothly trimmed risk during declines. PPO was safe and profitable, but its clipped objective made it more conservative than A2C.")

    # =========================================================================
    # SLIDE 9: Risk Management & Drawdown
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_bg(s9)
    add_header(s9, "Risk Management: Downside Protection & Capital Preservation", "RISK MANAGEMENT")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2), "Capital Preservation Analysis")
    add_bullets(s9, Inches(1.05), Inches(2.2), Inches(5.5), Inches(4.3), [
        ("True Alpha Definition", "True quantitative performance is not just raw return, but return per unit of downside risk taken."),
        ("Sharpe Ratio (1.26 vs 0.70)", "A2C's Sharpe of 1.26 confirms its returns were earned via strategic timing rather than reckless volatility."),
        ("Drawdown Defense (-9.02%)", "During major test corrections where the market dropped -10.87%, A2C limited max loss to -9.02%."),
        ("Dynamic Hedging", "A2C's critic correctly identified high-volatility market states and commanded the actor to reduce portfolio beta before pullbacks expanded."),
        ("Downside Volatility Squeezing", "A2C achieved the highest Sortino and Calmar ratios across all evaluated strategies.")
    ])

    dd_img = "slides_assets/drawdown_chart.png"
    if os.path.exists(dd_img):
        s9.shapes.add_picture(dd_img, Inches(7.1), Inches(1.6), width=Inches(5.4))

    set_notes(s9, "In institutional finance, risk management is paramount. A2C achieved a Sharpe Ratio of 1.26. Any Sharpe above 1.0 is considered investment-grade by asset managers. Looking at maximum drawdown, while the passive benchmark suffered an 10.87% drawdown and DQN lost 12.4%, A2C restricted its peak-to-trough decline to 9.02%. This demonstrates that the agent learned true risk mitigation rather than taking high-beta gambles.")

    # =========================================================================
    # SLIDE 10: System Architecture & Dashboard
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_bg(s10)
    add_header(s10, "Full-Stack Deployment: Interactive Streamlit Dashboard", "SYSTEM ARCHITECTURE")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "1. Core RL Environment")
    add_bullets(s10, Inches(1.05), Inches(2.2), Inches(3.2), Inches(4.3), [
        ("portfolio_env.py", "Custom Gymnasium environment."),
        ("Dual Spaces", "Supports continuous Box actions (A2C/PPO) and Discrete action spaces (DQN)."),
        ("Transaction Modeling", "Calculates net rebalancing turnover and deducts realistic fees."),
        ("Info Dict Logging", "Emits net NAV, daily returns, and allocations for auditability.")
    ])

    add_card(s10, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "2. Training & Checkpointing")
    add_bullets(s10, Inches(5.05), Inches(2.2), Inches(3.2), Inches(4.3), [
        ("train_rl.py", "Automated training orchestrator."),
        ("Multi-Agent Loop", "Executes 150k timesteps across DQN, A2C, and PPO sequentially."),
        ("Model Persistence", "Saves compressed PyTorch policy checkpoints to /models."),
        ("Tuning Metadata", "Generates performance JSON summaries for reproducibility.")
    ])

    add_card(s10, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "3. Streamlit Web Dashboard", border_color=CYAN)
    add_bullets(s10, Inches(9.05), Inches(2.2), Inches(3.2), Inches(4.3), [
        ("app.py", "Production-grade Streamlit web interface running on localhost:8501."),
        ("EDA Tab Panel", "Visualizes 34-year distributions and correlation matrices."),
        ("Single Model Simulation", "Interactive trajectories, metrics, and JSON hyperparameters."),
        ("Compare All Engine", "Live benchmark plots and multi-model performance tables.")
    ])

    set_notes(s10, "To make this research accessible, I engineered a modular full-stack application. The core Gymnasium environment models transaction costs and simplex actions. The training pipeline trains and checkpoints all three agents. Finally, I built a Streamlit web dashboard running locally on port 8501, allowing users to explore data distributions, run single-model step-by-step simulations, and compare all models on live charts.")

    # =========================================================================
    # SLIDE 11: Engineering Challenges
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_bg(s11)
    add_header(s11, "Engineering Challenges & Production Solutions Overcome", "TECHNICAL CHALLENGES")

    col_w11 = Inches(5.6)
    add_card(s11, Inches(0.8), Inches(1.6), col_w11, Inches(2.4), "1. Realistic Friction Modeling")
    add_bullets(s11, Inches(1.05), Inches(2.1), col_w11 - Inches(0.5), Inches(1.7), [
        ("Challenge", "Academic RL models frequently assume zero friction, resulting in phantom alpha that collapses in live trading."),
        ("Solution", "Implemented turnover-based transaction cost penalty kappa = 0.001 directly into the MDP transition dynamics.")
    ])

    add_card(s11, Inches(6.8), Inches(1.6), col_w11, Inches(2.4), "2. Simplex Action Normalization")
    add_bullets(s11, Inches(7.05), Inches(2.1), col_w11 - Inches(0.5), Inches(1.7), [
        ("Challenge", "Continuous policy outputs can violate budget constraints or output negative weights (unintended shorting)."),
        ("Solution", "Constructed mathematical Softmax projections ensuring asset weights strictly sum to 1.0 with zero leverage.")
    ])

    add_card(s11, Inches(0.8), Inches(4.3), col_w11, Inches(2.5), "3. Cross-Environment Serialization")
    add_bullets(s11, Inches(1.05), Inches(4.8), col_w11 - Inches(0.5), Inches(1.8), [
        ("Challenge", "Cloud training on Kaggle GPU serialized checkpoints using NumPy 2.x ABI, causing unpickling errors on local environments."),
        ("Solution", "Upgraded PyTorch and Gymnasium runtime binaries to ensure full cross-platform deserialization compatibility.")
    ])

    add_card(s11, Inches(6.8), Inches(4.3), col_w11, Inches(2.5), "4. Non-Stationarity Mitigation", border_color=EMERALD)
    add_bullets(s11, Inches(7.05), Inches(4.8), col_w11 - Inches(0.5), Inches(1.8), [
        ("Challenge", "Raw stock price indices exhibit non-stationary upward drift over 34 years, causing neural networks to diverge."),
        ("Solution", "Engineered relative return series and bounded technical oscillators, guaranteeing stationary Markov state inputs.")
    ])

    set_notes(s11, "Developing a reliable financial RL system required solving several critical engineering hurdles. First, modeling transaction friction was necessary to prevent illusory alpha. Second, I enforced a strict probability simplex on action outputs to guarantee valid 100% budget constraints without short-selling. Third, I resolved cross-platform tensor serialization between cloud GPU training and local deployment. Finally, transforming raw prices into stationary percentage returns allowed the networks to generalize across multi-decade market regimes.")

    # =========================================================================
    # SLIDE 12: Conclusion & Future Scope
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_bg(s12)
    add_header(s12, "Conclusions & Future Research Directions", "CONCLUSION & OUTLOOK")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Key Research Conclusions", border_color=EMERALD)
    add_bullets(s12, Inches(1.05), Inches(2.2), Inches(5.1), Inches(4.3), [
        ("RL Viability", "Deep Reinforcement Learning can successfully learn dynamic asset allocation strategies that outperform passive buy-and-hold benchmarks."),
        ("Continuous Supremacy", "Continuous actor-critic methods (A2C) significantly outperform discrete value-based approaches (DQN) by eliminating discretization churn."),
        ("Superior Risk-Adjusted Alpha", "A2C achieved +16.11% total return and an institutional-grade 1.26 Sharpe Ratio, doubling the market baseline (+8.66%)."),
        ("Downside Protection", "RL agents act as active risk managers, curtailing maximum drawdown to -9.02%."),
        ("Turnover Awareness", "Incorporating transaction costs in the reward function is mandatory to generate viable trading policies.")
    ])

    add_card(s12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Future Research Directions")
    add_bullets(s12, Inches(7.05), Inches(2.2), Inches(5.2), Inches(4.3), [
        ("Expanded Asset Universe", "Scaling from 3 macro indices to 50+ individual equities, corporate bonds, commodities, and crypto assets."),
        ("Temporal Attention / Transformers", "Integrating Temporal Fusion Transformers (TFT) or LSTM recurrent layers to model multi-scale temporal dependencies."),
        ("Risk-Constrained Objectives", "Incorporating Conditional Value-at-Risk (CVaR) and Maximum Drawdown constraints directly into the policy loss function."),
        ("Multi-Agent Competitive RL", "Simulating multi-agent market ecosystems with order book slippage and market impact dynamics."),
        ("Live API Paper Trading", "Connecting the Streamlit engine to Alpaca or Interactive Brokers APIs for real-time paper execution.")
    ])

    set_notes(s12, "In conclusion, this project demonstrates that deep reinforcement learning can dynamically optimize multi-asset portfolios and beat conventional passive baselines under realistic fee constraints. Continuous actor-critic methods proved vastly superior to discrete DQN by minimizing fee friction. In the future, I plan to expand this framework to larger asset universes and integrate Transformer-based state encoders. Thank you for your time, and I would be delighted to take any questions.")

    output_path = "Deep_RL_Portfolio_Optimization_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_deck()
