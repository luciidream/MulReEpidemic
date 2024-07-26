import numpy as np


def power_iteration(A, num_iterations=1000, epsilon=1e-10):
    """
    Compute the largest eigenvalue of matrix A using the power iteration method.

    Parameters:
    A (numpy.ndarray): The input matrix.
    num_iterations (int): The number of iterations to perform.
    epsilon (float): The tolerance for convergence.

    Returns:
    float: The largest eigenvalue.
    """
    # Initialize a random vector
    b_k = np.random.rand(A.shape[1])

    for _ in range(num_iterations):
        # Compute the matrix-by-vector product Ab
        b_k1 = np.dot(A, b_k)

        # Compute the norm
        b_k1_norm = np.linalg.norm(b_k1)

        # Normalize the vector
        b_k1 = b_k1 / b_k1_norm

        # Check for convergence
        if np.linalg.norm(b_k1 - b_k) < epsilon:
            break

        b_k = b_k1

    # The largest eigenvalue is the norm of the vector before normalization
    prime_eigenvalue = np.dot(A, b_k).dot(b_k) / b_k.dot(b_k)

    return prime_eigenvalue


def largest_eigenvalue(beta, gamma, trajectories, sites_num, num_steps):

    largest_eigenvalues = []
    for t in range(1, num_steps):
        # print("Largest eigenvalue " + "(" + str(t) + " ," + str(0) + ")")
        kernel = np.zeros((sites_num, sites_num))
        for a in range(sites_num):
            for b in range(sites_num):
                # agents who are at b site at time t-1, but at a site at time t
                agents_a = np.where(trajectories[:, t] == a)[0]
                agents_b = np.where(trajectories[:, 0] == b)[0]
                agents_ab = np.intersect1d(agents_a, agents_b)
                if agents_ab.size == 0:
                    break
                beta_ab_t = beta[agents_ab, a]
                gamma_ab_t = gamma[agents_ab, b]
                kernel[a, b] = np.sum(beta_ab_t * gamma_ab_t)
        # for small size matrix
        if sites_num <= 30:
            prime_eigenvalue = max(np.linalg.eigvals(kernel))
        else:
            prime_eigenvalue = power_iteration(kernel)

        largest_eigenvalues.append(prime_eigenvalue)

    return np.array(largest_eigenvalues)


