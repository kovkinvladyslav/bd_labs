class View:
    def show_message(self, message):
        print(message)

    def list_names(self, tables):
        print("Tables names:")
        for table in tables:
            print(table)

    def get_list_table_input(self):
        table_name = input("Enter table name: ")
        n_rows = int(input("Enter number of rows: "))
        return table_name, n_rows

    def get_data_input(self):
        try:
            table = input("Enter table name: ")
            columns = input("Enter column names separated by space: ").split()
            val = input("Enter values separated by space: ").split()
            if len(columns) != len(val):
                raise ValueError("The number of columns should be equal to the number of values")
        except ValueError as e:
            print((f"ERROR: {e}"))
        return table, columns, val


    def get_update_input(self):
        while True:
            try:
                table = input("Enter Table Name: ")
                id = int(input("Enter ID of row that needs to be edited: "))
                columns = input("Enter column names separated by space: ").split()
                new_values = input("Input new values separated by space: ").split()
                return table, id, columns, new_values
            except ValueError as e:
                print(f"ERROR: {e}")

    def get_delete_input(self):
        try:
            table = input("Enter Table Name: ")
            id = int(input("Enter ID of row that needs to be deleted: "))
            return table, id
        except ValueError as e:
            print(f"ERROR: {e}")

    def get_generate_data_input(self):
        try:
            table = input("Enter table name: ")
            n_rows = input("Enter number of generated rows: ")
            return table, n_rows
        except ValueError as e:
            print(f"ERROR: {e}")

    def get_search_query_1_input(self):
        print("Search Query 1: Find vaccinations within a specific date range and filter by citizen name.")
        range_start = input("Enter the start date (YYYY-MM-DD): ")
        range_end = input("Enter the end date (YYYY-MM-DD): ")
        citizen_name = input("Enter part of the citizen's name (for pattern matching): ")
        return range_start, range_end, citizen_name

    def get_search_query_2_input(self):
        print("Search Query 2: Find clinics with vaccines in a specific dosage range and filter by clinic address.")
        dosage_start = input("Enter the minimum dosage: ")
        dosage_end = input("Enter the maximum dosage: ")
        clinic_address = input("Enter part of the clinic's address (for pattern matching): ")
        return (int(dosage_start), int(dosage_end)), clinic_address

    def get_search_query_3_input(self):
        print("Search Query 3: Find doctors with fewer vaccinations than a given limit and filter by doctor name.")
        doctor_name = input("Enter part of the doctor's name (for pattern matching): ")
        max_vaccinations = input("Enter the maximum number of vaccinations: ")
        return doctor_name, int(max_vaccinations)

    def show_results(self, results):
        if not results:
            print("No results found.")
            return
        for row in results:
            print(" | ".join(map(str, row)))
