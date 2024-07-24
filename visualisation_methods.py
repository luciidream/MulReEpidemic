import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def lambda_curve(lambda_M, num_steps):

    x = np.linspace(1, num_steps-1, num_steps-1)
    y = np.real(lambda_M)

    sns.set(style="darkgrid")
    plt.figure(figsize=(16, 12), dpi=400)
    plt.plot(x, y, marker='o', markersize=5, linewidth=2, color='red')
    plt.title('Largest Eigenvalue Real Parts', fontsize=30)
    plt.xlabel('Time', fontsize=25)
    plt.xticks(fontsize=20)
    plt.ylabel('Largest Eigenvalue', fontsize=25)
    plt.xticks(fontsize=20)
    plt.show()
