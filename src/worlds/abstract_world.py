from abc import ABC, abstractmethod
import threading


class AbstractWorld(ABC, threading.Thread):
    """Abstract world-class."""

    def __init__(self, agents: list, num_steps: int, walls: list, path_to_results: str, create_step_images: bool):
        """Creating an instance of a class with agents and number of steps.

        :param agents: agents that in this world
        :type agents: list
        :param num_steps: number of steps to simulate
        :type num_steps: int
        :param walls: walls on world
        :type walls: list
        :param path_to_results: relative path to the folder with the result
        :type path_to_results: str
        :param create_step_images: whether to create pictures
        :type create_step_images: bool
        """
        super().__init__()
        self.agents = agents
        self.num_steps = num_steps
        self.walls = walls
        self.all_messages = {}
        self.path_to_results = path_to_results
        self.create_step_images = create_step_images

    @abstractmethod
    def is_have_connection(self, agent1_id: int, agent2_id: int) -> bool:
        """Check connection between two agents.

        :param agent1_id: first agent id
        :type agent1_id: int
        :param agent2_id: second agent id
        :type agent2_id: int
        :return: is connection
        :rtype: bool
        """
        pass

    @abstractmethod
    def rec_messages(self) -> None:
        """Receiving messages from agents."""
        pass

    @abstractmethod
    def sent_messages(self) -> None:
        """Sent messages to agents."""
        pass

    @abstractmethod
    def run(self) -> None:
        """Runs a simulation in this world."""
        pass
