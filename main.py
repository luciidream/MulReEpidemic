import sys
import time
import numpy as np
import networkx as nx
import pagerank_with_damping_factor as tfm
import biased_random_walk as brw
import generate_network_with_communities as gnwc
import state_calculation as sc
import kernel_matrix as km
import transmission_process as tp


def generate_row_normalized_matrix(dim1, dim2):
    # Generate a random N x M matrix with elements in the range (0, 1)
    matrix = np.random.rand(dim1, dim2)

    # Calculate the sum of each row
    row_sums = np.sum(matrix, axis=1)

    # Normalize each row by dividing each element by the row sum
    normalized_matrix = matrix / row_sums[:, np.newaxis]

    return normalized_matrix


def row_normalize(matrix):
    row_maxes = np.max(matrix, axis=1, keepdims=True)
    normalized_matrix = matrix / row_maxes
    return normalized_matrix


if __name__ == '__main__':
    # --------------------------------------MULTI ENTRY SETTING--------------------------------------
    multi_entry_prefix = sys.argv[1]
    # ---------------------------Initiation and Generation of Trajectories---------------------------
    # N --- number of agents
    start_time = time.time()
    N = 2000
    M = 50
    # M --- number of sites
    # generate synthetic sites network
    # sites_network = nx.scale_free_graph(M)
    sites_network = nx.gnp_random_graph(M, 0.5)
    sn_adj = nx.to_numpy_array(sites_network)
    pagerank = tfm.calculate_pagerank(sn_adj)
    transfer_matrix = tfm.pagerank_to_transfer_matrix(sn_adj, pagerank)
    # generate community-structured network
    num_communities = 10
    community_size = [int(N / 10)] * num_communities
    # community size should later be set heterogeneous
    agents_network = gnwc.generate_community_network(num_communities, community_size, 0.025)
    # relations between agents in social network
    relations = np.random.uniform(0, 1, (N, N))
    # initiate bias matrix N*M dimension
    bias = generate_row_normalized_matrix(N, M)
    num_steps = 200
    trajectories = brw.generate_trajectories(N, agents_network, sites_network,
                                             bias, relations, transfer_matrix, num_steps)
    # ----------------------------------------Epidemic model----------------------------------------
    # initialization time-invariant parameters
    # Initiate agent's susceptibility at each site --- N*M matrix
    gamma = np.random.uniform(0, 1, (N, M))
    # Initiate agent's infectiveness at each site --- N*M matrix
    beta = np.random.uniform(0, 1, (N, M))
    # time variant parameters
    # Initiate site risk --- num_steps*M matrix
    risk = np.random.uniform(0, 1, M)
    # risk = risk / np.sum(risk)
    # infectious probability distribution h(tau) --- gamma distribution
    shape = 2  # alpha --- shape param
    scale = 0.5  # beta --- scale param
    # states till time t
    test = sc.calculate_states(N, M, gamma, beta, risk, trajectories, shape, scale, num_steps)
    p_t = row_normalize(test[0])
    q_t = row_normalize(test[1])
    risk_t = row_normalize(test[2])

    lambda_M = km.largest_eigenvalue(beta, gamma, trajectories, M, num_steps)
    # multi entry file saving
    np.save(f'{multi_entry_prefix}_lambda_M.npy', lambda_M)
    # single entry file saving
    # np.save('lambda_M.npy', lambda_M)
    # ----------------------------------------SI Transmission----------------------------------------
    # a dictionary --- time —————— agents infected
    recovery_rate = 0.02
    infected_agent = tp.si_agents_infected_at_t(agents_network, p_t, q_t, trajectories, N,
                                                recovery_rate, 20, num_steps)
    # multi entry file saving
    np.save(f'{multi_entry_prefix}_infected_agent.npy', infected_agent)
    # single entry file saving
    # np.save('infected_agent.npy', infected_agent)
    endtime = time.time()
    print(f'Finished in {endtime - start_time:0.2f} seconds')


