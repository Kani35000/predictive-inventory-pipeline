# Predictive Inventory Management Pipeline
## Reorder Point & Demand Forecasting Model for Retail Distribution Networks

> **Kani Okorji** | Data Analyst | Supply Chain & Inventory Analytics
> SQL • Python • Power BI • REST API | Manhattan Associates | IBM Cognos
>
> A predictive analytics extension of the Retail Inventory Optimization Pipeline
> applying demand forecasting and reorder point optimization to prevent the 
> $163.9M in stockout losses identified in Phase 1.
>
> 📍 Dallas, TX | 🔗 [LinkedIn](https://www.linkedin.com/in/kani-okorji-20869666/) | 💻 [GitHub](https://github.com/Kani35000)

---

## 🔗 Related Project
This project is a direct extension of:
[Retail Inventory Optimization & Profitability Protection Pipeline](https://github.com/Kani35000/retail-inventory-pipeline)

Phase 1 → Quantified the losses (descriptive analytics)
Phase 2 → Prevents the losses (predictive analytics)

---

## Business Problem
Phase 1 identified $163.9M in stockout losses across 5 distribution centers.
The question Phase 2 answers:

**"How do we prevent these losses before they happen?"**

---

## What This Project Solves
1. When should each warehouse reorder each product?
2. How much safety stock should be maintained?
3. Which products are at highest stockout risk in the next 30 days?
4. What is the optimal reorder quantity per product per warehouse?
5. How much could proactive reordering save annually?

---

## 📊 KPI Story Arc
| KPI | Focus | Business Question |
|---|---|---|
| KPI 1 | Average Daily Demand | What is our baseline demand per product? |
| KPI 2 | Demand Variability | How unpredictable is demand? |
| KPI 3 | Reorder Point | When should we trigger a purchase order? |
| KPI 4 | Safety Stock | How much buffer inventory is needed? |
| KPI 5 | Stockout Risk Score | Which products face highest stockout risk? |
| KPI 6 | Demand Forecast | What will demand look like next 30 days? |
| KPI 7 | Optimal Order Quantity | How much should we order? |
| KPI 8 | Projected Savings | How much can proactive reordering save? |

---

## Tech Stack
| Layer | Tool | Purpose |
|---|---|---|
| Database | PostgreSQL | Data storage and KPI queries |
| Data Processing | Python (pandas) | Pipeline automation |
| Statistical Analysis | statsmodels | Time series analysis |
| ML Baseline | scikit-learn (Linear Regression) | Demand forecast baseline model |
| ML Advanced | scikit-learn (Random Forest) | Feature based demand forecasting |
| ML Time Series | Prophet | Seasonal demand forecasting with confidence intervals |
| Model Evaluation | scikit-learn (RMSE, MAE) | Model accuracy comparison and selection |
| Dashboard | Power BI | Executive visualization |
| API | FastAPI | REST endpoints |
| Version Control | Git + GitHub | Code management |

---

## Project Architecture
```
predictive-inventory-pipeline/
├── 01_database/        # sql queries
├── 02_forecasting/     # Demand forecasting scripts
├── 03_ML_forecast/     # Machine Learning Forecast
├── 04_powerbi/         # Predictive dashboard
└── README.md
```

## 📌 Project Status
| Layer | Status |
|---|---|
| Database Connection | ✅ Complete|
| Demand Analysis | ✅ Complete |
| Reorder Point per SKU per Warehouse | ✅ Complete |
| Safety Stock Optimization | ✅ Complete |
| Demand Forecasting Model | ✅ Complete |
| Stockout Risk Scoring | ✅ Complete  |
| Power BI Predictive Dashboard | 🔨 Planned |
| Research Publication | 🔨 Planned |

---

## Database
This project connects to the existing 
retail_analytics PostgreSQL database 
established in Phase 1.

See: [Phase 1 Database Setup](https://github.com/Kani35000/retail-inventory-pipeline)

### Configure Database Connection
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_analytics
DB_USER=postgres
DB_PASSWORD=your_password
```

## 📌 KPI Progress

| KPI | Description | Status |
|---|---|---|
| KPI 1 | Average Daily Demand | ✅ Complete |
| KPI 2 | Demand Variability (CV%) | ✅ Complete |
| KPI 3 | Reorder Point | ✅ Complete |
| KPI 4 | Safety Stock | ✅ Complete |
| KPI 5 | 7-Day Moving Average | ✅ Complete |
| KPI 6 | 30-Day Moving Average | ✅ Complete |
| KPI 7 | Stockout Risk Score | ✅ Complete |
| KPI 8 | Projected Savings | ✅ Complete |
| KPI 9 | Economic Order Quantity | 🔨 Planned |

## 📊 KPI Story Arc

| KPI | Method | Type |
|---|---|---|
| KPI 1-2 | Demand Analysis | Descriptive |
| KPI 3-4 | Reorder Point & Safety Stock | Deterministic |
| KPI 5-6 | Moving Average Forecast | Statistical |
| KPI 7 | Stockout Risk Score | Analytical |
| KPI 8 | Projected Savings | Scenario Analysis |
| KPI 9 | Linear Regression Forecast | Machine Learning |
| KPI 10 | Prophet Seasonal Forecast | Advanced ML |

## Pipeline Structure
```
02_forecasting/
├── db_connection.py      ← connect to database
├── extract_data.py       ← pull transactions
├── demand_analysis.py    ← KPI 1 & 2
├── reorder_point.py      ← KPI 3 & 4
├── demand_forecast.py    ← KPI 5 & 6
├── stockout_risk.py      ← KPI 7
├── savings_analysis.py   ← KPI 8
└── kpi_summary.py        ← combine all
```

## 🔬 Methodology
### Reorder Point Formula
ROP = (Average Daily Demand × Lead Time) + Safety Stock

### Safety Stock Formula
Safety Stock = Z × σ × √Lead Time
Where:
Z  = service level factor (1.65 for 95% service level)
σ  = standard deviation of daily demand
Lead Time = days for new order to arrive

### Demand Forecasting Approach
Method 1 → Moving Average (baseline)
Method 2 → Exponential Smoothing
Method 3 → Prophet (seasonal decomposition)


### Stockout Risk Scoring
Risk classification combines three analytical layers:

**Layer 1 — Demand Analysis:**
avg_daily_demand = AVG(units_sold) per SKU per warehouse
std_daily_demand = STDDEV(units_sold) — demand variability
demand_variability_pct = (std / avg) × 100 — coefficient of variation

**Layer 2 — Safety Stock Calculation:**
Safety Stock = Z × σ × √Lead Time
Where:
Z         = 1.65 (95% service level)
σ         = std_daily_demand
Lead Time = 7 days (assumed constant)

**Layer 3 — Reorder Point:**
ROP = (avg_daily_demand × lead_time) + safety_stock

**Layer 4 — Risk Classification:**
days_until_stockout = current_inventory / avg_daily_demand
CRITICAL → < 7 days  → Immediate reorder required
HIGH     → < 14 days → Reorder this week
MEDIUM   → < 30 days → Monitor closely
LOW      → 30+ days  → Sufficient stock

### Demand Forecasting
Moving average analysis using SQL window functions:
SMA_7  = 7 day simple moving average
SMA_30 = 30 day simple moving average
Divergence signal = SMA_7 - SMA_30

Significant divergence (>10 units) identified in 
47 of 500 SKU-warehouse combinations (9.4%) 
requiring immediate reorder point review.
---

### 📊 Demand Forecast Insights
| Finding | Observation | Implication |
|---|---|---|
| SMA_7 ≈ SMA_30 | Demand is stable across most SKUs | Fixed reorder points are reliable |
| Low SMA divergence | No dramatic short term spikes | Current safety stock buffers adequate |
| Seasonal divergence | SMA_7 > SMA_30 in Q4 | Reorder points need upward adjustment in holiday period |

> **Conclusion:** The similarity between 7-day and 
> 30-day moving averages confirms stable baseline 
> demand across warehouses. Divergence periods 
> concentrated in Q4 validate the seasonal 
> patterns identified in Phase 1 turnover analysis.

#### Demand Trend Analysis (Divergence > 10 units)
| Finding | Count | Implication |
|---|---|---|
| Products with increasing demand | 24 | Reorder points need upward adjustment |
| Products with decreasing demand | 23 | Risk of overstock — reduce order quantities |
| Total significant divergences | 47 of 500 SKUs (9.4%) | Targeted reorder review required |

#### Key Findings
| Warehouse | Pattern | Action Required |
|---|---|---|
| Dallas | Multiple products with increasing demand | Elevate reorder points for flagged SKUs |
| Los Angeles | Fragrance Product 96 consistently declining | Reduce safety stock for this SKU |
| Chicago | Mixed signals — seasonal products volatile | Dynamic reorder points for seasonal category |
| New Jersey | Multiple declining products | Monitor for overstock risk |

#### Product Category Intelligence
| Category | Trend | Implication |
|---|---|---|
| Seasonal | Highest divergence frequency | Requires dynamic reorder points |
| Fragrance | Mixed signals by warehouse | Warehouse specific reorder strategy |
| Body Care | Mostly positive signals | Increasing demand across network |
| Lotion | Mixed signals | Monitor individually |

> **Conclusion:** 9.4% of SKU-warehouse combinations 
> show significant demand divergence requiring 
> immediate reorder point review. Seasonal products 
> exhibit the highest volatility confirming the need 
> for dynamic rather than fixed reorder points — 
> particularly critical in pharmaceutical supply chains 
> where demand spikes cannot be met with delayed 
> replenishment.
---
### 🚨 Stockout Risk Analysis
| Risk Level | SKU Count | % of Network | Days Until Stockout |
|---|---|---|---|
| 🚨 CRITICAL | ~240 | 48% | < 7 days |
| 🔴 HIGH | ~60 | 12% | 7-14 days |
| 🟡 MEDIUM | ~30 | 6% | 14-30 days |
| 🟢 LOW | 1 | 0.2% | 30+ days |

> **Critical Finding:** 60% of all SKU-warehouse 
> combinations are at CRITICAL or HIGH stockout 
> risk confirming the $163.9M in stockout losses 
> identified in Phase 1. Only 1 of 500 SKUs 
> maintains adequate inventory levels.

### 🏭 Most Critical Warehouses
| Warehouse | Most Critical SKU | Current Inventory | Days Until Stockout |
|---|---|---|---|
| Dallas | Seasonal Product 39 | -946 units | -20 days |
| Atlanta | Fragrance Product 11 | -849 units | -18 days |
| New Jersey | Body Care Product 60 | -839 units | -18 days |
| Los Angeles | Fragrance Product 61 | -757 units | -16 days |
| Chicago | Seasonal Product 34 | -641 units | -14 days |

### 💡 Connected Insights — Phase 1 vs Phase 2
| Finding | Phase 1 | Phase 2 |
|---|---|---|
| Dallas risk | High shrinkage 8.97% | Most critical stockout -946 units |
| Atlanta risk | High stockout loss $38.3M | Second most critical -849 units |
| Network exposure | $163.9M stockout losses | 60% SKUs at critical/high risk |
| Inventory health | 28,769 stockout events | Only 1 SKU with adequate stock |

> **Conclusion:** Phase 2 risk analysis confirms and 
> quantifies the inventory crisis identified in Phase 1. 
> The reorder point and safety stock framework reveals 
> that network wide inventory replenishment is urgently 
> required with Dallas and Atlanta requiring immediate 
> intervention.

### 💰 Projected Savings from Inventory Optimization

**Business Question:**
"If we implement proper reorder points and safety 
stock what percentage of $163.9M in stockout 
losses can we prevent?"

| Scenario | Prevention Rate | Network Savings | Remaining Loss |
|---|---|---|---|
| Conservative | 70% | $114.7M | $49.1M |
| Moderate | 80% | $131.1M | $32.8M |
| Aggressive | 90% | $147.5M | $16.4M |

#### Savings by Warehouse (Conservative 70%)
| Warehouse | Current Loss | Projected Savings | Remaining Loss |
|---|---|---|---|
| Atlanta DC | $38.3M | $26.8M | $11.5M |
| Los Angeles DC | $35.4M | $24.8M | $10.6M |
| New Jersey DC | $33.7M | $23.6M | $10.1M |
| Dallas DC | $29.9M | $20.9M | $9.0M |
| Chicago DC | $26.6M | $18.6M | $8.0M |

> **Conclusion:** Implementing the reorder point 
> and safety stock framework developed in Phase 2 
> could prevent between $114.7M (conservative) 
> and $147.5M (aggressive) of the $163.9M in 
> stockout losses identified in Phase 1 — 
> representing a 70-90% reduction in inventory 
> loss exposure across the distribution network.

> **Phase 1 → Phase 2 Connection:** Phase 1 
> quantified $163.9M in losses. Phase 2 provides 
> the optimization framework to prevent them. 
> Together they form a complete inventory 
> analytics solution.

## 🔗 Phase 1 → Phase 2 Connected Intelligence

| Metric | Phase 1 Finding | Phase 2 Action |
|---|---|---|
| Chicago shrinkage 9.01% | High loss warehouse | ROP = 422 units avg |
| Dallas shrinkage 8.97% | High loss warehouse | Most critical SKU -946 units |
| Atlanta stockout $38.3M | Demand driven losses | 60% SKUs at critical risk |
| LA stockout $35.4M | Demand driven losses | Highest divergence signals |
| $163.9M total exposure | Phase 1 quantified | Phase 2 can prevent $114.7M-$147.5M |

> **The Complete Story:**
> Phase 1 diagnosed the problem.
> Phase 2 builds the prevention system.
> Together they form a complete
> inventory analytics solution.

## 🔗 Conclusive Intelligence
KPI 1-2 → Demand Analysis:
→ 500 SKU-warehouse combinations analyzed
→ Avg daily demand: 43-48 units/day
→ Demand variability: ~40% CV
→ Moderate but consistent volatility

KPI 3-4 → Reorder Point:
→ Average safety stock: ~82 units
→ Average reorder point: ~410 units
→ Lead time assumption: 7 days
→ Service level: 95% (Z=1.65)

KPI 5-6 → Demand Forecast:
→ 116 high risk divergence signals
→ 9.4% of SKUs showing significant
   demand shift in last 30 days
→ Seasonal products most volatile
→ Dallas showing highest positive signals

KPI 7 → Stockout Risk:
→ ~240 SKUs CRITICAL (<7 days)
→ ~60 SKUs HIGH (7-14 days)
→ ~30 SKUs MEDIUM (14-30 days)
→ 1 SKU LOW (30+ days)
→ Dallas worst: -946 units

KPI 8 → Projected Savings:
→ Conservative: $114.7M recoverable
→ Moderate:     $131.1M recoverable
→ Aggressive:   $147.5M recoverable

## 🤖 ML Forecasting Methodology

### Model Validation Approach
All models evaluated using holdout validation:
Training Set → Days 1-336   (first 336 days)
Test Set     → Days 337-366 (last 30 days)
Forecast     → Days 367-396 (next 30 days)

This ensures RMSE and MAE metrics reflect 
true out-of-sample forecasting accuracy 
rather than in-sample fit.

### Evaluation Metrics
| Metric | Formula | Interpretation |
|---|---|---|
| RMSE | √(mean(actual - predicted)²) | Penalizes large errors more |
| MAE | mean(|actual - predicted|) | Average absolute error in units |

### Models Implemented
| Model | Type | Strengths |
|---|---|---|
| Linear Regression | Baseline ML | Simple trend detection |
| Random Forest | Ensemble ML | Non-linear patterns, feature importance |
| Prophet | Time Series ML | Seasonality, confidence intervals |


#### Linear Regression (Baseline)
| Metric | Value | Interpretation |
|---|---|---|
| Avg RMSE | 22.37 units | Avg prediction error on test set |
| Avg MAE | 19.32 units | Avg absolute error on test set |
| Error Rate | ~49% | High — cannot capture seasonality |
| Increasing Trends | 499/500 SKUs | Demand growth across network |
| Decreasing Trends | 0/500 SKUs | No declining demand detected |

> **Conclusion:** Linear Regression establishes 
> baseline performance but high error rate (49%) 
> confirms demand patterns are non-linear — 
> motivating Random Forest and Prophet models.

### Output Analysis
RMSE = 22.37 (test set)
MAE  = 22.37 (test set)

This means:
→ Linear Regression predicts demand
   within ~19-22 units on average
→ Average daily demand = 45 units
→ Error rate = 22/45 = ~49%

This is expected for Linear Regression:
→ Cannot capture non-linear patterns
→ Cannot capture seasonality
→ Random Forest will improve this
→ Prophet will improve further

Interesting finding:
→ 499 of 500 SKUs show increasing trend
→ Only 1 stable
→ Suggests overall demand growth
   across simulation period

#### Random Forest (Coming Soon)
→ Feature engineering with seasonality variables
→ Expected RMSE improvement over baseline
→ Feature importance analysis

#### Prophet (Coming Soon)
→ Time series seasonal decomposition
→ Q4 holiday demand capture
→ Confidence interval forecasting

### 📊 Model Comparison Framework
| Model | RMSE | MAE | Captures Seasonality |
|---|---|---|---|
| Linear Regression | 22.37 | 19.32 | ❌ |
| Random Forest | 11.55 | 9.81 | ✅ Partial |
| Prophet | 🔨 In Progress | 🔨 | ✅ Full |

Improvement Comparing Linear Regression and Random Forest:
RMSE reduced by 48% ✅
MAE  reduced by 49% ✅

Random Forest is nearly 2x more accurate
### Model Evaluation Framework
All models evaluated using holdout validation:
Train set → Days 1-336 (first 336 days)
Test set  → Days 337-366 (last 30 days)
Forecast  → Days 367-396 (next 30 days)

This ensures RMSE and MAE metrics reflect 
true out-of-sample forecasting accuracy 
rather than in-sample fit.

### Evaluation Metrics
| Metric | Formula | Interpretation |
|---|---|---|
| RMSE | √(mean(y_pred - y_true)²) | Penalizes large errors more |
| MAE | mean(|y_pred - y_true|) | Average absolute error in units |

### Models Implemented
| Model | Type | Strengths |
|---|---|---|
| Linear Regression | Baseline ML | Trend detection, interpretable |
| Random Forest | Ensemble ML | Non-linear patterns, feature importance |
| Prophet | Time Series ML | Seasonality, confidence intervals |

RMSE = 22.37 units
MAE  = 22.37 units

Meaning:
→ On average predictions are off
   by ~19 units per day
→ Given avg demand of ~46 units/day
→ Error rate = 19/46 = 41%
→ Linear Regression alone is insufficient
→ This is exactly why we need
   Random Forest and Prophet

Trend findings:
→ 499 of 500 SKUs showing increasing trend
→ Only 1 stable
→ This is suspicious — likely simulation artifact
→ Linear model detecting noise as trend
→ Random Forest and Prophet should give more reliable results

### 🤖 ML Model Results

#### Linear Regression (Baseline)
| Metric | Value | Interpretation |
|---|---|---|
| Avg RMSE | 22.37 units | ~48% error rate on avg demand |
| Avg MAE | 19.32 units | Off by 19 units per day |
| Increasing trends | 499/500 | Likely noise detection |
| Limitation | Linear only | Cannot capture seasonality |

#### Random Forest
✅ Random Forest forecast complete
   SKUs modeled:    500
   Avg RMSE (test): 11.55
   Avg MAE (test):  9.81
   Top Features:
top_feature
rolling_7            306
is_holiday_season    192
month                  2

#### Prophet
→ Results after running

#### Model Comparison
| Model | RMSE | MAE | Best For |
|---|---|---|---|
| Linear Regression | 22.37 | 19.32 | Baseline benchmark |
| Random Forest | 11.55 | 9.81 | Feature based patterns |
| Prophet | TBD | TBD | Seasonal time series |

#### Feature Importance Intelligence from Random Forest
Top features:
rolling_7         → 306 SKUs (61%)
is_holiday_season → 192 SKUs (38%)
month             →   2 SKUs  (1%)

This tells us:
→ Recent sales momentum (rolling_7)
   is the strongest predictor
→ Holiday season flag is second most
   important for 38% of SKUs
→ Confirms Phase 1 seasonal finding
→ Q4 demand pattern is real and predictable


> **Conclusion:** To be documented after
> all three models complete

## 🔬 Limitations & Further Investigation

### Lead Time Assumption
Current model assumes a fixed lead time 
of 7 days for all products and warehouses.

| Limitation | Current Approach | Production Enhancement |
|---|---|---|
| Fixed lead time | 7 days constant | Vendor table with supplier specific lead times |
| Single service level | 95% (Z=1.65) for all products | Category based service levels (99%+ for critical items) |
| No supplier variability | Lead time variance ignored | Add lead time standard deviation to safety stock formula |

> **Note:** In a production pharmaceutical environment 
> lead times would be sourced from vendor master data 
> in SAP or Oracle ERP with different lead times per 
> supplier, product category, and transportation mode.
---


### Lead Time Assumption
| Limitation | Current Approach | Production Enhancement |
|---|---|---|
| Fixed lead time | 7 days constant for all SKUs | Vendor master data with supplier specific lead times |
| Single service level | Z=1.65 (95%) for all products | Category based levels (Z=2.33 for critical pharma items) |
| Lead time variability | Not included in safety stock | Add σ(lead time) to safety stock formula |
| Supplier reliability | Assumed 100% on time | Model lead time variability per supplier |

### Current Inventory Calculation
current_inventory = SUM of all historical transactions
This represents cumulative net inventory
from day 1 to present. Negative values indicate
cumulative stockout position not instantaneous
stock level. In production this would use
real time WMS inventory snapshots.

### Risk Score Limitations
| Limitation | Impact | Enhancement |
|---|---|---|
| No expiry date tracking | Critical for pharma | Add FEFO logic |
| No cold chain consideration | Pharma temperature requirements | Add temperature monitoring layer |
| Static Z score | Same buffer for all products | Dynamic Z by product criticality |
| No supplier lead time variability | Underestimates true safety stock | Add lead time standard deviation |

> **Note:** In a pharmaceutical environment 
> service levels would be set at 99%+ (Z=2.33) 
> for critical medications significantly increasing 
> safety stock requirements compared to the 95% 
> service level used in this retail simulation.


## 🔗 Research Publication
This project forms the basis of a companion research paper to:

*Okorji, K. (2026). Quantifying Retail Inventory Loss: A Combined Shrinkage 
and Stockout Analytics Framework for Distribution Centers. SSRN.*

Companion paper:
"Predictive Inventory Management: A Reorder Point and Demand Forecasting 
Model for Retail Distribution Networks"
→ Status: 🔨 In Progress

---

## Author
**Kani Okorji**
Data Analyst | Supply Chain & Inventory Analytics...

🎓 MS Project Management (Data Analytics) | MBA
🏢 Inventory Specialist — Bath & Body Works
📍 Dallas, TX

🔗 [LinkedIn](https://www.linkedin.com/in/kani-okorji-20869666/)
💻 [GitHub](https://github.com/Kani35000)
📧 kanidayeokorji@gmail.com
