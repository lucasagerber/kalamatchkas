"""
kalamatchkas.usda
saba pilots
description:  api for searching the usda database
11.28.16
"""


import json
import urllib.request
import urllib.parse
from collections import defaultdict
from .config import BASE_URL


class Usda(object):

    def __init__(self, api_key):
        self.__api_key = api_key


    @property
    def api_key(self):
        return self.__api_key
        
    
    def search(self,
            q,
            ds="Standard Reference",
            fg="",
            sort="r",
            max=25,
            offset=0,
            format="json"):
        """Search the USDA food database for a food from query terms using their API."""
        query_term_names = ["api_key","q","ds","fg","sort","max","offset","format"]
        query_term_values = [self.api_key,q,ds,fg,sort,max,offset,format]
        query_dict = {name:value  for name, value in zip(query_term_names, query_term_values)}
        
        url = url_ize(BASE_URL, "search", query_dict)
        
        url_result = urllib.request.urlopen(url).read().decode()
        json_result = json.loads(url_result)["list"]
        items = json_result["item"]
        
        return items

        
    def food_report(self,
            ndbno,
            type="b",
            format="json"):
        """Look up the nutrition information on a food in the USDA food database using their API."""
        query_term_names = ["api_key","ndbno","type","format"]
        query_term_values = [self.api_key,ndbno,type,format]
        query_dict = {name:value  for name, value in zip(query_term_names, query_term_values)}
        
        url = url_ize(BASE_URL, "reports", query_dict)
        
        try:
            url_result = urllib.request.urlopen(url).read().decode()
            json_result = json.loads(url_result)["report"]
        
            food_info = json_result["food"]
        
            return Food(food_info)
        except urllib.error.HTTPError:
            print("ERROR:  Couldn't find this number: " + ndbno)
    
    

class Food(object):

    def __init__(self, query_result):
        self.__ndbno = query_result["ndbno"]
        self.__name = query_result["name"]
        self.__gram = 100
        
        self.__nutrients = defaultdict(lambda: dict({'value':0}))
        for nutrient in query_result["nutrients"]:
            nutrient["value"] = float(nutrient["value"])
            self.__nutrients[nutrient.pop("nutrient_id")] = nutrient
            
        self.__protein = self.__nutrients["203"]["value"]
        self.__fat = self.__nutrients["204"]["value"]
        self.__carb = self.__nutrients["205"]["value"]
        self.__sugar = self.__nutrients["269"]["value"]
        
        print(self)


    @property
    def ndbno(self):
        return self.__ndbno


    @property
    def name(self):
        return self.__name


    @property
    def gram(self):
        return self.__gram


    @property
    def nutrients(self):
        return self.__nutrients


    @property
    def protein(self):
        return self.__protein


    @property
    def fat(self):
        return self.__fat


    @property
    def carb(self):
        return self.__carb


    @property
    def sugar(self):
        return self.__sugar
        
    
    def re_gram(self, gram_amt):
        gram_ratio = gram_amt / self.__gram
        self.__gram = gram_amt
        
        for nutrient in self.__nutrients.keys():
            self.__nutrients[nutrient]["value"] *= gram_ratio
        
        self.__protein *= gram_ratio
        self.__fat *= gram_ratio
        self.__carb *= gram_ratio
        self.__sugar *= gram_ratio
    
    
    def __str__(self):
        return self.ndbno + ":  " + self.name

    
    
def url_ize(base, type, query_dict):
    """Return a url based on a base, type, and dictionary of query terms."""
    query_string = urllib.parse.urlencode(query_dict)
    url = base + "/" + type + "/?" + query_string
    return url
    
    
def main():
    pass
    #usda = Usda(API_KEY)
    #print(usda.search("chicken"))
    #print(usda.food_report("01009"))
    
    
if __name__ == "__main__":
    main()