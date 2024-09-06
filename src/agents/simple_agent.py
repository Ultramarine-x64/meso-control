from src.agents.abstract_agent import AbstractAgent


class SimpleAgent(AbstractAgent):
    """Simple agent without additional options."""

    def do_action(self):
        self.behaviour.do_action()

    def get_message(self):
        return self.behaviour.get_message()

    def rec_messages(self, messages: dict):
        self.behaviour.rec_messages(messages)
