from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
load_dotenv() 
# Attempt to import the Generative AI SDK
try:
    import google.generativeai as genai
except ImportError:
    st.error("Google Generative AI SDK not found. Ensure it's installed.")
    st.stop()

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')

# Configure the Generative AI SDK
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Configuration error: {e}")
    st.stop()

## Function To Load Google Gemini Model and provide query as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Function To Retrieve query from Database
def read_sql_query(sql,db):
   connetion=sqlite3.connect(database=db)
   cursor=connetion.cursor()
   cursor.execute(sql)
   rows=cursor.fetchall()
   connetion.commit()
   connetion.close()
   for row in rows:
       print(rows)
   return rows

## define our Prompt
prompt=[
   """
      You are an expert in converting English questions to SQL query!
      The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
      SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
      the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
      \nExample 2 - Tell me all the students studying in Data Science class?, 
      the SQL command will be something like this SELECT * FROM STUDENT 
      where CLASS="Data Science"; 
      also the sql code should not have ``` in beginning or end and sql word in output

      """
] 

st.set_page_config(page_title="I can retrieve any sql Query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("ask the question")

## if submit is click 
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"student.db")
    st.subheader("The response is")
    for row in response:
       # print(row)
        st.header(row)