import numpy as np
import scipy
from repo import read_image
from repo import save_matr

def singular_advanced(path_in, path_out, N):


    im, (first, second) = read_image(path_in)
    k = int(first * second / (8 * N * (first + second + 1)))
    result_matrix = [] 

    for channel in range(3):
        A = im[:,:, channel]   
        n = A.shape[1]
        B = np.random.randn(n, k)
        Q = scipy.linalg.qr(A @ scipy.linalg.qr(A.T @ scipy.linalg.qr(A @ B)[0])[0])[0]
        B = Q.T @ A
        U, S, V = np.linalg.svd(B)
        U = Q @ U
        result_matrix.append((U[:, :k], np.diag(S[:k]), V[:k, :]))

    save_matr(path_out, result_matrix)
