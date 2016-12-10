"""
kalamatchkas.FoodList
saba pilots
description:  FoodList object, dataframe of potential ingredients with nutritional information
12.01.16
"""


from collections import OrderedDict
from .config import LINE_BEGIN


class Diet(object):

    def __init__(self,
            diet_name,
            meals=[('breakfast',400),('lunch',700),('dinner',700)],
            calorie_error=.05,
            macronutrient_rules=[('protein_cal_%',.15,.30), ('fat_cal_%',.15,.25), ('carb_cal_%',.45,.60)]
        ):
        """Creates a diet object."""
        self.name = diet_name
        self.meals = OrderedDict(meals)
        self.calories = sum(self.meals.values())
        self.calorie_error = calorie_error
        self.calorie_range = [ ('total_cal', self.calories*(1-self.calorie_error), self.calories*(1+self.calorie_error)) ]
        self.macronutrient_rules = macronutrient_rules
        
        print(self)
    
    
    def __str__(self):
        print_string = "\n" + LINE_BEGIN + self.name + ":\n" + LINE_BEGIN + str(len(self.meals.keys())) + " meals:\n"
        for meal, cals in self.meals.items():
            print_string += LINE_BEGIN + "    " + meal.title() + ", " + str(cals) + " calories\n"
            
        print_string += LINE_BEGIN + "With the following dietary rules:\n"
        for name, min_val, max_val in self.macronutrient_rules:
            name = name.split('_')[0]
            print_string += LINE_BEGIN + "    Percent of calories from " + name.title() + ", " + str(min_val*100) + '% to ' + str(max_val*100) + '%\n'

        return print_string
        

def main():
    pass
    
    
if __name__ == "__main__":
    main()            
        