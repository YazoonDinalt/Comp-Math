from repo import read_image
from repo import save_matr
import numpy as np
import time
from PIL import Image

def singular_simple(path_in, path_out, N):


    im, (first, second) = read_image(path_in)
    result_matrix = []

    k = int(first * second / (8 * N * (first + second + 1)))



    for channel in range(3):
        matrix = im[:, :, channel]
        cols = matrix.shape[1]
        svd = []

        for i in range(0, cols):
            new_matrix = matrix
            for u, s_num, v in svd[:i]:
                new_matrix = new_matrix - s_num * np.outer(u, v)
            vector = np.random.randn(cols)
            norm_vector = vector / np.linalg.norm(vector)
            v = new_matrix.T @ new_matrix @ norm_vector
            v = v / np.linalg.norm(v)
            u = matrix @ v
            s = np.linalg.norm(u)
            u = u / s
            svd.append((u, s, v))

        U, S, V = [], [], []
        for i in range(0, len(svd)):
            U.append(svd[i][0])
            S.append(svd[i][1])
            V.append(svd[i][2])
        U, S, V = np.array(U), np.array(S), np.array(V)

        result_matrix.append((U.T[:, :k], np.diag(S[:k]), V[:k, :]))

    save_matr(path_out, result_matrix)