import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture


def draw_y1(data, n_comp:int, aug) -> np.ndarray:
    size = data.shape[0]
    gmm = GaussianMixture(n_components=n_comp)
    gmm.fit(data)
    y1, _ = gmm.sample(size*aug)

    return y1


def make_r(data) -> np.ndarray:
    r = np.ones_like(data[:,1:])
    col_num = data.shape[1]
    for col_index in range(0, col_num-1) : 
        r[:,col_index] = data[:,col_index+1]/data[:,0]

    return r


def make_alpha(data) -> np.ndarray:
    means = np.mean(data, axis=0)
    variances = np.std(data, axis=0)

    alpha = means**2 / variances

    return alpha


def make_r_comb(size:int) -> np.ndarray:
    x = np.repeat(np.arange(size), size)
    y = np.tile(np.arange(size), size)

    mask = x < y
    x = x[mask]
    y = y[mask]
    unique_pairs = np.unique(np.column_stack((x, y)), axis=0)

    return unique_pairs


def make_rs_matrix(data, aug) -> np.ndarray:
    size = data.shape[0]
    r = make_r(data)
    r_comb = make_r_comb(size)
    lamb = np.random.dirichlet(make_alpha(r), r_comb.shape[0])
    rs_matrix = lamb * r[r_comb[:, 0]] + (1-lamb) * r[r_comb[:, 1]]

    # SRS len(r)*aug many samples from rs_matrix
    index = np.random.randint(0,len(rs_matrix), len(r) * aug)
    rs_df = rs_matrix[index]

    return rs_df


def draw_y1(data, n_comp, aug=5) -> np.ndarray:
    size = data.shape[0]
    gmm = GaussianMixture(n_components=n_comp)
    gmm.fit(data)
    y1, _ = gmm.sample(size*aug)

    return np.squeeze(y1)
