# MCP Chatbot 🤖

**MCP Chatbot - Intelligent automation through Model Context Protocol integration. Features browser automation, web search, and travel planning with robust error handling. Uses Google Gemini LLM and gracefully handles server failures for reliable operation.**

GitHub Repository: https://github.com/naakaarafr/MCP-Chatbot

A powerful chatbot built with Model Context Protocol (MCP) that provides intelligent automation through browser control, web search, and travel planning capabilities.

## Overview

This chatbot leverages the Model Context Protocol to integrate multiple specialized servers, creating a unified interface for web automation, search, and travel-related tasks. It uses Google's Gemini model as the underlying LLM and can gracefully handle server failures by testing each MCP server individually.

## Features

### 🌐 Browser Automation (Playwright MCP)
- Navigate to websites
- Take screenshots
- Click elements and interact with web pages
- Automate web-based tasks

### 🔍 Web Search (DuckDuckGo MCP)
- Perform web searches
- Get real-time information
- Research topics and find answers

### 🏠 Travel Planning (Airbnb MCP)
- Search for accommodations
- Find hotels and rentals
- Get travel recommendations

### 🛡️ Robust Error Handling
- Individual server testing on startup
- Graceful degradation when servers fail
- Fallback responses in limited mode
- Clear error reporting

## Prerequisites

### System Requirements
- Python 3.8+
- Node.js and npm (for MCP servers)
- UV package manager (for Python MCP servers)

### Required Packages
```bash
# Python dependencies
pip install asyncio python-dotenv langchain-google-genai mcp-use

# Node.js MCP servers
npm install -g @playwright/mcp
npm install -g @openbnb/mcp-server-airbnb

# Python MCP servers
uvx install duckduckgo-mcp-server
```

## Installation

1. **Clone or download the project files:**
   ```bash
   # Ensure you have both app.py and browser_mcp.json
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or install individually:
   ```bash
   pip install asyncio python-dotenv langchain-google-genai mcp-use
   ```

3. **Install MCP servers:**
   ```bash
   # Playwright for browser automation
   npm install -g @playwright/mcp
   
   # Airbnb for travel search
   npm install -g @openbnb/mcp-server-airbnb
   
   # DuckDuckGo for web search
   uvx install duckduckgo-mcp-server
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Configure MCP servers:**
   The `browser_mcp.json` file is already configured with default settings. Modify if needed:
   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest"]
       },
       "airbnb": {
         "command": "npx",
         "args": ["-y", "@openbnb/mcp-server-airbnb"]
       },
       "ddg-search": {
         "command": "uvx",
         "args": ["duckduckgo-mcp-server"]
       }
     }
   }
   ```

## Usage

### Starting the Chatbot
```bash
python app.py
```

### Available Commands
- `help` - Show available commands and example queries
- `tools` - List all available MCP tools
- `quit` or `exit` - End the conversation

### Example Queries

#### Browser Automation
```
"Take a screenshot of google.com"
"Navigate to wikipedia.org and search for Python"
"Click the login button on the website"
```

#### Web Search
```
"What's the weather like today?"
"Search for the latest news about AI"
"Find information about renewable energy"
```

#### Travel Planning
```
"Find hotels in New York City"
"Search for Airbnb rentals in San Francisco"
"What are the best accommodations in Tokyo?"
```

#### General Assistance
```
"Find the best restaurants in downtown Chicago"
"Help me research Python programming tutorials"
"Take a screenshot of the current stock market trends"
```

## Architecture

### Core Components

1. **MCPChatbot Class**: Main chatbot orchestrator
   - Initializes and manages MCP servers
   - Handles user interactions
   - Provides fallback responses

2. **Server Testing**: Individual server validation
   - Tests each MCP server on startup
   - Reports working and failed servers
   - Continues operation with available servers

3. **Agent Integration**: LangChain + MCP integration
   - Uses Google Gemini 2.0 Flash as the LLM
   - Integrates with MCP client for tool access
   - Supports up to 20 reasoning steps

### Error Handling

The chatbot implements robust error handling:
- **Server Failures**: Individual server testing prevents total failure
- **Limited Mode**: Provides basic responses when no servers are available
- **Graceful Degradation**: Continues operation with partial functionality
- **User Feedback**: Clear error messages and status reporting

## Configuration

### MCP Server Configuration
Edit `browser_mcp.json` to add or modify MCP servers:

```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "command-to-run",
      "args": ["arg1", "arg2"]
    }
  }
}
```

### Environment Variables
Required in `.env` file:
- `GOOGLE_API_KEY`: Your Google AI API key for Gemini access

### LLM Configuration
Modify in `app.py` if needed:
```python
self.llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",  # Model selection
    temperature=0.3                # Creativity level
)
```

## Troubleshooting

### Common Issues

1. **"browser_mcp.json not found"**
   - Ensure the configuration file is in the same directory as `app.py`

2. **"No MCP servers are working"**
   - Check that all MCP servers are properly installed
   - Verify Node.js and UV are installed and accessible
   - Check server logs for specific error messages

3. **Google API Key Issues**
   - Ensure your `.env` file contains a valid `GOOGLE_API_KEY`
   - Verify the API key has access to Gemini models

4. **Installation Issues**
   - Make sure Node.js and npm are installed
   - Install UV package manager: `pip install uv`
   - Try installing MCP servers individually to isolate issues

### Debug Mode
The chatbot provides detailed startup information:
- Server testing results
- Working server list
- Error messages for failed servers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with various MCP servers
5. Submit a pull request

## License

This project is open source. Please check individual MCP server licenses for their respective terms.

## Support

For issues related to:
- **MCP Protocol**: Check the official MCP documentation
- **Specific MCP Servers**: Refer to individual server documentation
- **LangChain Integration**: See LangChain documentation
- **Google Gemini**: Check Google AI documentation

## Acknowledgments

- Model Context Protocol (MCP) team for the innovative protocol
- Playwright team for browser automation capabilities
- LangChain team for the integration framework
- Google for providing Gemini AI models
