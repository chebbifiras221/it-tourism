"""
Analytics algorithms for tourism data
"""
import numpy as np
import pandas as pd
from collections import defaultdict


class TourismAnalytics:
    """
    Tourism data analysis and insights
    """
    
    @staticmethod
    def calculate_growth_rate(current: float, previous: float) -> float:
        """Calculate year-over-year or period growth"""
        if previous == 0:
            return 0
        return ((current - previous) / previous) * 100
    
    @staticmethod
    def seasonal_decomposition(data: np.ndarray, period: int = 12) -> dict:
        """
        Decompose time series into trend, seasonal, and residual
        """
        try:
            from statsmodels.tsa.seasonal import seasonal_decompose
            
            series = pd.Series(data)
            decomposition = seasonal_decompose(series, model='additive', period=period)
            
            return {
                'trend': decomposition.trend.values,
                'seasonal': decomposition.seasonal.values,
                'residual': decomposition.resid.values,
            }
        except:
            return {'trend': data, 'seasonal': [], 'residual': []}
    
    @staticmethod
    def calculate_volatility(data: np.ndarray) -> float:
        """Calculate price/visitor volatility"""
        returns = np.diff(data) / data[:-1]
        return np.std(returns)
    
    @staticmethod
    def peak_detection(data: np.ndarray, threshold: float = 1.5) -> list:
        """
        Detect peak periods in tourism data
        """
        mean = np.mean(data)
        std = np.std(data)
        peaks = []
        
        for i, val in enumerate(data):
            if val > mean + threshold * std:
                peaks.append({'index': i, 'value': val, 'deviation': (val - mean) / std})
        
        return peaks
    
    @staticmethod
    def correlation_analysis(data: pd.DataFrame) -> dict:
        """
        Analyze correlations between tourism metrics
        """
        correlations = data.corr()
        
        strong_correlations = []
        for col1 in correlations.columns:
            for col2 in correlations.columns:
                if col1 < col2:  # Avoid duplicates
                    corr_value = correlations.loc[col1, col2]
                    if abs(corr_value) > 0.5:
                        strong_correlations.append({
                            'variable1': col1,
                            'variable2': col2,
                            'correlation': round(corr_value, 3)
                        })
        
        return {
            'all_correlations': correlations.to_dict(),
            'strong_correlations': strong_correlations
        }
    
    @staticmethod
    def visitor_segmentation(data: pd.DataFrame, n_clusters: int = 3) -> dict:
        """
        Segment tourists based on behavior patterns
        """
        try:
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler
            
            # Prepare features
            features = ['avg_stay_days', 'spending', 'satisfaction']
            X = data[features].fillna(data[features].mean())
            
            # Scale and cluster
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            
            return {
                'n_clusters': n_clusters,
                'cluster_centers': kmeans.cluster_centers_.tolist(),
                'cluster_labels': clusters.tolist(),
                'inertia': float(kmeans.inertia_)
            }
        except:
            return {'error': 'Clustering analysis unavailable'}
    
    @staticmethod
    def revenue_analysis(data: pd.DataFrame) -> dict:
        """
        Analyze tourism revenue patterns
        """
        return {
            'total_revenue': float(data['revenue'].sum()),
            'avg_revenue_per_visitor': float(data['revenue'].sum() / data['visitor_count'].sum()),
            'revenue_by_region': data.groupby('region')['revenue'].sum().to_dict(),
            'revenue_growth': float(TourismAnalytics.calculate_growth_rate(
                data.iloc[-1]['revenue'],
                data.iloc[0]['revenue'] if len(data) > 1 else data.iloc[-1]['revenue']
            )),
            'peak_revenue_date': data.loc[data['revenue'].idxmax()]['date'] if len(data) > 0 else None
        }
    
    @staticmethod
    def sentiment_analysis(sentiments: np.ndarray) -> dict:
        """
        Analyze visitor sentiment/satisfaction
        """
        return {
            'average_sentiment': float(np.mean(sentiments)),
            'std_deviation': float(np.std(sentiments)),
            'min_sentiment': float(np.min(sentiments)),
            'max_sentiment': float(np.max(sentiments)),
            'median_sentiment': float(np.median(sentiments))
        }
    
    @staticmethod
    def regional_comparison(data: pd.DataFrame, metric: str = 'visitor_count') -> dict:
        """
        Compare regions on specific metrics
        """
        comparison = data.groupby('region')[metric].agg(['sum', 'mean', 'std']).to_dict()
        
        # Find best and worst regions
        totals = data.groupby('region')[metric].sum()
        best_region = totals.idxmax() if len(totals) > 0 else None
        worst_region = totals.idxmin() if len(totals) > 0 else None
        
        return {
            'metric': metric,
            'by_region': comparison,
            'best_region': best_region,
            'worst_region': worst_region,
            'variation': float(totals.std())
        }


# Global analytics instance
analytics = TourismAnalytics()
