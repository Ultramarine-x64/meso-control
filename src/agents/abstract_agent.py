from abc import ABC, abstractmethod

from src.behaviours.abstract_behaviour import AbstractBehaviour


class AbstractAgent(ABC):
    """Abstract agent class. Create agent with agent id and behaviour, cluster id"""

    def __init__(self, agent_id: int, cluster_id: int, behaviour: AbstractBehaviour):
        """Creating an instance of a class with agent id, cluster id and agent behavior.

        :param agent_id: agent id
        :type agent_id: int
        :param cluster_id: cluster id
        :type cluster_id: int
        :param behaviour: agent behaviour
        :type behaviour: AbstractBehaviour
        """
        self.id = agent_id
        self.cluster_id = cluster_id
        self.behaviour = behaviour

    @abstractmethod
    def do_action(self) -> None:
        """Make an action defined for the agent."""
        pass

    @abstractmethod
    def get_message(self) -> dict:
        """Get agent message.

        :return: agent message
        :rtype: dict
        """
        pass

    @abstractmethod
    def rec_messages(self, messages: dict) -> None:
        """Receiving messages from other agents.

        :param messages: received messages with key - agent id and value - agent message
        :type messages: dict
        """
        pass
