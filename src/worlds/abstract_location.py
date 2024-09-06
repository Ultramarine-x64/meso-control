from abc import ABC, abstractmethod


class AbstractLocation(ABC):
    """Abstract class for location."""

    @abstractmethod
    def compute_move(self, target_location):
        """Compute of movement relative to own and target location.

        :param target_location: target location
        :return: new location for moving towards the target
        """
        pass

    @abstractmethod
    def get_distance(self, other):
        """Get distance between self and other in metrics which define in location classes.

        :param other: other location
        :return: distance
        """
        pass

    @abstractmethod
    def get_possible_moves(self) -> list:
        """Get possible moves to all neighboring locations.

        :return: possible moves to all neighboring locations
        """
        pass

    @abstractmethod
    def get_random_move(self):
        """Get random move to one of the neighboring locations.

        :return: random move to one of the neighboring locations
        """
        pass
