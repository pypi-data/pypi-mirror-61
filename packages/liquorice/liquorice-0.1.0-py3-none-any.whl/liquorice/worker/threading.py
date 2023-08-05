import asyncio
import logging
import threading
from typing import Any

from liquorice.core.database import db


class BaseThread(threading.Thread):
    def __init__(self, id_: Any = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id_ if id_ is not None else threading.get_ident()
        self.loop = asyncio.new_event_loop()
        self.processed_tasks = 0

        self._stop_event = threading.Event()
        self._logger = logging.getLogger(self.ident)

    def run(self) -> None:
        asyncio.set_event_loop(self.loop)

        self.loop.run_until_complete(self._setup())
        self.loop.run_until_complete(self._run())
        self.loop.run_until_complete(self._teardown())

    def stop(self) -> None:
        self._stop_event.set()

    @property
    def name(self) -> str:
        return f'{self.ident}.{self.id}'

    @property
    def ident(self) -> str:
        raise NotImplementedError

    async def _setup(self) -> None:
        pass

    async def _run(self) -> None:
        raise NotImplementedError

    async def _teardown(self) -> None:
        await db.close_for_current_loop()
