# Retail Demand Forecasting with Hierarchical Time Series

## Project Overview

This project builds a hierarchical retail demand forecasting workflow using Python and Darts.

The goal is to forecast retail sales across multiple business levels:

* Total sales
* Store-level sales
* Item-level sales
* Store-item-level sales

Instead of only predicting aggregate demand, this project focuses on how demand forecasting can support different business decisions, from total demand planning to store-item replenishment.

The workflow includes:

* data audit and time series transformation
* hierarchical time series construction
* baseline forecasting
* forecast coherence checking
* forecast reconciliation
* model comparison
* store-item-level error analysis
* business interpretation

---

## Business Problem

Retailers need demand forecasts at different levels of decision-making.

Total sales forecasts are useful for high-level planning, while store-level and item-level forecasts support operations and category management. The most granular store-item forecasts are especially important for inventory replenishment, but they are also more difficult to predict because they contain more local demand variation.

This project addresses two key questions:

1. Can a global forecasting model produce accurate demand forecasts across different hierarchy levels?
2. Can forecast reconciliation improve lower-level forecast accuracy while maintaining consistency across the hierarchy?

---

## Dataset Description

The dataset contains daily sales records for:

* 10 stores
* 50 items
* daily sales from 2013-01-01 to 2017-12-31

After transformation, the hierarchical dataset contains:

* 1 total-level series
* 10 store-level series
* 50 item-level series
* 500 store-item-level series

This gives a total of 561 hierarchical time series components over 1,826 daily observations.

The dataset is not included in this repository. Please place the raw dataset manually under:

```text
data/raw/train.csv
```

---

## Project Structure

```text
retail-demand-forecasting/
│
├── data/
│   ├── raw/                  # raw data, not uploaded to GitHub
│   └── processed/            # processed data, not uploaded to GitHub
│
├── notebooks/
│   └── 01_retail_demand_forecasting_story.ipynb
│
├── src/
│   ├── data_prep.py
│   ├── hierarchy.py
│   ├── models.py
│   ├── evaluation.py
│   ├── reconciliation.py
│   └── visualization.py
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Methodology

### 1. Data Audit

The raw data is checked for:

* dataset size
* date range
* number of stores
* number of items
* missing values
* duplicated rows

This ensures that the dataset has the expected retail time series structure before modeling.

### 2. Hierarchical Time Series Construction

The raw store-item sales records are transformed into a hierarchical structure:

```text
Total
├── Store level
├── Item level
└── Store-item level
```

This allows the project to evaluate forecasts across both aggregate and granular business levels.

### 3. Baseline Forecasting

Two baseline models are compared:

* Seasonal Naive
* Linear Regression

The Seasonal Naive model assumes that future demand follows the same weekday pattern from the previous week.

The Linear Regression model uses lagged historical sales values and acts as a simple global forecasting model.

### 4. Forecast Coherence Check

Forecast coherence means that forecasts across hierarchy levels add up consistently.

For example:

```text
sum(store forecasts) = total forecast
sum(item forecasts) = total forecast
sum(store-item forecasts) = total forecast
```

This is important because different business teams should not receive conflicting demand numbers.

### 5. Forecast Reconciliation

Three reconciliation strategies are tested:

* Bottom-Up
* Top-Down
* MinT

The goal is to check whether reconciliation improves lower-level accuracy while maintaining a coherent forecast structure.

### 6. Error Analysis

Since store-item-level forecasting is the most difficult part of the hierarchy, the project identifies the hardest store-item combinations to forecast.

This helps translate model errors into business risks, such as potential stockouts or overstock.

---

## Key Results

### Linear Regression Baseline

The Linear Regression model performs much better than the Seasonal Naive baseline.

| Level      |  MAPE | sMAPE |     MAE |    RMSE |
| ---------- | ----: | ----: | ------: | ------: |
| Total      |  6.80 |  7.03 | 1514.04 | 1951.43 |
| Store      |  7.12 |  7.36 |  159.56 |  203.91 |
| Item       |  8.60 |  8.86 |   37.77 |   48.02 |
| Store-item | 20.05 | 19.91 |    7.78 |    9.66 |

The results show a clear hierarchy effect: forecasting becomes more difficult at lower levels. Total, store, and item-level demand are relatively stable, while store-item demand contains more local variation and noise.

### Baseline Model Comparison

| Model             | Total MAPE | Store MAPE | Item MAPE | Store-item MAPE |
| ----------------- | ---------: | ---------: | --------: | --------------: |
| Seasonal Naive    |      34.98 |      35.31 |     36.28 |           42.76 |
| Linear Regression |       6.80 |       7.12 |      8.60 |           20.05 |

Linear Regression clearly outperforms the Seasonal Naive benchmark across all hierarchy levels. This suggests that a lag-based global model captures more useful demand patterns than a simple weekly repeat rule.

### Reconciliation Results

| Method            | Total MAPE | Store MAPE | Item MAPE | Store-item MAPE |
| ----------------- | ---------: | ---------: | --------: | --------------: |
| Linear Regression |       6.80 |       7.12 |      8.60 |           20.05 |
| LR + Bottom-Up    |       6.80 |       7.12 |      8.60 |           20.05 |
| LR + Top-Down     |       6.80 |       6.98 |      7.74 |           15.50 |
| LR + MinT         |       6.80 |       7.12 |      8.60 |           20.05 |

Top-Down reconciliation provides the strongest improvement. It keeps total-level performance unchanged while improving accuracy at lower levels.

The most important improvement is at the store-item level:

```text
Store-item MAPE: 20.05% → 15.50%
```

This is especially relevant for replenishment planning, where store-item-level forecasts are directly connected to inventory decisions.

---

## Main Insights

1. Linear Regression significantly outperforms the Seasonal Naive baseline across all hierarchy levels.

2. Forecasting becomes harder as the hierarchy becomes more granular.

3. The original Linear Regression forecast is already coherent in practical terms, with coherence gaps close to zero.

4. Top-Down reconciliation does not mainly solve a major coherence problem in this case. Instead, its main value is improving lower-level forecast accuracy.

5. Store-item-level forecasting remains the most difficult task and should be prioritized for further feature engineering.

6. Several high-error store-item combinations are concentrated in specific stores, especially store 7 and store 5. These combinations may require further business investigation.

---

## Visual Outputs

The notebook generates several charts, including:

* Daily total sales trend
* Baseline MAPE comparison
* Forecast coherence before reconciliation
* Forecast coherence after Top-Down reconciliation
* Reconciliation MAPE comparison
* Top 10 hardest store-item series to forecast
* Actual vs predicted total sales

Generated figures are saved under:

```text
outputs/figures/
```

Generated tables are saved under:

```text
outputs/tables/
```

---

## How to Run This Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/retail-demand-forecasting.git
cd retail-demand-forecasting
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

For Windows PowerShell:

```bash
.venv\Scripts\activate
```

For macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the Dataset

Place the dataset manually at:

```text
data/raw/train.csv
```

The dataset is intentionally excluded from the repository.

### 5. Run the Notebook

```bash
jupyter notebook
```

Open:

```text
notebooks/01_retail_demand_forecasting_story.ipynb
```

---

## Tools Used

* Python
* pandas
* NumPy
* Matplotlib
* Darts
* scikit-learn
* Jupyter Notebook

---

## Future Improvements

Potential next steps include:

* adding holiday indicators
* adding promotion features
* adding price information
* using rolling-window backtesting
* comparing more advanced global forecasting models
* testing models such as LightGBM, N-BEATS, N-HiTS, or TFT
* adding inventory-oriented evaluation metrics
* analyzing high-error store-item combinations in more detail

