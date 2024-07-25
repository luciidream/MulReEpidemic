import numpy as np
import visualisation_methods as vm


if __name__ == '__main__':

    lambda_M = np.load("lambda_M.npy", allow_pickle=True)
    num_steps = 200
    vm.lambda_curve(lambda_M, num_steps)

    infected_agent = np.load("infected_agent.npy", allow_pickle=True).item()
    num_steps = 200
    agents_num = 2000
    sites_num = 50
    recovery_rate = 0.02
    vm.infection_curve(num_steps, agents_num, sites_num, recovery_rate, infected_agent)


