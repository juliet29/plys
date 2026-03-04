# each node knows its level
# metrics taken from Ostwald 2011

from typing import NamedTuple
from plys.jpg.interfaces import JPGraph
from utils4plans.lists import sort_and_group_objects_dict
from loguru import logger


class JPGMetrics(NamedTuple):
    total_depth: float
    mean_depth: float
    relative_asymmetry: float
    control_value: dict[str, float]


def calculate_total_depth(G: JPGraph):
    # sort and group ndoes based on level
    nodes = G.jpnodes
    levels = sort_and_group_objects_dict(nodes, lambda x: x.data.level)

    total_depth = 0
    for level, nodes in levels.items():
        val = level * len(nodes)
        logger.debug(f"level: {level}, n_nodes: {len(nodes)}")
        total_depth += val

    return total_depth


def calculate_mean_depth(G: JPGraph, total_depth: float):
    return total_depth / (
        G.num_nodes - 1
    )  # TODO: this should be -1 if the carrier is included as one of the nodes


def calculate_relative_asymmetry(G: JPGraph, mean_depth: float):
    return 2 * (mean_depth - 1) / (G.num_nodes - 2)


def calculate_control_value(G: JPGraph):
    # TODO: fix -> tests not passing...
    def calc_b_value(node: str):
        return len(list(G.neighbors(node)))

    def calc_a_value(node: str):
        nbs = G.neighbors(node)

        cv_a = sum(1 / calc_b_value(b) for b in nbs)

        return cv_a

    control_values = dict()

    for node in G.nodes:
        control_values[node] = calc_a_value(node)

    return control_values
