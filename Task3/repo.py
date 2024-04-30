from PIL import Image 
from numpy import array
from numpy import savez
from numpy import stack
from numpy import load
from numpy import uint8

def save_image(dec_mat, name):
    decompressed_image_array = stack(dec_mat, axis=-1).astype(uint8)
    decompressed_image = Image.fromarray(uint8(decompressed_image_array))
    decompressed_image.save(f"comp_image/{name}")

def read_image(path):
    im = Image.open(path)
    im_array = array(im)
    return im_array, im.size

def save_matr(path, matrix): 
    savez(f'{path}.npz', 
            **{'U_channel_{}'.format(i): matrix[0] for i, matrix in enumerate(matrix)},
            **{'S_channel_{}'.format(i): matrix[1] for i, matrix in enumerate(matrix)},
            **{'V_channel_{}'.format(i): matrix[2] for i, matrix in enumerate(matrix)})
    
def read_matr(path):
    loaded_matrices = []
    with load(f'{path}.npz') as data:
        for i in range(3):
            U = data[f'U_channel_{i}']
            S = data[f'S_channel_{i}']
            V = data[f'V_channel_{i}']
            loaded_matrices.append((U, S, V))
    return loaded_matrices