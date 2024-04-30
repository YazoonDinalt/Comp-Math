import argparse 

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['compress', 'decompress'])
    parser.add_argument('--method', choices=['numpy','simple','advanced'], default='simple')
    parser.add_argument('--compression', type=int, default=50)
    parser.add_argument('--in_path', type=str)
    parser.add_argument('--out_file', type=str, default='out.png')
    
    return parser