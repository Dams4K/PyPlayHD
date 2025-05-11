import requests
import os


class Response:
    def __init__(self, response: dict):
        self.status: int            = response.get("status", -1)
        self.path: str              = response.get("path", "")
        self.timestamp: str         = response.get("timeStamp", -1)
        self.processing_time: int   = response.get("processingTime", -1)
        self.data: dict             = response.get("data", {})

    def __repr__(self):
        return f"<Response status={self.status} data={self.data}>"

class Requester:
    ROOT = "https://mcplayhd.net/api/v1/"

    def __init__(self, token):
        self.token = token

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept":"*/*"
        }

    @property
    def unauthorized_headers(self):
        return {
            "Accept": "*/*"
        }

    def get(self, endpoint: str, root: str = ROOT) -> Response:
        response = requests.get(
            os.path.join(root, endpoint),
            headers=self.headers,
        )

        return Response(response.json())

    def ask(self, endpoint: str, root: str = ROOT) -> Response:
        response = requests.get(
            os.path.join(root, endpoint),
            headers=self.unauthorized_headers
        )
        return Response(response.json())
