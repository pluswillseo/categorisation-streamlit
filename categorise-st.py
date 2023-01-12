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

# Create a file uploader widget
uploaded_file = st.file_uploader('Choose a CSV file with your keywords in it')

# Check if the user has uploaded a file
if uploaded_file is not None:
  # If a file was uploaded, read the keywords from the CSV file
  keywords = []
  with open(uploaded_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      keywords.extend(row)
else:
  # If no file was uploaded, get the keywords from the text area widget
    keywords = st.text_area('Enter your keywords here')
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

# Add a filter to the sidebar that allows users to select multiple categories
remove_categories = st.sidebar.multiselect("Select categories to remove:", options=list(products.keys()))

# Filter the data by the entered word
#filtered_data = data[data['column_name'].str.contains(filter_word)]

# Display the filtered data
#st.table(filtered_data)

if selected_categories and remove_categories:
    filtered_df = df[(df['Categories'].isin(selected_categories)) & (~df["Categories"].isin(remove_categories))]
    csv = filtered_df
elif selected_categories:
    filtered_df = df[df['Categories'].isin(selected_categories)]
    csv = filtered_df
elif remove_categories:
    filtered_df = df[~df['Categories'].isin(remove_categories)]   
    csv = filtered_df
else:
    filtered_df = df
    csv = filtered_df

if not filtered_df.empty():
    st.download_button('Download Table as CSV', csv, file_name = 'output.csv', mime='text/csv')


#if selected_categories == [] and remove_categories == []:   # & filter_word == []:
#    st.table(df)
#    csv = df.to_csv(index=False)
#else:
#    # Filter the table by the selected categories
    # create an empty list to store the rows that match the filter criteria
#    filtered_rows = []

# iterate over the rows in the DataFrame
#    for index, row in df.iterrows():
#        # check if the fruit column contains any items from the list
#        if any(item in row['Categories'] for item in selected_categories):
#            # if it does, append the row to the filtered_rows list
#            filtered_rows.append(row)
            
# create a new DataFrame using the filtered rows
#            filtered_df = pd.DataFrame(filtered_rows)
    
    #add to this if need be to remove categories
#    filtered_rows = []
#    for index, row in filtered_df.iterrows():
#        # check if the fruit column contains any items from the list
#        if any(item not in row['Categories'] for item in remove_categories):
#            # if it does, append the row to the filtered_rows list
#            filtered_rows.append(row)
            
# create a new DataFrame using the filtered rows
#            filtered_df = pd.DataFrame(filtered_rows)
    
# Display the filtered DataFrame
#    st.table(filtered_df)
#    csv = filtered_df.to_csv(index=False)
