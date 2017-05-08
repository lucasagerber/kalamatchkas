"""
kalamatchkas.Usda
saba pilots
description:  api for searching the usda database
11.28.16
"""


import json
import urllib.request
import urllib.parse
from .Food import Food


# base url for searching usda database
BASE_URL = "http://api.nal.usda.gov/ndb/"


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
            type="f", #(b)asic or (f)ull
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
        except urllib.error.URLError:
            print("ERROR:  Well, it appears the USDA is down.")

    
    
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