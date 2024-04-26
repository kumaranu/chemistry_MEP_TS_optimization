import torch
import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt

def randomly_initialize_path(path, n_points, order_points=False, seed=1910):
    #times = rnd.uniform(shape=(n_points, 1), minval=0.1, maxval=0.9)
    times = torch.unsqueeze(torch.linspace(0, 1, n_points+2)[1:-1], -1)
    times.requires_grad = False

    n_dims = len(path.initial_point)
    rnd_dims = []
    for idx in range(n_dims):
        min_val = torch.min(
            torch.tensor([path.initial_point[idx], path.final_point[idx]])
        ).item()
        max_val = torch.max(
            torch.tensor([path.initial_point[idx], path.final_point[idx]])
        ).item()
        print("MIN MAX", min_val, max_val)
        rnd_vals = rnd.uniform(size=(n_points, 1), low=min_val, high=max_val)
        if order_points or idx == 0:
            if path.initial_point[idx] > path.final_point[idx]:
                rnd_dims.append(-1*np.sort(-1*rnd_vals, axis=0))
            else:
                rnd_dims.append(np.sort(rnd_vals, axis=0))
        else:
            rnd_dims.append(rnd_vals)
    print(len(rnd_dims), rnd_dims[0].shape)
    rnd_dims = torch.tensor(
        np.concatenate(rnd_dims, axis=-1), requires_grad=False
    )
    
    return initialize_path(path, times, rnd_dims)


def loss_init(path, times, points):
    preds = path.geometric_path(times)
    return torch.mean((points - preds)**2)


def initialize_path(path, times, init_points, lr=0.001, max_steps=5000):

    print("INFO: Beginning path initialization")
    loss, prev_loss = torch.tensor([2e-10]), torch.tensor([1e-10])
    print(path.named_parameters())
    optimizer = torch.optim.Adam(path.parameters(), lr=lr)
    idx, rel_error = 0, 100
    while (idx < 1500 or loss > 1e-8) and idx < max_steps:
        optimizer.zero_grad()

        prev_loss = loss.item()
        loss = loss_init(path, times, init_points)

        loss.backward()
        optimizer.step()
        rel_error = np.abs(prev_loss - loss.item())/prev_loss
        idx = idx + 1
        if idx % 250 == 0:
            print(f"\tIteration {idx}: Loss {loss:.4} | Relative Error {rel_error:.5}")
            fig, ax = plt.subplots()
            path_output = path.get_path()
            geometric_path = path_output.geometric_path.detach().numpy()
            ax.plot(init_points[:,0], init_points[:,1], 'ob')
            ax.plot(geometric_path[:,0], geometric_path[:,1], '-k')
            fig.savefig(f"./plots/initialization/init_path_{idx}.png")

        #print(prev_loss, loss, jnp.abs(prev_loss - loss)/prev_loss)
    
    print(f"INFO: Finished path initialization after {idx} iterations")
    fig, ax = plt.subplots()
    path_output = path.get_path()
    geometric_path = path_output.geometric_path.detach().numpy()
    ax.plot(init_points[:,0], init_points[:,1], 'ob')
    ax.plot(geometric_path[:,0], geometric_path[:,1], '-k')
    fig.savefig("./plots/init_path.png")

    return path









