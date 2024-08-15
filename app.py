from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')

# Configure the Generative AI SDK
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Configuration error: Please check your API key and try again. Error details: {e}")
    st.stop()

# Function to load the Gemini model and provide a response
@st.cache_data(show_spinner=False)
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Use updated model
        response = model.generate_content([prompt[0], question])
        # Extract text from response safely
        text_response = response.candidates[0].content.parts[0].text if response.candidates else "No response"
        
        # Remove any potential formatting characters
        text_response = text_response.replace("```", "").strip()
        return text_response
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Function to retrieve query from the database
def read_sql_query(sql, db):
    if "DELETE" in sql.upper() or "DROP" in sql.upper():
        st.error("Destructive SQL commands are not allowed.")
        return None
    
    try:
        with sqlite3.connect(db) as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return None

# Validate the user's question
def validate_question(question):
    if len(question) < 10:
        st.warning("Please enter a more detailed question.")
        return False
    return True

# Updated prompt to avoid code block formatting
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION,Marks \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this: SELECT * FROM STUDENT 
    WHERE CLASS="Data Science";
    Please ensure the output is plain SQL without any formatting characters such as ``` or 'sql'.
    """
]

# Streamlit app configuration
st.set_page_config(page_title="Retrieve SQL Data with Gemini")
st.header("Smart SQL Querying with  Gemini Generative AI App")

# Sidebar for settings or additional info
st.sidebar.header("Settings")

# User input for the question
question = st.text_input("Enter your question:", key="input")

# Button to submit the question
submit = st.button("Ask the question")

# If submit is clicked
if submit and question:
    if validate_question(question):
        # Generate SQL query
        sql_query = get_gemini_response(question, prompt)
        print(sql_query)
        if sql_query:
            st.subheader("Generated SQL Query:")
            st.code(sql_query, language="sql")
            
            # Execute the SQL query and display results
            query_results = read_sql_query(sql_query, "student.db")
            if query_results:
                st.subheader("Query Results:")
                st.dataframe(query_results)
            else:
                st.write("No data found or query error.")
