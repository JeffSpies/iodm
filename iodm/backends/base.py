import abc

from iodm import exceptions
from iodm.backends.util import QueryCommand


class ReadOnlyBackend(abc.ABC):

    @abc.abstractmethod
    def get(self, key):
        raise NotImplementedError

    @abc.abstractmethod
    def keys(self):
        raise NotImplementedError

    def query(self, query, order=None):
        return filter(query.as_lambda(), self.list(order))

    def first(self, query, order=None):
        try:
            return next(self.query(query, order=order))
        except StopIteration:
            raise exceptions.NotFound(query)

    def list(self, order=None):
        order = order or (lambda x: x)
        return order(self.get(key) for key in self.keys())

    def count(self, query):
        return len(self.query(query))

    def select(self):
        return QueryCommand(self)

    def _exec_query(self, command):
        return self.query(
            command._query,
            order=command._order_by,
            limit=command._limit,
            skip=command._skip,
        )

    def raw_backend(self):
        return self


class Backend(ReadOnlyBackend):

    @abc.abstractmethod
    def set(self, key, value):
        raise NotImplementedError

    @abc.abstractmethod
    def unset(self, key):
        raise NotImplementedError

    @abc.abstractmethod
    def unset_all(self):
        raise NotImplementedError
