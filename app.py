import asyncio
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import sys

class MCPChatbot:
    def __init__(self):
        self.agent = None
        self.llm = None
        self.client = None
        self.working_servers = {}
        
    async def initialize(self):
        """Initialize the MCP chatbot"""
        load_dotenv()
        
        print("🤖 Initializing MCP Chatbot...")
        print("=" * 50)
        
        try:
            # Load configuration
            with open('browser_mcp.json', 'r') as f:
                config = json.load(f)
            
            # Test servers
            await self._test_servers(config)
            
            if not self.working_servers:
                print("❌ No MCP servers are working. Chatbot will run in limited mode.")
                return False
            
            # Create MCP client and agent
            await self._create_agent()
            return True
            
        except FileNotFoundError:
            print("❌ browser_mcp.json not found. Please ensure it exists.")
            return False
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    async def _test_servers(self, config):
        """Test each MCP server individually"""
        print("Testing MCP servers...")
        
        for server_name, server_config in config["mcpServers"].items():
            try:
                from mcp_use import MCPClient, MCPAgent
                
                test_config = {"mcpServers": {server_name: server_config}}
                client = MCPClient.from_dict(test_config)
                
                # Test with basic LLM
                llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)
                agent = MCPAgent(llm=llm, client=client, max_steps=3)
                
                await agent.run("What tools are available?")
                print(f"✅ {server_name} server: Working")
                self.working_servers[server_name] = server_config
                
            except Exception as e:
                print(f"❌ {server_name} server: Failed ({str(e)[:50]}...)")
    
    async def _create_agent(self):
        """Create the MCP agent with working servers"""
        from mcp_use import MCPClient, MCPAgent
        
        final_config = {"mcpServers": self.working_servers}
        self.client = MCPClient.from_dict(final_config)
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.3
        )
        
        self.agent = MCPAgent(llm=self.llm, client=self.client, max_steps=20)
        print(f"✅ Agent created with servers: {list(self.working_servers.keys())}")
    
    async def get_available_tools(self):
        """Get list of available tools"""
        if not self.agent:
            return "No MCP agent available. Running in limited mode."
        
        try:
            result = await self.agent.run("List all available tools briefly.")
            return result
        except Exception as e:
            return f"Error getting tools: {e}"
    
    async def process_message(self, user_input):
        """Process user message and return response"""
        if not self.agent:
            return self._handle_no_agent_response(user_input)
        
        try:
            # Add context about available capabilities
            enhanced_input = f"""
            You have access to powerful MCP tools including browser automation, search capabilities, and more.
            
            User query: {user_input}
            
            Please use the appropriate tools to help answer this query. If it involves web browsing, 
            use your browser automation tools. If it needs search, use search tools. Be helpful and thorough.
            """
            
            result = await self.agent.run(enhanced_input)
            return result
            
        except Exception as e:
            return f"Error processing message: {e}"
    
    def _handle_no_agent_response(self, user_input):
        """Handle responses when no MCP agent is available"""
        # Basic responses for common queries
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['help', 'what can you do', 'capabilities']):
            return """
            I'm an MCP Chatbot, but currently running in limited mode because no MCP servers are available.
            
            Normally, I would have access to:
            - Browser automation (navigate, click, take screenshots)
            - Web search capabilities  
            - Airbnb search functionality
            
            Please check your MCP server installations and try again.
            """
        
        elif any(word in user_lower for word in ['restaurant', 'food', 'eat']):
            return "I'd normally help you find restaurants using web browsing tools, but MCP servers aren't available right now."
        
        else:
            return "I'm running in limited mode. Please check your MCP server setup to unlock full capabilities."
    
    def print_welcome(self):
        """Print welcome message"""
        print("\n" + "🤖" * 20)
        print("     MCP CHATBOT - READY TO HELP!")
        print("🤖" * 20)
        print(f"Active servers: {list(self.working_servers.keys()) if self.working_servers else 'None'}")
        print("\nType 'help' for available commands")
        print("Type 'tools' to see available tools")
        print("Type 'quit' or 'exit' to end the conversation")
        print("-" * 50)
    
    def print_help(self):
        """Print help information"""
        print("\n📖 HELP - Available Commands:")
        print("-" * 30)
        print("help     - Show this help message")
        print("tools    - List available MCP tools")
        print("quit     - Exit the chatbot")
        print("exit     - Exit the chatbot")
        print("\n💡 Example queries:")
        print("- 'Find the best restaurants in San Francisco'")
        print("- 'Search for hotels in New York'")
        print("- 'Take a screenshot of google.com'")
        print("- 'What's the weather like today?'")
        print("-" * 30)

async def main():
    """Main chatbot loop"""
    chatbot = MCPChatbot()
    
    # Initialize
    success = await chatbot.initialize()
    chatbot.print_welcome()
    
    if not success:
        print("\n⚠️  Running in limited mode - some features may not work.")
    
    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = input("\n🗣️  You: ").strip()
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Thanks for chatting!")
                break
            
            elif user_input.lower() == 'help':
                chatbot.print_help()
                continue
            
            elif user_input.lower() == 'tools':
                print("\n🔧 Getting available tools...")
                tools = await chatbot.get_available_tools()
                print(f"Available tools:\n{tools}")
                continue
            
            elif not user_input:
                print("Please enter a message or type 'help' for commands.")
                continue
            
            # Process the message
            print("\n🤖 Bot: Thinking...")
            response = await chatbot.process_message(user_input)
            print(f"\n🤖 Bot: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! (Ctrl+C pressed)")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'help' for commands.")

if __name__ == "__main__":
    print("🚀 Starting MCP Chatbot...")
    
    # Check if required files exist
    if not os.path.exists('browser_mcp.json'):
        print("❌ browser_mcp.json not found!")
        print("Please ensure the configuration file exists.")
        sys.exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Chatbot stopped.")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)