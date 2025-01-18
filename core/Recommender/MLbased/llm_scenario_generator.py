# llm_scenario_generator.py

from typing import Dict, List
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMScenarioGenerator:
    """
    A class that uses LLM to generate practice scenarios for gaming skill improvement.
    """
    
    def __init__(self, llm_client):
        """
        Initialize the LLM-based scenario generator.
        
        Args:
            llm_client: An initialized LLM client (e.g., OpenAI, Anthropic)
        """
        self.llm = llm_client

    def generate_scenarios(self, recommendations: List[Dict]) -> List[Dict]:
        """
        Generate practice scenarios using LLM based on recommendations.
        
        Args:
            recommendations (List[Dict]): Skill improvement recommendations
            
        Returns:
            List[Dict]: Practice scenarios for each skill
        """
        scenarios = []
        
        for rec in recommendations:
            # Create prompt for scenario generation
            prompt = self._create_scenario_prompt(rec)
            
            try:
                # Get LLM response
                response = self.llm.generate(prompt)
                
                # Parse and validate scenarios
                parsed_scenarios = self._parse_scenarios(response)
                
                if parsed_scenarios:
                    scenarios.append({
                        'metric': rec['metric'],
                        'scenarios': parsed_scenarios
                    })
                    
            except Exception as e:
                logger.error(f"Error generating scenarios for {rec['metric']}: {str(e)}")
                # Use fallback scenarios if LLM fails
                fallback = self._get_fallback_scenarios(rec)
                scenarios.append({
                    'metric': rec['metric'],
                    'scenarios': fallback
                })
        
        logger.info(f"Generated scenarios for {len(scenarios)} skills")
        return scenarios

    def _create_scenario_prompt(self, recommendation: Dict) -> str:
        """
        Create a prompt for the LLM to generate practice scenarios.
        
        Args:
            recommendation (Dict): Skill improvement recommendation
            
        Returns:
            str: Formatted prompt
        """
        prompt = """As a gaming coach, create 3 practice scenarios to improve {metric} skill.
Current level: {current_level:.1f}
Target level: {target_level:.1f}
Practice routine: {practice_routine}

Create scenarios that:
1. Are specific and measurable
2. Have clear success criteria
3. Can be completed in 5-10 minutes
4. Progress in difficulty

Format your response as a JSON array of scenarios, where each scenario has:
{
    "name": str,
    "description": str,
    "duration_minutes": int,
    "success_criteria": str,
    "difficulty": "beginner" | "intermediate" | "advanced"
}"""

        return prompt.format(
            metric=recommendation['metric'],
            current_level=recommendation.get('current_level', 0),
            target_level=recommendation.get('target_level', 0),
            practice_routine=recommendation.get('practice_routine', 'daily practice')
        )

    def _parse_scenarios(self, llm_response: str) -> List[Dict]:
        """
        Parse and validate LLM response.
        
        Args:
            llm_response (str): Raw response from LLM
            
        Returns:
            List[Dict]: Parsed scenarios
        """
        try:
            # Extract JSON from response
            scenarios = json.loads(llm_response)
            
            # Validate required fields
            required_fields = {
                'name', 'description', 'duration_minutes',
                'success_criteria', 'difficulty'
            }
            
            validated_scenarios = []
            for scenario in scenarios:
                if all(field in scenario for field in required_fields):
                    validated_scenarios.append(scenario)
            
            return validated_scenarios
            
        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response as JSON")
            return []

    def _get_fallback_scenarios(self, recommendation: Dict) -> List[Dict]:
        """
        Provide basic fallback scenarios if LLM fails.
        
        Args:
            recommendation (Dict): Skill improvement recommendation
            
        Returns:
            List[Dict]: Basic scenarios
        """
        fallback_templates = {
            'accuracy': [
                {
                    'name': 'Basic Target Practice',
                    'description': 'Hit 10 stationary targets within 45 seconds',
                    'duration_minutes': 5,
                    'success_criteria': 'Minimum 70% accuracy',
                    'difficulty': 'beginner'
                },
                {
                    'name': 'Moving Target Training',
                    'description': 'Hit 15 moving targets within 30 seconds',
                    'duration_minutes': 5,
                    'success_criteria': 'Minimum 75% accuracy',
                    'difficulty': 'intermediate'
                }
            ],
            'reaction_time': [
                {
                    'name': 'Quick Response Training',
                    'description': 'React to 20 visual cues as quickly as possible',
                    'duration_minutes': 5,
                    'success_criteria': 'Average reaction time under 300ms',
                    'difficulty': 'beginner'
                },
                {
                    'name': 'Multi-Target Reactions',
                    'description': 'React to multiple targets in sequence',
                    'duration_minutes': 5,
                    'success_criteria': 'Average reaction time under 250ms',
                    'difficulty': 'intermediate'
                }
            ],
            'decision_making': [
                {
                    'name': 'Basic Decision Challenge',
                    'description': 'Make correct decisions in simple game situations',
                    'duration_minutes': 10,
                    'success_criteria': '7/10 correct decisions',
                    'difficulty': 'beginner'
                },
                {
                    'name': 'Tactical Choices',
                    'description': 'Choose optimal strategies in complex situations',
                    'duration_minutes': 10,
                    'success_criteria': '8/10 optimal choices',
                    'difficulty': 'intermediate'
                }
            ],
            'teamwork': [
                {
                    'name': 'Communication Practice',
                    'description': 'Practice clear and efficient team communication',
                    'duration_minutes': 10,
                    'success_criteria': '80% communication accuracy',
                    'difficulty': 'beginner'
                },
                {
                    'name': 'Team Coordination',
                    'description': 'Execute coordinated team movements and actions',
                    'duration_minutes': 10,
                    'success_criteria': '85% successful coordination',
                    'difficulty': 'intermediate'
                }
            ]
        }
        
        return fallback_templates.get(recommendation['metric'], fallback_templates['accuracy'])

    def adjust_difficulty(self, scenario: Dict, player_level: float) -> Dict:
        """
        Adjust scenario difficulty based on player's current level.
        
        Args:
            scenario (Dict): Practice scenario
            player_level (float): Player's current skill level
            
        Returns:
            Dict: Adjusted scenario
        """
        adjusted = scenario.copy()
        
        # Adjust duration based on level
        if player_level < 50:  # Beginner
            adjusted['duration_minutes'] = min(adjusted['duration_minutes'] * 1.5, 15)
        elif player_level > 80:  # Advanced
            adjusted['duration_minutes'] = max(adjusted['duration_minutes'] * 0.8, 5)
        
        # Adjust success criteria
        if 'accuracy' in adjusted['success_criteria']:
            current_accuracy = int(''.join(filter(str.isdigit, adjusted['success_criteria'])))
            if player_level < 50:
                current_accuracy = max(current_accuracy - 10, 60)
            elif player_level > 80:
                current_accuracy = min(current_accuracy + 10, 95)
            adjusted['success_criteria'] = adjusted['success_criteria'].replace(
                str(current_accuracy),
                str(current_accuracy)
            )
        
        return adjusted