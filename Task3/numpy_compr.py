from numpy import diag
from repo import read_image
from repo import save_matr
from numpy.linalg import svd

def singular_numpy(path_in, path_out, N): 
    im, (first, second) = read_image(path_in)
    matrix_result = []

    k = int(first * second / (8 * N * (first + second + 1)))

    for channel in range(3):
        U, S, V = svd(im[:, :, channel])
        matrix_result.append((U[:, :k], diag(S[:k]), V[:k, :]))

    save_matr(path_out, matrix_result)

    

