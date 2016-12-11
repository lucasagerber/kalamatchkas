"""
kalamatchkas.Diet
saba pilots
description:  Diet object, information on person's diet
12.10.16
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
        self.__name = diet_name
        self.__meals = OrderedDict(meals)
        self.__calorie_error = calorie_error
        self.__macronutrient_rules = macronutrient_rules
        
        print(self)


    @property
    def name(self):
        return self.__name
    
    
    @property
    def meals(self):
        return self.__meals
    
    
    @property
    def calories(self):
        return sum(self.__meals.values())
    
    
    @property
    def calorie_error(self):
        return self.__calorie_error
    
    
    @property
    def calorie_range(self):
        return [ ('total_cal', self.calories*(1-self.calorie_error), self.calories*(1+self.calorie_error)) ]
    
    
    @property
    def macronutrient_rules(self):
        return self.__macronutrient_rules
    
    
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
        