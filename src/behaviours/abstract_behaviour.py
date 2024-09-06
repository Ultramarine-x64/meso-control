from abc import ABC, abstractmethod


class AbstractBehaviour(ABC):
    """Agent abstract behavior class."""

    def __init__(self, agent_id: int):
        """Creating an instance of a class with agent id.

        :param agent_id: agent id
        :type agent_id: int
        """
        self.agent_id = agent_id
        self.num_penalty_step = 0
        self.messages = {}

    @abstractmethod
    def compute_action(self) -> None:
        """Calculate the action of a specific agent."""
        pass

    @abstractmethod
    def do_action(self) -> None:
        """Make an action defined for the agent's behavior."""
        pass

    @abstractmethod
    def get_message(self):
        """Get agent message.

        :return: agent message
        """
        pass

    @abstractmethod
    def rec_messages(self, messages: dict) -> None:
        """Receiving messages from other agents.

        :param messages: received messages with key - agent id and value - agent message
        :type messages: dict
        """
        pass
