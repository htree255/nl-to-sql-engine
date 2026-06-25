import sqlite3
from database import create_sample_database, print_result
from ai_caller import ask_ai_for_sql
from validator import run_with_validation

conn = create_sample_database()

print("Ask me anything about the company database.")
print("Type 'quit' to exit.\n")

while True:
    question = input("Your question: ").strip()

    if question.lower() == "quit":
        break

    if not question:
        continue

    # Step 1: ask AI to write the initial sql
    print("\nThinking..")
    sql, schema_text, examples_text = ask_ai_for_sql(question)
    print("SQL generated.")
    print(f"Here is the SQL generated: {sql}")

    # Step 2: run sql on the database - with automatic fixing, if it fails
    result = run_with_validation(question, sql, conn, schema_text, examples_text )

    # Step 3: show the results
    print("\nResults: ")
    print_result(result)

    
