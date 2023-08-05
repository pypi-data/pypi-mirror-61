import collections
import typing
from typing import Deque, Dict, Iterator, Optional, Set, Tuple, List

from ..utils.impl import set

if typing.TYPE_CHECKING:
    from ..term import Term, TermSet
    from ..relationship import Relationship
    from ..ontology import Ontology


class SubclassesIterator(Iterator["Term"]):
    """An iterator over the subclasses of a `~pronto.Term`.
    """

    @classmethod
    def _build_cache(cls, ont: "Ontology") -> Dict[str, Set[str]]:
        is_a: Relationship = ont.get_relationship("is_a")
        graph: Dict[str, Set[str]] = dict()
        empty: List[Term] = list()
        for t in ont.terms():
            for t2 in t.relationships.get(is_a, []):
                graph.setdefault(t2.id, set()).add(t.id)
        return graph

    def __init__(
        self, term: "Term", distance: Optional[int] = None, with_self: bool = True
    ) -> None:
        self._distmax: float = float("inf") if distance is None else distance
        self._ontology = ont = term._ontology
        self._graph = graph = ont()._subclassing_cache
        if graph is None:
            self._graph = ont()._subclassing_cache = self._build_cache(ont())

        self._maxlen = len(ont().terms())

        self._sub: Set[str] = set()
        self._done: Set[str] = set()
        self._frontier: Deque[Tuple[str, int]] = collections.deque()
        self._queue: Deque[str] = collections.deque()

        self._frontier.append((term.id, 0))
        self._sub.add(term.id)
        if with_self:
            self._queue.append(term.id)

    def __iter__(self) -> "SubclassesIterator":
        return self

    def __next__(self) -> "Term":
        while self._frontier or self._queue:
            # Return any element currently queued
            if self._queue:
                return self._ontology().get_term(self._queue.popleft())
            # Get the next node in the frontier
            node, distance = self._frontier.popleft()
            self._done.add(node)
            # Process its neighbors if they are not too far
            neighbors: Set[str] = self._graph.get(node)
            if neighbors and distance < self._distmax:
                for node in sorted(neighbors - self._done):
                    self._frontier.append((node, distance + 1))
                for neighbor in sorted(neighbors - self._sub):
                    self._sub.add(neighbor)
                    self._queue.append(neighbor)
        # Stop iteration if no more elements to process
        raise StopIteration

    def __length_hint__(self) -> int:
        """Get an estimate of the number of remaining terms in the iterator.

        **This method never underestimates*.
        """
        if self._queue or self._frontier:
            return self._maxlen - len(self._sub)
        else:
            return 0

    def to_set(self) -> "TermSet":
        """Collect all subclasses into a `~pronto.TermSet`.

        Hint:
            This method is useful to query an ontology using a method chaining
            syntax, for instance::

            >>> cio = pronto.Ontology("cio.obo")
            >>> sorted(cio['CIO:0000034'].subclasses().to_set().ids)
            ['CIO:0000034', 'CIO:0000035', 'CIO:0000036']
        """
        from ..term import TermSet

        return TermSet(self)
