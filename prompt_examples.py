# A library of worked examples for the company database
# Each example pairs a natural language question with the correct SQL
# Goal:

EXAMPLES = [
    {
        "question": "Who has the highest salary?",
        "sql": "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 1",
    },
    {
        "question": "List employees in the Sales department",
        "sql": "SELECT name FROM employees WHERE dept = 'Sales'",
    },
    {
        "question": "What is the average salary by department?",
        "sql": "SELECT dept, AVG(salary) AS avg_salary FROM employees GROUP BY dept",
    },
    {
        "question": "Which product has the lowest stock?",
        "sql": "SELECT name, stock FROM products ORDER BY stock ASC LIMIT 1",
    },
    {
        "question": "List all products that cost more than $100",
        "sql": "SELECT name, price FROM products WHERE price > 100",
    },
    {
        "question": "How many total units has each product sold?",
        "sql": """SELECT p.name, SUM(s.quantity) AS total_units
FROM products p
JOIN sales s ON p.id = s.product_id
GROUP BY p.name""",
    },
    {
        "question": "How many sales did each employee make?",
        "sql": """SELECT e.name, COUNT(s.id) AS total_sales
FROM employees e
JOIN sales s ON e.id = s.employee_id
GROUP BY e.name
ORDER BY total_sales DESC""",
    },
    {
        "question": "What were the total sales after March 1st, 2024?",
        "sql": "SELECT * FROM sales WHERE sale_date > '2024-03-01'",
    },
]
