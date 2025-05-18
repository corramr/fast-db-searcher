from openai import OpenAI
from utils.prompt import NL2SQL_PROMPT
from utils.helper import get_column_info, get_table_sample
import json
import sqlite3
import os

# define flags
TOPIC_TO_TEST = "countries"

# define sample queries (taken from the database)
cars_queries = [
    "What are the engine specifications for Vortex X1?",
    "Who between Vortex X1 and Avalon S has the highest fuel consumption?",
]

countries_queries = [
    "What's the most common animal in Italy?",
    "How many habitants does Egypt have?",
]

# get database info
db_path = "data/data.db"
if TOPIC_TO_TEST == "cars":
    table_name = "cars_data"
    column_info = get_column_info(db_path, "cars_data")
    table_sample = get_table_sample(db_path, "cars_data")
    nl_query = cars_queries[1] # choose between 0 and 1

elif TOPIC_TO_TEST == "countries":
    table_name = "countries_data"
    column_info = get_column_info(db_path, "countries_data")
    table_sample = get_table_sample(db_path, "countries_data")
    nl_query = countries_queries[1] # choose between 0 and 1

# build prompt
prompt = NL2SQL_PROMPT.format(
    table_name=table_name,
    table_sample=table_sample,
    column_info=column_info,
    nl_query=nl_query,
)

# define and invoke LLM
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

completion = client.chat.completions.create(
  model="meta-llama/llama-3.3-8b-instruct:free",
  messages=[
    {
      "role": "user",
      "content": prompt
    }
  ]
)

response = completion.choices[0].message.content
print(response)

# extract info from response
try:
    # Attempt to load the string as a JSON object
    response_dictionary = json.loads(response)
    # If successful, access the value
    sql_query = response_dictionary["sql_query"]

except json.JSONDecodeError as e:
    # If loading fails, catch the JSONDecodeError
    print(f"Error: Could not decode the JSON string. Details: {e}\nThis is probably due to the wrong formatting of the LLM response.")
    sql_query = None # Or handle the failure in another way

# run sql query
if sql_query:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        print("SQL Query Result:")
        for row in result:
            print(row)
        conn.close()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
