"""
kalamatchkas.tools
saba pilots
description:  general tools file for kalamatchkas program
"""


import os
from .config import LINE_BEGIN


def k_print(statement, verbose=True):
    """Prints with LINE_BEGIN if option is on."""
    if verbose:
        print(LINE_BEGIN + statement)


def num_gen():
    i = 0
    while True:
        yield i
        i += 1


def create_destination(result_path, output_name, output_type, destination_names=["", "_detail", "_log_by_sum","_log_by_food"]):
    """Creates new destination file names for a recipe."""
    full_name = result_path + '/' + output_name
    i = (i for i in num_gen())
    
    number = str(next(i))
    destination_list = ["{0}{1}{2}.{3}".format(full_name, number, name, output_type) for name in destination_names]
    
    while os.path.exists(destination_list[0]):
        number = str(next(i))
        destination_list = ["{0}{1}{2}.{3}".format(full_name, number, name, output_type) for name in destination_names]
        
    return destination_list


def main():
    pass


if __name__ == '__main__':
    main()