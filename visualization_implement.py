import numpy as np
import visualisation_methods as vm


if __name__ == '__main__':

    lambda_M = np.load("lambda_M.npy", allow_pickle=True)
    num_steps = 100
    vm.lambda_curve(lambda_M, num_steps)
