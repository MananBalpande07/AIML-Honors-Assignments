import os
import pandas as pd


class PandasStaffRegistry:
    def __init__(self, csv_path="company_staff_records.csv"):
        self.csv_path = csv_path
        self.columns = ["staff_id", "full_name", "department", "monthly_pay"]
        self._initialize_storage()

    def _initialize_storage(self):
        if not os.path.exists(self.csv_path):
            empty_df = pd.DataFrame(columns=self.columns)
            empty_df.to_csv(self.csv_path, index=False)

    def _fetch_frame(self):
        try:
            return pd.read_csv(self.csv_path)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=self.columns)

    def _commit_frame(self, dataframe):
        dataframe.to_csv(self.csv_path, index=False)

    def insert_record(self):
        df = self._fetch_frame()
        try:
            staff_id = int(input("Enter Staff ID: ").strip())
        except ValueError:
            print("Error: Staff ID must be a valid integer.")
            return

        if staff_id in df["staff_id"].values:
            print(f"Error: Staff ID {staff_id} already exists.")
            return

        full_name = input("Enter Full Name: ").strip()
        department = input("Enter Department: ").strip()

        try:
            monthly_pay = float(input("Enter Monthly Pay: ").strip())
        except ValueError:
            print("Error: Monthly Pay must be a numeric value.")
            return

        new_entry = pd.DataFrame(
            [
                {
                    "staff_id": staff_id,
                    "full_name": full_name,
                    "department": department,
                    "monthly_pay": monthly_pay,
                }
            ]
        )
        updated_df = pd.concat([df, new_entry], ignore_index=True)
        self._commit_frame(updated_df)
        print("Record successfully saved to CSV via Pandas.")

    def display_all(self):
        df = self._fetch_frame()
        if df.empty:
            print("No employee records available.")
            return
        print("\n--- Current Staff Directory ---")
        print(df.to_string(index=False))

    def query_by_name(self):
        df = self._fetch_frame()
        if df.empty:
            print("Directory is empty.")
            return

        keyword = input("Enter name keyword to search: ").strip().lower()
        filtered = df[df["full_name"].str.lower().str.contains(keyword, na=False)]

        if filtered.empty:
            print("No matching staff found.")
        else:
            print("\n--- Search Results ---")
            print(filtered.to_string(index=False))

    def modify_pay(self):
        df = self._fetch_frame()
        try:
            target_id = int(input("Enter Staff ID to update pay: ").strip())
        except ValueError:
            print("Invalid ID format.")
            return

        if target_id not in df["staff_id"].values:
            print("Staff ID not found.")
            return

        try:
            revised_pay = float(input("Enter New Monthly Pay: ").strip())
        except ValueError:
            print("Invalid pay amount.")
            return

        df.loc[df["staff_id"] == target_id, "monthly_pay"] = revised_pay
        self._commit_frame(df)
        print("Monthly pay updated successfully.")

    def remove_record(self):
        df = self._fetch_frame()
        try:
            target_id = int(input("Enter Staff ID to remove: ").strip())
        except ValueError:
            print("Invalid ID format.")
            return

        if target_id not in df["staff_id"].values:
            print("Staff ID not found.")
            return

        df = df[df["staff_id"] != target_id].reset_index(drop=True)
        self._commit_frame(df)
        print(f"Staff ID {target_id} removed from registry.")


def run_cli():
    registry = PandasStaffRegistry()
    actions = {
        "1": registry.insert_record,
        "2": registry.display_all,
        "3": registry.query_by_name,
        "4": registry.modify_pay,
        "5": registry.remove_record,
    }

    while True:
        print("\n=== Pandas Employee Registry ===")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Search Employee by Name")
        print("4. Update Employee Pay")
        print("5. Delete Employee")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()
        if choice == "6":
            print("Exiting application.")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid selection. Please choose between 1 and 6.")


if __name__ == "__main__":
    run_cli()