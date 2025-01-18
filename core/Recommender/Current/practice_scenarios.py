# practice_scenarios.py

from typing import Dict, List, Optional
import logging
import random
from datetime import timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScenarioGenerator:
    """
    A class to generate specific practice scenarios based on skill recommendations.
    """
    
    def __init__(self):
        """Initialize the scenario generator with predefined scenario templates."""
        self.scenario_templates = {
            'accuracy': {
                'beginner': [
                    {
                        'name': 'Basic Target Practice',
                        'description': 'Hit 10 stationary targets within 45 seconds',
                        'success_criteria': 'Minimum 70% accuracy',
                        'difficulty': 1
                    },
                    {
                        'name': 'Precision Control',
                        'description': 'Hit 5 large targets in sequence without missing',
                        'success_criteria': 'No misses allowed',
                        'difficulty': 1
                    }
                ],
                'intermediate': [
                    {
                        'name': 'Moving Target Track',
                        'description': 'Hit 15 moving targets within 30 seconds',
                        'success_criteria': 'Minimum 75% accuracy',
                        'difficulty': 2
                    },
                    {
                        'name': 'Precision Flicks',
                        'description': 'Hit 10 targets that appear randomly within 20 seconds',
                        'success_criteria': 'Minimum 80% accuracy',
                        'difficulty': 2
                    }
                ],
                'advanced': [
                    {
                        'name': 'Speed Precision Challenge',
                        'description': 'Hit 20 small moving targets within 25 seconds',
                        'success_criteria': 'Minimum 85% accuracy',
                        'difficulty': 3
                    },
                    {
                        'name': 'Advanced Flick Training',
                        'description': 'Hit 15 targets that appear for only 0.5 seconds each',
                        'success_criteria': 'Minimum 90% accuracy',
                        'difficulty': 3
                    }
                ]
            },
            'reaction_time': {
                'beginner': [
                    {
                        'name': 'Basic Reaction Training',
                        'description': 'React to 10 visual cues within 5 seconds each',
                        'success_criteria': 'Average reaction time under 400ms',
                        'difficulty': 1
                    },
                    {
                        'name': 'Simple Choice Reaction',
                        'description': 'Respond to different colored targets correctly',
                        'success_criteria': 'Average reaction time under 450ms',
                        'difficulty': 1
                    }
                ],
                'intermediate': [
                    {
                        'name': 'Multi-Target Reaction',
                        'description': 'React to simultaneous targets in order',
                        'success_criteria': 'Average reaction time under 300ms',
                        'difficulty': 2
                    },
                    {
                        'name': 'Dynamic Response Training',
                        'description': 'React to changing patterns of targets',
                        'success_criteria': 'Average reaction time under 250ms',
                        'difficulty': 2
                    }
                ],
                'advanced': [
                    {
                        'name': 'Complex Reaction Challenge',
                        'description': 'React to multiple stimuli types with different responses',
                        'success_criteria': 'Average reaction time under 200ms',
                        'difficulty': 3
                    },
                    {
                        'name': 'Speed Precision Matrix',
                        'description': 'React to grid-based targets with precision requirements',
                        'success_criteria': 'Average reaction time under 180ms',
                        'difficulty': 3
                    }
                ]
            },
            'decision_making': {
                'beginner': [
                    {
                        'name': 'Basic Strategy Choices',
                        'description': 'Choose correct responses to simple game situations',
                        'success_criteria': '7/10 correct decisions',
                        'difficulty': 1
                    },
                    {
                        'name': 'Resource Management Basic',
                        'description': 'Allocate limited resources in simple scenarios',
                        'success_criteria': '70% efficiency in resource use',
                        'difficulty': 1
                    }
                ],
                'intermediate': [
                    {
                        'name': 'Tactical Decision Making',
                        'description': 'Make optimal choices in complex combat scenarios',
                        'success_criteria': '80% optimal decision rate',
                        'difficulty': 2
                    },
                    {
                        'name': 'Strategic Planning Exercise',
                        'description': 'Plan and execute multi-step strategies',
                        'success_criteria': 'Complete objective within time limit',
                        'difficulty': 2
                    }
                ],
                'advanced': [
                    {
                        'name': 'Advanced Tactical Simulator',
                        'description': 'Handle complex, multi-variable combat situations',
                        'success_criteria': '90% optimal decision rate',
                        'difficulty': 3
                    },
                    {
                        'name': 'Leadership Decision Challenge',
                        'description': 'Make team-wide strategic decisions under pressure',
                        'success_criteria': 'Successfully lead team to objective',
                        'difficulty': 3
                    }
                ]
            },
            'teamwork': {
                'beginner': [
                    {
                        'name': 'Basic Communication Drill',
                        'description': 'Relay simple information to teammates accurately',
                        'success_criteria': '80% communication accuracy',
                        'difficulty': 1
                    },
                    {
                        'name': 'Team Role Practice',
                        'description': 'Execute basic role-specific tasks in team context',
                        'success_criteria': 'Complete all role tasks',
                        'difficulty': 1
                    }
                ],
                'intermediate': [
                    {
                        'name': 'Coordination Exercise',
                        'description': 'Execute synchronized team movements and actions',
                        'success_criteria': '85% synchronization accuracy',
                        'difficulty': 2
                    },
                    {
                        'name': 'Strategic Communication',
                        'description': 'Coordinate complex team maneuvers with clear communication',
                        'success_criteria': '90% successful coordination',
                        'difficulty': 2
                    }
                ],
                'advanced': [
                    {
                        'name': 'Team Leadership Drill',
                        'description': 'Lead team through complex scenarios with multiple objectives',
                        'success_criteria': 'Complete all objectives with 90% team efficiency',
                        'difficulty': 3
                    },
                    {
                        'name': 'Advanced Team Tactics',
                        'description': 'Execute professional-level team strategies in high-pressure situations',
                        'success_criteria': 'Achieve victory with optimal resource usage',
                        'difficulty': 3
                    }
                ]
            }
        }
        logger.info("Scenario Generator initialized with predefined templates")

    def generate_practice_plan(self, 
                             recommendations: List[Dict],
                             player_preferences: Optional[Dict] = None) -> List[Dict]:
        """
        Generate a structured practice plan based on skill recommendations.
        
        Args:
            recommendations (List[Dict]): Skill improvement recommendations
            player_preferences (Dict, optional): Player's preferred practice styles
            
        Returns:
            List[Dict]: Structured practice scenarios
        """
        practice_plan = []
        
        for rec in recommendations:
            metric = rec['metric']
            skill_level = rec['skill_level']
            
            if metric in self.scenario_templates and skill_level in self.scenario_templates[metric]:
                # Get base scenarios for the skill level
                base_scenarios = self.scenario_templates[metric][skill_level]
                
                # Select and customize scenarios
                scenarios = self._customize_scenarios(
                    base_scenarios,
                    rec,
                    player_preferences
                )
                
                practice_plan.append({
                    'metric': metric,
                    'skill_level': skill_level,
                    'target_improvement': rec['target_level'] - rec['current_level'],
                    'scenarios': scenarios,
                    'progression_path': self._generate_progression_path(rec)
                })
        
        logger.info(f"Generated practice plan with {len(practice_plan)} focus areas")
        return practice_plan

    def _customize_scenarios(self, 
                           base_scenarios: List[Dict],
                           recommendation: Dict,
                           player_preferences: Optional[Dict] = None) -> List[Dict]:
        """
        Customize scenarios based on player's current level and preferences.
        
        Args:
            base_scenarios (List[Dict]): Base scenario templates
            recommendation (Dict): Skill improvement recommendation
            player_preferences (Dict, optional): Player's preferred practice styles
            
        Returns:
            List[Dict]: Customized practice scenarios
        """
        customized = []
        
        for scenario in base_scenarios:
            # Create a copy of the base scenario
            custom_scenario = scenario.copy()
            
            # Adjust difficulty based on current level
            difficulty_adjustment = self._calculate_difficulty_adjustment(
                recommendation['current_level'],
                recommendation['target_level']
            )
            
            # Modify scenario parameters
            custom_scenario.update({
                'adjusted_difficulty': scenario['difficulty'] + difficulty_adjustment,
                'estimated_improvement': self._estimate_scenario_impact(
                    scenario,
                    recommendation
                ),
                'recommended_attempts': self._calculate_recommended_attempts(
                    scenario,
                    recommendation
                )
            })
            
            # Apply player preferences if available
            if player_preferences:
                custom_scenario = self._apply_player_preferences(
                    custom_scenario,
                    player_preferences
                )
            
            customized.append(custom_scenario)
        
        return customized

    def _calculate_difficulty_adjustment(self, 
                                      current_level: float,
                                      target_level: float) -> float:
        """
        Calculate difficulty adjustment based on skill gap.
        
        Args:
            current_level (float): Current skill level
            target_level (float): Target skill level
            
        Returns:
            float: Difficulty adjustment factor
        """
        skill_gap = target_level - current_level
        return min(max(-0.5, skill_gap / 10), 0.5)

    def _estimate_scenario_impact(self, 
                                scenario: Dict,
                                recommendation: Dict) -> float:
        """
        Estimate the improvement impact of a scenario.
        
        Args:
            scenario (Dict): Practice scenario
            recommendation (Dict): Skill improvement recommendation
            
        Returns:
            float: Estimated improvement per successful completion
        """
        base_improvement = 0.05  # 5% improvement per successful completion
        difficulty_multiplier = 1 + (scenario['difficulty'] * 0.2)
        
        return base_improvement * difficulty_multiplier

    def _calculate_recommended_attempts(self, 
                                     scenario: Dict,
                                     recommendation: Dict) -> int:
        """
        Calculate recommended number of attempts for a scenario.
        
        Args:
            scenario (Dict): Practice scenario
            recommendation (Dict): Skill improvement recommendation
            
        Returns:
            int: Recommended number of attempts
        """
        base_attempts = 5
        difficulty_factor = 1 + (scenario['difficulty'] * 0.5)
        return max(3, int(base_attempts * difficulty_factor))

    def _apply_player_preferences(self, 
                                scenario: Dict,
                                preferences: Dict) -> Dict:
        """
        Modify scenario based on player preferences.
        
        Args:
            scenario (Dict): Practice scenario
            preferences (Dict): Player's preferences
            
        Returns:
            Dict: Modified scenario
        """
        modified = scenario.copy()
        
        if 'preferred_duration' in preferences:
            # Adjust time limits based on preference
            time_factor = preferences['preferred_duration'] / 30  # 30 seconds as base
            modified['description'] = self._adjust_time_limit(
                modified['description'],
                time_factor
            )
        
        if 'preferred_difficulty' in preferences:
            # Adjust difficulty based on preference
            modified['adjusted_difficulty'] *= preferences['preferred_difficulty']
        
        return modified

    def _generate_progression_path(self, recommendation: Dict) -> List[Dict]:
        """
        Generate a progression path for skill improvement.
        
        Args:
            recommendation (Dict): Skill improvement recommendation
            
        Returns:
            List[Dict]: Progression path with milestones
        """
        current_level = recommendation['current_level']
        target_level = recommendation['target_level']
        total_improvement = target_level - current_level
        
        milestones = []
        steps = 4  # Number of progression steps
        
        for i in range(steps):
            progress = (i + 1) / steps
            milestone_level = current_level + (total_improvement * progress)
            
            milestones.append({
                'level': milestone_level,
                'requirements': self._generate_milestone_requirements(
                    recommendation['metric'],
                    progress
                ),
                'unlocks': self._generate_milestone_unlocks(
                    recommendation['metric'],
                    progress
                )
            })
        
        return milestones

    def _generate_milestone_requirements(self, metric: str, progress: float) -> Dict:
        """
        Generate requirements for reaching a milestone.
        
        Args:
            metric (str): Skill metric
            progress (float): Progress through the improvement path
            
        Returns:
            Dict: Milestone requirements
        """
        base_requirements = {
            'accuracy': {
                'min_success_rate': 70 + (20 * progress),
                'consecutive_completions': 3 + int(2 * progress)
            },
            'reaction_time': {
                'max_average_time': 400 - (200 * progress),
                'consecutive_completions': 3 + int(2 * progress)
            },
            'decision_making': {
                'min_correct_decisions': 70 + (20 * progress),
                'consecutive_completions': 3 + int(2 * progress)
            },
            'teamwork': {
                'min_coordination_score': 70 + (20 * progress),
                'consecutive_completions': 3 + int(2 * progress)
            }
        }
        
        return base_requirements.get(metric, base_requirements['accuracy'])

    def _generate_milestone_unlocks(self, metric: str, progress: float) -> List[str]:
        """
        Generate rewards/unlocks for reaching a milestone.
        
        Args:
            metric (str): Skill metric
            progress (float): Progress through the improvement path
            
        Returns:
            List[str]: Unlocked features or achievements
        """
        base_unlocks = {
            'accuracy': [
                'New target patterns',
                'Advanced scoring modes',
                'Custom challenge creation'
            ],
            'reaction_time': [
                'Complex stimulus patterns',
                'Multi-target scenarios',
                'Speed run modes'
            ],
            'decision_making': [
                'Advanced scenario types',
                'Strategy analysis tools',
                'Custom scenario creation'
            ],
            'teamwork': [
                'Advanced team roles',
                'Leadership tools',
                'Custom drill creation'
            ]
        }
        
        metric_unlocks = base_unlocks.get(metric, base_unlocks['accuracy'])