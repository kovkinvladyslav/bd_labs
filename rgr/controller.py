from model import Model
from view import View

import sys

class Controller:
    def __init__(self):
        self.view = View()
        try:
            self.model = Model()
            self.view.show_message("Connected successfully")
        except Exception as e:
            self.view.show_message(f"Error occurred: {e}")
            sys.exit(1)
    def run(self):
        while True:
            choice = self.show_menu()
            if choice == '1':
                self.list_tables_names()
            elif choice == '2':
                self.add_data()
            elif choice == '3':
                self.edit_data()
            elif choice == '4':
                self.delete_data()
            elif choice == '5':
                self.list_table()
            elif choice == '6':
                self.generate_data()
            elif choice == '7':
                self.search_menu()
            elif choice == '8':
                break

    def show_menu(self):
        self.view.show_message("\nMenu:")
        self.view.show_message("1. List Table Names")
        self.view.show_message("2. Add Data")
        self.view.show_message("3. Edit Data")
        self.view.show_message("4. Delete Data")
        self.view.show_message("5. List table")
        self.view.show_message("6. Generate Data")
        self.view.show_message("7. Search")
        self.view.show_message("8. Exit")
        return input("Enter your choice: ")




    def list_tables_names(self):
        tables = self.model.get_tables()
        self.view.list_names(tables)

    def add_data(self):
        table, columns, val = self.view.get_data_input()
        self.view.show_message(self.model.add_data(table, columns, val))

    def edit_data(self):
        table, id, columns, new_value = self.view.get_update_input()
        self.view.show_message(self.model.edit_data(table, id, columns, new_value))

    def delete_data(self):
        table, id = self.view.get_delete_input()
        self.view.show_message(self.model.delete_data(table, id))

    def list_table(self):
        table_name, n_rows = self.view.get_list_table_input()
        listed_table, error = self.model.get_listed_table(table_name, n_rows)
        if error == 1:
            self.view.show_message(listed_table)
        else:
            for row in listed_table:
                self.view.show_message(row)

    def generate_data(self):
        self.view.show_message("\nGenerate Data Menu:")
        table_name = input("Enter Table Name:")
        n_rows = input("Enter number of generated rows:")
        self.view.show_message(self.model.generate_data(table_name, n_rows))

    def search_menu(self):
        self.view.show_message("Search Menu:")
        self.view.show_message("1: Query 1 - Find vaccinations by date range and citizen name.")
        self.view.show_message("2: Query 2 - Find clinics by dosage range and address.")
        self.view.show_message("3: Query 3 - Find doctors by name and vaccination count.")

        choice = input("Enter your choice (1-3): ")
        choice_query = {
            '1': (self.view.get_search_query_1_input, self.model.search_query_1),
            '2': (self.view.get_search_query_2_input, self.model.search_query_2),
            '3': (self.view.get_search_query_3_input, self.model.search_query_3),
        }
        if choice not in choice_query:
            self.view.show_message("Invalid choice. Please enter a valid option.")
            return
        input_func, query_func = choice_query[choice]
        inputs = input_func()
        results, execution_time = query_func(*inputs)

        self.view.show_results(results)
        self.view.show_message(f"Query executed in {execution_time:.2f} ms.")









