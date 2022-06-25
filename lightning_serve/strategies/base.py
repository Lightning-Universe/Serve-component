import abc
from typing import Any

import numpy as np
from fastapi import Request
import requests
from lightning import LightningWork
from lightning.app.structures import List
from requests import Response
from lightning_serve.utils import _configure_session

class Strategy(abc.ABC):

    def select_url(self, request, local_router_metadata):
        method = request.method.lower()
        keys = list(local_router_metadata)
        if len(keys) > 1:
            selected_url = np.random.choice(
                keys, p=list(local_router_metadata.values())
            )
        else:
            selected_url = keys[0]
        return selected_url, method

    def make_request(
        self, request: Request, full_path: str, local_router_metadata: Any
    ) -> Response:
        self._session = _configure_session()

        # async with httpx.AsyncClient() as client:
        #     selected_url, method = await self.select_url(request, local_router_metadata)
        #     return await getattr(client, method)(selected_url + "/" + full_path)
        selected_url, method = self.select_url(request, local_router_metadata)
        return getattr(self._session, method)(selected_url + "/" + full_path)

    @abc.abstractmethod
    def run(self, serve_works: List[LightningWork]) -> Any:
        pass

    def on_after_run(self, serve_works: List[LightningWork], res):
        pass
