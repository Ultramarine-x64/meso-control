from src.behaviours.abstract_hexagon_behaviour import AbstractHexagonBehaviour
from src.behaviours.behaviour_macro import MacroBehaviour
from src.behaviours.behaviour_meso import MesoBehaviour
from src.behaviours.behaviour_micro import MicroBehaviour
from src.behaviours.behaviour_mpc import MPCBehaviour
from src.worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation


def create_behaviours(
    agent_locations: list[Hexagon2DLocation],
    target_location: Hexagon2DLocation,
    walls: list[Hexagon2DLocation],
    strategy: str
) -> list[AbstractHexagonBehaviour]:
    behaviours = []
    if strategy == "Micro":
        for index, agent_location in zip(
            range(len(agent_locations)),
            agent_locations
        ):
            behaviour = MicroBehaviour(
                agent_id=index,
                agent_location=agent_location,
                target_location=target_location,
                walls=walls,
            )
            behaviours.append(behaviour)
    elif strategy == "Macro":
        for index, agent_location in zip(
            range(len(agent_locations)),
            agent_locations
        ):
            behaviour = MacroBehaviour(
                agent_id=index,
                cluster_id=0,
                agent_location=agent_location,
                target_location=target_location,
                walls=walls,
            )
            behaviours.append(behaviour)
    elif strategy == "Meso":
        for index, agent_location in zip(
            range(len(agent_locations)),
            agent_locations
        ):
            behaviour = MesoBehaviour(
                agent_id=index,
                agent_location=agent_location,
                cluster_radius=9,
                target_location=target_location,
                walls=walls,
            )
            behaviours.append(behaviour)
    elif strategy == "MPC":
        for index, agent_location in zip(
            range(len(agent_locations)),
            agent_locations
        ):
            behaviour = MPCBehaviour(
                agent_id=index,
                agent_location=agent_location,
                target_location=target_location,
                walls=walls,
            )
            behaviours.append(behaviour)
    else:
        raise ValueError("Incorrect agent strategy")

    return behaviours