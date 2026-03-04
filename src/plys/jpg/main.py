from pathlib import Path
from datetime import datetime

from plan2eplus.ezcase.ez import EZ
from plan2eplus.ops.afn.ezobject import Airboundary
from plan2eplus.ops.subsurfaces.ezobject import Subsurface
from plan2eplus.ops.zones.ezobject import Zone
from plys.jpg.interfaces import JPGraph, JPNode, JPNodeData
import networkx as nx
from utils4plans.sets import set_difference

from plys.qoi.registry import QOIRegistry, QOIandData, select_time


def set_levels(G: JPGraph, carrier_node: str):
    def update_level(node_name: str, level: int):
        node = G.get_jpnode(node_name)
        # NOTE: this is not very functional, should create a new data ..
        node.data.level = level
        G.update_jpnode(node.name, node.data)

    # set level of carrier node
    update_level(carrier_node, 0)

    # set others based on distance from carrier..
    other_nodes = set_difference(G.nodes, [carrier_node])
    for node in other_nodes:
        distance = nx.shortest_path_length(G, source=carrier_node, target=node)
        update_level(node, int(distance))

    return G


def idf_to_jpgraph(idf_path: Path, sql_path: Path, datetime_: datetime):
    case = EZ(idf_path)

    def make_jpnode_from_zone(zone: Zone):
        return JPNode(name=zone.room_name, data=JPNodeData())

    def make_edge_from_surface(afn_surface: Subsurface | Airboundary):
        e = afn_surface.edge
        return (e.space_a, e.space_b)

    def make_carrier_jpnode():
        # TODO: this should be pretty flexible, may want to make the carrier node be based on some other factor..
        wind_pressure_data = QOIandData(
            QOIRegistry.custom.unique_wind_pressure, sql_path
        ).original_arr
        max_node_at_time = (
            select_time(wind_pressure_data, datetime_).idxmax().to_dict()["data"]
        )
        return JPNode(name=max_node_at_time, data=JPNodeData(is_carrier=True, level=0))

    jpnodes = [make_jpnode_from_zone(i) for i in case.objects.zones] + [
        make_carrier_jpnode()
    ]
    edges = [
        make_edge_from_surface(i)
        for i in case.objects.subsurfaces + case.objects.airboundaries
    ]

    G = JPGraph()
    G.add_jpnodes(jpnodes)
    G.add_edges_from(edges)

    return G
