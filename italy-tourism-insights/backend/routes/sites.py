"""
Cultural sites endpoints - Heritage location data
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import CulturalSite, TourismAnalytic
from datetime import datetime, timedelta

router = APIRouter()


# Sample Italian cultural sites data
SAMPLE_SITES = [
    {
        "name": "Colosseum",
        "region": "Lazio",
        "rating": 4.9,
        "visitors": 7000000,
        "designation": "UNESCO World Heritage",
        "lat": 41.8902,
        "lng": 12.4924,
        "description": "Ancient Roman amphitheater, iconic symbol of Imperial Rome"
    },
    {
        "name": "Venice Canals",
        "region": "Veneto",
        "rating": 4.8,
        "visitors": 3800000,
        "designation": "UNESCO World Heritage",
        "lat": 45.4408,
        "lng": 12.3155,
        "description": "Historic canal city with unique Venetian architecture"
    },
    {
        "name": "Uffizi Gallery",
        "region": "Tuscany",
        "rating": 4.7,
        "visitors": 2100000,
        "designation": "World Class Museum",
        "lat": 43.7674,
        "lng": 11.2557,
        "description": "Premier art museum housing Renaissance masterpieces"
    },
    {
        "name": "Milan Cathedral",
        "region": "Lombardy",
        "rating": 4.6,
        "visitors": 1500000,
        "designation": "UNESCO World Heritage",
        "lat": 45.4640,
        "lng": 9.1919,
        "description": "Gothic cathedral with ornate architecture and sculptures"
    },
    {
        "name": "Trevi Fountain",
        "region": "Lazio",
        "rating": 4.8,
        "visitors": 4000000,
        "designation": "Monument",
        "lat": 41.9009,
        "lng": 12.4833,
        "description": "Baroque masterpiece and world-famous coin fountain"
    },
    {
        "name": "Vatican Museums",
        "region": "Lazio",
        "rating": 4.8,
        "visitors": 6000000,
        "designation": "UNESCO World Heritage",
        "lat": 41.9064,
        "lng": 12.4557,
        "description": "World's greatest collection of art and history"
    },
    {
        "name": "Florence Duomo",
        "region": "Tuscany",
        "rating": 4.7,
        "visitors": 1800000,
        "designation": "UNESCO World Heritage",
        "lat": 43.7731,
        "lng": 11.2558,
        "description": "Renaissance cathedral with iconic dome"
    },
    {
        "name": "Pompeii",
        "region": "Campania",
        "rating": 4.8,
        "visitors": 2800000,
        "designation": "UNESCO World Heritage",
        "lat": 40.7485,
        "lng": 14.6267,
        "description": "Preserved Roman city buried by volcanic eruption"
    },
]


@router.get("/sites/")
async def list_cultural_sites(
    region: str = Query(None),
    rating_min: float = Query(0, ge=0, le=5),
    search: str = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    List Italian cultural heritage sites
    
    Parameters:
    - region: Filter by region (optional)
    - rating_min: Minimum rating (0-5)
    - search: Search site name (optional)
    - limit: Number of results
    - offset: Pagination offset
    """
    query = db.query(CulturalSite)
    
    if region:
        query = query.filter(CulturalSite.region == region)
    
    if rating_min > 0:
        query = query.filter(CulturalSite.rating >= rating_min)
    
    if search:
        query = query.filter(CulturalSite.name.ilike(f"%{search}%"))
    
    total = query.count()
    sites = query.limit(limit).offset(offset).all()
    
    # If no results from database, return sample data
    if not sites:
        sites = [
            {
                "id": i,
                "name": s["name"],
                "region": s["region"],
                "designation": s["designation"],
                "rating": s["rating"],
                "visitor_count": s["visitors"],
                "coordinates": {"lat": s["lat"], "lng": s["lng"]},
                "description": s["description"]
            }
            for i, s in enumerate(SAMPLE_SITES)
        ]
        if search:
            sites = [s for s in sites if search.lower() in s["name"].lower()]
        if region:
            sites = [s for s in sites if s["region"] == region]
        sites = sites[offset:offset+limit]
    
    return {
        "total": len(sites) + total,
        "limit": limit,
        "offset": offset,
        "sites": [s.to_dict() if hasattr(s, 'to_dict') else s for s in sites]
    }


