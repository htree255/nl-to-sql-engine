# This is the database schema represented as structured data.
# Each table maps to its description and columns

SCHEMA = {
    "employees": {
        "description": "Employee records including department and salary",
        "columns": {
            "id": "unique ID for each employee",
            "name": "employee's full name",
            "dept": "department they work in: Engineering, Sales, or Marketing",
            "salary": "annual salary in dollars",
        },
    },
    "products": {
        "description": "Products the company sells, with price and inventory",
        "columns": {
            "id": "unique ID for each employee",
            "name": "employee's full name",
            "dept": "department they work in: Engineering, Sales, or Marketing",
            "salary": "annual salary in dollars",
        },
    },
    "sales": {
        "description": "Individual sales transactions linking employees to products",
        "columns": {
            "id": "unique sale  ID",
            "employee_id": "which employee made the sale, links to employees.id",
            "product_id": "which product was sold, links to products.id",
            "quantity": "number of units sold in this transaction",
            "sale_date": "date of the sale in YYYY-MM-DD format",
        },
    },
}
