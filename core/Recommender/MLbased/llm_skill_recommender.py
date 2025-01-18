# llm_skill_recommender.py

from typing import Dict, List
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMSkillRecommender:
    """
    A class that uses LLM to generate personalized gaming skill recommendations.
    """
    
    def __init__(self, llm_client):
        """
        Initialize the LLM-based recommender.
        
        Args:
            llm_client: An initialized LLM client (e.g., OpenAI, Anthropic)
        """
        self.llm = llm_client
        
    def generate_recommendations(self, analysis_results: Dict) -> List[Dict]:
        """
        Generate skill improvement recommendations using LLM.
        
        Args:
            analysis_results (Dict): Performance analysis results
            
        Returns:
            List[Dict]: Personalized recommendations
        """
        # Create a prompt for the LLM
        prompt = self._create_recommendation_prompt(analysis_results)
        
        try:
            # Get LLM response
            response = self.llm.generate(prompt)
            
            # Parse and validate recommendations
            recommendations = self._parse_recommendations(response)
            
            logger.info(f"Generated {len(recommendations)} recommendations using LLM")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._get_fallback_recommendations(analysis_results)

    def _create_recommendation_prompt(self, analysis_results: Dict) -> str:
        """
        Create a prompt for the LLM to generate recommendations.
        
        Args:
            analysis_results (Dict): Performance analysis results
            
        Returns:
            str: Formatted prompt
        """
        metrics_needing_improvement = []
        
        for metric, analysis in analysis_results.items():
            if analysis['improvement_analysis']['needs_improvement']:
                metrics_needing_improvement.append({
                    'metric': metric,
                    'current_level': analysis['current_stats']['mean'],
                    'target_level': analysis['improvement_analysis']['suggested_target']
                })
        
        prompt = """As a professional gaming coach, provide specific practice recommendations for a player who needs to improve in the following areas:

{metrics_details}

For each metric that needs improvement, provide:
1. A clear practice routine (what to practice and how long)
2. Specific goals to aim for
3. Tips for effective practice

Format your response as a JSON object with the following structure for each metric:
{
    "metric": str,
    "practice_routine": str,
    "daily_duration": int (in minutes),
    "goals": str,
    "tips": list[str]
}"""

        metrics_details = ""
        for metric in metrics_needing_improvement:
            metrics_details += f"\n- {metric['metric'].title()}: Currently at {metric['current_level']:.1f}, aiming for {metric['target_level']:.1f}"
        
        return prompt.format(metrics_details=metrics_details)

    def _parse_recommendations(self, llm_response: str) -> List[Dict]:
        """
        Parse and validate LLM response.
        
        Args:
            llm_response (str): Raw response from LLM
            
        Returns:
            List[Dict]: Parsed recommendations
        """
        try:
            # Extract JSON from response
            recommendations = json.loads(llm_response)
            
            # Validate required fields
            required_fields = {'metric', 'practice_routine', 'daily_duration', 'goals', 'tips'}
            
            validated_recommendations = []
            for rec in recommendations:
                if all(field in rec for field in required_fields):
                    validated_recommendations.append(rec)
            
            return validated_recommendations
            
        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response as JSON")
            return []

    def _get_fallback_recommendations(self, analysis_results: Dict) -> List[Dict]:
        """
        Provide basic fallback recommendations if LLM fails.
        
        Args:
            analysis_results (Dict): Performance analysis results
            
        Returns:
            List[Dict]: Basic recommendations
        """
        fallback_templates = {
            'accuracy': {
                'practice_routine': 'Practice aiming drills daily',
                'daily_duration': 20,
                'goals': 'Improve accuracy by 10% within two weeks',
                'tips': ['Start with stationary targets', 'Gradually increase speed']
            },
            'reaction_time': {
                'practice_routine': 'Complete reaction time exercises',
                'daily_duration': 15,
                'goals': 'Reduce reaction time by 50ms',
                'tips': ['Stay focused', 'Take regular breaks']
            },
            'decision_making': {
                'practice_routine': 'Analyze gameplay recordings',
                'daily_duration': 30,
                'goals': 'Improve decision accuracy by 15%',
                'tips': ['Study pro players', 'Practice with purpose']
            },
            'teamwork': {
                'practice_routine': 'Participate in team practice sessions',
                'daily_duration': 45,
                'goals': 'Enhance team coordination score by 20%',
                'tips': ['Communicate clearly', 'Learn from teammates']
            }
        }
        
        recommendations = []
        for metric, analysis in analysis_results.items():
            if analysis['improvement_analysis']['needs_improvement']:
                if metric in fallback_templates:
                    rec = fallback_templates[metric].copy()
                    rec['metric'] = metric
                    recommendations.append(rec)
        
        return recommendations