# NL-to-SQL-Engine

A natural language to SQL query engine that translates plain English questions into executable SQL, evaluated against BIRD-SQL bnechmark. 

## What it does

You ask a question in plain English:

> "Who made the most sales last quarter?"

The engine translates it to SQL, runs it against the database, and returns the answer — no SQL knowledge required.

---
 
## What makes this "agentic"
 
The validation loop is the agentic part. Unlike a simple pipeline where each step is predetermined, the loop:
 
1. **Acts** — runs the generated SQL
2. **Observes** — checks whether it succeeded or failed, and *how* it failed
3. **Decides** — chooses between returning the result, fixing a syntax error, or rethinking a semantic mismatch
4. **Reacts** — generates a new attempt with the error as additional context
No human is involved between steps 2 and 3. The system decides what to do next based on what it observed. That is what distinguishes an agent from a fixed workflow.
 

## Benchmark
 
Evaluated against the [BIRD-SQL](https://bird-bench.github.io/) benchmark — 10,000+ natural language / SQL pairs across 11 real-world databases.
 
## Tech stack
 
- Python 3.11+
- SQLite (via Python's built-in `sqlite3`)
- Meta llama-3.3-70b-versatile

## License
 
MIT
 