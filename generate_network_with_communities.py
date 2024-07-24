import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def visualize_network(G, num_communities, community_sizes, figsize=(16, 12), dpi=300):
    plt.figure(figsize=figsize, dpi=dpi)
    pos = nx.spring_layout(G)  # Layout for visualization

    # Color map for nodes
    colors = plt.cm.get_cmap('viridis', num_communities)
    node_colors = []
    for i in range(num_communities):
        node_colors.extend([colors(i)] * community_sizes[i])

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color=node_colors)

    # Color map for edges
    intra_edges = [(u, v) for u, v in G.edges() if abs(u - v) < min(community_sizes)]
    inter_edges = [(u, v) for u, v in G.edges() if abs(u - v) >= min(community_sizes)]

    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=intra_edges, edge_color='blue', alpha=0.5)
    nx.draw_networkx_edges(G, pos, edgelist=inter_edges, edge_color='red', alpha=0.5)

    # Style with seaborn
    sns.set(style="whitegrid")
    plt.axis('off')  # Turn off the axis
    plt.show()


def generate_community_network(num_communities, community_sizes):
    if num_communities != len(community_sizes):
        raise ValueError("Number of communities must match the length of community_sizes list.")

    G = nx.Graph()

    # Generate intra-community edges
    communities = []
    for i in range(num_communities):
        community = nx.erdos_renyi_graph(community_sizes[i], 0.5)
        communities.append(community)
        G = nx.disjoint_union(G, community)

    # Add inter-community edges with a power-law distribution
    total_nodes = sum(community_sizes)
    for i in range(num_communities):
        for j in range(i + 1, num_communities):
            community_i_nodes = list(range(sum(community_sizes[:i]), sum(community_sizes[:i + 1])))
            community_j_nodes = list(range(sum(community_sizes[:j]), sum(community_sizes[:j + 1])))

            num_edges = int(np.random.power(2) * min(community_sizes[i], community_sizes[j]))
            for _ in range(num_edges):
                node_i = random.choice(community_i_nodes)
                node_j = random.choice(community_j_nodes)
                G.add_edge(node_i, node_j)

    return G