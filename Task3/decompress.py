from repo import read_matr
from repo import save_image
import numpy


def decompr(path_in, path_out):
    loaded_matrices = read_matr(path_in)
    decompresed_matrices = []

    for U, S, V in loaded_matrices:
        reconstructed_channel = (U @ S @ V).clip(0, 255).astype(numpy.uint8)
        decompresed_matrices.append(reconstructed_channel)
        
    save_image(decompresed_matrices, path_out)
