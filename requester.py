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
        return f"<{self.__class__.__name__} status={self.status} data={self.data}>"

    @staticmethod
    def create_from(data: dict):
        status = data.get("status", -1)
        if 200 <= status < 300:
            return ResponseSuccess(data)
        return ResponseFailed(data)

class ResponseFailed(Response):
    @property
    def message(self):
        return self.data.get("message", "")

    def __repr__(self):
        return f"<{self.__class__.__name__} status={self.status} message={self.message}>"

class ResponseSuccess(Response):
    pass

class Requester:
    ROOT = "https://mcplayhd.net/api/v1/"

    def __init__(self, token):
        self.token = token

    @property
    def authorized_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept":"*/*"
        }

    @property
    def unauthorized_headers(self):
        return {
            "Accept": "*/*"
        }

    def _get(self, endpoint: str, headers: dict, root: str = ROOT, **kwargs) -> Response:
        response = requests.get(
            os.path.join(root, endpoint).format(**kwargs),
            headers=headers,
        )

        return Response.create_from(response.json())

    def consume(self, endpoint: str, root: str = ROOT, **kwargs) -> Response:
        return self._get(endpoint, self.authorized_headers, root, **kwargs)

    def ask(self, endpoint: str, root: str = ROOT, **kwargs) -> Response:
        return self._get(endpoint, self.unauthorized_headers, root, **kwargs)

    def api_info(self, root: str = ROOT) -> Response:
        return self.consume("", root)
