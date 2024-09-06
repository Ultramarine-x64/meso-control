import json
import math
import os
from collections import OrderedDict

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle

from src.worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation

import matplotlib
matplotlib.use('Agg')


class Hexagon2DDrawer:
    def __init__(
        self,
        num_of_titles_side: int,
        agents: list,
        walls: list,
        path_to_results: str,
        create_step_images: bool
    ):
        self.path_to_results = path_to_results
        self.create_step_images = create_step_images
        self.num_of_titles_side = num_of_titles_side
        self.agents = agents
        self.walls = walls
        self.colors = [
            "gray",
            "blue",
            "red",
            "purple",
            "green",
            "deeppink",
            "brown",
            "cyan",
            "antiquewhite",
            "darkgreen",
            "darkviolet",
            "goldenrod",
            "lawngreen",
            "mediumaquamarine",
            "navy",
            "sienna",
            "greenyellow",
            "hotpink",
            "ivory",
            "moccasin",
            "coral",
            "darkgoldenrod",
            "mediumseagreen",
            "lightyellow",
            "mintcream",
            "linen",
            "chocolate",
            "aliceblue",
            "darkred",
            "tomato",
            "royalblue",
        ]
        self.draw_center_cluster_label = []
        self.draw_center_cluster_location = []
        self.draw_cluster_area_label = []
        self.steps = []
        self.accuracy = []
        self.diameter = []
        self.num_of_clusters = []
        self.avg_agents_in_cluster = []
        self.radius_centers = 0.7

    def draw_plane(self, num_steps: int, step: int) -> None:
        self.write_result(num_steps, step)

        if self.create_step_images == "False":
            return

        # figure = plt.figure(figsize=(8, 8))
        figure = plt.figure(figsize=(5, 5))
        figure.subplots_adjust(left=0.01, bottom=0.005, top=0.99, right=0.99)

        sub_plot = figure.add_subplot()

        if self.num_of_titles_side > 60:
            self.radius_centers = 1.2
        else:
            self.radius_centers = 0.7

        # self.draw_hexagon_area(sub_plot)
        # self.draw_cluster_area(sub_plot)
        self.draw_walls(sub_plot)
        self.draw_target(sub_plot)
        # self.draw_cluster_targets(sub_plot)
        # self.draw_center_clusters(sub_plot)
        self.draw_center_system(sub_plot)
        self.draw_agents(sub_plot)

        # plt.xlabel("Step number: " + str(step), fontsize="xx-large")
        sub_plot.set(
            xlim=(-1.5 * math.sin(math.pi / 3), (self.num_of_titles_side + 1) * math.sin(math.pi / 3)),
            ylim=(-1.5, self.num_of_titles_side * math.sin(math.pi / 3)),
        )

        plt.xticks([])
        plt.yticks([])
        plt.legend(loc="upper right", ncol=2, fontsize="x-large")

        self.steps.append(step)
        self.accuracy.append(self.get_accuracy())
        self.diameter.append(self.get_diameter())
        self.num_of_clusters.append(self.get_num_of_clusters())
        self.avg_agents_in_cluster.append(len(self.agents) / self.get_num_of_clusters() * 1.0)

        # plt.subplot(1, 2, 2)
        # plt.xlabel("Time steps")
        # plt.ylabel("Conventional units")
        # plt.xlim(-4, 134)
        # plt.ylim(-2, self.num_of_titles_side * len(agents))
        # plt.plot(self.steps, self.accuracy, "r-", label="Accuracy")
        # plt.plot(self.steps, self.max_diameter, "b-", label="Diameter")
        #
        # plt.legend(loc="best")

        if not os.path.exists(self.path_to_results + "/img"):
            os.mkdir(self.path_to_results + "/img")

        plt.savefig(self.path_to_results + f"/img/img_{step}.png", transparent=False, facecolor="white", dpi=300)
        plt.savefig(self.path_to_results + f"/img/img_{step}.svg", transparent=False, facecolor="white", dpi=300)
        plt.close()

        self.draw_center_cluster_label.clear()
        self.draw_center_cluster_location.clear()
        self.draw_cluster_area_label.clear()

    def write_result(self, num_steps: int, step: int) -> None:
        self.steps.append(step)
        self.accuracy.append(self.get_accuracy())
        self.diameter.append(self.get_diameter())
        self.num_of_clusters.append(self.get_num_of_clusters())
        self.avg_agents_in_cluster.append(len(self.agents) / self.get_num_of_clusters() * 1.0)

        if step == num_steps - 1:
            with open(self.path_to_results + "/result.json", "w") as file:
                json_str = f'"accuracy": {self.accuracy},\
                    "diameter": {self.diameter},\
                    "num_of_clusters": {self.num_of_clusters},\
                    "avg_agents_in_cluster": {self.avg_agents_in_cluster}'
                json_data = json.loads("{" + json_str + "}")
                json.dump(json_data, file, indent=2)

    def draw_hexagon_area(self, sup_plot):
        for i in range(0, self.num_of_titles_side):
            for j in range(0, self.num_of_titles_side):
                polygon = RegularPolygon(
                    xy=((j + (i % 2) / 2.0) * math.sin(math.pi / 3), i * 0.75),
                    numVertices=6,
                    radius=0.5,
                    edgecolor="black",
                    facecolor="white",
                )

                sup_plot.add_patch(polygon)

    def draw_cluster_area(self, sub_plot) -> None:
        try:
            cluster_ids = list(OrderedDict.fromkeys([agent.cluster_id for agent in self.agents]))
            clusters = []
            for cluster_id in cluster_ids:
                if cluster_id == 0:
                    continue
                cluster = []
                for agent in self.agents:
                    if agent.cluster_id == cluster_id:
                        cluster.append(agent.behaviour.agent_location)
                clusters.append(cluster)

            cluster_areas = []
            for cluster in clusters:
                min_row = cluster[0].row
                max_row = cluster[0].row
                min_column = cluster[0].column
                max_column = cluster[0].column
                for location in cluster:
                    min_row = min(min_row, location.row)
                    max_row = max(max_row, location.row)
                    min_column = min(min_column, location.column)
                    max_column = max(max_column, location.column)
                cluster_areas.append([Hexagon2DLocation(min_row, min_column), Hexagon2DLocation(max_row, max_column)])

            for cluster_id, cluster_area in zip(cluster_ids, cluster_areas):
                for row in range(cluster_area[0].row, cluster_area[1].row + 1):
                    for column in range(cluster_area[0].column, cluster_area[1].column + 1):
                        polygon = RegularPolygon(
                            xy=((column + (row % 2) / 2.0) * math.sin(math.pi / 3), row * 0.75),
                            numVertices=6,
                            radius=0.5,
                            edgecolor=self.colors[cluster_id],
                            facecolor="white",
                            hatch="..",
                        )

                        if self.draw_cluster_area_label.count(cluster_id) == 0:
                            polygon.set_label("Cluster " + str(cluster_id) + " area")
                            self.draw_cluster_area_label.append(cluster_id)

                        sub_plot.add_patch(polygon)
        except TypeError:
            pass

    def draw_agents(self, sub_plot) -> None:
        for agent in self.agents:
            try:
                cluster_id = agent.behaviour.cluster_id
            except AttributeError:
                cluster_id = agent.cluster_id
            location = agent.behaviour.agent_location

            polygon = RegularPolygon(
                xy=((location.column + (location.row % 2) / 2.0) * math.sin(math.pi / 3), location.row * 0.75),
                numVertices=6,
                radius=0.5,
                edgecolor="black",
                facecolor=self.colors[cluster_id],
            )

            if self.draw_center_cluster_label.count(cluster_id) == 0:
                # if cluster_id == 0:
                #     polygon.set_label("Agents without cluster")
                # else:
                #     polygon.set_label("Agents with cluster " + str(cluster_id))
                self.draw_center_cluster_label.append(cluster_id)

            sub_plot.add_patch(polygon)

            # if self.num_of_titles_side < 35:
            #     plt.text(
            #         (location.column + (location.row % 2) / 2.0) * math.sin(math.pi / 3) - 2 / self.num_of_titles_side,
            #         location.row * 0.75 - 2 / self.num_of_titles_side,
            #         agent.id,
            #     )

    def get_accuracy(self) -> int:
        sum_accuracy = 0
        for agent in self.agents:
            sum_accuracy += agent.behaviour.agent_location.get_distance(agent.behaviour.target_location)
        return sum_accuracy

    def get_diameter(self) -> int:
        diameter = 0
        for agent_i in self.agents:
            for agent_j in self.agents:
                distance = agent_j.behaviour.agent_location.get_distance(agent_i.behaviour.agent_location)
                if distance > diameter:
                    diameter = distance

        return diameter

    def get_num_of_clusters(self) -> int:
        try:
            count = 0
            cluster_ids = []
            for agent in self.agents:
                cluster_id = agent.behaviour.cluster_id
                if cluster_ids.count(cluster_id) == 0:
                    cluster_ids.append(cluster_id)
                    count += 1

            return count
        except AttributeError:
            return 1

    def draw_cluster_targets(self, sub_plot) -> None:
        try:
            cluster_ids = list(OrderedDict.fromkeys([agent.cluster_id for agent in self.agents]))
            cluster_targets = []
            for agent in self.agents:
                if agent.behaviour.cluster_target not in cluster_targets:
                    cluster_targets.append(agent.behaviour.cluster_target)

            for cluster_id, location in zip(cluster_ids, cluster_targets):
                polygon = RegularPolygon(
                    xy=((location.column + (location.row % 2) / 2.0) * math.sin(math.pi / 3), location.row * 0.75),
                    numVertices=6,
                    radius=self.radius_centers,
                    edgecolor=self.colors[cluster_id],
                    facecolor="white",
                    # label="Target for cluster " + str(cluster_id),
                )

                sub_plot.add_patch(polygon)
        except AttributeError:
            pass

    def draw_target(self, sub_plot) -> None:
        location = self.agents[0].behaviour.target_location

        circle = Circle(
            xy=((location.column + (location.row % 2) / 2.0) * math.sin(math.pi / 3), location.row * 0.75),
            radius=self.radius_centers,
            edgecolor="black",
            facecolor="white",
            label="Target",
        )
        sub_plot.add_patch(circle)

        dummy_circle = Circle(
            xy=((location.column + (location.row % 2) / 2.0) * math.sin(math.pi / 3), location.row * 0.75),
            radius=self.radius_centers,
            edgecolor="black",
            facecolor="white",
        )
        sub_plot.add_patch(dummy_circle)

        sub_plot.vlines(
            (location.column + (location.row % 2) / 2.0) * math.sin(math.pi / 3),
            location.row * 0.75 - self.radius_centers * 1.5,
            location.row * 0.75 + self.radius_centers * 1.5,
            color="black",
            linewidth=0.6,
        )
        sub_plot.hlines(
            location.row * 0.75,
            (location.column + (location.row % 2) / 2.0) * math.sin(math.pi / 3) - self.radius_centers * 1.5,
            (location.column + (location.row % 2) / 2.0) * math.sin(math.pi / 3) + self.radius_centers * 1.5,
            color="black",
            linewidth=0.6,
        )

    def draw_center_clusters(self, sup_plot):
        try:
            for agent in self.agents:
                cluster_id = agent.behaviour.cluster_id
                location = agent.behaviour.center_cluster_location

                polygon = RegularPolygon(
                    xy=((location.column + (location.row % 2) / 2.0) * math.sin(math.pi / 3), location.row * 0.75),
                    numVertices=6,
                    radius=self.radius_centers,
                    edgecolor="black",
                    facecolor=self.colors[cluster_id],
                    hatch="|||||",
                )

                if self.draw_center_cluster_location.count(cluster_id) == 0:
                    polygon.set_label("Center of " + str(cluster_id) + " cluster")
                    self.draw_center_cluster_location.append(cluster_id)

                sup_plot.add_patch(polygon)
        except AttributeError:
            pass

    def draw_center_system(self, sup_plot):
        location = Hexagon2DLocation(0, 0)
        for agent in self.agents:
            location += agent.behaviour.agent_location
        location //= len(self.agents)

        circle = Circle(
            xy=((location.column + (location.row % 2) / 2.0) * math.sin(math.pi / 3), location.row * 0.75),
            radius=self.radius_centers,
            edgecolor="black",
            facecolor="orange",
        )

        circle.set_label("Center of system")
        sup_plot.add_patch(circle)

    def draw_walls(self, sup_plot):
        for wall_location in self.walls:

            polygon = RegularPolygon(
                xy=(
                    (wall_location.column + (wall_location.row % 2) / 2.0) * math.sin(math.pi / 3),
                    wall_location.row * 0.75,
                ),
                numVertices=6,
                radius=0.5,
                edgecolor="lightgray",
                facecolor="lightgray",
            )

            sup_plot.add_patch(polygon)
