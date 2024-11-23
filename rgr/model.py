
import psycopg2
from time import time

class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname = "vaccination_control",
            user = "postgres",
            password = "2534",
            host = "localhost",
            port = 5432
        )

    def get_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT table_name FROM information_schema.tables
                   WHERE table_schema = 'public'""")
            return [table[0] for table in cursor.fetchall()]
        except psycopg2.Error as e:
            return f"Error fetching tables: {e.pgerror}"

    def edit_data(self, table, id, columns, new_values):
        try:
            cursor = self.conn.cursor()
            set_clause = ", ".join([f"{col} = %s" for col in columns])
            primary_keys = self.get_primary_key_columns(table)
            query = f"UPDATE {table} SET {set_clause} WHERE {primary_keys[0]} = %s"
            values = new_values + [id]
            cursor.execute(query, values)
            self.conn.commit()
            return "Data updated successfully!"
        except psycopg2.Error as e:
            self.conn.rollback()
            return e.pgerror
        finally:
            cursor.close()

    def add_data(self, table, columns, values):
        try:
            cursor = self.conn.cursor()
            columns_str = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(values))
            query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
            cursor.execute(query, values)
            self.conn.commit()
            return "Data added successfully!"
        except psycopg2.Error as e:
            self.conn.rollback()
            return e.pgerror
        finally:
            cursor.close()


    def delete_data(self, table, id):
        try:
            cursor = self.conn.cursor()
            primary_keys = self.get_primary_key_columns(table)
            query = f"DELETE FROM {table} WHERE {primary_keys[0]} = %s"
            cursor.execute(query, (id,))
            self.conn.commit()
            return "Data deleted successfully!"
        except psycopg2.Error as e:
            self.conn.rollback()
            return e.pgerror
        finally:
            cursor.close()

    def get_columns(self, table_name):
        query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (table_name,))
                columns = [row[0] for row in cursor.fetchall()]
            return columns
        except Exception as e:
            self.conn.rollback()
            print(f"Error retrieving columns for table {table_name}: {e}")
            return []
        finally:
            cursor.close()

    def get_primary_key_columns(self, table_name):
        try:
            query = """
                SELECT a.attname
                FROM pg_index i
                JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
                WHERE i.indrelid = %s::regclass AND i.indisprimary;
            """
            cursor = self.conn.cursor()
            cursor.execute(query, (table_name,))
            result = cursor.fetchall()
            return [row[0] for row in result]
        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Error: {e.pgerror}"
        finally:
            cursor.close()


    def get_listed_table(self, table_name, n_rows):
        try:
            query = f"SELECT * FROM {table_name} LIMIT %s"
            cursor = self.conn.cursor()
            cursor.execute(query, (n_rows,))

            column_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            result = [column_names] + rows
            return result, 0
        except psycopg2.Error as e:
            return f"Error: {e.pgerror}", 1
        finally:
            cursor.close()

    def generate_data(self, table_name, n_rows):
        if table_name not in self.get_tables():
            return f"Error: Table '{table_name}' does not exist! {self.get_tables()}"
        try:
            primary_key = self.get_primary_key_columns(table_name)[0]
            with self.conn.cursor() as cursor:
                cursor.execute(f"SELECT COALESCE(MAX({primary_key}), 0) FROM {table_name}")
                last_key = cursor.fetchone()[0]

            table_generators = {
                "vaccine": self.generate_vaccine_data,
                "doctor": self.generate_doctor_data,
                "clinic": self.generate_clinic_data,
                "vaccination": self.generate_vaccination_data,
                "doctor_clinic": self.generate_doctor_clinic_data,
                "citizen": self.generate_citizen_data
            }

            if table_name not in table_generators:
                return f"Error: No data generator defined for table '{table_name}'"

            return table_generators[table_name](int(last_key), int(n_rows), primary_key)

        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Database error: {e.pgerror}"

        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def generate_vaccine_data(self, last_key, n_rows, primary_key):
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                    INSERT INTO vaccine ({primary_key}, dosage)
                    SELECT i, floor(random() * 10 + 1)::integer
                    FROM generate_series(%s, %s) AS i
                """
                cursor.execute(query, (last_key + 1, last_key + n_rows))
                self.conn.commit()
                return f"Inserted {n_rows} vaccine records starting from ID {last_key + 1}."
        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Error generating vaccine data: {e.pgerror}"

    def generate_doctor_data(self, last_key, n_rows, primary_key):
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                    INSERT INTO doctor ({primary_key}, name, phone)
                    SELECT i, 'Doctor_' || i,
                        '+380' || LPAD((floor(random() * 1000000000)::bigint)::text, 9, '0')
                    FROM generate_series(%s, %s) AS i
                """
                cursor.execute(query, (last_key + 1, last_key + n_rows))
                self.conn.commit()
                return f"Inserted {n_rows} doctor records starting from ID {last_key + 1}."
        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Error generating doctor data: {e.pgerror}"

    def generate_clinic_data(self, last_key, n_rows, primary_key):
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                    INSERT INTO clinic ({primary_key}, address)
                    SELECT i, 'Clinic Address ' || i
                    FROM generate_series(%s, %s) AS i
                """
                cursor.execute(query, (last_key + 1, last_key + n_rows))
                self.conn.commit()
                return f"Inserted {n_rows} clinic records starting from ID {last_key + 1}."
        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Error generating clinic data: {e.pgerror}"

    def generate_citizen_data(self, last_key, n_rows, primary_key):
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                    INSERT INTO citizen ({primary_key}, name, address, phone)
                    SELECT i, 'Citizen_' || i, 'City, Street ' || i,
                        '+380' || LPAD((floor(random() * 1000000000)::bigint)::text, 9, '0')
                    FROM generate_series(%s, %s) AS i
                """
                cursor.execute(query, (last_key + 1, last_key + n_rows))
                self.conn.commit()
                return f"Inserted {n_rows} citizen records starting from ID {last_key + 1}."
        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Error generating citizen data: {e.pgerror}"

    def generate_doctor_clinic_data(self, last_key, n_rows, primary_key):
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                    INSERT INTO doctor_clinic ({primary_key}, doctor_id, clinic_id)
                    SELECT i,
                        (SELECT doctor_id FROM doctor ORDER BY random() LIMIT 1),
                        (SELECT clinic_id FROM clinic ORDER BY random() LIMIT 1)
                    FROM generate_series(%s, %s) AS i
                """
                cursor.execute(query, (last_key + 1, last_key + n_rows))
                self.conn.commit()
                return f"Inserted {n_rows} doctor_clinic records starting from ID {last_key + 1}."
        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Error generating doctor_clinic data: {e.pgerror}"

    def generate_vaccination_data(self, last_key, n_rows, primary_key):
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                    INSERT INTO vaccination ({primary_key}, citizen_id, doctor_id, vaccine_id, clinic_id, date)
                    SELECT i,
                        (SELECT citizen_id FROM citizen ORDER BY random() LIMIT 1),
                        (SELECT doctor_id FROM doctor ORDER BY random() LIMIT 1),
                        (SELECT vaccine_id FROM vaccine ORDER BY random() LIMIT 1),
                        (SELECT clinic_id FROM clinic ORDER BY random() LIMIT 1),
                        NOW() - (floor(random() * 365)::int * INTERVAL '1 day')
                    FROM generate_series(%s, %s) AS i
                """
                cursor.execute(query, (last_key + 1, last_key + n_rows))
                self.conn.commit()
                return f"Inserted {n_rows} vaccination records starting from ID {last_key + 1}."
        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Error generating vaccination data: {e.pgerror}"

    def generate_vaccine_clinic_data(self, last_key, n_rows, primary_key):
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                    INSERT INTO vaccine_clinic ({primary_key}, vaccine_id, clinic_id)
                    SELECT i,
                        (SELECT vaccine_id FROM vaccine ORDER BY random() LIMIT 1),
                        (SELECT clinic_id FROM clinic ORDER BY random() LIMIT 1)
                    FROM generate_series(%s, %s) AS i
                """
                cursor.execute(query, (last_key + 1, last_key + n_rows))
                self.conn.commit()
                return f"Inserted {n_rows} vaccine_clinic records starting from ID {last_key + 1}."
        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Error generating vaccine_clinic data: {e.pgerror}"

    def search_query_1(self, date_start, date_end, citizen_name_pattern):
        """
        Пошук вакцинацій у вказаному діапазоні дат, імені громадянина за шаблоном.
        """
        query = """
          SELECT vaccination.vaccination_id, citizen.name, doctor.name, vaccination.date
           FROM vaccination
           JOIN citizen ON vaccination.citizen_id = citizen.citizen_id
           JOIN doctor ON vaccination.doctor_id = doctor.doctor_id
           WHERE vaccination.date BETWEEN %s AND %s
            AND citizen.name LIKE %s
           GROUP BY vaccination.vaccination_id, citizen.name, doctor.name, vaccination.date
           ORDER BY vaccination.date;
           """
        try:
            with self.conn.cursor() as cursor:
                start_time = time()
                cursor.execute(query, (date_start, date_end, f"%{citizen_name_pattern}%"))
                column_names = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                results = [column_names] + rows
                execution_time = (time() - start_time) * 1000
                return results, execution_time
        except psycopg2.Error as e:
            return f"Database error: {e.pgerror}", 0

    def search_query_2(self, dosage_range, clinic_address_pattern):
        """
        Пошук клінік з вакциною у зазначеному діапазоні дозувань та адресою за шаблоном.
        """
        query = """
           SELECT clinic.address, vaccine.dosage, COUNT(vaccine_clinic.vaccine_id)
           FROM clinic
           JOIN vaccine_clinic ON clinic.clinic_id = vaccine_clinic.clinic_id
           JOIN vaccine ON vaccine_clinic.vaccine_id = vaccine.vaccine_id
           WHERE vaccine.dosage BETWEEN %s AND %s
             AND clinic.address LIKE %s
           GROUP BY clinic.address, vaccine.dosage
           ORDER BY COUNT(vaccine_clinic.vaccine_id) DESC;
           """
        try:
            with self.conn.cursor() as cursor:
                start_time = time()
                cursor.execute(query, (dosage_range[0], dosage_range[1], f"%{clinic_address_pattern}%"))
                column_names = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                results = [column_names] + rows
                execution_time = (time() - start_time) * 1000
                return results, execution_time
        except psycopg2.Error as e:
            return f"Database error: {e.pgerror}", 0

    def search_query_3(self, doctor_name_pattern, max_vaccines):
        """
        Пошук лікарів, які проводили менше зазначеної кількості вакцинацій, і їх клінік.
        """
        query = """
            SELECT doctor.name, clinic.address, COUNT(vaccination.vaccination_id)
            FROM doctor
            JOIN doctor_clinic ON doctor.doctor_id = doctor_clinic.doctor_id
            JOIN clinic ON doctor_clinic.clinic_id = clinic.clinic_id
            LEFT JOIN vaccination ON doctor.doctor_id = vaccination.doctor_id
            WHERE doctor.name LIKE %s
            GROUP BY doctor.name, clinic.address
            HAVING COUNT(vaccination.vaccination_id) < %s
            ORDER BY COUNT(vaccination.vaccination_id) ASC;
           """
        try:
            with self.conn.cursor() as cursor:
                start_time = time()
                cursor.execute(query, (f"%{doctor_name_pattern}%", max_vaccines))
                column_names = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                results = [column_names] + rows
                execution_time = (time() - start_time) * 1000
                return results, execution_time
        except psycopg2.Error as e:
            return f"Database error: {e.pgerror}", 0