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
| Layer | Tool |
|---|---|
| Database | PostgreSQL (existing Phase 1 database) |
| Forecasting | Python (statsmodels, Prophet, scikit-learn) |
| Pipeline | Python (pandas, SQLAlchemy) |
| Dashboard | Power BI |
| Version Control | Git + GitHub |

---

## Project Architecture
predictive-inventory-pipeline/
├── 01_database/        # Additional views and stored procedures
├── 02_forecasting/     # Demand forecasting scripts
├── 03_reorder/         # Reorder point calculations
├── 04_powerbi/         # Predictive dashboard
└── README.md
---

## 📌 Project Status
| Layer | Status |
|---|---|
| Database Connection | 🔨 In Progress |
| Demand Analysis | 🔨 In Progress |
| Reorder Point Calculation | 🔨 Planned |
| Safety Stock Optimization | 🔨 Planned |
| Demand Forecasting Model | 🔨 Planned |
| Stockout Risk Scoring | 🔨 Planned |
| Power BI Predictive Dashboard | 🔨 Planned |
| Research Publication | 🔨 Planned |

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

### Demand Forecasting Approach
Method 1 → Moving Average (baseline)
Method 2 → Exponential Smoothing
Method 3 → Prophet (seasonal decomposition)

---

## 📊 Key Findings So Far
→ Coming soon as analysis is completed

---

## 🔬 Limitations & Further Investigation
→ To be documented as methodology develops

---

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