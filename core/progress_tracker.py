# progress_tracker.py

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from scipy import stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProgressTracker:
    """
    A class to track and analyze player progress over time by comparing
    current performance with historical data.
    """
    
    def __init__(self, lookback_periods: Dict[str, int] = None):
        """
        Initialize the progress tracker with customizable lookback periods.
        
        Args:
            lookback_periods (Dict[str, int], optional): Custom lookback periods in days
                for different types of analysis
        """
        self.lookback_periods = lookback_periods or {
            'short_term': 7,    # 1 week
            'medium_term': 30,  # 1 month
            'long_term': 90     # 3 months
        }
        logger.info("Progress Tracker initialized")

    def track_progress(self, 
                      current_stats: Dict,
                      historical_data: pd.DataFrame,
                      target_metrics: Dict) -> Dict:
        """
        Track progress by comparing current stats with historical data.
        
        Args:
            current_stats (Dict): Current performance metrics
            historical_data (pd.DataFrame): Historical performance data
            target_metrics (Dict): Target values for each metric
            
        Returns:
            Dict: Comprehensive progress analysis
        """
        progress_report = {}
        
        for metric, current_value in current_stats.items():
            if metric in historical_data.columns:
                # Get historical values for the metric
                metric_history = historical_data[metric].dropna()
                
                if not metric_history.empty:
                    # Calculate progress metrics
                    progress_report[metric] = {
                        'current_value': current_value,
                        'target_value': target_metrics.get(metric),
                        'historical_comparison': self._compare_with_history(
                            current_value,
                            metric_history
                        ),
                        'trend_analysis': self._analyze_trend(metric_history),
                        'improvement_rate': self._calculate_improvement_rate(
                            current_value,
                            metric_history
                        ),
                        'milestone_progress': self._track_milestones(
                            current_value,
                            target_metrics.get(metric, current_value * 1.2)
                        )
                    }
        
        logger.info(f"Completed progress tracking for {len(progress_report)} metrics")
        return progress_report

    def _compare_with_history(self, 
                            current_value: float,
                            history: pd.Series) -> Dict:
        """
        Compare current value with historical data across different time periods.
        
        Args:
            current_value (float): Current metric value
            history (pd.Series): Historical values with timestamps
            
        Returns:
            Dict: Comparison results for different time periods
        """
        comparisons = {}
        
        for period_name, days in self.lookback_periods.items():
            cutoff_date = datetime.now() - timedelta(days=days)
            period_data = history[history.index >= cutoff_date]
            
            if not period_data.empty:
                period_avg = period_data.mean()
                period_std = period_data.std()
                
                comparisons[period_name] = {
                    'average': period_avg,
                    'change': ((current_value - period_avg) / period_avg) * 100,
                    'z_score': (current_value - period_avg) / period_std if period_std > 0 else 0,
                    'percentile': stats.percentileofscore(period_data, current_value)
                }
        
        return comparisons

    def _analyze_trend(self, history: pd.Series) -> Dict:
        """
        Analyze performance trends over different time periods.
        
        Args:
            history (pd.Series): Historical performance data
            
        Returns:
            Dict: Trend analysis results
        """
        trend_analysis = {}
        
        for period_name, days in self.lookback_periods.items():
            cutoff_date = datetime.now() - timedelta(days=days)
            period_data = history[history.index >= cutoff_date]
            
            if len(period_data) >= 2:
                # Calculate linear regression
                x = np.arange(len(period_data))
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    x,
                    period_data.values
                )
                
                trend_analysis[period_name] = {
                    'slope': slope,
                    'direction': 'improving' if slope > 0 else 'declining',
                    'strength': abs(r_value),
                    'significance': p_value < 0.05,
                    'volatility': period_data.std() / period_data.mean()
                }
        
        return trend_analysis

    def _calculate_improvement_rate(self,
                                 current_value: float,
                                 history: pd.Series) -> Dict:
        """
        Calculate rate of improvement over different time periods.
        
        Args:
            current_value (float): Current metric value
            history (pd.Series): Historical values
            
        Returns:
            Dict: Improvement rates and projections
        """
        improvement_analysis = {}
        
        for period_name, days in self.lookback_periods.items():
            cutoff_date = datetime.now() - timedelta(days=days)
            period_data = history[history.index >= cutoff_date]
            
            if not period_data.empty:
                start_value = period_data.iloc[0]
                
                # Calculate improvement rate
                total_change = current_value - start_value
                daily_rate = total_change / days
                
                improvement_analysis[period_name] = {
                    'total_change_percent': (total_change / start_value) * 100,
                    'daily_rate': daily_rate,
                    'weekly_rate': daily_rate * 7,
                    'projected_30d': current_value + (daily_rate * 30),
                    'consistency': self._calculate_consistency(period_data)
                }
        
        return improvement_analysis

    def _calculate_consistency(self, data: pd.Series) -> float:
        """
        Calculate consistency score based on variation in performance.
        
        Args:
            data (pd.Series): Performance data
            
        Returns:
            float: Consistency score (0-100)
        """
        if len(data) < 2:
            return 100.0
            
        # Calculate coefficient of variation (normalized standard deviation)
        cv = data.std() / data.mean()
        
        # Convert to consistency score (0-100)
        consistency = 100 * (1 - min(cv, 1))
        
        return consistency

    def _track_milestones(self, 
                         current_value: float,
                         target_value: float,
                         num_milestones: int = 5) -> Dict:
        """
        Track progress towards milestones between current and target values.
        
        Args:
            current_value (float): Current metric value
            target_value (float): Target metric value
            num_milestones (int): Number of milestone points
            
        Returns:
            Dict: Milestone tracking information
        """
        milestone_tracking = {
            'total_progress': 0.0,
            'next_milestone': None,
            'remaining_milestones': [],
            'completed_milestones': []
        }
        
        if target_value != current_value:
            # Calculate progress percentage
            total_progress = (current_value - target_value) / abs(target_value - current_value)
            milestone_tracking['total_progress'] = max(0, min(100, total_progress * 100))
            
            # Generate milestone points
            milestone_values = np.linspace(current_value, target_value, num_milestones + 1)
            
            # Track each milestone
            for i, value in enumerate(milestone_values[1:], 1):
                milestone = {
                    'level': i,
                    'value': value,
                    'progress': (value - current_value) / (target_value - current_value) * 100
                }
                
                if current_value >= value:
                    milestone_tracking['completed_milestones'].append(milestone)
                else:
                    if milestone_tracking['next_milestone'] is None:
                        milestone_tracking['next_milestone'] = milestone
                    else:
                        milestone_tracking['remaining_milestones'].append(milestone)
        
        return milestone_tracking

    def generate_progress_summary(self, progress_report: Dict) -> Dict:
        """
        Generate a summarized progress report with key insights.
        
        Args:
            progress_report (Dict): Detailed progress analysis
            
        Returns:
            Dict: Summarized progress report
        """
        summary = {
            'overall_progress': self._calculate_overall_progress(progress_report),
            'key_improvements': [],
            'areas_of_concern': [],
            'recent_milestones': [],
            'next_targets': []
        }
        
        for metric, analysis in progress_report.items():
            # Check for significant improvements
            short_term = analysis['historical_comparison'].get('short_term', {})
            if short_term.get('change', 0) > 5:  # 5% improvement
                summary['key_improvements'].append({
                    'metric': metric,
                    'improvement': short_term['change']
                })
            
            # Identify areas of concern
            if short_term.get('change', 0) < -5:  # 5% decline
                summary['areas_of_concern'].append({
                    'metric': metric,
                    'decline': abs(short_term['change'])
                })
            
            # Track recent milestones
            if analysis['milestone_progress']['completed_milestones']:
                latest_milestone = analysis['milestone_progress']['completed_milestones'][-1]
                summary['recent_milestones'].append({
                    'metric': metric,
                    'level': latest_milestone['level'],
                    'value': latest_milestone['value']
                })
            
            # Identify next targets
            if analysis['milestone_progress']['next_milestone']:
                next_milestone = analysis['milestone_progress']['next_milestone']
                summary['next_targets'].append({
                    'metric': metric,
                    'target': next_milestone['value'],
                    'progress': next_milestone['progress']
                })
        
        return summary

    def _calculate_overall_progress(self, progress_report: Dict) -> float:
        """
        Calculate overall progress across all metrics.
        
        Args:
            progress_report (Dict): Progress analysis for all metrics
            
        Returns:
            float: Overall progress score (0-100)
        """
        if not progress_report:
            return 0.0
            
        progress_scores = []
        
        for analysis in progress_report.values():
            milestone_progress = analysis['milestone_progress']['total_progress']
            trend_strength = max(
                (trend['strength'] if trend['direction'] == 'improving' else -trend['strength'])
                for trend in analysis['trend_analysis'].values()
            )
            
            # Combine milestone progress and trend strength
            progress_scores.append(milestone_progress * (1 + trend_strength))
        
        return min(100, max(0, sum(progress_scores) / len(progress_scores)))

    def get_improvement_suggestions(self, 
                                 progress_report: Dict,
                                 player_preferences: Optional[Dict] = None) -> List[Dict]:
        """
        Generate improvement suggestions based on progress analysis.
        
        Args:
            progress_report (Dict): Progress analysis results
            player_preferences (Dict, optional): Player's training preferences
            
        Returns:
            List[Dict]: Personalized improvement suggestions
        """
        suggestions = []
        
        for metric, analysis in progress_report.items():
            # Check if improvement is needed
            short_term = analysis['historical_comparison'].get('short_term', {})
            trend = analysis['trend_analysis'].get('short_term', {})
            
            if short_term.get('change', 0) < 0 or trend.get('direction') == 'declining':
                suggestion = {
                    'metric': metric,
                    'priority': 'high' if short_term.get('change', 0) < -5 else 'medium',
                    'focus_areas': self._identify_focus_areas(analysis),
                    'training_adjustments': self._suggest_training_adjustments(
                        analysis,
                        player_preferences
                    )
                }
                suggestions.append(suggestion)
        
        return sorted(suggestions, key=lambda x: x['priority'] == 'high', reverse=True)

    def _identify_focus_areas(self, metric_analysis: Dict) -> List[str]:
        """
        Identify specific areas needing focus based on analysis.
        
        Args:
            metric_analysis (Dict): Analysis for a single metric
            
        Returns:
            List[str]: Specific areas to focus on
        """
        focus_areas = []
        
        # Check consistency
        for period, improvement in metric_analysis['improvement_rate'].items():
            if improvement['consistency'] < 70:
                focus_areas.append(f"Improve consistency in {period} performance")
        
        # Check trend strength
        for period, trend in metric_analysis['trend_analysis'].items():
            if trend['strength'] < 0.5 and trend['direction'] == 'improving':
                focus_areas.append(f"Strengthen improvement trend in {period}")
        
        return focus_areas

    def _suggest_training_adjustments(self,
                                   metric_analysis: Dict,
                                   player_preferences: Optional[Dict] = None) -> List[str]:
        """
        Suggest training adjustments based on analysis and preferences.
        
        Args:
            metric_analysis (Dict): Analysis for a single metric
            player_preferences (Dict, optional): Player's training preferences
            
        Returns:
            List[str]: Suggested training adjustments
        """
        adjustments = []
        
        # Based on improvement rate
        for period, rate in metric_analysis['improvement_rate'].items():
            if rate['consistency'] < 70:
                adjustments.append(
                    f"Increase practice frequency in {period} to improve consistency"
                )
        
        # Based on trend analysis
        for period, trend in metric_analysis['trend_analysis'].items():
            if trend['volatility'] > 0.2:
                adjustments.append(
                    f"Focus on stabilizing performance in {period} sessions"
                )
        
        # Consider player preferences
        if player_preferences:
            preferred_time = player_preferences.get('preferred_practice_time')
            if preferred_time:
                adjustments.append(
                    f"Schedule focused practice sessions during {preferred_time}"
                )
        
        return adjustments