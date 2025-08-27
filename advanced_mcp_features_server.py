from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_context
from dataclasses import dataclass
import asyncio

# Create a basic server instance
mcp = FastMCP(name="MyAdvancedMCPServer")


#-----------------------Context-------------------------------
@mcp.tool
async def process_file(file_uri: str, ctx: Context) -> str:
    """Processes a file, using context for logging and resource access."""
    # Context is available as the ctx parameter
    return "Processed file"

# Utility function that needs context but doesn't receive it as a parameter
async def process_data(data: list[float]) -> dict:
    # Get the active context - only works when called within a request
    ctx = get_context()    
    await ctx.info(f"Processing {len(data)} data points")
    
@mcp.tool
async def analyze_dataset(dataset_name: str) -> dict:
    # Call utility function that uses context internally

    # load data from file
    # data = load_data(dataset_name)
    
    data = [1,2,3,4,5,6,7,8,9,10]
    await process_data(data)

    return {"processed": len(data), "results": data}

#-----------------------Elicitation---------------------------
@dataclass
class UserInfo:
    name: str
    age: int

@mcp.tool
async def collect_user_info(ctx: Context) -> str:
    """Collect user information through interactive prompts."""
    result = await ctx.elicit(
        message="Please provide your information",
        response_type=UserInfo
    )
    
    if result.action == "accept":
        user = result.data
        return f"Hello {user.name}, you are {user.age} years old"
    elif result.action == "decline":
        return "Information not provided"
    else:  # cancel
        return "Operation cancelled"

#----------------------Progress Reporting-------------------------------
@mcp.tool
async def process_items(items: list[str], ctx: Context) -> dict:
    """Process a list of items with progress updates."""
    total = len(items)
    results = []
    
    for i, item in enumerate(items):
        # Report progress as we process each item [total is optional]
        await ctx.report_progress(progress=i, total=total)
        
        # Simulate processing time
        await asyncio.sleep(1)
        results.append(item.upper())
    
    # Report 100% completion
    await ctx.report_progress(progress=total, total=total)
    
    return {"processed": len(results), "results": results}

#----------------------LLM Sampling---------------------------

@mcp.tool
async def analyze_sentiment(text: str, ctx: Context) -> dict:
    """Analyze the sentiment of text using the client's LLM."""
    prompt = f"""Analyze the sentiment of the following text as positive, negative, or neutral. 
    Just output a single word - 'positive', 'negative', or 'neutral'.
    
    Text to analyze: {text}"""
    
    # Request LLM analysis
    response = await ctx.sample(prompt)

    # from fastmcp.client.sampling import SamplingMessage
    # messages = [
    #     SamplingMessage(role="user", content=f"I have this data: {context_data}"),
    #     SamplingMessage(role="assistant", content="I can see your data. What would you like me to analyze?"),
    #     SamplingMessage(role="user", content=user_query)
    # ]

    #response = await ctx.sample(
    #     messages=messages,
    #     system_prompt="You are an expert Python programmer. Provide concise, working code examples without explanations.",
    #     model_preferences="claude-3-sonnet",  # Prefer a specific model   
    #     include_context="thisServer",  # Use the server's context 
    #     temperature=0.7,
    #     max_tokens=300
    # )
    
    # Process the LLM's response
    sentiment = response.text.strip().lower()
    
    # Map to standard sentiment values
    if "positive" in sentiment:
        sentiment = "positive"
    elif "negative" in sentiment:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {"text": text, "sentiment": sentiment}


if __name__ == "__main__":
    # Start server with HTTP on port 8000
    mcp.run(transport="http", host="127.0.0.1", port=8000)