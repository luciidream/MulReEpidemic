import numpy as np
import visualisation_methods as vm


if __name__ == '__main__':
    num_steps = 200
    agents_num = 2000
    sites_num = 50
    recovery_rate = 0.02
    # -----------------------------Single Entry-----------------------------
    # lambda_M = np.load("lambda_M.npy", allow_pickle=True)
    # vm.lambda_curve(lambda_M, num_steps)
    #
    # infected_agent = np.load("infected_agent.npy", allow_pickle=True).item()
    # vm.infection_curve(num_steps, agents_num, sites_num, recovery_rate, infected_agent)
    # ----------------------------Multiple Entry----------------------------
    processing_instance = 10
    infected_agent = np.zeros(num_steps)
    for i in range(processing_instance):
        dict_temp = np.load(f'output_{i}_infected_agent.npy', allow_pickle=True).item()
        array_temp = []
        for t, v in dict_temp.items():
            array_temp.append(len(v))
        array_temp = np.array(array_temp)
        vm.infection_curve(num_steps, agents_num, sites_num, recovery_rate, array_temp, order=i)
        infected_agent += array_temp

    infected_agent = infected_agent/processing_instance
    vm.infection_curve(num_steps, agents_num, sites_num, recovery_rate, infected_agent)







