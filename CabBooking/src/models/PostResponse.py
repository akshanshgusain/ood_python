from __future__ import annotations  # postpone evaluation of annotations '


class PostResponse:
    OK_RESPONSE: str = "ok"
    ERROR_RESPONSE: str = "error"

    def __init__(self, status: str, message: str):
        self.status: str = status
        self.message: str = message

    @classmethod
    def ok(cls) -> PostResponse:
        return PostResponse(cls.OK_RESPONSE, "")

    @classmethod
    def error(cls) -> PostResponse:
        return PostResponse(cls.ERROR_RESPONSE, "")
