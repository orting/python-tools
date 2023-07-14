import os
import sys
import argparse
from multiprocessing import Pool
from subprocess import run
import csv

def main():
    description = '''Run python script in parallel.'''
    parser = argparse.ArgumentParser(description)
    parser.add_argument('script', type=str, help='Path to script')
    parser.add_argument('params_file', type=str, help='''csv file containing parameters.
    One row for each invocation of script.
    First line is a header.
    Named columns are passed as named arguments, --<column-name> <column-value>.
    Unnamed columns are passed as positional arguments.''')
    parser.add_argument('--interpreter', type=str, default=None,
                        help='Python interpreter used to run script')
    parser.add_argument('--num-workers', type=int, default=4)
    parser.add_argument('--silent', action='store_true',
                        help='''If set, do not print anything. Otherwise print the result of calls
                        with non-zero returncode.''')
    args = parser.parse_args()

    params_list = []
    with open(args.params_file) as infile:
        reader = csv.reader(infile)
        header = next(reader)
        for row in reader:
            if len(row) != len(header):
                continue
            if args.interpreter is not None:
                params = [args.interpreter, args.script]
            else:
                params = [args.script]
            for param_name, param in zip(header, row):
                if param_name != '':
                    params.append(f'--{param_name}')
                params.append(param)
            params_list.append(params)

    errors = []
    with Pool(args.num_workers) as pool:
        for result in pool.imap_unordered(run, params_list):
            if result.returncode != 0:
                errors.append(result)
                print(result)
    if len(errors) > 0:
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
