from abc import ABC
from abc import abstractmethod


class Database(ABC):
    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def save_score(self, player_name, score):
        pass

    @abstractmethod
    def fetch_scores(self):
        pass



