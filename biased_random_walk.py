import numpy
import numpy as np
import random


def update_bias_vector(bias_matrix, relation_matrix, transfer_matrix, agent_network, agent_id):
    """Update the bias vector for a given agent based on its neighbors."""
    neighbors = list(agent_network.neighbors(agent_id))
    if not neighbors:
        return bias_matrix[agent_id]

    # Sum the neighbors' bias vectors weighted by the relation matrix
    new_bias_vector = bias_matrix[agent_id]
    for neighbor in neighbors:
        new_bias_vector += (bias_matrix[neighbor] * relation_matrix[agent_id, neighbor])
    new_bias_vector = transfer_matrix @ new_bias_vector

    # Normalize the derived vector
    new_bias_vector /= np.sum(new_bias_vector)
    # update the bias matrix
    bias_matrix[agent_id] = new_bias_vector
    return new_bias_vector


def biased_random_walk(sites_network, bias_matrix, agent_id, num_steps):
    """Perform a biased random walk for a given agent on the network."""
    current_node = random.choice(list(sites_network.nodes()))
    trajectory = [current_node]

    for _ in range(num_steps):
        neighbors = list(sites_network.neighbors(current_node))
        if not neighbors:
            break

        # Calculate probabilities based on bias matrix
        probabilities = [bias_matrix[agent_id, neighbor] for neighbor in neighbors]
        probabilities = np.array(probabilities) / np.sum(probabilities)

        # Choose the next node based on the biased probabilities
        next_node = np.random.choice(neighbors, p=probabilities)
        trajectory.append(next_node)
        current_node = next_node

    return trajectory


def pop_next_site(sites_network, bias_matrix, agent_id, current_node):
    """Pop next site in a biased random walk."""

    neighbors = list(sites_network.neighbors(current_node))
    if not neighbors:
        return

    # Calculate probabilities based on bias matrix
    probabilities = [bias_matrix[agent_id, neighbor] for neighbor in neighbors]
    probabilities = np.array(probabilities) / np.sum(probabilities)

    # Choose the next node based on the biased probabilities
    next_node = np.random.choice(neighbors, p=probabilities)

    return next_node


def generate_trajectories(N, agents_network, sites_network, bias_matrix, relation_matrix, transfer_matrix, num_steps):
    """Generate trajectories for each agent."""
    trajectories = np.zeros((N, num_steps))
    for step in range(num_steps):
        print("Walking at " + str(step))
        for agent_id in range(N):
            if step == 0:
                current_node = random.choice(list(sites_network.nodes()))
                trajectories[agent_id][0] = current_node
            else:
                # Update bias vector for each agent
                bias_matrix[agent_id] = update_bias_vector(bias_matrix, relation_matrix, transfer_matrix,
                                                           agents_network, agent_id)

            # Perform biased random walk for each agent
                next_node = pop_next_site(sites_network, bias_matrix, agent_id, trajectories[agent_id][step-1])
                trajectories[agent_id][step] = next_node

    trajectories = trajectories.astype(numpy.int64)

    return trajectories
