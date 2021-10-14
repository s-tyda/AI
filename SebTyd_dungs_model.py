import networkx as nx
from networkx import DiGraph
import pygraphviz
import os

if not os.path.exists('plots/Dung'):
    os.makedirs('plots/Dung')

graph = DiGraph()

with open('resources/dung.txt') as f:
    lines = [x.strip() for x in f.readlines()]
    args = lines[1].split(",")
    attacks = lines[3][1:-1].split("),(")

graph.add_nodes_from(args, status="")

for attack in attacks:
    attack = attack.split(",")
    graph.add_edge(attack[0], attack[1])


def iterate(graph):
    changed = True
    ins = []
    outs = []
    while changed:
        changed = False
        for i in graph.nodes:
            if graph.nodes[i]["status"] == '':
                if any(graph.nodes[x[0]]["status"] == 'in' for x in graph.in_edges(i)) or any(graph.nodes[x[1]]["status"] == 'in' for x in graph.out_edges(i)):
                    graph.nodes[i]["status"] = 'out'
                    outs.append(i)
                    changed = True
                elif len(graph.in_edges(i)) == 0 or all(graph.nodes[x[0]]["status"] == 'out' for x in graph.in_edges(i)):
                    graph.nodes[i]["status"] = 'in'
                    ins.append(i)
                    changed = True
    subgraph_nodes = [x for x in graph.nodes if graph.nodes[x]["status"] == ""]
    return tuple((ins, subgraph_nodes, outs))


def recursion(all_ins, sub_nodes):
    if len(sub_nodes) == 1:
        prefered.append(all_ins)
        return
    else:
        graph2 = graph.subgraph(sub_nodes)
        for sub_node in [x for x in graph2.nodes if graph2.nodes[x]["status"] == ""]:
            graph2.nodes[sub_node]["status"] = "in"
            sub_ins, subg_nodes, sub_outs = iterate(graph2.copy())
            sub_ins.append(sub_node)
            tmp_ins = all_ins.copy()
            tmp_ins += sub_ins
            if len(subg_nodes) == 0:
                prefered.append(tmp_ins)
                graph2.nodes[sub_node]["status"] = ""
                continue
            else:
                recursion(tmp_ins, subg_nodes + [sub_node])
            graph2.nodes[sub_node]["status"] = ""


A = nx.nx_agraph.to_agraph(graph)
A.node_attr['style'] = 'filled'
A.graph_attr['label'] = 'Graph'
A.node_attr['shape'] = 'circle'
A.layout()
A.draw("plots/Dung/graph_input.png")
A.clear()

prefered = []
grounded, subgraph_nodes, outs = iterate(graph)
recursion(grounded.copy(), subgraph_nodes)
grounded.sort()
prefered = [tuple(sorted(x)) for x in prefered]
prefered = list(set(prefered))

print("Grounded:")
for i in grounded:
    print(i, end=" ")
print("\n")

A = nx.nx_agraph.to_agraph(graph)
A.node_attr['style'] = 'filled'
A.graph_attr['label'] = 'Grounded'
A.node_attr['shape'] = 'circle'
nodes = [A.get_node(x) for x in graph.nodes]
for node in nodes:
    if node in grounded:
        node.attr['fillcolor'] = 'green'
    elif node in outs:
        node.attr['fillcolor'] = 'red'
    else:
        node.attr['fillcolor'] = 'grey'
A.layout()
A.draw("plots/grounded.png")
A.clear()

print("Preffered:")
for idx, prefer in enumerate(prefered):
    print(f"Option {idx + 1}:")
    for i in prefer:
        print(i, end=" ")
    print()

    A = nx.nx_agraph.to_agraph(graph)
    A.node_attr['style'] = 'filled'
    A.graph_attr['label'] = f"Prefered {idx + 1}"
    A.node_attr['shape'] = 'circle'
    nodes = [A.get_node(x) for x in graph.nodes]
    for node in nodes:
        if node in prefer:
            node.attr['fillcolor'] = 'green'
        else:
            node.attr['fillcolor'] = 'red'
    A.layout()
    A.draw(f"plots/Dung/prefered_{idx + 1}.png")
    A.clear()
