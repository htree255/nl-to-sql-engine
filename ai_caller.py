from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_schema_description():
    """
    Returns a plain text description of the database
    """

    return """
    Database: company.db
    
    Table: employees
      - id (integer): unique ID for each employee
      - name (text): employee's full name
      - dept (text): department they work in (Engineering, Sales, Marketing)
      - salary (integer): annual salary in dollars
    
    Table: products
      - id (integer): unique product ID
      - name (text): product name
      - price (real): price in dollars
      - stock (integer): how many units we have
    
    Table: sales
      - id (integer): unique sale ID
      - employee_id (integer): which employee made the sale (links to employees.id)
      - product_id (integer): which product was sold (links to products.id)
      - quantity (integer): how many units sold
      - sale_date (text): date of the sale (format: YYYY-MM-DD)
    """

def ask_ai_for_sql(question):
     """
    Takes a plain English question.
    Sends it to LLM along with the database schema.
    Returns the SQL that LLM writes.
    """
     # 1. connection to llm
     client = Groq()

     # 2. Describe model's role
     system_instruction = (
          
          f"""You are an expert SQL engineer. You will be given a database schema and a question. 
          Your job is to convert natural language questions into clean, valid SQL.  
          Return ONLY the raw SQL code block. Do not include conversational text, markdown formatting blocks (like ```sql), or explanations.
          {get_schema_description()}
          """
    
     )

     # 3. Call the API using the recommended Llama 3.3 model
     completion = client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          temperature=0.0,
          messages=[{"role": "system", "content": system_instruction},
            {"role": "user", "content": question}]
     )

    # 4. Extract and return the generated text
     return completion.choices[0].message.content

#Test    
if __name__ == "__main__":
     
     questions = [
        "Which employees are in the Sales department?",
        "What is the most expensive product?",
        "How many sales did each employee make?",
    ]
     
     for question in questions:
        print(f"\nQuestion: {question}")
        sql = ask_ai_for_sql(question)
        print(f"AI wrote this SQL:\n{sql}")
     
    