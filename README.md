# Arcadia - AI-Powered Game Coach
![BANNERGAMING](https://github.com/user-attachments/assets/785d2533-9c06-492b-a341-b26f4f8e2667)

**Master Your Game with Arcadia**

Welcome to **Arcadia**, your personal AI-powered game coach. Designed for gamers of all levels, Arcadia analyzes your gameplay performance and offers tailored strategies, tips, and tactics to help you excel in your favorite games. Whether you're into MOBA, FPS, or RPGs, Arcadia adapts to your playstyle and goals, empowering you to reach your full potential.

---

## **About Arcadia**

Arcadia leverages cutting-edge artificial intelligence to provide real-time insights and actionable advice for players. By analyzing in-game performance metrics, it identifies areas for improvement, suggests optimal strategies, and tracks your progress over time. Whether you're aiming for higher ranks, better accuracy, or smarter decision-making, Arcadia is here to guide you every step of the way.

---

## **Requirements**

- Nvidia RTX 980, higher or equivalent
- Nvidia CUDA Toolkit 11.8 [Download](https://developer.nvidia.com/cuda-11-8-0-download-archive)
- Python 3.8 or higher
- Required Python packages (specified in requirements.txt)
- Access to game APIs or data sources for performance tracking

---

## Key Features

- **Multi-Source Data Collection**  
  Gather performance data through web scraping, API integration, and database connections.

- **Advanced Performance Analysis**  
  Comprehensive analysis of gameplay metrics including outlier detection and trend analysis.

- **Dual Recommendation Systems**  
  - Template-based recommendations for consistent, structured advice
  - LLM-powered recommendations for dynamic, context-aware coaching

- **Intelligent Scenario Generation**  
  - Pre-defined scenario templates for systematic skill development
  - AI-generated custom scenarios based on player needs

- **Progress Tracking**  
  Sophisticated tracking system with historical comparisons and improvement analytics.

---

## Technologies Used

### Core Components
- **Data Collection Module**
  - BeautifulSoup4 for web scraping
  - Async HTTP clients for API integration
  - SQLite for local data storage
  - Pandas for data manipulation

- **Analysis Engine**
  - NumPy and SciPy for statistical analysis
  - Outlier detection using IQR method
  - Trend analysis using linear regression
  - Z-score based performance evaluation

- **Recommendation Systems**
  - Template-based system with predefined strategies
  - LLM integration for dynamic recommendations
  - Hybrid approach combining both methods

- **Progress Tracking**
  - Time-series analysis
  - Multiple lookback periods (short, medium, long-term)
  - Milestone tracking and projection

### Architecture
- **Backend Framework:** Python with async support
- **Data Processing:** Pandas, NumPy, SciPy
- **AI/ML Components:** 
  - Large Language Models for dynamic content generation
  - Statistical models for performance analysis
- **Database:** SQLite with potential for PostgreSQL scaling

---

## System Components

### 1. Data Collection (`data_collector.py`)
- Multi-source data gathering
- Error handling and data validation
- Asynchronous API calls
- Web scraping capabilities

### 2. Performance Analysis (`performance_analyzer.py`)
- Statistical analysis of gameplay metrics
- Outlier detection
- Trend analysis
- Performance benchmarking

### 3. Skill Recommendation
#### Template-Based (`skill_recommender.py`)
- Predefined improvement strategies
- Structured practice routines
- Experience-level appropriate recommendations

#### LLM-Based (`llm_skill_recommender.py`)
- Dynamic recommendation generation
- Context-aware advice
- Natural language interactions

### 4. Scenario Generation
#### Template-Based (`practice_scenarios.py`)
- Structured training scenarios
- Difficulty progression
- Skill-specific exercises

#### LLM-Based (`llm_scenario_generator.py`)
- Custom scenario creation
- Adaptive difficulty
- Personalized challenges

### 5. Progress Tracking (`progress_tracker.py`)
- Historical performance comparison
- Improvement rate calculation
- Milestone tracking
- Trend analysis

---

## How to Use

Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Arcadia.git
   ```
Open the config.py file and tweak the onnxChoice variable to correspond with your hardware specs:

- onnxChoice = 1 # CPU ONLY
- onnxChoice = 2 # AMD/NVIDIA ONLY
- onnxChoice = 3 # NVIDIA ONLY

IF you have an NVIDIA set up, run the following
   ```bash
pip install onnxruntime-gpu
pip install cupy-cuda11x
```

Install dependencies:
   ```bash
   cd Arcadia
   pip install -r requirements.txt
   ```

Set Your Environmental Variables

- C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\lib
- C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\libnvvp
- C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin

Run the script:
   ```bash
python .\export.py --weights ./yolov5s.pt --include engine --half --imgsz 320 320 --device 0
   ```

Run the application
   ```bash
python app.py
```


---

## Contributing

We welcome contributions from the community! Fork the repository, create pull requests, or submit issues to help improve Arcadia.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

- **GitHub:** [Arcadia Repository](https://github.com/yourusername/Arcadia)  
- **Email:** your-email@example.com  
- **Twitter:** [@ArcadiaAI](https://twitter.com/ArcadiaAI)  

---

**Elevate your skills. Conquer your game. Welcome to Arcadia.**
