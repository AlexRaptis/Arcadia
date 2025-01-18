# skill_recommender.py

from typing import Dict, List, Optional
import logging
from datetime import timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkillRecommender:
    """
    A class to generate personalized skill improvement recommendations
    based on performance analysis.
    """
    
    def __init__(self):
        """Initialize the recommendation engine with predefined improvement strategies."""
        self.skill_strategies = {
            'accuracy': {
                'beginner': {
                    'practices': [
                        "Practice basic aiming drills for 15 minutes daily",
                        "Focus on stationary target practice",
                        "Use training maps with larger targets"
                    ],
                    'duration': timedelta(weeks=2),
                    'intensity': 'low'
                },
                'intermediate': {
                    'practices': [
                        "Practice precision aiming drills for 20 minutes daily",
                        "Incorporate moving target practice",
                        "Use aim trainer software for varied scenarios"
                    ],
                    'duration': timedelta(weeks=3),
                    'intensity': 'medium'
                },
                'advanced': {
                    'practices': [
                        "Practice advanced aiming techniques for 30 minutes daily",
                        "Focus on flick shots and micro-adjustments",
                        "Incorporate pressure training scenarios"
                    ],
                    'duration': timedelta(weeks=4),
                    'intensity': 'high'
                }
            },
            'reaction_time': {
                'beginner': {
                    'practices': [
                        "Practice basic reaction exercises for 10 minutes daily",
                        "Use simple reaction time training tools",
                        "Focus on consistent timing patterns"
                    ],
                    'duration': timedelta(weeks=2),
                    'intensity': 'low'
                },
                'intermediate': {
                    'practices': [
                        "Practice varied reaction drills for 20 minutes daily",
                        "Incorporate multiple stimulus types",
                        "Use advanced reaction training software"
                    ],
                    'duration': timedelta(weeks=3),
                    'intensity': 'medium'
                },
                'advanced': {
                    'practices': [
                        "Practice complex reaction scenarios for 25 minutes daily",
                        "Focus on multi-target acquisition",
                        "Incorporate decision-making elements"
                    ],
                    'duration': timedelta(weeks=4),
                    'intensity': 'high'
                }
            },
            'decision_making': {
                'beginner': {
                    'practices': [
                        "Review gameplay recordings for 15 minutes daily",
                        "Practice basic strategy scenarios",
                        "Focus on fundamental decision trees"
                    ],
                    'duration': timedelta(weeks=2),
                    'intensity': 'low'
                },
                'intermediate': {
                    'practices': [
                        "Analyze pro gameplay videos for 20 minutes daily",
                        "Practice situational awareness exercises",
                        "Participate in structured scrimmages"
                    ],
                    'duration': timedelta(weeks=3),
                    'intensity': 'medium'
                },
                'advanced': {
                    'practices': [
                        "Study advanced tactics for 30 minutes daily",
                        "Practice complex decision-making scenarios",
                        "Lead team strategy sessions"
                    ],
                    'duration': timedelta(weeks=4),
                    'intensity': 'high'
                }
            },
            'teamwork': {
                'beginner': {
                    'practices': [
                        "Practice basic communication drills",
                        "Focus on role-specific responsibilities",
                        "Participate in casual team games"
                    ],
                    'duration': timedelta(weeks=2),
                    'intensity': 'low'
                },
                'intermediate': {
                    'practices': [
                        "Practice advanced communication strategies",
                        "Focus on team coordination exercises",
                        "Participate in organized team practice"
                    ],
                    'duration': timedelta(weeks=3),
                    'intensity': 'medium'
                },
                'advanced': {
                    'practices': [
                        "Lead team coordination drills",
                        "Develop and execute team strategies",
                        "Organize scrimmage sessions"
                    ],
                    'duration': timedelta(weeks=4),
                    'intensity': 'high'
                }
            }
        }
        logger.info("Skill Recommender initialized with predefined strategies")

    def determine_skill_level(self, metric_value: float, metric_type: str) -> str:
        """
        Determine the skill level based on metric value.
        
        Args:
            metric_value (float): Current value of the performance metric
            metric_type (str): Type of metric being evaluated
            
        Returns:
            str: Skill level classification
        """
        # Metric-specific thresholds
        thresholds = {
            'accuracy': {'beginner': 60, 'intermediate': 80},
            'reaction_time': {'beginner': 300, 'intermediate': 200},  # ms
            'decision_making': {'beginner': 65, 'intermediate': 85},
            'teamwork': {'beginner': 70, 'intermediate': 85}
        }
        
        metric_thresholds = thresholds.get(metric_type, {'beginner': 50, 'intermediate': 75})
        
        if metric_type == 'reaction_time':  # Lower is better
            if metric_value > metric_thresholds['beginner']:
                return 'beginner'
            elif metric_value > metric_thresholds['intermediate']:
                return 'intermediate'
            return 'advanced'
        else:  # Higher is better
            if metric_value < metric_thresholds['beginner']:
                return 'beginner'
            elif metric_value < metric_thresholds['intermediate']:
                return 'intermediate'
            return 'advanced'

    def generate_recommendations(self, 
                              analysis_results: Dict,
                              player_history: Optional[Dict] = None) -> List[Dict]:
        """
        Generate personalized skill improvement recommendations.
        
        Args:
            analysis_results (Dict): Results from performance analysis
            player_history (Dict, optional): Historical training data
            
        Returns:
            List[Dict]: List of personalized recommendations
        """
        recommendations = []
        
        for metric, analysis in analysis_results.items():
            if analysis['improvement_analysis']['needs_improvement']:
                current_level = analysis['current_stats']['mean']
                skill_level = self.determine_skill_level(current_level, metric)
                
                # Get appropriate strategies
                if metric in self.skill_strategies:
                    strategy = self.skill_strategies[metric][skill_level]
                    
                    recommendation = {
                        'metric': metric,
                        'current_level': current_level,
                        'skill_level': skill_level,
                        'target_level': analysis['improvement_analysis']['suggested_target'],
                        'practices': strategy['practices'],
                        'duration': strategy['duration'].days,
                        'intensity': strategy['intensity'],
                        'priority': 'high' if analysis['improvement_analysis']['z_score'] < -2 else 'medium'
                    }
                    
                    recommendations.append(recommendation)
        
        # Sort by priority and expected improvement impact
        recommendations.sort(key=lambda x: (
            x['priority'] == 'high',
            abs(x['target_level'] - x['current_level'])
        ), reverse=True)
        
        logger.info(f"Generated {len(recommendations)} skill improvement recommendations")
        return recommendations

    def estimate_improvement_timeline(self, 
                                   recommendation: Dict,
                                   player_data: Optional[Dict] = None) -> Dict:
        """
        Estimate timeline for skill improvement based on recommendation.
        
        Args:
            recommendation (Dict): Single skill improvement recommendation
            player_data (Dict, optional): Historical player improvement data
            
        Returns:
            Dict: Timeline estimation and milestones
        """
        base_improvement = {
            'low': 0.1,
            'medium': 0.15,
            'high': 0.2
        }
        
        intensity_factor = base_improvement[recommendation['intensity']]
        expected_weekly_improvement = (
            recommendation['target_level'] - recommendation['current_level']
        ) * intensity_factor
        
        milestones = []
        current = recommendation['current_level']
        
        for week in range(1, recommendation['duration'] // 7 + 1):
            current += expected_weekly_improvement
            milestones.append({
                'week': week,
                'expected_level': current,
                'improvement': expected_weekly_improvement
            })
        
        return {
            'total_duration_days': recommendation['duration'],
            'expected_weekly_improvement': expected_weekly_improvement,
            'milestones': milestones
        }