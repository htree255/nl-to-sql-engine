from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

MAX_RETRIES = 3


def fix_sql_with_error(original_question, broken_sql, error_message, schema_text, examples_text):
    """
    When the SQL fails, send the AI:
     - the original NL question
     - the original SQL
     - error
     - database schema
     - example text
    Ask AI to regenerate the correct SQL

    """

    prompt = f"""You are an expert SQL writer. You wrote the following SQL to answer a question, but it produced an error.

Original question: {original_question}

Your SQL:
{broken_sql}

Error message:
{error_message}

Database schema:
{schema_text}

Write a corrected SQL query that fixes the error. Return ONLY the SQL — no explanation, no markdown, no backticks."""

    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.choices[0].message.content

def run_with_validation(question, initial_sql, connection, schema_text, examples_text):
    """
    The agentic loop 

    Try to run the SQL. If it fails:
        - show the error
        - ask AI to fix it
        - try again
    Repeat upto MAX_RETRIES times.

    Return a results dictionary
    """

    from database import run_query

    current_sql = initial_sql

    for attempt in range(1, MAX_RETRIES +1):
        print(f"\nAttempt {attempt}: Running SQL...")
        result = run_query(connection, current_sql)
    
        if result["success"]:
             # It worked — return immediately
             if attempt > 1:
                 print(f"Fixed after {attempt} attempts.")

             return result
        
        # It failed — show the error and try to fix it
        print(f"Error on attempt {attempt}: {result["error"]}")

        if attempt < MAX_RETRIES:
            print ("Asking AI to fix the error...")

            current_sql = fix_sql_with_error(question, current_sql, result["error"], schema_text, examples_text)
            print (f"New SQL: {current_sql}")
        else:
            # Ran out of attempts — return the last failure
            print(f"Could not fix after {MAX_RETRIES} attempts.")
            return result

    return result