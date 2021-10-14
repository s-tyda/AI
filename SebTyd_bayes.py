from networkx import nx_agraph, nx_pydot
from networkx import DiGraph
import os
from itertools import product

main_path = "plots/Bayes/"
probability_dict = {}
graph = DiGraph()


def to_probability(string, dependencies=None):
    if not dependencies:
        return f"P({string})"
    else:
        deps = ""
        for idx, i in enumerate(dependencies):
            if idx != 0:
                deps += ","
            if i[1]:
                deps += i[0]
            else:
                deps += f"~{i[0]}"
        return f"P({string}|{deps})"


def print_graph(filename):
    pydot_graph = nx_pydot.to_pydot(graph)
    pydot_graph.set_size('"5,5!"')
    A = nx_pydot.from_pydot(pydot_graph)
    A = nx_agraph.to_agraph(A)
    for edge in graph.edges:
        prob = get_probability(edge[1], dependencies=[(edge[0], True)])
        edge = A.get_edge(edge[0], edge[1])
        edge.attr['label'] = prob
    A.graph_attr['label'] = 'Graph'
    A.node_attr['shape'] = 'circle'
    A.layout(prog="dot")
    A.draw(f"{main_path}{filename}.png")
    A.clear()


def get_probability(x, dependencies=None):
    if dependencies:
        prob_x = to_probability(x, dependencies)
        if (x, True) in dependencies:
            p = get_probability(x)
        elif prob_x in probability_dict:
            p = probability_dict[prob_x]
        else:
            p = compute_probability(x, dependencies=dependencies)
            probability_dict[prob_x] = p
    else:
        prob_x = to_probability(x)
        if prob_x in probability_dict:
            p = probability_dict[prob_x]
        else:
            p = compute_probability(x)
            probability_dict[prob_x] = p
    return p


def compute_probability(x, dependencies=None):
    x_in_edges = [i[0] for i in graph.in_edges(x)]
    combinations = list(product([False, True], repeat=len(x_in_edges)))
    sum = 0.0
    jump_mode = False
    if dependencies and any(x[0] not in x_in_edges for x in dependencies):
        jump_mode = True
    for combination in combinations:
        prob = 1.0
        combination = list(zip(x_in_edges, combination))
        if not jump_mode and dependencies and not all(a in combination for a in dependencies):
            continue
        for idx, i in enumerate(combination):
            if dependencies and i in dependencies:
                p = 1
            else:
                p = get_probability(i[0], dependencies)
                if not i[1]:
                    p = 1.0 - p
            prob *= p
        p = get_probability(x, combination)
        prob *= p
        sum += prob
    return round(sum, 8)


if __name__ == "__main__":
    if not os.path.exists(main_path):
        os.makedirs(main_path)

    with open('resources/bayes.txt') as f:
        lines = [x.strip() for x in f.readlines()]
        nodes = lines[1].split(",")
        attacks = lines[3][1:-1].split("),(")
        for line in lines[5:]:
            splitted = [x.strip() for x in line.split("=")]
            x = splitted[0]
            probability = splitted[1]
            probability_dict[x] = float(probability)
        # print(probability_dict)

    graph.add_nodes_from(nodes, status="")

    for attack in attacks:
        attack = attack.split(",")
        graph.add_edge(attack[0], attack[1])

    for node in graph.nodes:
        in_edges = [x[0] for x in graph.in_edges(node)]
        pr = get_probability(node)
        # print(f"{to_probability(node)} = {pr}")

        if len(in_edges):
            for in_edge in in_edges:
                deps = [(in_edge, True)]
                pr = get_probability(node, dependencies=deps)
                graph.edges[in_edge, node]['weight'] = pr
                # print(f"{to_probability(node, dependencies=deps)} = {pr}")
                deps = [(in_edge, False)]
                pr = get_probability(node, dependencies=deps)
                # print(f"{to_probability(node, dependencies=deps)} = {pr}")

    print_graph("graph")

    while True:
        prob = input('Podaj formułę do sprawdzenia w formacie P(Wynik|Warunek,~Warunek) np. P(H|G)\n').split("|")
        x = prob[0][2:]
        dependencies = prob[1][:-1].split(",")
        dependencies = [(x[1], False) if x.startswith("~") else (x, True) for x in dependencies]
        pr = get_probability(x, dependencies=dependencies)
        print(f"{to_probability(x, dependencies=dependencies)} = {pr}")

