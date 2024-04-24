import streamlit as st
from PIL import Image
from rec_sys import RecSys


def make_clickable(name, link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = name
    return f'<a target="_blank" href="{link}">{text}</a>'

def main():
    image = Image.open("input/wordcloud.png").resize((680, 150))
    st.image(image)
    st.markdown("# *Recipedia :cooking:*")

    st.markdown(
        "An ML-powered app by Group-29 <a href='https://github.com' > <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/600px-Octicons-mark-github.svg.png' width='20' height='20' > </a> ",
        unsafe_allow_html=True,
    )
    st.markdown(
        "## Given a list of ingredients, what different recipes can we make? :tomato: "
    )
    st.markdown(
        "For example, what recipes can you make with the food in your apartment? The ML based model will look through over 4500 recipes to find matches for you... :mag: Try it out for yourself below! :arrow_down:"
    )

    st.text("")

    # Session state dictionary
    session_state = st.session_state
    if not hasattr(session_state, 'recipe_df'):
        session_state.recipe_df = ""
    if not hasattr(session_state, 'recipes'):
        session_state.recipes = ""
    if not hasattr(session_state, 'model_computed'):
        session_state.model_computed = False
    if not hasattr(session_state, 'execute_recsys'):
        session_state.execute_recsys = False
    if not hasattr(session_state, 'recipe_df_clean'):
        session_state.recipe_df_clean = ""

    ingredients = st.text_input("Enter ingredients you would like to cook with")
    session_state.execute_recsys = st.button("Give me recommendations!")

    if session_state.execute_recsys:
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            gif_runner = st.image("input/cooking_gif.gif")
        recipe = RecSys(ingredients)
        gif_runner.empty()
        session_state.recipe_df_clean = recipe.copy()
        # link is the column with hyperlinks
        recipe["url"] = recipe.apply(
            lambda row: make_clickable(row["recipe"], row["url"]), axis=1
        )
        recipe_display = recipe[["recipe", "url", "ingredients", "score"]]
        session_state.recipe_display = recipe_display.to_html(escape=False)
        session_state.recipes = recipe.recipe.values.tolist()
        session_state.model_computed = True
        session_state.execute_recsys = False

    if session_state.model_computed:
        recipe_all_box = st.selectbox(
            "Either see the top 5 recommendations or pick a particular recipe you fancy",
            ["Show me them all!", "Select a single recipe"],
        )
        if recipe_all_box == "Show me them all!":
            st.write(session_state.recipe_display, unsafe_allow_html=True)
        else:
            selection = st.selectbox(
                "Select a delicious recipe", options=session_state.recipes
            )
            selection_details = session_state.recipe_df_clean.loc[
                session_state.recipe_df_clean.recipe == selection
            ]

            # Display recipe details with each ingredient as a bullet point
            st.markdown(f"**Recipe:** {selection_details.recipe.values[0]}")
            st.markdown(f"**URL:** {selection_details.url.values[0]}")
            # Display recipe details with each ingredient as a checkbox bullet point
            st.markdown("**Ingredients:**")
            ingredients_list = selection_details.ingredients.values[0].split(',')

            col1, col2 = st.columns(2)

            # Calculate the split point for the ingredients list
            split_point = len(ingredients_list) // 2

            # Display the first half of ingredients in the first column
            for ingredient in ingredients_list[:split_point]:
                checkbox_state = col1.checkbox(f"{ingredient.strip()}")

            # Display the second half of ingredients in the second column
            for ingredient in ingredients_list[split_point:]:
                checkbox_state = col2.checkbox(f"{ingredient.strip()}")

            score_percentage = float(selection_details.score.values[0])
            st.markdown(f"**How much the recipe meets your ingredients:** {score_percentage:.2f}%")


if __name__ == "__main__":
    main()
