import networkx as nx
import random
import numpy as np
import generate_network_with_communities as nwc

if __name__ == '__main__':

    num_communities = 8
    community_sizes = [5, 6, 7, 8, 9, 10, 11, 12]
    G = nwc.generate_community_network(num_communities, community_sizes)

    # Visualize the network
    nwc.visualize_network(G, num_communities, community_sizes)
