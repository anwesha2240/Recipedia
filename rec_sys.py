import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from ingredient_parser import ingredient_parser
import joblib
import config
import ast

# Top-N recommendations ordered by score
def get_recommendations(N, scores):
    # Load in recipe dataset
    df_recipes = pd.read_csv(config.PARSED_PATH)
    # Order the scores and filter to get the highest N scores
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]
    # Create a DataFrame to load in recommendations
    recommendation = pd.DataFrame(columns=['recipe', 'ingredients', 'score', 'url'])
    count = 0
    for i in top:
        recommendation.at[count, 'recipe'] = title_parser(df_recipes['recipe_name'][i])
        recommendation.at[count, 'ingredients'] = ingredient_parser_final(df_recipes['ingredients'][i])
        recommendation.at[count, 'url'] = df_recipes['recipe_urls'][i]
        recommendation.at[count, 'score'] = "{:.3f}".format(float(scores[i]))
        count += 1
    return recommendation

# Neaten the ingredients being outputted
def ingredient_parser_final(ingredient):
    if isinstance(ingredient, list):
        ingredients = ingredient
    else:
        ingredients = ast.literal_eval(ingredient)

    ingredients = ','.join(ingredients)
    # Remove diacritics without unidecode
    ingredients = ''.join(char for char in ingredients if char.isascii() or char.isspace())
    return ingredients

def title_parser(title):
    # Remove diacritics without unidecode
    title = ''.join(char for char in title if char.isascii() or char.isspace())
    return title

def RecSys(ingredients, N=5):
    """
    The recommendation system takes in a list of ingredients and returns a list of top 5
    recipes based on cosine similarity.
    :param ingredients: a list of ingredients
    :param N: the number of recommendations returned
    :return: top 5 recommendations for cooking recipes
    """

    # Load in TF-IDF model and encodings
    tfidf_encodings = joblib.load(config.TFIDF_ENCODING_PATH)
    tfidf = joblib.load(config.TFIDF_MODEL_PATH)

    # Parse the ingredients using my ingredient_parser
    try:
        ingredients_parsed = ingredient_parser(ingredients)
    except:
        ingredients_parsed = ingredient_parser([ingredients])

    # Concatenate the list of ingredients into a single string
    ingredients_string = ' '.join(ingredients_parsed)

    # Use our pretrained TF-IDF model to encode our input ingredients
    ingredients_tfidf = tfidf.transform([ingredients_string])  # Pass a list with a single string

    # Calculate cosine similarity between actual recipe ingredients and test ingredients
    cos_sim = map(lambda x: cosine_similarity(ingredients_tfidf, x), tfidf_encodings)
    scores = list(cos_sim)

    # Filter top N recommendations
    recommendations = get_recommendations(N, scores)
    return recommendations


if __name__ == "__main__":
    # Test ingredients
    test_ingredients = "pasta, tomato, onion"
    recs = RecSys(test_ingredients)
    print(recs)


