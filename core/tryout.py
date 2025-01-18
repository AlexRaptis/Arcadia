# main_comparison.py

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
from typing import Dict, List
import logging

# Import both versions of recommenders and generators
from Recommender.Current.skill_recommender import SkillRecommender
from Recommender.Current.practice_scenarios import ScenarioGenerator
from Recommender.MLbased.llm_skill_recommender import LLMSkillRecommender
from Recommender.MLbased.llm_scenario_generator import LLMScenarioGenerator

# Import other components
from data_gathering import DataCollector
from performance_analyzer import PerformanceAnalyzer
from progress_tracker import ProgressTracker

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GamingAssistantComparison:
    """
    Class to compare template-based and LLM-based approaches for gaming skill improvement.
    """
    
    def __init__(self, llm_client):
        """Initialize components for both approaches."""
        # Initialize data collection and analysis
        self.collector = DataCollector()
        self.analyzer = PerformanceAnalyzer()
        self.tracker = ProgressTracker()
        
        # Initialize template-based components
        self.template_recommender = SkillRecommender()
        self.template_generator = ScenarioGenerator()
        
        # Initialize LLM-based components
        self.llm_recommender = LLMSkillRecommender(llm_client)
        self.llm_generator = LLMScenarioGenerator(llm_client)
        
        logger.info("Gaming Assistant Comparison initialized")

    async def generate_sample_data(self) -> Dict:
        """Generate sample player data for testing."""
        current_stats = {
            'accuracy': 75.5,
            'reaction_time': 250,  # milliseconds
            'decision_making': 82.3,
            'teamwork': 68.7
        }
        
        # Generate historical data
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=90),
            end=datetime.now(),
            freq='D'
        )
        
        historical_data = pd.DataFrame(index=dates)
        historical_data['accuracy'] = 70 + np.random.normal(0, 5, len(dates))
        historical_data['reaction_time'] = 300 + np.random.normal(0, 20, len(dates))
        historical_data['decision_making'] = 75 + np.random.normal(0, 7, len(dates))
        historical_data['teamwork'] = 65 + np.random.normal(0, 6, len(dates))
        
        # Add trend
        historical_data['accuracy'] += np.linspace(0, 5, len(dates))
        historical_data['reaction_time'] -= np.linspace(0, 50, len(dates))
        
        return {
            'current_stats': current_stats,
            'historical_data': historical_data
        }

    async def run_comparison(self) -> Dict:
        """Run comparison between template-based and LLM-based approaches."""
        try:
            # Generate sample data
            data = await self.generate_sample_data()
            
            # Analyze performance
            analysis_results = self.analyzer.analyze_performance(
                data['historical_data']
            )
            
            # Track progress
            progress_report = self.tracker.track_progress(
                data['current_stats'],
                data['historical_data'],
                {
                    'accuracy': 85.0,
                    'reaction_time': 200.0,
                    'decision_making': 90.0,
                    'teamwork': 80.0
                }
            )
            
            # Generate recommendations using both approaches
            template_recommendations = self.template_recommender.generate_recommendations(
                analysis_results
            )
            
            llm_recommendations = await self.llm_recommender.generate_recommendations(
                analysis_results
            )
            
            # Generate practice scenarios using both approaches
            template_scenarios = self.template_generator.generate_practice_plan(
                template_recommendations
            )
            
            llm_scenarios = await self.llm_generator.generate_scenarios(
                llm_recommendations
            )
            
            # Compile comparison results
            comparison = {
                'template_based': {
                    'recommendations': template_recommendations,
                    'scenarios': template_scenarios,
                    'metrics': self._calculate_metrics(template_recommendations, template_scenarios)
                },
                'llm_based': {
                    'recommendations': llm_recommendations,
                    'scenarios': llm_scenarios,
                    'metrics': self._calculate_metrics(llm_recommendations, llm_scenarios)
                },
                'progress_tracking': progress_report,
                'analysis_summary': self._generate_comparison_summary(
                    template_recommendations,
                    llm_recommendations,
                    progress_report
                )
            }
            
            logger.info("Completed approach comparison")
            return comparison
            
        except Exception as e:
            logger.error(f"Error in comparison: {str(e)}")
            raise

    def _calculate_metrics(self, 
                         recommendations: List[Dict],
                         scenarios: List[Dict]) -> Dict:
        """Calculate metrics for comparing approaches."""
        return {
            'num_recommendations': len(recommendations),
            'num_scenarios': len(scenarios),
            'avg_scenarios_per_skill': sum(len(s['scenarios']) for s in scenarios) / len(scenarios) if scenarios else 0,
            'skills_covered': len({rec['metric'] for rec in recommendations}),
            'recommendation_specificity': self._calculate_specificity(recommendations),
            'scenario_complexity': self._calculate_complexity(scenarios)
        }

    def _calculate_specificity(self, recommendations: List[Dict]) -> float:
        """Calculate how specific the recommendations are."""
        total_words = sum(
            len(str(rec).split()) 
            for rec in recommendations
        )
        return total_words / len(recommendations) if recommendations else 0

    def _calculate_complexity(self, scenarios: List[Dict]) -> float:
        """Calculate average complexity of scenarios."""
        if not scenarios:
            return 0.0
            
        total_complexity = 0
        total_scenarios = 0
        
        for skill_scenarios in scenarios:
            for scenario in skill_scenarios['scenarios']:
                # Calculate complexity based on description length and difficulty
                complexity = len(scenario['description'].split()) * (
                    1 + self._get_difficulty_multiplier(scenario.get('difficulty', 'beginner'))
                )
                total_complexity += complexity
                total_scenarios += 1
        
        return total_complexity / total_scenarios if total_scenarios > 0 else 0

    def _get_difficulty_multiplier(self, difficulty: str) -> float:
        """Get multiplier based on difficulty level."""
        return {
            'beginner': 0.5,
            'intermediate': 1.0,
            'advanced': 1.5
        }.get(difficulty.lower(), 1.0)

    def _generate_comparison_summary(self,
                                  template_recs: List[Dict],
                                  llm_recs: List[Dict],
                                  progress: Dict) -> Dict:
        """Generate a summary comparing both approaches."""
        return {
            'template_strengths': [
                'Consistent structure',
                'Predictable outputs',
                'Fast execution',
                'No external dependencies'
            ],
            'llm_strengths': [
                'More dynamic responses',
                'Better context adaptation',
                'Natural language variation',
                'Handles edge cases better'
            ],
            'progress_insights': self._extract_progress_insights(progress),
            'recommendation_overlap': self._calculate_recommendation_overlap(
                template_recs,
                llm_recs
            )
        }

    def _extract_progress_insights(self, progress_report: Dict) -> List[str]:
        """Extract key insights from progress report."""
        insights = []
        
        for metric, data in progress_report.items():
            # Check for significant improvements
            if data['historical_comparison']['short_term']['change'] > 5:
                insights.append(
                    f"Significant improvement in {metric}: "
                    f"{data['historical_comparison']['short_term']['change']:.1f}%"
                )
            
            # Check for concerning trends
            if data['trend_analysis']['short_term']['direction'] == 'declining':
                insights.append(
                    f"Declining trend in {metric} over short term"
                )
        
        return insights

    def _calculate_recommendation_overlap(self,
                                       template_recs: List[Dict],
                                       llm_recs: List[Dict]) -> Dict:
        """Calculate overlap between recommendations from both approaches."""
        template_metrics = {rec['metric'] for rec in template_recs}
        llm_metrics = {rec['metric'] for rec in llm_recs}
        
        return {
            'common_metrics': len(template_metrics & llm_metrics),
            'template_only': len(template_metrics - llm_metrics),
            'llm_only': len(llm_metrics - template_metrics),
            'overlap_percentage': (
                len(template_metrics & llm_metrics) / 
                len(template_metrics | llm_metrics) * 100
                if template_metrics or llm_metrics else 0
            )
        }

async def main():
    """Main entry point for comparison."""
    # Example LLM client configuration
    llm_client = {
        'api_key': 'your_api_key_here',
        'model': 'your_model_here'
    }
    
    # Initialize comparison
    comparison = GamingAssistantComparison(llm_client)
    
    try:
        # Run comparison
        results = await comparison.run_comparison()
        
        # Print summary
        print("\nComparison Summary:")
        print(json.dumps(results['analysis_summary'], indent=2))
        
        # Print metrics comparison
        print("\nMetrics Comparison:")
        print("Template-based approach:")
        print(json.dumps(results['template_based']['metrics'], indent=2))
        print("\nLLM-based approach:")
        print(json.dumps(results['llm_based']['metrics'], indent=2))
        
        # Print progress insights
        print("\nProgress Insights:")
        for insight in results['analysis_summary']['progress_insights']:
            print(f"- {insight}")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())