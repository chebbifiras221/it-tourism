# Backend Routes

This folder contains all API route handlers organized by feature.

## Files

- **health.py** - Health check and status endpoints
- **analytics.py** - Tourism data analytics endpoints
- **forecasts.py** - ML forecasting and predictions
- **sites.py** - Cultural heritage sites endpoints

## API Endpoints

### Health (`/api/health`)
- `GET /api/health` - System health check
- `GET /api/status` - Detailed status

### Analytics (`/api/analytics`)
- `GET /api/analytics/overview` - Tourism overview statistics
- `GET /api/analytics/regions` - Regional analytics
- `GET /api/analytics/temporal/{period}` - Temporal analysis
- `GET /api/analytics/regions/{region}` - Region-specific data

### Forecasting (`/api/forecasts`)
- `POST /api/forecasts/visitors` - Visitor forecasts
- `GET /api/forecasts/seasonality/{region}` - Seasonal decomposition
- `GET /api/forecasts/comparison/{region}` - Model comparison
- `GET /api/forecasts/anomalies/{region}` - Anomaly detection

### Sites (`/api/sites`)
- `GET /api/sites/` - List cultural sites
- `GET /api/sites/{site_id}` - Site details
- `GET /api/sites/{site_id}/similar` - Similar sites
- `GET /api/sites/by-region/{region}` - Sites by region
- `GET /api/sites/stats/top-rated` - Top-rated sites
- `GET /api/sites/stats/most-visited` - Most visited sites
