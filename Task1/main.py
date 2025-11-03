from collections import deque
from typing import Deque, Dict, List, Set, Tuple

SOURCE_NODE: str = "Source"
SINK_NODE: str = "Sink"
TERMINALS: List[str] = ["Термінал 1", "Термінал 2"]
WAREHOUSES: List[str] = ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]
STORE_PREFIX: str = "Магазин "
WAREHOUSE_PREFIX: str = "Склад"

Graph = Dict[str, Dict[str, float]]


def find_path_bfs(graph: Graph, source: str, sink: str, parent_map: Dict[str, str]) -> bool:
    parent_map.clear()
    visited_nodes: Set[str] = {source}
    queue: Deque[str] = deque([source])

    while queue:
        current_node: str = queue.popleft()
        for neighbor, capacity in graph[current_node].items():
            if neighbor not in visited_nodes and capacity > 0:
                parent_map[neighbor] = current_node
                visited_nodes.add(neighbor)
                queue.append(neighbor)
                if neighbor == sink:
                    return True
    return False


def edmonds_karp_algorithm(graph: Graph, source: str, sink: str) -> Tuple[float, Graph]:
    residual_graph: Graph = {node: neighbors.copy() for node, neighbors in graph.items()}
    parent_map: Dict[str, str] = {}
    max_flow: float = 0.0

    while find_path_bfs(residual_graph, source, sink, parent_map):
        path_flow: float = float("Inf")
        node: str = sink
        while node != source:
            parent: str = parent_map[node]
            path_flow = min(path_flow, residual_graph[parent][node])
            node = parent

        max_flow += path_flow

        v: str = sink
        while v != source:
            u: str = parent_map[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v].setdefault(u, 0)
            residual_graph[v][u] += path_flow
            v = parent_map[v]

    return max_flow, residual_graph


def get_network_graph() -> Graph:
    graph_data: Graph = {
        SOURCE_NODE: {TERMINALS[0]: float("inf"), TERMINALS[1]: float("inf")},
        TERMINALS[0]: {"Склад 1": 25, "Склад 2": 20, "Склад 3": 15},
        TERMINALS[1]: {"Склад 3": 15, "Склад 4": 30, "Склад 2": 10},
        "Склад 1": {"Магазин 1": 15, "Магазин 2": 10, "Магазин 3": 20},
        "Склад 2": {"Магазин 4": 15, "Магазин 5": 10, "Магазин 6": 25},
        "Склад 3": {"Магазин 7": 20, "Магазин 8": 15, "Магазин 9": 10},
        "Склад 4": {"Магазин 10": 20, "Магазин 11": 10, "Магазин 12": 15, "Магазин 13": 5, "Магазин 14": 10},
        "Магазин 1": {SINK_NODE: 15}, "Магазин 2": {SINK_NODE: 10}, "Магазин 3": {SINK_NODE: 20},
        "Магазин 4": {SINK_NODE: 15}, "Магазин 5": {SINK_NODE: 10}, "Магазин 6": {SINK_NODE: 25},
        "Магазин 7": {SINK_NODE: 20}, "Магазин 8": {SINK_NODE: 15}, "Магазин 9": {SINK_NODE: 10},
        "Магазин 10": {SINK_NODE: 20}, "Магазин 11": {SINK_NODE: 10}, "Магазин 12": {SINK_NODE: 15},
        "Магазин 13": {SINK_NODE: 5}, "Магазин 14": {SINK_NODE: 10},
        SINK_NODE: {},
    }
    return graph_data


def calculate_terminal_to_store_flows(original_graph: Graph, residual_graph: Graph) -> List[Tuple[str, str, int]]:
    terminal_flows: Dict[str, Dict[str, float]] = {t: {} for t in TERMINALS}
    for terminal in TERMINALS:
        for node, capacity in original_graph[terminal].items():
            if node.startswith(WAREHOUSE_PREFIX):
                sent: float = capacity - residual_graph[terminal].get(node, 0)
                if sent > 0:
                    terminal_flows[terminal][node] = sent

    warehouse_flows: Dict[str, Dict[str, float]] = {}
    for warehouse in WAREHOUSES:
        warehouse_flows[warehouse] = {}
        for store, capacity in original_graph[warehouse].items():
            if store.startswith(STORE_PREFIX):
                delivered: float = capacity - residual_graph[warehouse].get(store, 0)
                if delivered > 0:
                    warehouse_flows[warehouse][store] = delivered

    final_flows: List[Tuple[str, str, int]] = []
    for terminal in TERMINALS:
        for warehouse, amount_from_terminal in terminal_flows.get(terminal, {}).items():
            rem_flow: float = amount_from_terminal
            if warehouse not in warehouse_flows:
                continue
            
            for store in list(warehouse_flows[warehouse].keys()):
                if rem_flow == 0:
                    break
                
                available_at_store: float = warehouse_flows[warehouse][store]
                flow_to_assign: float = min(rem_flow, available_at_store)
                
                if flow_to_assign > 0:
                    final_flows.append((terminal, store, int(flow_to_assign)))
                    warehouse_flows[warehouse][store] -= flow_to_assign
                    if warehouse_flows[warehouse][store] == 0:
                        del warehouse_flows[warehouse][store]
                    rem_flow -= flow_to_assign
    return final_flows


def main() -> None:
    network_graph: Graph = get_network_graph()

    max_flow, residual_graph = edmonds_karp_algorithm(network_graph, SOURCE_NODE, SINK_NODE)
    print(f"Максимальний потік: {int(max_flow)}")

    distributed_flows: List[Tuple[str, str, int]] = calculate_terminal_to_store_flows(network_graph, residual_graph)
    for terminal, store, value in distributed_flows:
        print(f"{terminal} -> {store} : {value}")


if __name__ == "__main__":
    main()