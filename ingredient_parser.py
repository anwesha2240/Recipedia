import string
import ast
import pandas as pd
from stopwordsiso import stopwords as stopwords_package


def remove_accents(word):
    return ''.join(char for char in word if char.isalnum() or char.isspace())


def preprocess_text(text):
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    items = [word for word in text.split() if word.isalpha()]
    items = [word.lower() for word in items]
    items = [remove_accents(word) for word in items]
    return items


def lemmatize_basic(word):
    # Basic lemmatization, you can replace this with a more sophisticated approach if needed
    # This is just an example
    return word


def ingredient_parser(ingredients):
    measures = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', ...]
    words_to_remove = ['fresh', 'oil', 'a', 'red', 'bunch', ...]

    ingred_list = []

    if isinstance(ingredients, list):
        ingredients = ingredients
    else:
        ingredients = ast.literal_eval(ingredients)

    stop_words = set(stopwords_package("en"))

    for i in ingredients:
        items = preprocess_text(i)
        items = [lemmatize_basic(word) for word in items]
        items = [word for word in items if word not in measures]
        items = [word for word in items if word not in words_to_remove]
        items = [word for word in items if word not in stop_words]

        if items:
            ingred_list.append(' '.join(items))

    return ingred_list


# Read the CSV file
csv_file_path = "./input/df_recipes.csv"
recipe_df = pd.read_csv(csv_file_path)

# Assuming 'ingredients' is the column containing the ingredients
recipe_df['ingredients_parsed'] = recipe_df['ingredients'].apply(ingredient_parser)

# Save the updated DataFrame to a new CSV file
output_csv_path = "./input/recipe_urls.csv"
recipe_df.to_csv(output_csv_path, index=False)
