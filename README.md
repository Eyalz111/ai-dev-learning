# 🤖 AI Development Learning Journey

A comprehensive repository documenting my journey through AI development, data science, and machine learning concepts. This project serves as both a learning portfolio and a practical toolkit for AI development.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Modules](#modules)
  - [Module 2: Python Fundamentals](#module-2-python-fundamentals)
  - [Module 3: Data Science & Machine Learning](#module-3-data-science--machine-learning)
  - [Claude Practice: AI Tools Development](#claude-practice-ai-tools-development)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Learning Outcomes](#learning-outcomes)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository represents a structured approach to learning AI development, covering everything from Python fundamentals to advanced machine learning techniques and AI tool development. The project is organized into distinct modules, each focusing on specific aspects of AI and data science.

## 📁 Project Structure

```
ai-dev-learning/
├── Module 2 Python problem_sets/     # Python fundamentals and problem solving
├── Module 3 data-science-module/     # Data science and ML comprehensive course
├── Claude practice/                  # AI assistant and game development
├── Mini Streamlit Project/          # Web application development
├── Python Scripts/                  # Additional practice scripts
└── game_tools/                     # Reusable game development components
```

## 📚 Modules

### Module 2: Python Fundamentals

**Focus**: Core Python programming concepts and problem-solving skills

**Contents**:
- **Problem Sets 1-5**: Progressive difficulty exercises covering:
  - Basic Python syntax and data structures
  - Object-oriented programming concepts
  - File handling and data manipulation
  - Advanced Python features and best practices

**Key Files**:
- `PS1-PS5.IPYNB`: Interactive Jupyter notebooks with exercises
- `PS5/`: Advanced problems including chat systems and zoo management

### Module 3: Data Science & Machine Learning

**Focus**: Comprehensive data science pipeline from data manipulation to advanced ML models

#### 📊 Lectures Covered:

1. **Pandas & Data Manipulation**
   - Data cleaning and preprocessing
   - DataFrame operations and analysis

2. **Data Visualization**
   - Creating insightful charts and graphs
   - Statistical visualization techniques

3. **SQLite Database Management**
   - Database design and querying
   - Integration with Python applications

4. **Streamlit Web Applications**
   - Interactive dashboard development
   - Data visualization web apps

5. **Machine Learning Fundamentals**
   - Linear and Logistic Regression
   - Model evaluation and validation

6. **Clustering Techniques**
   - K-means clustering implementation
   - Unsupervised learning applications

7. **Ensemble Models**
   - Random Forest implementation
   - XGBoost, LightGBM, and CatBoost classifiers
   - Advanced ensemble techniques

8. **Version Control with Git**
   - Git workflow and best practices
   - Collaborative development

9. **CrewAI Framework**
   - Multi-agent AI systems
   - Research and customer support automation

10. **Claude Code Integration**
    - AI-powered code generation and assistance

### Claude Practice: AI Tools Development

**Focus**: Building practical AI applications and tools using Claude API

#### 🛠️ AI Tools (`ai_tools/`):
- **`ai_assistant.py`**: Reusable AI assistant powered by Claude
- **`game_narrator.py`**: Interactive storytelling AI
- **`personalized_learner.py`**: Adaptive learning system
- **`check_models.py`**: Model validation and testing utilities

#### 🎮 Game Development (`game_tools/`):
- **`player.py`**: Player management system
- **`enemies.py`**: Enemy AI and combat mechanics
- **`save_system.py`**: Game state persistence

#### 🧪 Testing Framework (`tests/`):
- Comprehensive test suite for all components
- Automated testing for AI tools and game mechanics

## ✨ Key Features

### 🤖 AI Assistant Integration
- **Claude API Integration**: Professional AI assistant with conversation history
- **Multiple Model Support**: Haiku, Sonnet, and Opus models
- **Flexible System Prompts**: Customizable AI behavior for different use cases

### 📈 Data Science Pipeline
- **End-to-End ML Workflows**: From data preprocessing to model deployment
- **Multiple ML Algorithms**: Regression, classification, clustering, and ensemble methods
- **Interactive Visualizations**: Streamlit-based dashboards and analysis tools

### 🎯 Game Development
- **Modular Architecture**: Reusable components for game development
- **Save System**: JSON-based game state management
- **AI-Powered Narration**: Dynamic storytelling using Claude

### 📊 Project Management
- **Learning Journey Tracking**: JSON-based progress monitoring
- **Gantt Chart Integration**: Project timeline visualization
- **Comprehensive Testing**: Automated test suites for quality assurance

## 🛠️ Technologies Used

### Programming Languages
- **Python 3.x**: Primary development language
- **SQL**: Database queries and management

### AI & Machine Learning
- **Anthropic Claude API**: AI assistant and text generation
- **Scikit-learn**: Machine learning algorithms
- **XGBoost, LightGBM, CatBoost**: Advanced ensemble models
- **Pandas & NumPy**: Data manipulation and analysis

### Web Development
- **Streamlit**: Interactive web applications
- **HTML/CSS**: Frontend styling

### Data & Visualization
- **Matplotlib & Seaborn**: Statistical visualization
- **Plotly**: Interactive charts
- **SQLite**: Lightweight database management

### Development Tools
- **Jupyter Notebooks**: Interactive development environment
- **Git**: Version control
- **pytest**: Testing framework

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Anthropic API key (for Claude integration)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-dev-learning.git
   cd ai-dev-learning
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   # Create .env file in project root
   echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
   ```

## 💡 Usage Examples

### AI Assistant

```python
from Claude_practice.ai_tools.ai_assistant import AIAssistant

# Initialize assistant
assistant = AIAssistant(model="claude-3-5-sonnet-20241022")

# Have a conversation
response = assistant.chat("Explain machine learning in simple terms")
print(response)
```

### Game Development

```python
from Claude_practice.game_tools.player import create_player
from Claude_practice.game_tools.enemies import create_enemy

# Create game entities
player = create_player("Hero")
enemy = create_enemy("Dragon", 50)

# Game logic
print(f"{player['name']} encounters a {enemy['name']}!")
```

### Data Analysis

```python
# Run Jupyter notebooks in Module 3
jupyter notebook "Module 3 data-science-module/Lecture 1 - Pandas/PS.ipynb"
```

## 🎓 Learning Outcomes

Through this project, I have developed expertise in:

- **Python Programming**: Advanced Python concepts and best practices
- **Data Science**: Complete data analysis pipeline from collection to visualization
- **Machine Learning**: Implementation of various ML algorithms and ensemble methods
- **AI Integration**: Practical application of large language models in software development
- **Web Development**: Creating interactive applications with Streamlit
- **Database Management**: SQL operations and database design
- **Software Engineering**: Testing, version control, and modular architecture
- **Project Management**: Structured learning approach and progress tracking

## 🤝 Contributing

This is a personal learning repository, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add some improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic**: For providing the Claude API that powers the AI assistant features
- **Open Source Community**: For the excellent libraries and tools used throughout this project
- **Educational Resources**: Various online courses and tutorials that guided this learning journey

---

**Note**: This repository is actively maintained and updated as I continue my AI development learning journey. Check back regularly for new modules and improvements!

## 📞 Contact

For questions or collaboration opportunities, feel free to reach out through GitHub issues or discussions.

---

*Last updated: November 2024*
