# LegalSmart Pro - Advanced Legal Client Management System

## 🚀 Overview
LegalSmart Pro is a sophisticated Streamlit application for managing legal clients with AI-powered analysis using Claude 3.5 Sonnet. The application features advanced caching, rate limiting, model fallback, and professional UI/UX design.

## ✨ Features

### Core Functionality
- **Client Management**: Add, view, search, and filter legal clients
- **Database Operations**: SQLite database with automatic initialization
- **Data Export**: Export client data to CSV format
- **Professional UI**: Modern, responsive design with Hebrew support

### AI-Powered Features
- **Advanced Analysis**: Claude AI provides comprehensive client data analysis
- **Smart Virtual Assistant**: Q&A system for client database queries
- **Multiple Model Support**: Latest Sonnet, Haiku, and fallback models
- **Intelligent Caching**: 1-hour response caching for improved performance
- **Rate Limiting**: 50 requests per minute with automatic management

### Advanced Technical Features
- **Progressive Model Fallback**: Automatically tries different models when one is overloaded
- **Exponential Backoff**: Smart retry logic for API failures
- **Performance Monitoring**: Real-time cache and request statistics
- **Error Handling**: Comprehensive error management with user-friendly messages
- **Session State Management**: Persistent cache and request history

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Anthropic API key (Claude)

### Setup
1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run main.py
   ```

## 🎯 Usage

### Basic Operations
1. **View Clients**: Browse all clients in the "Client Management" tab
2. **Add Clients**: Use the "Add Client" tab to register new clients
3. **Search & Filter**: Use name search and age/legal area filters
4. **Export Data**: Download client data as CSV

### AI Features
1. **Advanced Analysis**: Click "Advanced Analysis" for comprehensive insights
2. **Virtual Assistant**: Ask questions about your client data
3. **Model Selection**: Choose between different Claude models in the sidebar
4. **Performance Monitoring**: Monitor cache usage and API requests

### Model Options
- **Latest Sonnet**: Recommended for balanced performance and quality
- **Haiku**: Fastest responses, good for simple queries
- **Opus 4.1**: Most powerful model with best quality (slower but highest accuracy)

## 🔧 Configuration

### Environment Variables
- `ANTHROPIC_API_KEY`: Your Claude API key (required)

### Advanced Settings (in main.py)
```python
CACHE_TTL = 3600  # Cache duration in seconds
MAX_CACHE_ENTRIES = 100  # Maximum cached responses
MAX_REQUESTS_PER_MINUTE = 50  # Rate limit
```

## 📊 Technical Architecture

### Database Schema
```sql
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    legal_issue TEXT NOT NULL
);
```

### Caching System
- MD5-based cache keys for unique request identification
- Automatic cache expiration and cleanup
- Real-time cache statistics

### Error Handling
- Progressive model fallback (Sonnet → Haiku → Fallback)
- Exponential backoff for retries
- Graceful degradation to basic analysis

## 🚀 Deployment Ready

### Checklist
✅ **Code Quality**: No linting errors  
✅ **Dependencies**: All requirements documented  
✅ **Error Handling**: Comprehensive error management  
✅ **Performance**: Caching and rate limiting implemented  
✅ **UI/UX**: Professional, responsive design  
✅ **Documentation**: Complete setup and usage instructions  
✅ **Testing**: Database and import functionality verified  
✅ **Security**: Environment variables for sensitive data  

### Production Considerations
- Ensure `.env` file is properly configured
- Monitor API usage to stay within rate limits
- Regular database backups recommended
- Consider scaling cache settings for high-traffic usage

## 🐛 Troubleshooting

### Common Issues
1. **API Key Error**: Ensure `ANTHROPIC_API_KEY` is set in `.env`
2. **Model Not Found**: Some models may not be available with your API tier
3. **Rate Limiting**: Wait a minute if you hit the rate limit
4. **Cache Issues**: Use "Clear Cache" button in sidebar if needed

### Error Messages
- **404 Model Error**: Model not available, will auto-fallback to Haiku
- **529 Overloaded**: Server busy, will retry with different model
- **Rate Limit**: Too many requests, automatic throttling applied

## 📝 License
This project is part of an AI development course and is for educational purposes.

## 🤝 Support
For issues or questions, refer to the error messages in the application or check the console output for detailed debugging information.
