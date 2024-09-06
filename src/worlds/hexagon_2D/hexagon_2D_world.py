from src.worlds.abstract_world import AbstractWorld
from src.worlds.hexagon_2D.hexagon_2D_drawer import Hexagon2DDrawer


class Hexagon2DWorld(AbstractWorld):
    """Class world for storing the location of agents on a plane, consisting of regular hexagons."""

    def __init__(self, num_of_tiles_side: int, agents: list, num_steps: int, walls: list, path_to_results: str, create_step_images: bool):
        """Create world by number of tiles per side.

        :param num_of_tiles_side: number of tiles per side of a square
        :type num_of_tiles_side: int
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
        super().__init__(agents, num_steps, walls, path_to_results, create_step_images)
        self.num_of_titles_side = num_of_tiles_side
        self.drawer = Hexagon2DDrawer(num_of_tiles_side, agents, walls, path_to_results, create_step_images)

    def agent_reset(self) -> None:
        """Reset clustering settings for all agents."""
        for agent in self.agents:
            agent.behaviour.reset()

    def compute_agent_action(self):
        """Compute action for all agents."""
        for agent in self.agents:
            agent.behaviour.compute_action()

    def correct_agent_action(self):
        """Correct action for all agents."""
        for agent in self.agents:
            agent.behaviour.correct_next_move()

    def do_agent_action(self) -> None:
        """Do action for all agents."""
        required_agent_locations = self.get_required_locations()
        agents_locations = [agent.behaviour.agent_location for agent in self.agents]

        for agent, required_location in zip(self.agents, required_agent_locations):
            if required_location == agent.behaviour.agent_location:
                agent.do_action()
                continue
            elif required_agent_locations.count(required_location) > 1:
                agent.behaviour.num_penalty_step = 1
            elif agents_locations.count(required_location) > 0 or self.walls.count(required_location) > 0:
                agent.behaviour.num_penalty_step = 1

            agent.do_action()

    def get_required_locations(self) -> list:
        """Get required locations from all agents."""
        required_locations = []
        for agent in self.agents:
            agent_behaviour = agent.behaviour
            if agent_behaviour.num_penalty_step > 0:
                required_locations.append(agent_behaviour.agent_location)
            else:
                required_locations.append(agent_behaviour.agent_location + agent_behaviour.get_next_move())

        return required_locations

    def is_have_connection(self, agent1_id: int, agent2_id: int) -> bool:
        return True

    def rec_messages(self) -> None:
        self.all_messages.update([(agent.id, agent.get_message()) for agent in self.agents])

    def run(self) -> None:
        for step in range(self.num_steps):
            print("Step: " + str(step))
            self.agent_reset()
            self.compute_agent_action()
            self.rec_messages()
            self.sent_messages()
            self.correct_agent_action()
            self.drawer.draw_plane(self.num_steps, step)
            self.do_agent_action()

    def sent_messages(self) -> None:
        for agent in self.agents:
            messages_for_agent = {}
            for agent_id, message in self.all_messages.items():
                if self.is_have_connection(agent.id, agent_id):
                    messages_for_agent.update({agent_id: message})
            agent.rec_messages(messages_for_agent)
