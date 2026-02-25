"""
Forecasting endpoints - ML predictions
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
import random
from database import get_db
from models import Forecast
from schemas import ForecastingRequest, ForecastingResponse, ForecastPoint, ModelMetrics

router = APIRouter()


def generate_forecast_data(
    region: str,
    days_ahead: int,
    base_visitors: int = 150000,
    seasonality: float = 0.1,
    model: str = "prophet"
) -> ForecastingResponse:
    """
    Generate mock forecast data
    
    In production, this would call actual ML models (ARIMA, Prophet, LSTM)
    """
    forecast_points = []
    today = datetime.utcnow().date()
    
    # Generate forecast with seasonality
    for i in range(1, days_ahead + 1):
        forecast_date = today + timedelta(days=i)
        
        # Add seasonal pattern
        day_of_year = forecast_date.timetuple().tm_yday
        seasonal_factor = 1 + seasonality * (0.5 * (day_of_year / 365) - 0.25)
        
        # Base prediction with trend and noise
        trend = 1.0 + (0.002 * i)  # Slight upward trend
        noise = random.uniform(-0.1, 0.1)
        
        predicted = base_visitors * seasonal_factor * trend * (1 + noise)
        confidence_interval = predicted * 0.15
        
        forecast_points.append(ForecastPoint(
            date=forecast_date,
            predicted_visitors=int(max(50000, predicted)),
            confidence_lower=int(max(40000, predicted - confidence_interval)),
            confidence_upper=int(predicted + confidence_interval)
        ))
    
    # Calculate mock metrics (would be real metrics from trained models)
    mape = 5.8 + random.uniform(-1, 1)
    rmse = 8500 + random.randint(-2000, 2000)
    r_squared = 0.88 + random.uniform(-0.05, 0.05)
    mae = 7200 + random.randint(-1500, 1500)
    
    return ForecastingResponse(
        forecast=forecast_points,
        model_metrics=ModelMetrics(
            mape=round(mape, 2),
            rmse=rmse,
            r_squared=round(max(0, min(1, r_squared)), 3),
            mae=mae
        ),
        model_type=model,
        training_samples=365,
        last_updated=datetime.utcnow()
    )


@router.post("/forecasts/visitors", response_model=ForecastingResponse)
async def forecast_visitors(
    request: ForecastingRequest,
    db: Session = Depends(get_db)
):
    """
    Generate visitor count forecasts using ML models
    
    Models available:
    - 'prophet': Facebook's Prophet (seasonal decomposition)
    - 'arima': ARIMA time series model
    - 'lstm': LSTM neural network
    
    Returns:
    - Predicted visitor counts with confidence intervals
    - Model performance metrics (MAPE, RMSE, R²)
    """
    if request.region not in [
        "Lazio", "Veneto", "Tuscany", "Lombardy", "Piedmont",
        "Sicily", "Campania", "Emilia-Romagna", "Liguria", "Marche"
    ]:
        raise HTTPException(
            status_code=404,
            detail=f"No data available for region: {request.region}"
        )
    
    # Generate forecast (in production, would use actual trained models)
    forecast = generate_forecast_data(
        region=request.region,
        days_ahead=request.days_ahead,
        model=request.model
    )
    
    return forecast


@router.get("/forecasts/seasonality/{region}")
async def get_seasonality_analysis(
    region: str,
    period: str = "monthly",
    db: Session = Depends(get_db)
):
    """
    Get seasonal decomposition analysis
    
    Breaks down time series into:
    - Trend component
    - Seasonal component
    - Residual component
    """
    # Mock seasonal decomposition
    days = 365
    seasonal_component = [
        80000 * (0.5 - 0.5 * (i % 30) / 30) for i in range(days)
    ]
    trend_component = [
        120000 + (100 * i) for i in range(days)
    ]
    residual = [
        random.randint(-5000, 5000) for _ in range(days)
    ]
    
    # Detect anomalies (values beyond 2 standard deviations)
    residual_std = (sum(r**2 for r in residual) / len(residual)) ** 0.5
    anomalies = [
        {
            "day": i,
            "value": residual[i],
            "threshold": 2 * residual_std
        }
        for i, r in enumerate(residual)
        if abs(r) > 2 * residual_std
    ]
    
    return {
        "region": region,
        "period": period,
        "components": {
            "trend": trend_component[-30:],  # Last 30 days
            "seasonal": seasonal_component[-30:],
            "residual": residual[-30:]
        },
        "seasonal_strength": 0.72,
        "anomalies": anomalies[:5],  # Top 5 anomalies
        "interpretation": f"Strong seasonality in {region} with significant weekly patterns"
    }


@router.get("/forecasts/comparison/{region}")
async def compare_models(
    region: str,
    days_ahead: int = 30
):
    """
    Compare multiple forecast models for the same region
    
    Returns predictions from:
    - ARIMA
    - Prophet
    - LSTM
    """
    models = ["arima", "prophet", "lstm"]
    comparisons = {}
    
    for model in models:
        forecast = generate_forecast_data(
            region=region,
            days_ahead=days_ahead,
            model=model
        )
        comparisons[model] = {
            "accuracy": forecast.model_metrics.r_squared,
            "mape": forecast.model_metrics.mape,
            "forecast": [
                {
                    "date": point.date.isoformat(),
                    "predicted": point.predicted_visitors
                }
                for point in forecast.forecast[:7]  # First week
            ]
        }
    
    # Determine best model
    best_model = max(comparisons, key=lambda m: comparisons[m]["accuracy"])
    
    return {
        "region": region,
        "days_ahead": days_ahead,
        "models": comparisons,
        "best_model": best_model,
        "recommendation": f"Use {best_model.upper()} model for {region} (R² = {comparisons[best_model]['accuracy']:.3f})"
    }


@router.get("/forecasts/anomalies/{region}")
async def detect_anomalies(
    region: str,
    sensitivity: float = 2.0
):
    """
    Detect anomalies in tourism patterns
    
    Uses statistical methods to identify unusual events:
    - Unexpected visitor surges/drops
    - Seasonal anomalies
    - Trend breaks
    
    Parameters:
    - sensitivity: Standard deviation multiplier (1.0-3.0)
    """
    if not 1.0 <= sensitivity <= 3.0:
        raise HTTPException(
            status_code=400,
            detail="Sensitivity must be between 1.0 and 3.0"
        )
    
    # Mock anomaly detection
    anomalies = [
        {
            "date": (datetime.utcnow() - timedelta(days=x)).date().isoformat(),
            "type": "surge" if x % 3 == 0 else "drop",
            "severity": round(random.uniform(0.5, 1.0), 2),
            "explanation": [
                "Major event or holiday",
                "Unusual weather conditions",
                "Data collection issue"
            ][x % 3]
        }
        for x in range(1, 6)
    ]
    
    return {
        "region": region,
        "detection_method": "Isolation Forest + Z-score",
        "sensitivity": sensitivity,
        "anomalies_detected": len(anomalies),
        "anomalies": anomalies,
        "last_check": datetime.utcnow().isoformat()
    }
