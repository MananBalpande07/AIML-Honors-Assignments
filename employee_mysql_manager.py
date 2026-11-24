import mysql.connector
from mysql.connector import Error


class EmployeeMySQLManager:
    """Manages employee records in a MySQL relational database."""

    def __init__(self, host: str = "localhost", user: str = "root", password: str = "", database: str = "company_db"):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
        }
        self.database = database
        self._initialize_database()

    def _connect(self, use_db: bool = True):
        conn_params = dict(self.config)
        if use_db:
            conn_params["database"] = self.database
        return mysql.connector.connect(**conn_params)

    def _initialize_database(self) -> None:
        try:
            with self._connect(use_db=False) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")

            create_table_sql = """
            CREATE TABLE IF NOT EXISTS employees (
                emp_id VARCHAR(20) PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                department VARCHAR(50) NOT NULL,
                role VARCHAR(50) NOT NULL,
                salary DECIMAL(10, 2) NOT NULL CHECK (salary >= 0)
            )
            """
            with self._connect(use_db=True) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(create_table_sql)
        except Error as err:
            print(f"[Database Setup Notice] Ensure MySQL Server is running: {err}")

    def add_employee(self, emp_id: str, full_name: str, department: str, role: str, salary: float) -> None:
        if salary < 0:
            raise ValueError("Salary cannot be negative.")

        sql = "INSERT INTO employees (emp_id, full_name, department, role, salary) VALUES (%s, %s, %s, %s, %s)"
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (emp_id, full_name, department, role, salary))
                conn.commit()
            print(f"[Success] Employee '{full_name}' added to MySQL database.")
        except Error as err:
            print(f"[Database Error] {err}")

    def view_all_employees(self) -> None:
        sql = "SELECT emp_id, full_name, department, role, salary FROM employees ORDER BY emp_id"
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()

            if not rows:
                print("\n[Info] No employee records found.")
                return

            print("\n" + "-" * 74)
            print(f"{'ID':<10} {'Name':<20} {'Department':<15} {'Role':<15} {'Salary':>10}")
            print("-" * 74)
            for emp_id, name, dept, role, salary in rows:
                print(f"{emp_id:<10} {name:<20} {dept:<15} {role:<15} {float(salary):>10.2f}")
            print("-" * 74)
        except Error as err:
            print(f"[Database Error] {err}")

    def search_employee(self, emp_id: str) -> None:
        sql = "SELECT emp_id, full_name, department, role, salary FROM employees WHERE emp_id = %s"
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (emp_id,))
                    row = cursor.fetchone()

            if not row:
                print(f"\n[Not Found] No employee found with ID '{emp_id}'.")
                return

            labels = ["Employee ID", "Full Name", "Department", "Role", "Salary"]
            print("\n--- Employee Details ---")
            for label, val in zip(labels, row):
                print(f"{label:<12}: {val}")
        except Error as err:
            print(f"[Database Error] {err}")

    def update_employee(self, emp_id: str, new_role: str, new_salary: float) -> None:
        if new_salary < 0:
            raise ValueError("Salary cannot be negative.")

        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    if new_role:
                        cursor.execute(
                            "UPDATE employees SET role = %s, salary = %s WHERE emp_id = %s",
                            (new_role, new_salary, emp_id),
                        )
                    else:
                        cursor.execute(
                            "UPDATE employees SET salary = %s WHERE emp_id = %s",
                            (new_salary, emp_id),
                        )
                    conn.commit()
                    if cursor.rowcount == 0:
                        print(f"\n[Not Found] Employee ID '{emp_id}' does not exist.")
                    else:
                        print(f"[Success] Record updated for Employee ID '{emp_id}'.")
        except Error as err:
            print(f"[Database Error] {err}")

    def delete_employee(self, emp_id: str) -> None:
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        print(f"\n[Not Found] Employee ID '{emp_id}' does not exist.")
                    else:
                        print(f"[Success] Deleted Employee ID '{emp_id}'.")
        except Error as err:
            print(f"[Database Error] {err}")


def main():
    print("--- MySQL Connection Setup ---")
    host = input("MySQL Host (default 'localhost'): ").strip() or "localhost"
    user = input("MySQL User (default 'root'): ").strip() or "root"
    password = input("MySQL Password: ").strip()

    db_manager = EmployeeMySQLManager(host=host, user=user, password=password)

    while True:
        print("\n=== Employee Management System (MySQL) ===")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")

        choice = input("Select option (1-6): ").strip()

        try:
            if choice == "1":
                emp_id = input("Employee ID: ").strip()
                name = input("Full Name: ").strip()
                dept = input("Department: ").strip()
                role = input("Role: ").strip()
                salary = float(input("Salary: ").strip())
                db_manager.add_employee(emp_id, name, dept, role, salary)
            elif choice == "2":
                db_manager.view_all_employees()
            elif choice == "3":
                emp_id = input("Employee ID to search: ").strip()
                db_manager.search_employee(emp_id)
            elif choice == "4":
                emp_id = input("Employee ID to update: ").strip()
                role = input("New Role (leave blank to keep current): ").strip()
                salary = float(input("New Salary: ").strip())
                db_manager.update_employee(emp_id, role, salary)
            elif choice == "5":
                emp_id = input("Employee ID to delete: ").strip()
                db_manager.delete_employee(emp_id)
            elif choice == "6":
                print("Exiting MySQL Employee Manager.")
                break
            else:
                print("[Invalid Input] Enter a number between 1 and 6.")
        except ValueError as err:
            print(f"[Input Error] {err}")


if __name__ == "__main__":
    main()