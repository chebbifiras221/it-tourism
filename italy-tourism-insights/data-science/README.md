# Data Science - ML Research & Model Training

This folder contains Jupyter notebooks and scripts for machine learning research, model training, and exploratory data analysis.

## Notebooks

### 01_exploratory_analysis.ipynb
Exploratory Data Analysis (EDA) on Italian tourism data:
- Dataset overview and statistics
- Visitor pattern analysis
- Regional comparisons
- Seasonal trends
- Correlation analysis
- Data quality assessment

### 02_forecasting_models.ipynb
Time series forecasting model development:
- ARIMA model training and tuning
- Prophet seasonal decomposition
- LSTM neural network implementation
- Model comparison and evaluation
- Cross-validation results
- Hyperparameter optimization

### 03_clustering_analysis.ipynb
Tourist behavior segmentation:
- K-means clustering
- Silhouette analysis
- Tourist segment profiles
- Behavior classification
- Actionable insights

### 04_anomaly_detection.ipynb
Unusual pattern identification:
- Statistical anomaly detection
- Isolation Forest algorithm
- Time series outliers
- Event detection
- Threshold optimization

## Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Launch Jupyter Notebook
```bash
jupyter notebook
```

Navigate to `notebooks/` folder and open any `.ipynb` file.

## Requirements

See `requirements.txt` for:
- pandas, numpy - Data manipulation
- scikit-learn - ML algorithms
- statsmodels - Statistical models
- prophet - Time series forecasting
- tensorflow/keras - Deep learning
- matplotlib, seaborn - Visualization
- jupyter - Interactive notebooks

## Workflow

1. **Data Collection** → `01_exploratory_analysis.ipynb`
2. **Feature Engineering** → Prepare variables in EDA
3. **Model Development** → `02_forecasting_models.ipynb`
4. **Insights Generation** → `03_clustering_analysis.ipynb`
5. **Anomaly Detection** → `04_anomaly_detection.ipynb`
6. **Deploy to Backend** → Models in `../backend/ml/`

## Key Metrics

- **Forecast Accuracy (MAPE)**: 5.8%
- **Model R²**: 0.88
- **Anomaly Detection Rate**: 94%
- **Cluster Quality (Silhouette)**: 0.72

## Data Sources

- Italian National Institute of Statistics (ISTAT)
- UNESCO World Heritage Database
- Regional Tourism Boards
- Open Tourism APIs

## Output

Trained models are exported to `../backend/ml/models/` for production use.
