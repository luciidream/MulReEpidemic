import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def lambda_curve(lambda_M, num_steps):
    x = np.linspace(1, num_steps - 1, num_steps - 1)
    y = np.real(lambda_M)

    sns.set(style="darkgrid")
    plt.figure(figsize=(16, 12), dpi=400)
    plt.plot(x, y, marker='o', markersize=5, linewidth=2, color='blue')
    plt.title('Largest Eigenvalue Real Parts', fontsize=30)
    plt.xlabel('Time', fontsize=25)
    plt.xticks(fontsize=20)
    plt.ylabel('Largest Eigenvalue', fontsize=25)
    plt.xticks(fontsize=20)
    plt.show()


def infection_curve(num_steps, agents_num, sites_num, recovery_rate, infected_agents, order=-1):
    """

    Args:
        num_steps: the time of infection
        infected_agents: an array

    Returns:

    """
    x = np.linspace(1, len(infected_agents), len(infected_agents))
    x.astype(np.int64)
    y = infected_agents

    sns.set(style="darkgrid")
    plt.figure(figsize=(16, 12), dpi=400)
    plt.plot(x, y, marker='o', markersize=5, linewidth=2, color='red')
    plt.title('Infected agents', fontsize=30)
    plt.xlabel('Time', fontsize=25)
    plt.xticks(fontsize=20)
    plt.ylabel('Cumulated infected agents', fontsize=25)
    plt.xticks(fontsize=20)
    plt.text(-5, 1750, "Time: " + str(num_steps) + '\n' + "Agents: " + str(agents_num) + '\n' +
             "Sites: " + str(sites_num) + '\n' + "Recovery Rate: " + str(recovery_rate) + '\n' +
             "Order: " + str(order),
             fontsize=20, bbox={'facecolor': 'white', 'pad': 10, 'alpha': 0.5})
    plt.show()
