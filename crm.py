import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="crm_db",
    user="skunian",
    password="formula01"
)

# Create tables if they don't exist
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        company_id INTEGER REFERENCES companies(id)
    )
""")
conn.commit()

def create_company():
    name = input("Enter company name: ")
    cur.execute("INSERT INTO companies (name) VALUES (%s)", (name,))
    conn.commit()
    print("Company created successfully.")

def create_employee():
    name = input("Enter employee name: ")
    company_id = input("Enter company ID: ")
    cur.execute("INSERT INTO employees (name, company_id) VALUES (%s, %s)", (name, company_id))
    conn.commit()
    print("Employee created successfully.")

def read_companies():
    cur.execute("SELECT * FROM companies")
    companies = cur.fetchall()
    for company in companies:
        print(f"ID: {company[0]}, Name: {company[1]}")

def read_employees():
    cur.execute("""
        SELECT employees.id, employees.name, companies.name AS company_name
        FROM employees
        JOIN companies ON employees.company_id = companies.id
    """)
    employees = cur.fetchall()
    for employee in employees:
        print(f"ID: {employee[0]}, Name: {employee[1]}, Company: {employee[2]}")

def update_company():
    company_id = input("Enter company ID: ")
    new_name = input("Enter new company name: ")
    cur.execute("UPDATE companies SET name = %s WHERE id = %s", (new_name, company_id))
    conn.commit()
    print("Company updated successfully.")

def update_employee():
    employee_id = input("Enter employee ID: ")
    new_name = input("Enter new employee name: ")
    new_company_id = input("Enter new company ID: ")
    cur.execute("UPDATE employees SET name = %s, company_id = %s WHERE id = %s", (new_name, new_company_id, employee_id))
    conn.commit()
    print("Employee updated successfully.")

def delete_company():
    company_id = input("Enter company ID: ")
    cur.execute("DELETE FROM companies WHERE id = %s", (company_id,))
    conn.commit()
    print("Company deleted successfully.")

def delete_employee():
    employee_id = input("Enter employee ID: ")
    cur.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
    conn.commit()
    print("Employee deleted successfully.")

while True:
    print("\nCRM Menu:")
    print("1. Create Company")
    print("2. Create Employee")
    print("3. Read Companies")
    print("4. Read Employees")
    print("5. Update Company")
    print("6. Update Employee")
    print("7. Delete Company")
    print("8. Delete Employee")
    print("9. Exit")

    choice = input("Enter your choice (1-9): ")

    if choice == "1":
        create_company()
    elif choice == "2":
        create_employee()
    elif choice == "3":
        read_companies()
    elif choice == "4":
        read_employees()
    elif choice == "5":
        update_company()
    elif choice == "6":
        update_employee()
    elif choice == "7":
        delete_company()
    elif choice == "8":
        delete_employee()
    elif choice == "9":
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
conn.close()