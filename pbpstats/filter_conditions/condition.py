from abc import ABC, abstractmethod
from typing import Union

from pbpstats.resources.enhanced_pbp.enhanced_pbp_item import EnhancedPbpItem
from pbpstats.resources.possessions.possession import Possession


class Condition(ABC):
    @abstractmethod
    def meets(self, input: Union[Possession, EnhancedPbpItem]) -> bool:
        pass
