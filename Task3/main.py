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
                case "numpy"    : singular_numpy("image/Lake.bmp", "helpi", 10)
                case "simple"   : singular_simple("image/Lake.bmp", "helpi", 3)
                case "advanced" : singular_advanced("image/Lake.bmp", "helpi", 5) 
        case "decompress" :
            decompr("helpi", "simple/Lake_x3.bmp")
            

if __name__ == '__main__':
    main()
