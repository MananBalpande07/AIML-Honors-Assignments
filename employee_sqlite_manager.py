import sqlite3


class EmployeeSQLiteManager:
    """Manages employee records in a local SQLite database."""

    def __init__(self, db_name: str = "company_employees.db"):
        self.db_name = db_name
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_name)

    def _create_table(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS employees (
            emp_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL,
            salary REAL NOT NULL CHECK(salary >= 0)
        )
        """
        with self._connect() as conn:
            conn.execute(query)

    def add_employee(self, emp_id: str, full_name: str, department: str, role: str, salary: float) -> None:
        if salary < 0:
            raise ValueError("Salary cannot be negative.")

        query = "INSERT INTO employees (emp_id, full_name, department, role, salary) VALUES (?, ?, ?, ?, ?)"
        try:
            with self._connect() as conn:
                conn.execute(query, (emp_id, full_name, department, role, salary))
            print(f"[Success] Employee '{full_name}' added to SQLite database.")
        except sqlite3.IntegrityError:
            raise ValueError(f"Employee ID '{emp_id}' already exists.")

    def view_all_employees(self) -> None:
        query = "SELECT emp_id, full_name, department, role, salary FROM employees ORDER BY emp_id"
        with self._connect() as conn:
            rows = conn.execute(query).fetchall()

        if not rows:
            print("\n[Info] No records found in database.")
            return

        print("\n" + "-" * 74)
        print(f"{'ID':<10} {'Name':<20} {'Department':<15} {'Role':<15} {'Salary':>10}")
        print("-" * 74)
        for emp_id, name, dept, role, salary in rows:
            print(f"{emp_id:<10} {name:<20} {dept:<15} {role:<15} {salary:>10.2f}")
        print("-" * 74)

    def search_employee(self, emp_id: str) -> None:
        query = "SELECT emp_id, full_name, department, role, salary FROM employees WHERE emp_id = ?"
        with self._connect() as conn:
            row = conn.execute(query, (emp_id,)).fetchone()

        if not row:
            print(f"\n[Not Found] No employee with ID '{emp_id}'.")
            return

        labels = ["Employee ID", "Full Name", "Department", "Role", "Salary"]
        print("\n--- Employee Details ---")
        for label, val in zip(labels, row):
            formatted = f"{val:.2f}" if isinstance(val, float) else val
            print(f"{label:<12}: {formatted}")

    def update_employee(self, emp_id: str, new_role: str, new_salary: float) -> None:
        if new_salary < 0:
            raise ValueError("Salary cannot be negative.")

        with self._connect() as conn:
            if new_role:
                cursor = conn.execute(
                    "UPDATE employees SET role = ?, salary = ? WHERE emp_id = ?",
                    (new_role, new_salary, emp_id),
                )
            else:
                cursor = conn.execute(
                    "UPDATE employees SET salary = ? WHERE emp_id = ?",
                    (new_salary, emp_id),
                )

            if cursor.rowcount == 0:
                print(f"\n[Not Found] Employee ID '{emp_id}' does not exist.")
            else:
                print(f"[Success] Updated record for Employee ID '{emp_id}'.")

    def delete_employee(self, emp_id: str) -> None:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))

        if cursor.rowcount == 0:
            print(f"\n[Not Found] Employee ID '{emp_id}' does not exist.")
        else:
            print(f"[Success] Deleted Employee ID '{emp_id}'.")


def main():
    db_manager = EmployeeSQLiteManager()

    while True:
        print("\n=== Employee Management System (SQLite) ===")
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
                print("Exiting SQLite Employee Manager.")
                break
            else:
                print("[Invalid Input] Enter a number between 1 and 6.")
        except ValueError as err:
            print(f"[Input Error] {err}")


if __name__ == "__main__":
    main()