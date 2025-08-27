from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult
from fastmcp.client.logging import LogMessage
from fastmcp.client.sampling import (
    SamplingMessage,
    SamplingParams,
    RequestContext,
)


# Local server (STDIO)
# client = Client("advanced_mcp_features_server.py")

# HTTP server
# client = Client("http://127.0.0.1:8000/mcp")

# JSON config (multiple servers)
# Tools are namespaced by server name eg: server_name_tool_name [my_server_add]
# Resources are namespaced by server name eg: resource://server_name/resource_name [resource://my_server/greeting]
config = {
    "mcpServers": {
        "my_advanced_server": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "http"
        },
        "my_server": {
            "command": "python",
            "args": ["./mcp_server.py"],
            "env": {"LOG_LEVEL": "INFO"}
        }
    }
}


async def elicitation_handler(message: str, response_type: type, params, context):
    # Present the message to the user and collect input
    print(message)
    name = input("Enter name: ")
    age = input("Enter age: ")

    if name == "" or age == "":
        return ElicitResult(action="decline")
    
    # Create response using the provided dataclass type
    # FastMCP converted the JSON schema to this Python type for you
    response_data = response_type(name=name, age=age)
    
    # You can return data directly - FastMCP will implicitly accept the elicitation
    return response_data
    
    # Or explicitly return an ElicitResult for more control
    # return ElicitResult(action="accept", content=response_data)


async def log_handler(message: LogMessage):
    """
    Handles incoming logs from the MCP server and forwards them
    to the standard Python logging system.
    """
    msg = message.data.get('msg')
    extra = message.data.get('extra')
    level = message.level

    print("======Log Data from handler======")
    print(msg)
    print(extra)
    print(level)
    print("=================================")

    # Convert the MCP log level to a Python log level
    # level = LOGGING_LEVEL_MAP.get(message.level.upper(), logging.INFO)

    # Log the message using the standard logging library
    # logger.log(level, msg, extra=extra)

async def progress_handler(
    progress: float, 
    total: float | None, 
    message: str | None
) -> None:
    if total is not None:
        percentage = (progress / total) * 100
        print(f"Progress: {percentage:.1f}% - {message or ''}")
    else:
        print(f"Progress: {progress} - {message or ''}")

async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext
) -> str:
    print("======Sampling Data from handler======")
    print(messages[0].content.text)
    print("=================================")
    # Your LLM integration logic here
    # Extract text from messages and generate a response
    return "neutral"

client = Client(
    config,
    elicitation_handler=elicitation_handler,
    log_handler=log_handler,
    progress_handler=progress_handler,
    sampling_handler=sampling_handler
    )

async def call_mcp():
    async with client:
        # Basic server interaction
        await client.ping()
        
        # List available operations
        tools = await client.list_tools()
        resources = await client.list_resources()
        resource_templates= await client.list_resource_templates()
        prompts = await client.list_prompts()
        
        print("\n===============================Tools===============================\n")
        print("\n".join([tool.name for tool in tools]))
        print("\n===============================Resources===============================\n")
        print("\n".join([resource.name for resource in resources]))
        print("\n===============================Resource Templates===============================\n")
        print("\n".join([resource_template.name for resource_template in resource_templates]))
        print("\n===============================Prompts===============================\n")
        print("\n".join([prompt.name for prompt in prompts]))

        # Call tools
        result = await client.call_tool("my_server_add", {"a": 1, "b": 2})
        print("\n===============================Tool Result===============================\n")
        print(result.content[0].text)

        # Call resources
        result = await client.read_resource("resource://my_server/greeting")
        print("\n===============================Resource Result===============================\n")
        print(result[0].text)

        # Call prompts
        messages = await client.get_prompt("my_server_ask_about_topic", {"topic": "AI"})
        print("\n===============================Prompt Result===============================\n")
        print(messages.messages[0].content.text)

        # Call advanced server tools with context
        result = await client.call_tool("my_advanced_server_process_file", {"file_uri": "file://test.txt"})
        print("\n===============================Advanced Server Tool with context Result===============================\n")
        print(result.content[0].text)

        # Call advanced server tools with elicitation
        print("\n===============================Advanced Server Tool with elicitation Result===============================\n")
        result = await client.call_tool("my_advanced_server_collect_user_info")
        print(result.content[0].text)

        # Call advanced server tools with logging
        print("\n===============================Advanced Server Tool with logging Result===============================\n")
        result = await client.call_tool("my_advanced_server_analyze_dataset", {"dataset_name": "test.txt"})
        print(result.content[0].text)

        # Call advanced server tools with progress reporting
        print("\n===============================Advanced Server Tool with progress reporting Result===============================\n")
        result = await client.call_tool("my_advanced_server_process_items", {"items": ["item1", "item2", "item3"]})
        print(result.content[0].text)

        #Call advanced server tools with LLM sampling
        print("\n===============================Advanced Server Tool with LLM sampling Result===============================\n")
        result = await client.call_tool("my_advanced_server_analyze_sentiment", {"text": "AI is the future of technology"})
        print(result.content[0].text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(call_mcp())
    