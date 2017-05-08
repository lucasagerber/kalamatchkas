"""
kalamatchkas.tools
saba pilots
description:  general tools file for kalamatchkas program
"""


import os
from .config import LINE_BEGIN


def k_print(statement, verbose=True, line=LINE_BEGIN):
    """Prints with LINE_BEGIN if option is on."""
    if verbose:
    
        if type(statement) == str:
            print(line + statement)
        elif type(statement) == dict:
            for k, v in statement.items():
                print("{}{} : {}".format(line, k, v))
        elif type(statement) == list:
            for i in statement:
                print(line + str(i))
        else:
            print(statement)
            
    
def test_print(test, statement, name, verbose=True):
    """Prints results of test."""
    if not test:
        k_print(statement, verbose)
    
    k_print("{} test found {}".format(name, str(test)), verbose)
    
    
def num_gen():
    i = 1
    while True:
        yield i
        i += 1


def create_destination(result_path, output_name, output_type, destination_names=["", "_detail", "_log_by_sum","_log_by_food"]):
    """Creates new destination file names for a recipe."""
    full_name = result_path + '/' + output_name
    i = (i for i in num_gen())
    
    number = str(next(i))
    destination_list = ["{}{}{}.{}".format(full_name, number, name, output_type) for name in destination_names]
    
    while os.path.exists(destination_list[0]):
        number = str(next(i))
        destination_list = ["{}{}{}.{}".format(full_name, number, name, output_type) for name in destination_names]
        
    return destination_list

    
def order_columns(column_list, keys=["food","serving","gram"]):
    """Order a list of columns to include food, servings, grams first, with any other optional keys."""
    column_dict = {col:i for i,col in enumerate(column_list)}
    
    for i, key in enumerate(keys):
        try:
            column_dict[key] = i - len(keys)
        except KeyError:
            k_print("KeyError when ordering columns" + key)
        
    return sorted(column_list, key=lambda col: column_dict[col])
    

def main():
    pass


if __name__ == '__main__':
    main()