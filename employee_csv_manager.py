import csv
import os


class EmployeeCSVManager:
    """Manages employee records stored persistently in a CSV file."""

    FIELDNAMES = ["emp_id", "full_name", "department", "role", "salary"]

    def __init__(self, filename: str = "employees_data.csv"):
        self.filename = filename
        self._initialize_storage()

    def _initialize_storage(self) -> None:
        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writeheader()

    def _read_all(self) -> list[dict]:
        with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def _write_all(self, records: list[dict]) -> None:
        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            writer.writerows(records)

    def add_employee(self, emp_id: str, full_name: str, department: str, role: str, salary: float) -> None:
        if salary < 0:
            raise ValueError("Salary cannot be negative.")

        records = self._read_all()
        if any(row["emp_id"] == emp_id for row in records):
            raise ValueError(f"Employee ID '{emp_id}' already exists.")

        records.append({
            "emp_id": emp_id,
            "full_name": full_name,
            "department": department,
            "role": role,
            "salary": f"{salary:.2f}",
        })
        self._write_all(records)
        print(f"[Success] Employee '{full_name}' added successfully.")

    def view_all_employees(self) -> None:
        records = self._read_all()
        if not records:
            print("\n[Info] No employee records found.")
            return

        print("\n" + "-" * 72)
        print(f"{'ID':<10} {'Name':<20} {'Department':<15} {'Role':<15} {'Salary':>8}")
        print("-" * 72)
        for row in records:
            print(
                f"{row['emp_id']:<10} {row['full_name']:<20} "
                f"{row['department']:<15} {row['role']:<15} {row['salary']:>8}"
            )
        print("-" * 72)

    def search_employee(self, emp_id: str) -> None:
        records = self._read_all()
        for row in records:
            if row["emp_id"] == emp_id:
                print("\n--- Employee Details ---")
                for key, value in row.items():
                    print(f"{key.replace('_', ' ').title():<12}: {value}")
                return
        print(f"\n[Not Found] No employee found with ID '{emp_id}'.")

    def update_employee(self, emp_id: str, new_role: str, new_salary: float) -> None:
        if new_salary < 0:
            raise ValueError("Salary cannot be negative.")

        records = self._read_all()
        updated = False
        for row in records:
            if row["emp_id"] == emp_id:
                if new_role:
                    row["role"] = new_role
                row["salary"] = f"{new_salary:.2f}"
                updated = True
                break

        if not updated:
            print(f"\n[Not Found] Employee ID '{emp_id}' does not exist.")
            return

        self._write_all(records)
        print(f"[Success] Record updated for Employee ID '{emp_id}'.")

    def delete_employee(self, emp_id: str) -> None:
        records = self._read_all()
        filtered = [row for row in records if row["emp_id"] != emp_id]

        if len(filtered) == len(records):
            print(f"\n[Not Found] Employee ID '{emp_id}' does not exist.")
            return

        self._write_all(filtered)
        print(f"[Success] Employee ID '{emp_id}' deleted.")


def main():
    manager = EmployeeCSVManager()

    while True:
        print("\n=== Employee Management System (CSV) ===")
        print("1. Add New Employee")
        print("2. View All Employees")
        print("3. Search Employee by ID")
        print("4. Update Employee Role & Salary")
        print("5. Delete Employee")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()

        try:
            if choice == "1":
                emp_id = input("Employee ID: ").strip()
                name = input("Full Name: ").strip()
                dept = input("Department: ").strip()
                role = input("Role: ").strip()
                salary = float(input("Salary: ").strip())
                manager.add_employee(emp_id, name, dept, role, salary)
            elif choice == "2":
                manager.view_all_employees()
            elif choice == "3":
                emp_id = input("Enter Employee ID to search: ").strip()
                manager.search_employee(emp_id)
            elif choice == "4":
                emp_id = input("Enter Employee ID to update: ").strip()
                role = input("New Role (leave blank to keep current): ").strip()
                salary = float(input("New Salary: ").strip())
                manager.update_employee(emp_id, role, salary)
            elif choice == "5":
                emp_id = input("Enter Employee ID to delete: ").strip()
                manager.delete_employee(emp_id)
            elif choice == "6":
                print("Exiting CSV Employee Manager.")
                break
            else:
                print("[Invalid Input] Please select an option between 1 and 6.")
        except ValueError as err:
            print(f"[Input Error] {err}")


if __name__ == "__main__":
    main()