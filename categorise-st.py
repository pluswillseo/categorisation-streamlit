import streamlit as st
import csv
import re
import pandas as pd
import numpy as np

st.title("Keyword Categoriser")

# Define a dictionary of Samsung products and their relevant keywords
st.header("Categories")
st.write("Add the categories you would like to use, along with the keywords and regex that identify each. Once you've completed all your categories, leave the last one blank and move on to adding your keywords.")
products = {}
category_count = 0
while True:
    category_count += 1
    category = st.text_input("Enter category name - if you don't need another, leave it blank:", key="category_{}".format(category_count))
    if not category:
        break
    keywords = st.text_input("Add the identifiers for the category '{}', separated by commas. This can also use Regex:".format(category), key="keywords_{}".format(category_count))
    keywords = [k.strip() for k in keywords.split(",")]
    products[category] = keywords

# Read the keywords from the keywords.csv file
st.header("Keywords")
keywords = st.text_area("Enter keywords, separated by a new line for each:", key="input_keywords")
keywords = keywords.split("\n")

# Loop through each keyword and write its corresponding category to the output.csv file
output = []
for keyword in keywords:
    categories = []
    for product, product_keywords in products.items():
        for product_keyword in product_keywords:
            if re.search(product_keyword, keyword, re.IGNORECASE):
                categories.append(product)
                break
    output.append([keyword, ", ".join(categories)])

st.header("Full data table")

import pandas as pd

df = pd.DataFrame(output)

df.rename(columns = {0:'Keywords', 1:'Categories'}, inplace = True)

# Add a sidebar to the app
st.sidebar.title("Filter categories")

# Add a filter to the sidebar that allows users to select multiple categories
selected_categories = st.sidebar.multiselect("Select categories to filter by:", options=list(products.keys()))

if selected_categories == []:
    st.table(df)
    csv = df.to_csv(index=False)
else:
    # Filter the table by the selected categories
    # create an empty list to store the rows that match the filter criteria
    filtered_rows = []

# iterate over the rows in the DataFrame
    for index, row in df.iterrows():
        # check if the fruit column contains any items from the list
        if any(item in row['Categories'] for item in selected_categories):
            # if it does, append the row to the filtered_rows list
            filtered_rows.append(row)
            
# create a new DataFrame using the filtered rows
            filtered_df = pd.DataFrame(filtered_rows)

# Display the filtered DataFrame
    st.table(filtered_df)
    csv = filtered_df.to_csv(index=False)

st.download_button('Download Table as CSV', csv, file_name = 'output.csv', mime='text/csv')
