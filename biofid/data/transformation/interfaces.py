from abc import ABC, abstractmethod
from typing import Any


class DataTransformation(ABC):
    """ The base class for all DataTransformations. """

    @abstractmethod
    def transform(self, data: Any) -> Any:
        pass
