import sys
import os
import json
from typing import Dict, List, Any

# Add the src directory to the Python path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


from urllib.parse import unquote_plus
from mcp.server.fastmcp import FastMCP, Context
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
async def get_param(var: str, num: int = 10) -> Dict[str, Any]:
    """Get one parameter from the MongoDB mflix database."""
    try:
        collection = db[var]
        cursor = collection.find().limit(num)
        results = []
        for doc in cursor:
            doc = oid_to_str(doc)
            results.append(doc)
        return {"results": results}

    except Exception as e:
        return {"error": str(e)}
    
@mcp.tool()
async def list_genres() -> Dict[str,List[str]]:
    """List all genres in the movies collection.

    Returns:
        List[str]: genres sorted alphabetically.
    """
    movies = db["movies"]
    genres = movies.distinct("genres")
    return {"Genres":sorted(genres)}

@mcp.tool()
async def get_movies_by_genre(genre: str, num: int = 10) -> List[Dict[str, Any]]:
    """Get movies by genre.

    Args:
        genre (str): genre to filter movies by.
        num (int, optional): Number of movies to show. Defaults to 10.

    Returns:
        List[Dict[str, Any]]: List of movie documents with the specified genre, limited to num results.
    """
    try:
        movies = db["movies"]
        cursor = movies.find({"genres": genre}).limit(num)
        
        results = []
        for doc in cursor:
            doc = oid_to_str(doc)
            results.append(doc)
        return results
        
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_theatre_states() -> Dict[str,List[str]]:
    """Get all unique theatre states from the theatres collection.

    Returns:
        List[str]: List of unique theatre cities.
    """
    cursor = db.theaters.find(
        {},
        {"_id": 0, "location.address": 1, "location.geo.coordinates": 1}
    )
    locations = []
    for doc in cursor:
        loc = doc.get("location", {})
        address = loc.get("address", {})
        city = address.get("state")
        if city and city not in locations:
            locations.append(city)
    return {"Locations":locations}
            
@mcp.tool()
async def get_theatres_by_state(state: str) -> List[Dict[str, Any]]:
    """Get theatres by state.

    Args:
        state (str): State to filter theatres by.

    Returns:
        List[Dict[str, Any]]: List of theatre documents in the specified state.
    """
    try:
        theatres = db["theaters"]
        cursor = theatres.find({"location.address.state": state})
        
        results = []
        for doc in cursor:
            doc = oid_to_str(doc)
            results.append(doc)
        return results
        
    except Exception as e:
        return {"error": str(e)}
    

@mcp.resource("mongo://collections", name="ListCollections")
def list_collections() -> list[str]:
    """Returns all collection names in the mflix database."""
    db = get_db()
    return sorted(db.list_collection_names())

@mcp.resource("mongo://{collection}/distinct/{field}", name="DistinctValues")
def distinct_values(collection: str, field: str) -> list:
    """
    Returns the sorted list of distinct values for `field` in `collection`.
    Example URI: mongo://movies/distinct/genres
    """    
    values = db[collection].distinct(field)
    
    # drop nulls and sort if possible
    cleaned = [v for v in values if v is not None]
    try:
        return sorted(cleaned)
    except TypeError:
        return cleaned
    
# @mcp.resource(
#     "mongo://{collection}/query/{filter}/{projection}/{limit}",
#     name="QueryCollection",
#     description=(
#         "Run a MongoDB query against `<collection>`.\n"
#         "  • `filter` and `projection` are URL-encoded JSON strings.\n"
#         "  • `limit` is the maximum number of docs to return.\n"
#         "\n"
#         "Example:\n"
#         "  mongo://movies/query/%7B%22year%22%3A%7B%22%24gte%22%3A2000%7D%7D"
#         "/%7B%22title%22%3A1%2C%22_year%22%3A1%7D/5"
#     )
# )
# async def query_collection(
#     collection: str,
#     filter: str,
#     projection: str,
#     limit: str,
#     ctx: Context
# ) -> dict:
#     """
#     :param collection: name of the MongoDB collection
#     :param filter:     URL-encoded JSON filter (e.g. {"year":{"$gte":2000}})
#     :param projection: URL-encoded JSON projection (e.g. {"title":1,"_id":0})
#     :param limit:      URL segment indicating how many docs to return
#     """
#     db = get_db()

#     # Decode JSON from the URI segments
#     filter_doc     = json.loads(unquote_plus(filter))
#     proj_doc       = json.loads(unquote_plus(projection))
#     limit_int      = int(limit)

#     cursor = db[collection]\
#         .find(filter_doc, proj_doc)\
#         .limit(limit_int)

#     results = [oid_to_str(doc) for doc in await cursor.to_list(length=limit_int)]
#     return {collection: results}

if __name__ == "__main__":
    mcp.run()
    