# %%
import os
import re
import sqlite3
import json
import zipfile
#From ACS Environment
from bs4 import BeautifulSoup
from lxml import etree
from datetime import datetime

# %%
#Connect to DB
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS powerpoint
                (id INTEGER PRIMARY KEY, filename TEXT, created_at TEXT, last_edited_at TEXT, folder_location TEXT, drill LIST, years TEXT, age TEXT, repayment TEXT, stipend TEXT, estimated TEXT, program TEXT)''')

# %%
# Function to extract text from PowerPoint files
def extract_text_from_pptx(file_path):
    text = ""
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for name in zip_ref.namelist():
            if name.startswith('ppt/slides/slide'):
                with zip_ref.open(name) as slide_file:
                    slide_content = slide_file.read()
                    # Extract text from XML content
                    xml_content = etree.fromstring(slide_content)
                    #This text extracter uses information from XML content of the PPT. you can get to XML content by "unzipping" a ppt
                    text += " ".join(xml_content.xpath(".//*[local-name()='t']//text()"))

    return text

# Function to find numbers and their surrounding words
#I just suggested any numbers with context of 5 words in either direction. Very arbitrary just to show capability of searching for things in a PPT.
def find_numbers_with_context(text):
    pattern = r'(\b\w+\b\s+){0,5}\b(\d+)\b(\s+\b\w+\b){0,5}'
    matches = re.findall(pattern, text)
    results = []
    for match in matches:
        # Combine the surrounding words with the number
        context = " ".join(match)
        results.append(context)
    return results

# %%
# Iterate through PowerPoint files in the directory
pptx_directory = "/Users/annivoigt/Documents/coding/python/DS-S_Ship_Testing/Powerpoints & DB/powerpoints"

# %%
# Function to convert list of numbers to dictionary format according to various "context" words we care about
def dict_list(list_num):
    my_information = {"drill":[],"years":[], "age":[], "repayment":[], "stipend":[], "estimated":[],'program':[]}
    for i in list_num:
        if 'drill' in i:
            num = re.findall(r'\d+', i)
            my_information["drill"].append(num[0])
        if 'years' in i:
            num = re.findall(r'\d+', i)
            my_information["years"].append(num[0])
        if 'age' in i:
            num = re.findall(r'\d+', i)
            my_information["age"].append(num[0])
        if 'repayment' in i:
            num = re.findall(r'\d+', i)
            my_information["repayment"].append(num[0])
        if 'stipend' in i:
            num = re.findall(r'\d+', i)
            my_information["stipend"].append(num[0])
        if 'estimated' in i:
            num = re.findall(r'\d+', i)
            my_information["estimated"].append(num[0])
        if 'program' in i:
            num = re.findall(r'\d+', i)
            my_information["program"].append(num[0])
    return my_information

# %%
# Function to insert data into SQLite database
def sql_add(filename, created_at, last_edited_at, folder_location, my_information):
    age_json = json.dumps(my_information['age'])
    drill_json = json.dumps(my_information['drill'])
    years_json = json.dumps(my_information['years'])
    repayment_json  = json.dumps(my_information['repayment'])
    stipend_json = json.dumps(my_information['stipend'])
    estimate_json = json.dumps(my_information['estimated'])
    program_json = json.dumps(my_information['program'])

    cursor.execute('INSERT INTO powerpoint (filename, created_at, last_edited_at, folder_location, drill, years, age, repayment, stipend, estimated, program) VALUES (?,?,?, ?, ?, ?, ?, ?, ?, ?, ?)',\
            (filename, created_at, last_edited_at, folder_location, drill_json, years_json,\
            age_json, repayment_json, \
            stipend_json, estimate_json, program_json))

# %%
def delete_duplicates():
    # Connect to the SQLite database

    try:
        # Identify the criteria for determining duplicate entries
        # For example, let's say we want to delete rows with duplicate 'name' column
        cursor.execute('''
            DELETE FROM powerpoint
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM powerpoint
                GROUP BY filename
            )
        ''')
        print("Duplicate entries deleted successfully.")
    except sqlite3.Error as e:
        print("Error deleting duplicates:", e)


# %%
list_num = []
# Iterate through PowerPoint files in the directory

for filename in os.listdir(pptx_directory):
    if filename.endswith(".pptx"):
        file_path = os.path.join(pptx_directory, filename)
        last_modified_time = os.path.getmtime(file_path)
        folder_location = os.path.dirname(file_path)
        file_stats = os.stat(file_path)
        created_at = datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        text = extract_text_from_pptx(file_path)
        numbers_with_context = find_numbers_with_context(text)
        if numbers_with_context:
            for context in numbers_with_context:
                list_num.append(context)
            info = dict_list(list_num)
            print(info)
            sql_add(filename, created_at, last_modified_time, folder_location, info)
            # Call the function to delete duplicate entries
        else:
            numbers = re.findall(r'\b\d+\b', text)
            if numbers:
                for number in numbers:
                    list_num.append(number)
                info = dict_list(list_num)
                created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql_add(filename, created_at,last_modified_time, folder_location, info)
                # Call the function to delete duplicate entries

delete_duplicates()






# %%
# Commit the transaction
conn.commit()

# Close connection
conn.close()

# %%
#This is how users could connect to the database and look at what exists in the database 
# -- we can create analytic products based off of this information
conn = sqlite3.connect('example.db')
cursor = conn.cursor()



def query_database(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


# Example query to select all data from the 'person' table
query = 'SELECT folder_location FROM powerpoint'

# Query the database
results = query_database(conn, query)
print(results)

# Close connection
conn.close()

# %%
# Connect to the SQLite database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Define the SQL query
query = "SELECT filename FROM powerpoint WHERE years IS NOT NULL"

# Execute the query
cursor.execute(query)

# Fetch all the matching rows
rows = cursor.fetchall()

# Extract the filenames from the rows
file_names = [row[0] for row in rows]

# Print the filenames
print("File names associated with entries having 'years':")
for file_name in file_names:
    print(file_name)

# Close the connection
conn.close()


# %%
# Connect to the SQLite database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Define the SQL query
query = "SELECT filename FROM powerpoint"

# Execute the query
cursor.execute(query)

# Fetch all the matching rows
rows = cursor.fetchall()

# Extract the filenames from the rows
file_names = [row[0] for row in rows]

# Print the filenames
print("File names:")
for file_name in file_names:
    print(file_name)

# Close the connection
conn.close()


