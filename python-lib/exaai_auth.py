import requests


class ExaAIAuth(requests.auth.AuthBase):
    def __init__(self, access_token=None):
        self.access_token = access_token

    def __call__(self, request):
        request.headers["x-api-key"] = "{}".format(
            self.access_token
        )
        return request
