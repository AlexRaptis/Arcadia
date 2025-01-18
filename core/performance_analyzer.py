# performance_analyzer.py

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Tuple, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceAnalyzer:
    """
    A class to analyze gaming performance metrics and detect areas for improvement.
    """
    
    def __init__(self, threshold_multiplier: float = 1.5):
        """
        Initialize the PerformanceAnalyzer.
        
        Args:
            threshold_multiplier (float): Multiplier for IQR in outlier detection
        """
        self.threshold_multiplier = threshold_multiplier
        logger.info(f"PerformanceAnalyzer initialized with threshold multiplier {threshold_multiplier}")

    def detect_outliers(self, data: pd.Series) -> Tuple[pd.Series, Dict]:
        """
        Detect statistical outliers using the IQR method.
        
        Args:
            data (pd.Series): Time series of performance metrics
            
        Returns:
            Tuple[pd.Series, Dict]: Boolean mask of outliers and outlier statistics
        """
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - (self.threshold_multiplier * IQR)
        upper_bound = Q3 + (self.threshold_multiplier * IQR)
        
        outliers = (data < lower_bound) | (data > upper_bound)
        
        stats = {
            'total_outliers': outliers.sum(),
            'outlier_percentage': (outliers.sum() / len(data)) * 100,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
        
        logger.info(f"Detected {stats['total_outliers']} outliers ({stats['outlier_percentage']:.2f}%)")
        return outliers, stats

    def analyze_performance(self, historical_data: pd.DataFrame) -> Dict:
        """
        Analyze player performance metrics comprehensively.
        
        Args:
            historical_data (pd.DataFrame): Historical performance data
            
        Returns:
            Dict: Comprehensive analysis results for each metric
        """
        metrics = {}
        
        for column in ['accuracy', 'reaction_time', 'decision_making', 'teamwork']:
            if column in historical_data.columns:
                data = historical_data[column]
                
                # Detect outliers
                outliers, outlier_stats = self.detect_outliers(data)
                clean_data = data[~outliers]
                
                # Calculate basic statistics
                metrics[column] = {
                    'current_stats': {
                        'mean': data.mean(),
                        'median': data.median(),
                        'std': data.std(),
                        'trend': self._calculate_trend(data)
                    },
                    'outlier_stats': outlier_stats,
                    'clean_stats': {
                        'mean': clean_data.mean(),
                        'median': clean_data.median(),
                        'std': clean_data.std()
                    }
                }
                
                # Add improvement analysis
                metrics[column].update(
                    self._analyze_improvement_needs(data, clean_data, column)
                )
                
        logger.info("Completed performance analysis for all metrics")
        return metrics

    def _calculate_trend(self, data: pd.Series) -> Dict:
        """
        Calculate performance trend using linear regression.
        
        Args:
            data (pd.Series): Time series of performance metric
            
        Returns:
            Dict: Trend analysis results
        """
        x = np.arange(len(data))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)
        
        trend_strength = abs(r_value)
        trend_direction = 'improving' if slope > 0 else 'declining'
        
        trend_info = {
            'direction': trend_direction,
            'slope': slope,
            'r_squared': r_value ** 2,
            'significance': p_value < 0.05,
            'strength': 'strong' if trend_strength > 0.7 else 'moderate' if trend_strength > 0.3 else 'weak'
        }
        
        return trend_info

    def _analyze_improvement_needs(self, 
                                raw_data: pd.Series, 
                                clean_data: pd.Series, 
                                metric: str) -> Dict:
        """
        Determine if and how much improvement is needed for a metric.
        
        Args:
            raw_data (pd.Series): Original performance data
            clean_data (pd.Series): Performance data with outliers removed
            metric (str): Name of the metric being analyzed
            
        Returns:
            Dict: Improvement analysis results
        """
        recent_window = 5  # Consider last 5 observations
        
        recent_mean = raw_data.tail(recent_window).mean()
        historical_mean = clean_data.mean()
        historical_std = clean_data.std()
        
        # Define metric-specific thresholds and ideal directions
        metric_configs = {
            'accuracy': {'threshold': -1.0, 'higher_better': True},
            'reaction_time': {'threshold': 1.0, 'higher_better': False},
            'decision_making': {'threshold': -1.0, 'higher_better': True},
            'teamwork': {'threshold': -1.0, 'higher_better': True}
        }
        
        config = metric_configs.get(metric, {'threshold': -1.0, 'higher_better': True})
        z_score = (recent_mean - historical_mean) / historical_std
        
        # Determine improvement needs
        needs_improvement = (
            (z_score < config['threshold']) if config['higher_better']
            else (z_score > config['threshold'])
        )
        
        improvement_data = {
            'needs_improvement': needs_improvement,
            'z_score': z_score,
            'recent_performance': {
                'mean': recent_mean,
                'vs_historical': (recent_mean - historical_mean) / historical_mean * 100
            },
            'suggested_target': historical_mean + (historical_std if config['higher_better'] else -historical_std)
        }
        
        return {'improvement_analysis': improvement_data}

    def generate_recommendations(self, analysis_results: Dict) -> List[Dict]:
        """
        Generate specific recommendations based on performance analysis.
        
        Args:
            analysis_results (Dict): Results from analyze_performance()
            
        Returns:
            List[Dict]: List of specific recommendations for improvement
        """
        recommendations = []
        
        for metric, analysis in analysis_results.items():
            if analysis['improvement_analysis']['needs_improvement']:
                current = analysis['current_stats']['mean']
                target = analysis['improvement_analysis']['suggested_target']
                trend = analysis['current_stats']['trend']
                
                recommendations.append({
                    'metric': metric,
                    'current_level': current,
                    'target_level': target,
                    'improvement_needed': abs(target - current),
                    'trend_info': trend,
                    'priority': 'high' if analysis['improvement_analysis']['z_score'] < -2 else 'medium'
                })
        
        # Sort recommendations by priority
        recommendations.sort(key=lambda x: x['priority'] == 'high', reverse=True)
        
        logger.info(f"Generated {len(recommendations)} improvement recommendations")
        return recommendations