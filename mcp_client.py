from fastmcp import Client

# Local server (STDIO)
client = Client("mcp_server.py")

# HTTP server
# client = Client("http://127.0.0.1:8000/mcp")

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
        result = await client.call_tool("add", {"a": 1, "b": 2})
        print("\n===============================Tool Result===============================\n")
        print(result.content[0].text)

        # Call resources
        result = await client.read_resource("resource://greeting")
        print("\n===============================Resource Result===============================\n")
        print(result[0].text)

        # Call prompts
        messages = await client.get_prompt("ask_about_topic", {"topic": "AI"})
        print("\n===============================Prompt Result===============================\n")
        print(messages.messages[0].content.text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(call_mcp())
    