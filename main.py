import httpx
from mcp.server.fastmcp import FastMCP

from constants import ADMIN_API_URL, NEXLA_SERVICE_KEY, NEXLA_USER_AGENT, NEXSET_ID
from nexset_handler import VectorDBNexsetHandler

mcp = FastMCP("nexset-mcp-poc")


async def get_nexla_token() -> str:
    """
    Get the Nexla token for the given service key.
    """
    try:
        url = ADMIN_API_URL + "token"
        headers = {
            "Authorization": f"Basic {NEXLA_SERVICE_KEY}",
            "User-Agent": f"{NEXLA_USER_AGENT}",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url=url, headers=headers)
            return response.json()["access_token"]
    except Exception as e:
        return {
            "error": "There was an error getting the Nexla token, please verify that your service key is correct.",
            "detail": str(e),
        }


@mcp.tool()
async def get_relevant_wine_reviews(query: str) -> list[dict]:
    """
    Find the most relevant wines from the wine reviews dataset for a given natural language query. Discuss the flavor profile in detail and mention any notes. Discuss the wine's points rating and price when available.

    Args:
        query: A natural language query to find relevant wines from the wine reviews dataset.

    Returns:
        A list of dictionaries, each representing a wine review.
    """
    try:
        nexla_token = await get_nexla_token()
        vector_db_handler = VectorDBNexsetHandler(NEXSET_ID, nexla_token, query)
        relevant_wine_reviews = await vector_db_handler.process()
        return relevant_wine_reviews
    except Exception as e:
        return {
            "error": "There was an error querying your vector database source, please verify that your configuration is valid.",
            "detail": str(e),
        }


if __name__ == "__main__":
    mcp.run(transport="stdio")
