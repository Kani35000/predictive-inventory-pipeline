# Predictive Inventory Management Pipeline
## Reorder Point & Demand Forecasting Model for Retail Distribution Networks

> **Kani Okorji** | Data Analyst | Supply Chain & Inventory Analytics
> SQL • Python • scikit-learn • Prophet • Power BI | Manhattan Associates | IBM Cognos
>
> A predictive analytics extension of the Retail Inventory Optimization Pipeline
> applying machine learning demand forecasting and reorder point optimization
> to prevent the $163.9M in stockout losses identified in Phase 1.
>
> 📍 Dallas, TX | 🔗 [LinkedIn](https://www.linkedin.com/in/kani-okorji-20869666/) | 💻 [GitHub](https://github.com/Kani35000)

---

## 🔗 Related Project
This project is a direct extension of:
[Retail Inventory Optimization & Profitability Protection Pipeline](https://github.com/Kani35000/retail-inventory-pipeline)


Phase 1 → Quantified the losses     (descriptive analytics)
Phase 2 → Prevents the losses       (predictive analytics + ML)


---
---

## Business Problem
Phase 1 identified $163.9M in stockout losses across 5 distribution centers.
Phase 2 answers:

**"How do we prevent these losses before they happen?"**

---

## What This Project Solves
1. When should each warehouse reorder each product?
2. How much safety stock should be maintained?
3. Which products are at highest stockout risk?
4. What will demand look like in the next 30 days?
5. How much could proactive reordering save annually?

---

## 📊 KPI Story Arc

| KPI | Method | Type | Business Question |
|---|---|---|---|
| KPI 1-2 | Demand Analysis | Descriptive | What is baseline demand and variability? |
| KPI 3-4 | Reorder Point & Safety Stock | Deterministic | When and how much to reorder? |
| KPI 5-6 | Moving Average Forecast | Statistical | What are recent demand trends? |
| KPI 7 | Stockout Risk Score | Analytical | Which SKUs face immediate stockout? |
| KPI 8 | Projected Savings | Scenario Analysis | How much can optimization save? |
| KPI 9 | ML Demand Forecast | Machine Learning | What will demand be in 30 days? |

---

## 📌 KPI Progress

| KPI | Description | Status |
|---|---|---|
| KPI 1 | Average Daily Demand per SKU per Warehouse | ✅ Complete |
| KPI 2 | Demand Variability (CV%) | ✅ Complete |
| KPI 3 | Reorder Point | ✅ Complete |
| KPI 4 | Safety Stock Optimization | ✅ Complete |
| KPI 5 | 7-Day Moving Average | ✅ Complete |
| KPI 6 | 30-Day Moving Average | ✅ Complete |
| KPI 7 | Stockout Risk Score | ✅ Complete |
| KPI 8 | Projected Savings from Optimization | ✅ Complete |
| KPI 9 | ML Demand Forecast (3 Models) | ✅ Complete |
| KPI 10 | Economic Order Quantity (EOQ) | 🔨 Planned |

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Database | PostgreSQL | Data storage and KPI queries |
| Data Processing | Python (pandas) | Pipeline automation |
| ML Baseline | scikit-learn (Linear Regression) | Demand forecast baseline |
| ML Advanced | scikit-learn (Random Forest) | Feature based forecasting |
| ML Time Series | Prophet | Seasonal demand forecasting |
| Model Evaluation | scikit-learn (RMSE, MAE) | Model accuracy comparison |
| Dashboard | Power BI | Executive visualization |
| API | FastAPI | REST endpoints |
| Version Control | Git + GitHub | Code management |

---

## Project Architecture
```
predictive-inventory-pipeline/
├── 01_database/        # SQL KPI queries
├── 02_forecasting/     # Python analytics pipeline
├── 03_ML_forecast/     # Machine learning models
├── 04_powerbi/         # Predictive dashboard
└── README.md
```

---

## Pipeline Structure

02_forecasting/
├── db_connection.py    ← database connection
├── extract_data.py     ← data extraction
├── demand_analysis.py  ← KPI 1 & 2
├── reorder_point.py    ← KPI 3 & 4
├── demand_forecast.py  ← KPI 5 & 6
├── stockout_risk.py    ← KPI 7
├── savings_analysis.py ← KPI 8
└── kpi_summary.py      ← combined summary
03_ML_forecast/
├── linear_regression_forecast.py  ← baseline model
├── random_forest_forecast.py      ← advanced model
├── prophet_forecast.py            ← time series model
└── model_comparison.py            ← model evaluation
---

## 📌 Project Status

| Layer | Status |
|---|---|
| Database Connection | ✅ Complete |
| Analytics Pipeline (KPI 1-8) | ✅ Complete |
| ML Forecasting Layer (3 Models) | ✅ Complete |
| Model Comparison Framework | ✅ Complete |
| Power BI Predictive Dashboard | 🔨 Planned |
| Research Publication | 🔨 In Progress |

---

## ▶️ How to Run

### 1. Clone Repository
```bash
git clone https://github.com/Kani35000/predictive-inventory-pipeline.git
cd predictive-inventory-pipeline
```

### 2. Install Dependencies
```bash
pip install pandas sqlalchemy psycopg2-binary scikit-learn prophet python-dotenv
```

### 3. Configure Database Connection
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 4. Run Analytics Pipeline
```bash
cd 02_forecasting
python demand_analysis.py
python reorder_point.py
python demand_forecast.py
python stockout_risk.py
python savings_analysis.py
```

### 5. Run ML Models
```bash
cd 03_ML_forecast
python linear_regression_forecast.py
python random_forest_forecast.py
python prophet_forecast.py
python model_comparison.py
```

---

## 🔬 Methodology

### Reorder Point Formula
ROP = (Average Daily Demand × Lead Time) + Safety Stock

### Safety Stock Formula
Safety Stock = Z × σ × √Lead Time
Where:
Z  = service level factor (1.65 for 95% service level)
σ  = standard deviation of daily demand
Lead Time = days for new order to arrive



### Stockout Risk Classification
days_until_stockout = current_inventory / avg_daily_demand
🚨 CRITICAL → < 7 days   → Immediate reorder required
🔴 HIGH     → < 14 days  → Reorder this week
🟡 MEDIUM   → < 30 days  → Monitor closely
🟢 LOW      → 30+ days   → Sufficient stock

### ML Model Validation Approach
Training Set → Days 1-336   (first 336 days per SKU)
Test Set     → Days 337-366 (last 30 days per SKU)
Forecast     → Days 367-396 (next 30 days prediction)

All RMSE and MAE metrics reflect true out-of-sample 
accuracy on the held-out test set — not training data fit.

---

## 📊 Key Findings

### Demand Analysis (KPI 1-2)
| Metric | Value | Implication |
|---|---|---|
| SKU-Warehouse combinations | 500 | Full network coverage |
| Avg daily demand | 43-48 units/day | Consistent baseline demand |
| Avg demand variability (CV%) | ~40% | Moderate volatility |
| Days of data | 366 days | Full year history |

### Reorder Point Analysis (KPI 3-4)
| Metric | Value | Implication |
|---|---|---|
| Avg safety stock | ~82 units | Buffer per SKU per warehouse |
| Avg reorder point | ~410 units | Trigger level for purchase orders |
| Service level | 95% (Z=1.65) | Standard retail target |
| Lead time assumption | 7 days | Fixed — see limitations |

> **Pharma Note:** In pharmaceutical supply chains 
> service levels would be set at 99%+ (Z=2.33) 
> significantly increasing safety stock requirements 
> for critical medications.

### Demand Forecast (KPI 5-6)
| Finding | Count | Implication |
|---|---|---|
| SKUs with significant divergence (>10 units) | 47 of 500 (9.4%) | Targeted reorder review required |
| SKUs with increasing demand | 24 | Reorder points need upward adjustment |
| SKUs with decreasing demand | 23 | Risk of overstock |
| Most volatile category | Seasonal | Dynamic reorder points required |

### Stockout Risk Score (KPI 7)
| Risk Level | SKU Count | % of Network |
|---|---|---|
| 🚨 CRITICAL | 364 | 72.8% |
| 🔴 HIGH | 96 | 19.2% |
| 🟡 MEDIUM | 39 | 7.8% |
| 🟢 LOW | 1 | 0.2% |

### Most Critical SKUs
| Warehouse | Product | Inventory | Days Until Stockout |
|---|---|---|---|
| Dallas | Seasonal Product 39 | -946 units | -20 days |
| Atlanta | Fragrance Product 11 | -849 units | -18 days |
| New Jersey | Body Care Product 60 | -839 units | -18 days |
| Los Angeles | Fragrance Product 61 | -757 units | -16 days |
| Chicago | Seasonal Product 34 | -641 units | -14 days |

### Projected Savings (KPI 8)
| Scenario | Prevention Rate | Network Savings | Remaining Loss |
|---|---|---|---|
| Conservative | 70% | $114.7M | $49.1M |
| Moderate | 80% | $131.1M | $32.8M |
| Aggressive | 90% | $147.5M | $16.4M |

---

## 🤖 ML Forecasting Results (KPI 9)

### Model Comparison
| Model | Avg RMSE | Avg MAE | RMSE vs Baseline | Captures Seasonality |
|---|---|---|---|---|
| Linear Regression | 22.37 | 19.32 | — (baseline) | ❌ |
| Prophet | 16.65 | 13.86 | -25.6% | ✅ Full |
| **Random Forest** | **11.54** | **9.80** | **-48.4%** | ✅ Partial |

### 🏆 Best Model: Random Forest
RMSE = 11.54 units
MAE  = 9.80 units
Improvement over baseline = 48.4%

### Random Forest Feature Importance
| Feature | SKUs Dominated | Insight |
|---|---|---|
| month | 366 (73%) | Seasonal month patterns strongest predictor |
| rolling_7 | 134 (27%) | Recent momentum second strongest |
| is_holiday_season | 0 (direct) | Captured via month feature |

### Model Insights

**Linear Regression:**
→ RMSE 22.37 = ~49% error rate on avg demand
→ 499/500 SKUs showing increasing trend
→ Cannot capture non-linear seasonal patterns
→ Useful only as baseline benchmark

**Random Forest:**
→ RMSE 11.54 = ~25% error rate (2x improvement)
→ Month feature dominates (73% of SKUs)
confirming strong seasonal demand patterns
→ Rolling 7-day average second strongest
confirming recent momentum matters
→ Best overall forecasting accuracy

**Prophet:**
→ RMSE 16.65 = ~36% error rate
→ 415 increasing / 60 decreasing / 25 stable
→ More balanced trend detection than LR
→ Confidence intervals valuable for planning
→ yhat_lower and yhat_upper bound uncertainty

### Model Selection Recommendation
Production use case:
→ Random Forest for daily demand forecasting
(highest accuracy, RMSE 11.54)
→ Prophet for executive reporting
(confidence intervals show uncertainty range)
→ Linear Regression as sanity check baseline
(quick validation of other models)

---

## 🔗 Phase 1 → Phase 2 Connected Intelligence

| Finding | Phase 1 | Phase 2 |
|---|---|---|
| Chicago shrinkage 9.01% | $137K loss warehouse | ROP avg 422 units |
| Dallas shrinkage 8.97% | $134K loss warehouse | Most critical SKU -946 units |
| Atlanta stockout $38.3M | Demand driven losses | 364 CRITICAL SKUs network wide |
| $163.9M total exposure | Quantified in Phase 1 | $114.7M-$147.5M preventable |
| Q4 demand spike | Phase 1 turnover finding | Confirmed by RF month feature |

> **The Complete Story:**
> Phase 1 diagnosed: $163.9M in stockout losses and $385,625 in shrinkage.
> Phase 2 prescribes: reorder points, safety stock, and ML forecasting
> that could prevent 70-90% of identified losses.
> Random Forest demand forecasting at RMSE 11.54 provides
> the most accurate 30-day demand prediction for proactive
> inventory replenishment decisions.

---

## 🔬 Limitations & Further Investigation

### Lead Time Assumption
| Limitation | Current | Production Enhancement |
|---|---|---|
| Fixed lead time | 7 days constant | Vendor master with supplier specific times |
| Single service level | Z=1.65 (95%) | Category based (Z=2.33 for pharma) |
| Lead time variability | Not modeled | Add σ(lead time) to safety stock |
| Supplier reliability | 100% assumed | Model on-time delivery rates |

### Stockout Risk Calculation
current_inventory = SUM of all historical net transactions
Negative values = cumulative stockout position
Not instantaneous real-time stock level
Production enhancement:
→ Real-time WMS inventory snapshots
→ Manhattan Associates live feed
→ Intraday inventory monitoring

### ML Model Limitations
| Limitation | Impact | Enhancement |
|---|---|---|
| Simulated data only | Results not validated on real operations | Apply to real WMS data |
| Fixed train/test split | Cannot account for concept drift | Rolling window validation |
| No external features | Missing promotions, pricing, competition | Add external regressors to Prophet |
| No expiry tracking | Critical for pharma FEFO | Add batch expiry date logic |
| No cold chain | Temperature sensitive products | Add temperature monitoring layer |

### Pharma Production Notes
For pharmaceutical supply chain application:
Service level: Z=2.33 (99%) for critical medications
Lead time: Source from SAP/Oracle vendor master
Safety stock: Include lead time variance
Expiry tracking: FEFO (First Expired First Out)
Cold chain: Temperature monitoring integration
FDA compliance: Drug shortage reporting requirements

---

## 🔗 Research Publication

This project forms the basis of a companion research paper:

**"Predictive Inventory Management: A Reorder Point and 
Demand Forecasting Model for Retail Distribution Networks"**

Extending:
*Okorji, K. (2026). Quantifying Retail Inventory Loss. 
SSRN Electronic Journal. [ssrn.com/author=11236048](https://ssrn.com/author=11236048)*

→ Status: 🔨 In Progress — targeting peer reviewed journal

---

## Author

**Kani Okorji**
Data Analyst | Supply Chain & Inventory Analytics

🎓 MS Project Management (Data Analytics) | MBA
🏢 Inventory Specialist — Bath & Body Works
📍 Dallas, TX

🔗 [LinkedIn](https://www.linkedin.com/in/kani-okorji-20869666/)
💻 [GitHub](https://github.com/Kani35000)
📧 kanidayeokorji@gmail.com
📄 [Research Paper](https://ssrn.com/author=11236048)
