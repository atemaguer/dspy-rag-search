from typing import Any, Optional, Callable


class Router:
    """A router responsible for determining the appropriate pipeline to run for each incoming query.
    It determines type of query(e.g Tip-of-Tongue, Retrive-Read, etc) and calls the registered endpoint to handle it.
    """

    def __init__(self, lm: any, template: str) -> None:
        self.handlers = {}
        self.demos = {}
        self.lm = lm
        self.router_prompt_template = template

    def add_route(
        self, path: str, handler: Callable[[str], str], demos: list[str] = None
    ) -> None:
        self.handlers[path] = handler

        if demos:
            self.demos[path] = demos

    def _prepare_query(self, query):
        return self.router_prompt_template + f"\nsentence: {query}\nlabel:"

    def __call__(self, query):
        output = self.lm(self._prepare_query(query))

        return output
