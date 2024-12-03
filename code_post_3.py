import numpy as np
import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

dessert = pd.read_csv("C:\\Users\\alyss\\BYU\\Stat 386\\lab-06-alyssajford\\dessert_cookies.csv")

st.write("Find Your Favorite Dessert")

tab1, tab2 = st.tabs(["Dessert Adjectives", "Ranked Desserts"])

desserts_data = dessert.iloc[:100]
cookies_data = dessert.iloc[100:]

# Dropdown to filter by type
filter_type = st.sidebar.radio("Select Type:", options=["Desserts", "Cookies", "Both"])


if filter_type == "Desserts":
    filtered_dataset = desserts_data
elif filter_type == "Cookies":
    filtered_dataset = cookies_data
else:  # "Both"
    filtered_dataset = dessert

# List of adjectives (you can modify this if needed)
list_dessert = ["Delicious", "Yummy", "Sweet", "Moist", "Perfect", "Tasty", "Rich", "Creamy", "Fluffy", "Crispy",
                "Crunchy", "Buttery", "Juicy", "Tender", "Heavenly", "Amazing", "Incredible", "Scrumptious", "Mouthwatering",
                "Flavorful", "Soft", "Goey", "Divine"]

with tab1:
    st.write("### List of Adjectives:")
    st.write(", ".join(list_dessert))
    # Sidebar input for adjective
    input_adjective = st.sidebar.text_input("Enter an adjective from the list:", "")

    if input_adjective:
        input_adjective = input_adjective.capitalize()  # Capitalize for consistency
        if input_adjective in list_dessert:
            # Filter the dataset for rows containing the adjective in the description column
            if 'Comment' in filtered_dataset.columns:
                filtered_data = filtered_dataset[filtered_dataset['Comment'].str.contains(input_adjective, case=False, na=False)]
                
                # Display the filtered data (only 'title' and 'rank')
                if not filtered_data.empty:
                    st.write(f"{filter_type} that contain the adjective '{input_adjective}':")
                    st.write(filtered_data[['Recipe_Name', 'Rank']])
                else:
                    st.write(f"No {filter_type.lower()} found with the adjective '{input_adjective}'.")
            else:
                st.error("The column 'Comment' was not found in the dataset.")
        else:
            st.write("Please enter a valid adjective from the list.")
    else:
        st.write("Enter an adjective from the list to filter.")

with st.expander("See Comparison Graph"):
        # Count how many recipes contain the adjective
        adjective_count = filtered_dataset[filtered_dataset['Comment'].str.contains(input_adjective, case=False, na=False)].shape[0]
        
        # Total number of recipes
        total_count = filtered_dataset.shape[0]

        # Create a bar chart comparing the adjective count vs total count
        fig, ax = plt.subplots()
        ax.bar(['With Adjective', 'Total Recipes'], [adjective_count, total_count], color=['blue', 'gray'])
        ax.set_ylabel('Count')
        ax.set_title(f"Comparison of Recipes Containing '{input_adjective}' vs. Total Recipes")
        st.pyplot(fig)


rank_input = st.sidebar.number_input("Enter a rank number to view the corresponding recipe:", min_value=1, max_value=filtered_dataset['Rank'].max(), step=1)

if rank_input:
        rank_recipe = filtered_dataset[filtered_dataset['Rank'] == rank_input]
        if not rank_recipe.empty:
            st.write(f"Recipe with rank {rank_input}:")
            st.write(rank_recipe[['Recipe_Name', 'Rank']])
        else:
            st.write(f"No recipe found with rank {rank_input}.")


# Tab 2: Ranked Desserts (You can add any content here for the second tab)
with tab2:
    st.write(f"### Ranked {filter_type}:")
    if 'Rank' in filtered_dataset.columns and 'Recipe_Name' in filtered_dataset.columns:
        ranked_data = filtered_dataset.sort_values(by='Rank')
        st.write(ranked_data[['Recipe_Name', 'Rank']])
    else:
        st.error("The dataset does not contain the necessary columns ('Recipe_Name', 'Rank').")