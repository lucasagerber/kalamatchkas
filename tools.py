"""
kalamatchkas.tools
saba pilots
description:  general tools file for kalamatchkas program
"""


import os


def verbose_print(verbose, statement):
    if verbose:
        print(statement)


def num_gen():
    i = 0
    while True:
        yield i
        i += 1


def create_destination(result_path, output_name, output_type):
    destination = result_path + '/' + output_name + '.' + output_type
    log_by_sum_destination = result_path + '/' + output_name + '_log_by_sum' + '.' + output_type
    log_by_food_destination = result_path + '/' + output_name + '_log_by_food' + '.' + output_type
    
    i = (i+1 for i in num_gen())
    while os.path.exists(destination):
        number = str(next(i))
        destination = result_path + '/' + output_name + number + '.' + output_type
        log_by_sum_destination = result_path + '/' + output_name + number + '_log_by_sum' + '.' + output_type
        log_by_food_destination = result_path + '/' + output_name + number + '_log_by_food' + '.' + output_type
        
    return destination, log_by_sum_destination, log_by_food_destination


def main():
    pass


if __name__ == '__main__':
    main()