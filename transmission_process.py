import numpy as np


def si_agents_infected_at_t(agents_network, p_t, q_t, trajectories, N, recovery_rate, initial_seed, num_steps):
    agents = np.linspace(0, N - 1, N)
    agents = agents.astype(np.int64)
    infected_agent = {0: np.random.choice(agents, initial_seed, replace=False)}
    for t in range(1, num_steps):
        agents_location = trajectories[:, t]
        infected_agent_till_t = infected_agent[t - 1]
        infected_agent_till_t = infected_agent_till_t[recovery_rate <=
                                                      np.random.uniform(0, 1, len(infected_agent_till_t))]
        # print("Transmission at " + str(t) + " Infected agent: " + str(len(infected_agent_till_t)) + " / " + str(N))
        if len(infected_agent_till_t) == N:
            # print("*****WASTED*****")
            break
        for s in np.unique(agents_location):
            agents_at_s = np.where(agents_location == s)[0]
            agents_at_s = agents_at_s.astype(np.int64)
            infected_agent_here = np.intersect1d(agents_at_s, infected_agent_till_t)
            if infected_agent_here.size == 0:
                break
            else:
                for i in infected_agent_here:
                    neighbors = np.array(list(agents_network.neighbors(i)))
                    # exclude agents already infected
                    mask = np.isin(neighbors, infected_agent_here, invert=True)
                    neighbors = neighbors[mask]
                    infection = q_t[t][i] * p_t[t][neighbors]
                    random_val = np.random.uniform(0, 1, len(infection))
                    newly_infected_agents = neighbors[infection >= random_val]
                    mask = np.isin(newly_infected_agents, infected_agent_till_t, invert=True)
                    newly_infected_agents = newly_infected_agents[mask]
                    infected_agent_till_t = np.concatenate((infected_agent_till_t, newly_infected_agents), axis=0)

        infected_agent[t] = infected_agent_till_t

    return infected_agent
