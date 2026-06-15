from groq import Groq
from dotenv import load_dotenv
from schema_linker import get_relevant_tables, build_schema

load_dotenv()


def ask_ai_for_sql(question):
    """
    Takes a plain English question.
    Sends it to LLM along with the database schema.
    Returns the SQL that LLM writes.
    """

    # 1 Schema linking
    relevant_tables = get_relevant_tables(question)
    schema_text = build_schema(relevant_tables)

    print(f"Schema linker created: {relevant_tables}")

    # 2. connection to llm
    client = Groq()

    # 3. Describe model's role
    system_instruction = f"""You are an expert SQL engineer. You will be given a database schema and a question. 
          Your job is to convert natural language questions into clean, valid SQL.  
          Return ONLY the raw SQL code block. Do not include conversational text, markdown formatting blocks (like ```sql), or explanations.
          {schema_text}
          """

    # 4. Call the API using the recommended Llama 3.3 model
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.0,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": question},
        ],
    )

    # 5. Extract and return the generated text
    return completion.choices[0].message.content


# Test
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
