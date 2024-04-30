from info import inform_message
from arg_creator import createParser
from numpy_compr import singular_numpy 
from advanced_compr import singular_advanced
from simple_compr import singular_simple
from decompress import decompr


def main(): 
    namespace = createParser().parse_args()

    inform_message()

    match namespace.mode: 
        case "compress"   : 
            match namespace.method:
                case "numpy"    : singular_numpy(namespace.in_path, namespace.out_file, namespace.compression)
                case "simple"   : singular_simple(namespace.in_path, namespace.out_file, namespace.compression)
                case "advanced" : singular_advanced(namespace.in_path, namespace.out_file, namespace.compression) 
        case "decompress" :
            decompr(namespace.in_path, namespace.out_file)
            

if __name__ == '__main__':
    main()
