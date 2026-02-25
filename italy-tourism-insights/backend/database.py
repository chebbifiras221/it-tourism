"""
Database configuration and initialization
"""
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./tourism.db')

# Create engine based on database type
if 'sqlite' in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # PostgreSQL or other databases
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    
    # Check if tables exist
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if tables:
        print(f"✓ Database tables initialized: {', '.join(tables)}")
    
    # Initialize sample data if needed
    _init_sample_data()


def _init_sample_data():
    """Initialize sample tourism data"""
    db = SessionLocal()
    try:
        from models import TourismAnalytic, CulturalSite
        from datetime import datetime, timedelta
        import random
        
        # Check if data exists
        existing = db.query(TourismAnalytic).first()
        if existing:
            return
        
        # Italian regions
        regions = [
            "Lazio", "Veneto", "Tuscany", "Lombardy", "Piedmont",
            "Sicily", "Campania", "Emilia-Romagna", "Liguria", "Marche"
        ]
        
        # Sample cultural sites
        sites_data = [
            {"name": "Colosseum", "region": "Lazio", "rating": 4.9, "visitors": 7000000},
            {"name": "Venice Canals", "region": "Veneto", "rating": 4.8, "visitors": 3800000},
            {"name": "Uffizi Gallery", "region": "Tuscany", "rating": 4.7, "visitors": 2100000},
            {"name": "Milan Cathedral", "region": "Lombardy", "rating": 4.6, "visitors": 1500000},
            {"name": "Trevi Fountain", "region": "Lazio", "rating": 4.8, "visitors": 4000000},
        ]
        
        # Add cultural sites
        for site in sites_data:
            cultural_site = CulturalSite(
                name=site["name"],
                region=site["region"],
                rating=site["rating"],
                visitor_count=site["visitors"],
                designation="Cultural Heritage"
            )
            db.add(cultural_site)
        
        # Add sample analytics data (last 30 days)
        now = datetime.utcnow()
        for i in range(30):
            date = now - timedelta(days=i)
            for region in regions[:5]:  # Sample 5 regions
                analytics = TourismAnalytic(
                    region=region,
                    date=date.date(),
                    visitor_count=random.randint(100000, 500000),
                    revenue=random.random() * 10000000,
                    sentiment_score=random.uniform(4.0, 5.0),
                    anomaly_flag=random.random() > 0.95
                )
                db.add(analytics)
        
        db.commit()
        print("✓ Sample data initialized")
        
    except Exception as e:
        db.rollback()
        print(f"⚠ Sample data initialization skipped: {e}")
    finally:
        db.close()
