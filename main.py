import sqlite3
from database import create_sample_database, run_query
from ai_caller import ask_ai_for_sql

conn = create_sample_database()

print("Ask me anything about the company database.")
print("Type 'quit' to exit.\n")

while True:
    question = input("Your question: ").strip()
    
    if question.lower() == "quit":
        break

    if not question:
        continue

    #Step 1: ask AI to write sql
    print("Thinking..")
    sql = ask_ai_for_sql(question)
    print("SQL generated.")

    #Step 2: run sql on the database
    print("Results: ")
    run_query(conn, sql)
