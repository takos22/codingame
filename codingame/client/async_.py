from .base import BaseClient


class AsyncClient(BaseClient):
    def __init__(self):
        super().__init__(is_async=True)
