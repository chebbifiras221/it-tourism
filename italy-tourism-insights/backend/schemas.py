"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


# Tourism Analytics Schemas
class TourismAnalyticBase(BaseModel):
    region: str
    date: date
    visitor_count: int
    revenue: float
    sentiment_score: float = Field(ge=0, le=5)


class TourismAnalyticCreate(TourismAnalyticBase):
    pass


class TourismAnalyticResponse(TourismAnalyticBase):
    id: int
    anomaly_flag: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Cultural Sites Schemas
class CulturalSiteBase(BaseModel):
    name: str
    region: str
    designation: str
    rating: float = Field(ge=0, le=5)
    visitor_count: int


class CulturalSiteCreate(CulturalSiteBase):
    description: Optional[str] = None


class CulturalSiteResponse(CulturalSiteBase):
    id: int
    description: Optional[str]
    coordinates_lat: Optional[float]
    coordinates_lng: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Forecast Schemas
class ForecastBase(BaseModel):
    region: str
    date: date
    predicted_visitors: int
    confidence_lower: int
    confidence_upper: int
    model_type: str
    accuracy: float = Field(ge=0, le=1)


class ForecastCreate(ForecastBase):
    pass


class ForecastResponse(ForecastBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Analytics Request/Response
class AnalyticsRequest(BaseModel):
    region: Optional[str] = None
    days: int = Field(default=30, ge=1, le=365)
    metric: str = "visitor_count"


class OverviewResponse(BaseModel):
    total_visitors: int
    total_revenue: float
    regions: int
    cultural_sites: int
    avg_satisfaction: float
    year_over_year_change: float


class RegionalAnalyticsResponse(BaseModel):
    region: str
    total_visitors: int
    avg_visitors_daily: float
    total_revenue: float
    avg_sentiment: float
    growth_rate: float
    cultural_sites: int


class TemporalDataPoint(BaseModel):
    date: date
    visitor_count: int
    revenue: float
    sentiment_score: float
    anomaly: bool = False


class TemporalAnalyticsResponse(BaseModel):
    data: List[TemporalDataPoint]
    trend: str  # 'increasing', 'decreasing', 'stable'
    volatility: float
    peak_date: Optional[date]
    min_date: Optional[date]


# Forecasting Request/Response
class ForecastingRequest(BaseModel):
    region: str
    days_ahead: int = Field(default=30, ge=1, le=90)
    confidence_level: float = Field(default=0.95, ge=0.8, le=0.99)
    model: str = Field(default="prophet")  # 'arima', 'prophet', 'lstm'


class ForecastPoint(BaseModel):
    date: date
    predicted_visitors: int
    confidence_lower: int
    confidence_upper: int


class ModelMetrics(BaseModel):
    mape: float
    rmse: float
    r_squared: float
    mae: float


class ForecastingResponse(BaseModel):
    forecast: List[ForecastPoint]
    model_metrics: ModelMetrics
    model_type: str
    training_samples: int
    last_updated: datetime


# Seasonality Schemas
class SeasonalityRequest(BaseModel):
    region: str
    period: str = Field(default="monthly")  # 'daily', 'weekly', 'monthly', 'yearly'


class SeasonalityResponse(BaseModel):
    components: dict  # {'trend': [...], 'seasonal': [...], 'residual': [...]}
    seasonal_strength: float
    anomalies: List[dict]
    period: str


# User Query Tracking
class UserQueryCreate(BaseModel):
    query_type: str
    region: Optional[str] = None
    parameters: Optional[dict] = None


# Health Check
class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    ml_models: str
    uptime_seconds: int


# Error Response
class ErrorResponse(BaseModel):
    detail: str
    status_code: int
    timestamp: datetime
    request_id: Optional[str] = None
