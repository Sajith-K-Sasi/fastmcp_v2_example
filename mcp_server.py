from fastmcp import FastMCP
from fastmcp.prompts.prompt import PromptMessage, TextContent

# Create a basic server instance
mcp = FastMCP(name="MyMCPServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.resource("resource://greeting")
def get_greeting() -> str:
    """Provides a simple greeting message."""
    return "Hello from FastMCP Resources!"

@mcp.resource("data://{name}/greeting")
def get_greeting_by_name(name: str) -> str:
    """Provides a greeting message for a specific name."""
    return f"Hello {name} from FastMCP Resources!"

# Basic prompt returning a string (converted to user message automatically)
@mcp.prompt
def ask_about_topic(topic: str) -> str:
    """Generates a user message asking for an explanation of a topic."""
    return f"Can you please explain the concept of '{topic}'?"

# Prompt returning a specific message type
@mcp.prompt
def generate_code_request(language: str, task_description: str) -> PromptMessage:
    """Generates a user message requesting code generation."""
    content = f"Write a {language} function that performs the following task: {task_description}"
    return PromptMessage(role="user", content=TextContent(type="text", text=content))


if __name__ == "__main__":
    # Start server with STDIO
    mcp.run()
    # Start server with HTTP on port 8000
    # mcp.run(transport="http", host="127.0.0.1", port=8000)
    

