from exaai_auth import ExaAIAuth
from exaai_pagination import ExaAIPagination
from api_client import APIClient


class ExaAIClient():
    def __init__(self, access_token=None):
        server_url = "https://api.exa.ai"
        pagination = ExaAIPagination()
        self.client = APIClient(
            server_url=server_url,
            auth=ExaAIAuth(access_token=access_token),
            pagination=pagination,
            max_number_of_retries=1
        )

    def get_next_item(self, endpoint):
        for page in self.get_next_page(endpoint):
            for item in page.get("results", []):
                yield item

    def get_next_page(self, endpoint):
        response = self.get(endpoint)
        return response

    def get(self, endpoint, url=None, raw=False):
        response = self.client.get(endpoint, url=url, raw=raw)
        return response

    def post(self, endpoint, url=None, raw=False, params=None, data=None, json=None, headers=None):
        response = self.client.post(endpoint, url=url, raw=raw, params=params, data=data, json=json, headers=headers)
        return response

    def patch(self, endpoint, url=None, raw=False, params=None, data=None, json=None, headers=None):
        response = self.client.patch(endpoint, url=url, raw=raw, params=params, data=data, json=json, headers=headers)
        return response
