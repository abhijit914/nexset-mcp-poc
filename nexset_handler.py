import httpx
from openai import OpenAI

from constants import ADMIN_API_URL, NEXLA_USER_AGENT, OPENAI_API_KEY


class VectorDBNexsetHandler:
    def __init__(self, nexset_id: str, token: str, query: str):
        self.nexset_id = nexset_id
        self.token = token
        self.query = query
        self.sync_api_url = None
        self.vector_embeddings = None

    async def process(self):
        try:
            self.sync_api_url = await self._get_sync_api_url()
            self.vector_embeddings = await self._get_vector_embeddings()
            return await self._query_sync_api()
        except Exception as e:
            return {
                "error": "There was an error processing the Nexset, please verify that your Nexset is SyncAPI compatible.",
                "detail": str(e),
            }

    async def _get_sync_api_url(self):
        """
        Get the sync API URL for the given Nexset ID
        """
        try:
            url = ADMIN_API_URL + f"data_sets/{self.nexset_id}"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "User-Agent": f"{NEXLA_USER_AGENT}",
            }
            params = {"expand": 1}

            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, headers=headers, params=params)
                return response.json()["sync_api_config"]["url"]
        except Exception as e:
            return {
                "error": "There was an error getting the Sync API URL, please verify that your Nexset is SyncAPI compatible.",
                "detail": str(e),
            }

    async def _get_vector_embeddings(self) -> list[float]:
        """
        Get vector embeddings for the given user query.
        """
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.embeddings.create(
                input=self.query, model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            return {
                "error": "There was an error getting vector embeddings, please verify that your OpenAI API key is correct.",
                "detail": str(e),
            }

    async def _query_sync_api(self) -> list[dict]:
        """
        Query a vector database using the given query embedding to find the most relevant results.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=self.sync_api_url, json={"vector": self.vector_embeddings}
                )
                relevant_wine_reviews = response.json()
                return [review["metadata"] for review in relevant_wine_reviews[:3]]
        except Exception as e:
            return {
                "error": "There was an error querying the Sync API, please verify that Nexset is SyncAPI compatible.",
                "detail": str(e),
            }
