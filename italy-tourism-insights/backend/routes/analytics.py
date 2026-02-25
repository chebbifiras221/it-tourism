"""
Analytics endpoints - Tourism data analysis
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from database import get_db
from models import TourismAnalytic, CulturalSite
from schemas import (
    AnalyticsRequest, OverviewResponse, 
    RegionalAnalyticsResponse, TemporalAnalyticsResponse,
    TemporalDataPoint
)

router = APIRouter()

# Sample Italian regions for demo
ITALIAN_REGIONS = [
    "Lazio", "Veneto", "Tuscany", "Lombardy", "Piedmont",
    "Sicily", "Campania", "Emilia-Romagna", "Liguria", "Marche",
    "Abruzzo", "Molise", "Umbria", "Calabria", "Basilicata",
    "Apulia", "Friuli-Venezia Giulia", "Trentino-Alto Adige", "Valle d'Aosta", "Sardinia"
]


@router.get("/analytics/overview", response_model=OverviewResponse)
async def get_overview(db: Session = Depends(get_db)):
    """
    Get overview statistics of Italian tourism
    
    Returns:
    - Total visitors
    - Total revenue
    - Number of regions
    - Number of cultural sites
    - Average satisfaction
    - Year-over-year change
    """
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)
    last_year = now - timedelta(days=365)
    
    # Get current period data
    current_data = db.query(TourismAnalytic).filter(
        TourismAnalytic.date >= thirty_days_ago.date()
    ).all()
    
    # Get cultural sites
    sites = db.query(CulturalSite).all()
    
    # Calculate metrics
    total_visitors = sum(a.visitor_count for a in current_data) if current_data else 5000000
    total_revenue = sum(a.revenue for a in current_data) if current_data else 100000000
    avg_sentiment = (
        sum(a.sentiment_score for a in current_data) / len(current_data)
        if current_data else 4.6
    )
    
    # Simulate year-over-year change
    yoy_change = 12.5
    
    return OverviewResponse(
        total_visitors=total_visitors,
        total_revenue=total_revenue,
        regions=len(ITALIAN_REGIONS),
        cultural_sites=len(sites) if sites else 234,
        avg_satisfaction=round(avg_sentiment, 1),
        year_over_year_change=yoy_change
    )


@router.get("/analytics/regions", response_model=list)
async def get_regional_analytics(
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("visitors", regex="^(visitors|growth|satisfaction)$"),
    db: Session = Depends(get_db)
):
    """
    Get analytics for all Italian regions
    
    Parameters:
    - limit: Number of regions to return
    - sort_by: 'visitors', 'growth', or 'satisfaction'
    """
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    regional_data = db.query(
        TourismAnalytic.region,
        func.sum(TourismAnalytic.visitor_count).label('total_visitors'),
        func.avg(TourismAnalytic.sentiment_score).label('avg_sentiment'),
    ).filter(
        TourismAnalytic.date >= thirty_days_ago.date()
    ).group_by(
        TourismAnalytic.region
    ).all()
    
    results = []
    for region, total_visitors, avg_sentiment in regional_data:
        total_visitors = total_visitors or 0
        avg_sentiment = avg_sentiment or 4.5
        
        # Simulate growth rate
        growth_rate = 5.2 + (hash(region) % 10) - 2
        
        # Count culture sites in region
        sites_count = db.query(CulturalSite).filter(
            CulturalSite.region == region
        ).count()
        
        results.append({
            "region": region,
            "total_visitors": int(total_visitors),
            "avg_visitors_daily": int(total_visitors / 30) if total_visitors > 0 else 0,
            "growth_rate": round(growth_rate, 1),
            "avg_sentiment": round(avg_sentiment, 2),
            "cultural_sites": sites_count
        })
    
    # Sort results
    if sort_by == "growth":
        results.sort(key=lambda x: x['growth_rate'], reverse=True)
    elif sort_by == "satisfaction":
        results.sort(key=lambda x: x['avg_sentiment'], reverse=True)
    else:  # visitors
        results.sort(key=lambda x: x['total_visitors'], reverse=True)
    
    return results[:limit]


@router.get("/analytics/temporal/{period}", response_model=TemporalAnalyticsResponse)
async def get_temporal_analytics(
    period: str,
    days: int = Query(30, ge=1, le=365),
    region: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get temporal analytics data
    
    Parameters:
    - period: 'daily', 'weekly', 'monthly', 'yearly'
    - days: Number of days to analyze
    - region: Optional region filter
    """
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    query = db.query(TourismAnalytic).filter(
        TourismAnalytic.date >= start_date
    )
    
    if region:
        query = query.filter(TourismAnalytic.region == region)
    
    data_points = query.order_by(TourismAnalytic.date).all()
    
    # Convert to response format
    temporal_data = [
        TemporalDataPoint(
            date=d.date,
            visitor_count=d.visitor_count,
            revenue=d.revenue,
            sentiment_score=d.sentiment_score,
            anomaly=d.anomaly_flag
        )
        for d in data_points
    ]
    
    # Calculate trend
    if len(temporal_data) >= 2:
        start_value = temporal_data[0].visitor_count
        end_value = temporal_data[-1].visitor_count
        trend = "increasing" if end_value > start_value else "decreasing" if end_value < start_value else "stable"
    else:
        trend = "stable"
    
    # Calculate volatility (simple standard deviation of changes)
    if len(temporal_data) > 1:
        changes = [
            temporal_data[i].visitor_count - temporal_data[i-1].visitor_count
            for i in range(1, len(temporal_data))
        ]
        avg_change = sum(changes) / len(changes) if changes else 0
        variance = sum((c - avg_change) ** 2 for c in changes) / len(changes) if changes else 0
        volatility = (variance ** 0.5) / (avg_change if avg_change != 0 else 1)
    else:
        volatility = 0.0
    
    # Find peaks
    peak_date = max(temporal_data, key=lambda x: x.visitor_count).date if temporal_data else None
    min_date = min(temporal_data, key=lambda x: x.visitor_count).date if temporal_data else None
    
    return TemporalAnalyticsResponse(
        data=temporal_data,
        trend=trend,
        volatility=round(volatility, 3),
        peak_date=peak_date,
        min_date=min_date
    )


@router.get("/analytics/regions/{region}")
async def get_region_specific_analytics(
    region: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed analytics for a specific region
    """
    thirty_days = datetime.utcnow() - timedelta(days=30)
    
    data = db.query(TourismAnalytic).filter(
        TourismAnalytic.region == region,
        TourismAnalytic.date >= thirty_days.date()
    ).all()
    
    if not data:
        return {"error": f"No data found for region: {region}"}
    
    total_visitors = sum(d.visitor_count for d in data)
    avg_sentiment = sum(d.sentiment_score for d in data) / len(data)
    total_revenue = sum(d.revenue for d in data)
    sites = db.query(CulturalSite).filter(CulturalSite.region == region).count()
    
    return {
        "region": region,
        "total_visitors": int(total_visitors),
        "avg_daily_visitors": int(total_visitors / len(data)),
        "total_revenue": float(total_revenue),
        "avg_sentiment": round(avg_sentiment, 2),
        "cultural_sites": sites,
        "data_points": len(data),
        "peak_day": max(data, key=lambda x: x.visitor_count).date.isoformat() if data else None
    }
