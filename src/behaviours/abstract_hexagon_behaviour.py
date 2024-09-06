from abc import ABC, abstractmethod

from src.behaviours.abstract_behaviour import AbstractBehaviour
from src.worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation


class AbstractHexagonBehaviour(AbstractBehaviour, ABC):
    """Behavior implementing abstract behaviour for hexagon world."""

    def __init__(
        self,
        agent_id: int,
        agent_location: Hexagon2DLocation,
        target_location: Hexagon2DLocation,
        walls: list
    ):
        """Creating an instance of a class with agent id, location and target.

        :param agent_id: agent id
        :type agent_id: int
        :param agent_location: agent start location
        :type agent_location: Hexagon2DLocation
        :param target_location: agent target location
        :type target_location: Hexagon2DLocation
        :param walls: walls on hexagon plane
        :type walls: list
        """
        super().__init__(agent_id)
        self.agent_location = agent_location
        self.target_location = target_location
        self.previous_location = self.agent_location
        self.walls = walls
        self.next_move = Hexagon2DLocation(0, 0)
        self.is_random_move = False

    @abstractmethod
    def define_center_cluster_location(self, messages: dict) -> None:
        """Define center cluster location for agent with algorithms with clustering.

        :param messages: received messages
        :type messages: dict
        """
        pass

    @abstractmethod
    def define_cluster_target(self, messages) -> None:
        """Define cluster target for agent with algorithms with clustering.

        :param messages: received messages
        :type messages: dict
        """
        pass

    @abstractmethod
    def compute_next_move(self) -> None:
        """Update next move for agent."""
        pass

    @abstractmethod
    def correct_next_move(self) -> None:
        """Correct next move from neighbour's q and move."""
        pass

    @abstractmethod
    def move(self) -> None:
        """Move agent to target."""
        pass

    @abstractmethod
    def obstacle_avoidance(self) -> None:
        """Correct next move if there are walls on the hexagon plane."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset clustering settings."""
        pass

    def get_next_move(self) -> Hexagon2DLocation:
        return self.next_move
