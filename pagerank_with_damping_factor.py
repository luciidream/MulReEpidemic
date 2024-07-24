import numpy as np


def calculate_pagerank(adj_matrix, damping_factor=0.85, max_iterations=100, tol=1e-6):
    """
    Calculate the PageRank with a damping factor for a complex network.

    Parameters:
    adj_matrix (np.ndarray): The adjacency matrix of the network.
    damping_factor (float): The damping factor (default is 0.85).
    max_iterations (int): The maximum number of iterations for the power method.
    tol (float): The tolerance for convergence.

    Returns:
    np.ndarray: The PageRank vector.
    """
    n = adj_matrix.shape[0]
    # Normalize the adjacency matrix columns to represent transition probabilities
    transition_matrix = adj_matrix / adj_matrix.sum(axis=0)
    transition_matrix[np.isnan(transition_matrix)] = 0  # Handle division by zero

    # Initialize the PageRank vector with equal probabilities
    pagerank = np.ones(n) / n

    # Damping vector
    damping_vector = np.ones(n) / n

    for _ in range(max_iterations):
        new_pagerank = (1 - damping_factor) * damping_vector + damping_factor * transition_matrix.dot(pagerank)
        # Check for convergence
        if np.linalg.norm(new_pagerank - pagerank) < tol:
            break
        pagerank = new_pagerank

    return pagerank


def pagerank_to_transfer_matrix(adj_matrix, pagerank):

    sum_vector = np.sum(adj_matrix * pagerank, 1)
    transfer_matrix = adj_matrix * pagerank / sum_vector[:, np.newaxis]

    return transfer_matrix



