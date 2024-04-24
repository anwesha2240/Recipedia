import requests
from bs4 import BeautifulSoup
import pandas as pd

# Jamie Oliver recipe website
url = "https://www.jamieoliver.com/recipes/category/course/mains/"
page = requests.get(url)

# Initializing DataFrame to store the scraped URLs
recipe_url_df = pd.DataFrame() 

# BeautifulSoup enables to find the elements/tags in a webpage
soup = BeautifulSoup(page.text, "html.parser")

# Different food catergories on JamieOliver website
food_cat = ["mains", "snacks", "breakfast", "desserts"]

# Selecting all the 'a' tags (URLs) present in the webpage and extracting 
# their 'href' attribute
recipe_urls = pd.Series([a.get("href") for a in soup.find_all("a")])

# All the recipes contain '-' and the '/recipes/' etc etc ...
recipe_urls = recipe_urls[(recipe_urls.str.count("-")>0) 
                         & (recipe_urls.str.contains("/recipes/")==True)
                         & (recipe_urls.str.contains("-recipes/")==True)
                         & (recipe_urls.str.contains("course")==False)
                         & (recipe_urls.str.contains("books")==False)
                         & (recipe_urls.str.endswith("recipes/")==False)
                         ].unique()

# DataFrame to store the scraped URLs
df = pd.DataFrame({"recipe_urls":recipe_urls})
df['recipe_urls'] = "https://www.jamieoliver.com" + df['recipe_urls'].astype('str')
# Appending 'df' to a main DataFrame 'init_urls_df'
recipe_url_df = pd.concat([recipe_url_df, df], ignore_index=True).copy()

recipe_url_df.to_csv('recipe_urls.csv')

