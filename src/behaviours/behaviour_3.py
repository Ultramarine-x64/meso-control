from src.behaviours.abstract_hexagon_behaviour import AbstractHexagonBehaviour
from src.worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation


class Behaviour3(AbstractHexagonBehaviour):
    """!!!DEPRECATED!!!
    Behavior implementing algorithm 2c(3).
    Agents determine the center and area of their cluster.
    Then calculate the optimal trajectory for all clusters without collisions.
    Then, moving the cluster center to the target for their cluster,
    they move themselves parallel to the movement of the cluster center.
    """

    def __init__(
        self,
        agent_id: int,
        cluster_id: int,
        agent_location: Hexagon2DLocation,
        target_location: Hexagon2DLocation,
        cluster_target: Hexagon2DLocation,
        path: [],
        walls: []
    ):
        """Creating an instance of a class with agent id, location and target and cluster id.
        Now there is a cluster target task, but then we need to remove it,
        and the agents themselves must calculate it.

        :param agent_id: agent id
        :type agent_id: int
        :param agent_location: agent start location
        :type agent_location: Hexagon2DLocation
        :param target_location: agent target location
        :type target_location: Hexagon2DLocation
        """
        super().__init__(agent_id, agent_location, target_location, walls)
        self.cluster_id = cluster_id
        self.center_cluster_location = agent_location
        self.cluster_target = cluster_target
        self.cluster_area = []
        self.is_synchronization = False
        self.occupied_area = []
        self.is_cluster_target_defined = False
        self.path = path

    def define_center_cluster_location(self, messages: dict) -> None:
        center_cluster_locations = [message[1] for _, message in messages.items() if message[0] == self.cluster_id]

        cluster_location = Hexagon2DLocation(0, 0)
        for location in center_cluster_locations:
            cluster_location += location
        cluster_location //= len(center_cluster_locations)

        self.center_cluster_location = cluster_location
        self.is_synchronization = True

    def define_cluster_area(self, messages: dict) -> None:
        agent_locations = [message[2] for _, message in messages.items() if message[0] == self.cluster_id]
        min_row = self.agent_location.row
        max_row = self.agent_location.row
        min_column = self.agent_location.column
        max_column = self.agent_location.column

        for agent_location in agent_locations:
            min_row = min(min_row, agent_location.row)
            max_row = max(max_row, agent_location.row)
            min_column = min(min_column, agent_location.column)
            max_column = max(max_column, agent_location.column)

        self.cluster_area = [Hexagon2DLocation(min_row, min_column), Hexagon2DLocation(max_row, max_column)]

    def define_cluster_target(self, messages) -> None:
        cluster_ids = []
        center_cluster_locations = []
        cluster_areas = []
        for _, message in messages.items():
            if message[0] not in cluster_ids:
                cluster_ids.append(message[0])
                center_cluster_locations.append(message[1])
                cluster_areas.append(message[3])

        for cluster_id, center_cluster_location in zip(cluster_ids, center_cluster_locations):
            pass

        # self.cluster_target = Hexagon2DLocation(0, 0)
        self.is_cluster_target_defined = True

    def do_action(self) -> None:
        if not self.is_synchronization or not self.is_cluster_target_defined:
            return
        else:
            self.move()

    def get_message(self) -> list:
        return [self.cluster_id, self.center_cluster_location, self.agent_location, self.cluster_area]

    def rec_messages(self, messages: dict) -> None:
        if not self.is_synchronization:
            self.define_center_cluster_location(messages)
        if not self.is_cluster_target_defined:
            self.define_cluster_area(messages)
            self.define_cluster_target(messages)
        self.update_next_move()

    def move(self) -> None:
        self.agent_location += self.next_move
        if len(self.path) != 0:
            self.center_cluster_location += self.center_cluster_location.get_move(self.path[0])
            self.path.remove(self.path[0])
        else:
            self.center_cluster_location += Hexagon2DLocation(0, 0)

    def update_next_move(self) -> None:
        if len(self.path) != 0:
            self.next_move = self.agent_location.get_move(self.path[0])
        else:
            self.next_move = Hexagon2DLocation(0, 0)
        """self.next_move = self.agent_location.compute_move(
            self.cluster_target - self.center_cluster_location + self.agent_location
        )"""

    def correct_next_move(self) -> None:
        pass
