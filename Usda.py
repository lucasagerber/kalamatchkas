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
        self.api_key = api_key
    
    
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
        self.ndbno = query_result["ndbno"]
        self.name = query_result["name"]
        self.gram = 100
        
        self.nutrients = defaultdict(lambda: dict({'value':0}))
        for nutrient in query_result["nutrients"]:
            nutrient["value"] = float(nutrient["value"])
            self.nutrients[nutrient.pop("nutrient_id")] = nutrient
            
        self.protein = self.nutrients["203"]["value"]
        self.fat = self.nutrients["204"]["value"]
        self.carb = self.nutrients["205"]["value"]
        self.sugar = self.nutrients["269"]["value"]
        
        print(self)
    
    
    def re_gram(self, gram_amt):
        gram_ratio = gram_amt / self.gram
        self.gram = gram_amt
        
        for nutrient in self.nutrients.keys():
            self.nutrients[nutrient]["value"] *= gram_ratio
        
        self.protein *= gram_ratio
        self.fat *= gram_ratio
        self.carb *= gram_ratio
        self.sugar *= gram_ratio
    
    
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