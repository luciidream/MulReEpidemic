import numpy as np
from scipy.stats import gamma as g


def calculate_states(agents_num, sites_num, gamma, beta, risk, trajectories, shape, scale, num_steps):
    """

    :param scale: gamma distribution scale
    :param shape: gamma distribution shape
    :param beta: agent's infectiveness at each site
    :param sites_num: M
    :param agents_num: N
    :param num_steps: iteration
    :param gamma: susceptibility of agent i at site a
    :param risk: risk of a site at time t
    :param trajectories: biased random walk
    :return: p_i(t) agents' rate of infection at time t
             q_i(t) agents' probability to be infectious at time t
             risk at time t
    """
    # order --- risk_t-1--->p_t--->q_t--->risk_t
    p_t = np.zeros((num_steps, agents_num))
    q_t = np.zeros((num_steps, agents_num))
    risk_t = np.zeros((num_steps, sites_num))
    risk_t[0] = risk

    p_t[0] = np.random.uniform(0, 1, agents_num)
    # p_t[0] = p_t[0] / np.sum(p_t[0])

    q_t[0] = np.random.uniform(0, 1, agents_num)
    # q_t[0] = q_t[0] / np.sum(q_t[0])

    for t in range(1, num_steps):
        # print("Calculating state at " + str(t))
        # sites agents go at time t
        trajectories_till_t = trajectories[:, 1:t+1]
        for i in range(agents_num):
            p_t[t][i] = np.sum(gamma[i][trajectories_till_t[i]] * risk_t[t-1][trajectories_till_t[i]])
            # if t == 1:
            #     gamma_dist_val = g.pdf(1, shape, scale)
            # else:
            gamma_dist_val = np.array([g.pdf(tau, shape, scale) for tau in reversed(range(1, t+1))])
            q_t[t][i] = np.sum(p_t[1:t+1, i] * gamma_dist_val)

        for j in range(sites_num):
            trajectory_at_t = trajectories[:, t]
            agents_arrive_at_j = np.where(trajectory_at_t == j)[0]
            risk_t[t][j] = np.sum(beta[agents_arrive_at_j, j] * q_t[t, agents_arrive_at_j]) / len(trajectory_at_t)

        # p_t[t-1] = p_t[t-1] / np.sum(p_t[t-1])
        # q_t[t-1] = q_t[t-1] / np.sum(q_t[t-1])
        # risk_t[t] = risk_t[t] / np.sum(risk_t[t])

    return p_t, q_t, risk_t







