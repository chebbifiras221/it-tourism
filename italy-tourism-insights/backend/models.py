"""
SQLAlchemy database models for tourism data
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, Date, Boolean, JSON, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from database import Base


class TourismAnalytic(Base):
    """Tourism analytics data model"""
    __tablename__ = "tourism_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(100), index=True)
    date = Column(Date, index=True)
    visitor_count = Column(Integer)
    revenue = Column(Float)
    sentiment_score = Column(Float)
    anomaly_flag = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_region_date', 'region', 'date'),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "region": self.region,
            "date": self.date.isoformat(),
            "visitor_count": self.visitor_count,
            "revenue": self.revenue,
            "sentiment_score": self.sentiment_score,
            "anomaly_flag": self.anomaly_flag,
            "created_at": self.created_at.isoformat()
        }


class CulturalSite(Base):
    """Italian cultural heritage sites model"""
    __tablename__ = "cultural_sites"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    region = Column(String(100), index=True)
    designation = Column(String(100))
    rating = Column(Float)
    visitor_count = Column(Integer)
    coordinates_lng = Column(Float)
    coordinates_lat = Column(Float)
    description = Column(String(2000))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "region": self.region,
            "designation": self.designation,
            "rating": self.rating,
            "visitor_count": self.visitor_count,
            "coordinates": {
                "lat": self.coordinates_lat,
                "lng": self.coordinates_lng
            },
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }


class Forecast(Base):
    """ML model predictions/forecasts"""
    __tablename__ = "forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(100), index=True)
    date = Column(Date)
    predicted_visitors = Column(Integer)
    confidence_lower = Column(Integer)
    confidence_upper = Column(Integer)
    model_type = Column(String(50))  # 'arima', 'prophet', 'lstm'
    accuracy = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_region_date_model', 'region', 'date', 'model_type'),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "region": self.region,
            "date": self.date.isoformat(),
            "predicted_visitors": self.predicted_visitors,
            "confidence_lower": self.confidence_lower,
            "confidence_upper": self.confidence_upper,
            "model_type": self.model_type,
            "accuracy": self.accuracy,
            "created_at": self.created_at.isoformat()
        }


class UserQuery(Base):
    """Track user queries and interactions"""
    __tablename__ = "user_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query_type = Column(String(50))  # 'analytics', 'forecast', 'sites'
    region = Column(String(100))
    parameters = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "query_type": self.query_type,
            "region": self.region,
            "parameters": self.parameters,
            "timestamp": self.timestamp.isoformat()
        }
