import streamlit as st
import csv
import re
import pandas as pd

st.title("Keyword Categoriser")

# Define a dictionary of Samsung products and their relevant keywords
st.header("Categories and Keywords")
products = {}
category_count = 0
while True:
    category_count += 1
    category = st.text_input("Enter category name (leave empty to finish):", key="category_{}".format(category_count))
    if not category:
        break
    keywords = st.text_input("Enter keywords for category '{}', separated by commas. This can also include regex:".format(category), key="keywords_{}".format(category_count))
    keywords = [k.strip() for k in keywords.split(",")]
    products[category] = keywords

# Read the keywords from the keywords.csv file
st.header("Keywords")
keywords = st.text_area("Enter keywords, separated by newlines:", key="input_keywords")
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

st.header("Output")

import pandas as pd

df = pd.DataFrame(output)

df.rename(columns = {0:'Keywords', 1:'Categories'}, inplace = True)

csv = df.to_csv(index=False)
st.download_button('Download Table as CSV', csv, file_name = 'output.csv', mime='text/csv')

# Add a sidebar to the app
st.sidebar.title("Filters")

# Add a filter to the sidebar that allows users to select multiple categories
selected_categories = st.sidebar.multiselect("Select categories to filter by:", options=list(products.keys()))

# Filter the table by the selected categories
filtered_df = df[np.isin(df["Categories"], selected_categories)]

# Display the filtered DataFrame
st.table(filtered_df)

st.table(df)