@router.get("/sites/{site_id}")
async def get_site_details(
    site_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific cultural site
    """
    site = db.query(CulturalSite).filter(
        CulturalSite.name.ilike(f"%{site_id}%")
    ).first()
    
    # Return sample data if not found
    if not site:
        sample = next((s for s in SAMPLE_SITES if site_id.lower() in s["name"].lower()), None)
        if not sample:
            raise HTTPException(status_code=404, detail="Site not found")
        
        return {
            "name": sample["name"],
            "region": sample["region"],
            "rating": sample["rating"],
            "visitor_count": sample["visitors"],
            "designation": sample["designation"],
            "coordinates": {"lat": sample["lat"], "lng": sample["lng"]},
            "description": sample["description"],
            "annual_visitors": sample["visitors"],
            "monthly_trend": [sample["visitors"] // 12 for _ in range(12)],
            "peak_months": ["June", "July", "August"],
            "seasonal_pattern": "strong",
            "pricing": {
                "standard": round(sample["visitors"] / 500000, 1),
                "student": round(sample["visitors"] / 600000, 1),
                "child": round(sample["visitors"] / 1000000, 1)
            }
        }
    
    return site.to_dict()


@router.get("/sites/{site_id}/similar")
async def get_similar_sites(
    site_id: str,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Get culturally similar sites to the specified one
    """
    # Get the original site
    site = db.query(CulturalSite).filter(
        CulturalSite.name.ilike(f"%{site_id}%")
    ).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Get similar sites (same region or similar rating)
    similar = db.query(CulturalSite).filter(
        (CulturalSite.region == site.region) |
        ((CulturalSite.rating >= site.rating - 0.5) & 
         (CulturalSite.rating <= site.rating + 0.5))
    ).filter(
        CulturalSite.id != site.id
    ).limit(limit).all()
    
    return {
        "original_site": site.name,
        "similarity_criteria": "Same region, similar rating",
        "similar_sites": [s.to_dict() for s in similar]
    }


@router.get("/sites/by-region/{region}")
async def get_sites_by_region(
    region: str,
    sort_by: str = Query("rating", regex="^(rating|visitors|name)$"),
    db: Session = Depends(get_db)
):
    """
    Get all cultural sites in a specific region
    
    Parameters:
    - region: Region name
    - sort_by: 'rating', 'visitors', or 'name'
    """
    sites = db.query(CulturalSite).filter(
        CulturalSite.region == region
    ).all()
    
    if not sites:
        # Return sample data for the region
        sites = [
            s for s in SAMPLE_SITES if s["region"] == region
        ]
        sites_data = [
            {
                "name": s["name"],
                "rating": s["rating"],
                "visitors": s["visitors"],
                "designation": s["designation"],
                "coordinates": {"lat": s["lat"], "lng": s["lng"]}
            } for s in sites
        ]
    else:
        sites_data = [s.to_dict() for s in sites]
    
    # Sort
    if sort_by == "rating":
        sites_data.sort(key=lambda x: x.get("rating", 0), reverse=True)
    elif sort_by == "visitors" or sort_by == "visitor_count":
        sites_data.sort(
            key=lambda x: x.get("visitor_count", x.get("visitors", 0)), 
            reverse=True
        )
    else:
        sites_data.sort(key=lambda x: x.get("name", ""))
    
    return {
        "region": region,
        "total_sites": len(sites_data),
        "sites": sites_data
    }


@router.get("/sites/stats/top-rated")
async def get_top_rated_sites(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get top-rated cultural sites
    """
    sites = db.query(CulturalSite).order_by(
        CulturalSite.rating.desc()
    ).limit(limit).all()
    
    if not sites:
        sites_data = sorted(SAMPLE_SITES, key=lambda x: x["rating"], reverse=True)[:limit]
        sites_result = [
            {
                "name": s["name"],
                "region": s["region"],
                "rating": s["rating"],
                "visitors": s["visitors"]
            } for s in sites_data
        ]
    else:
        sites_result = [s.to_dict() for s in sites]
    
    return {
        "title": "Top-Rated Italian Cultural Sites",
        "count": len(sites_result),
        "sites": sites_result
    }


@router.get("/sites/stats/most-visited")
async def get_most_visited_sites(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get most visited cultural sites
    """
    sites = db.query(CulturalSite).order_by(
        CulturalSite.visitor_count.desc()
    ).limit(limit).all()
    
    if not sites:
        sites_data = sorted(SAMPLE_SITES, key=lambda x: x["visitors"], reverse=True)[:limit]
        sites_result = [
            {
                "name": s["name"],
                "region": s["region"],
                "annual_visitors": s["visitors"],
                "rating": s["rating"]
            } for s in sites_data
        ]
    else:
        sites_result = [s.to_dict() for s in sites]
    
    return {
        "title": "Most Visited Italian Cultural Sites",
        "count": len(sites_result),
        "sites": sites_result
    }
