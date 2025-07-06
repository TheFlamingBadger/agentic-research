import sys
import os
import json
from typing import Dict, List, Any

# Add the src directory to the Python path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp.server.fastmcp import FastMCP
from research_agent.mongodb.mongo_client import get_db

# Create a server instance
mcp = FastMCP(name="MyAssistantServer")

# Get the MongoDB database
db = get_db()

# Helper functions
def oid_to_str(doc: dict[str, Any]) -> dict[str, Any]:
    """Converts MongoDB ObjectId to string in a document.

    Args:
        doc (dict[str, Any]): A document from MongoDB.

    Returns:
        dict[str, Any]: The document with ObjectId fields converted to strings.
    """
    doc["_id"] = str(doc["_id"])
    return doc

# Tools
@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}"

@mcp.tool()
async def list_collections() -> Dict[str, List[str]]:
    """List all collections in the MongoDB database as JSON."""
    try:
        return {"collections": db.list_collection_names()}
    except Exception as e:
        # still returns a JSON object with an error message
        return { "collections": [], "error": str(e) }

@mcp.tool()
async def get_one_param(var: str) -> Dict[str, Any]:
    """Get one parameter from the MongoDB database."""
    try:
        collection = db[var]
        doc = collection.find_one()
        if doc:
            return {"doc": oid_to_str(doc)}
        else:
            return {"error": "No document found"}
    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    mcp.run()
    