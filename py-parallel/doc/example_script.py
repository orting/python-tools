import argparse
import sys

def main():
    description = '''Example script illustrating use of py_parallel'''
    parser = argparse.ArgumentParser(description)
    parser.add_argument('pos_arg1', type=str)
    parser.add_argument('pos_arg2', type=str)
    parser.add_argument('--named-arg1', type=str, default=None)
    parser.add_argument('--named-arg2', type=int, default=1)
    args = parser.parse_args()
    
    return args.named_arg2 < 1


if __name__ == '__main__':
    sys.exit(main())
