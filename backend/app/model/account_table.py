import controller.mysql_connection as mc  # Assuming this module contains connect_to_database function
import mysql

def insert_account(**kwargs):
    try:
        with mc.connect_to_database() as conn:
            with conn.cursor() as cursor:
                columns = ', '.join(kwargs.keys())
                values_template = ', '.join(['%s'] * len(kwargs))
                sql = f"INSERT INTO account ({columns}) VALUES ({values_template})"
                cursor.execute(sql, tuple(kwargs.values()))
                conn.commit()  # Commit the transaction

                # Get the ID of the last inserted row
                last_inserted_id = cursor.lastrowid
                print(f"Record inserted successfully into account table with ID: {last_inserted_id}")
                return last_inserted_id  # Return the ID of the inserted row
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None  # Return None in case of an error

def update_account(id, **kwargs):
    try:
        with mc.connect_to_database() as conn:
            with conn.cursor() as cursor:
                set_values = ', '.join([f"{key} = %s" for key in kwargs])
                values = list(kwargs.values())
                values.append(id)
                sql = f"UPDATE account SET {set_values} WHERE id = %s"
                cursor.execute(sql, tuple(values))
                conn.commit()  # Commit the transaction
                print(f"Record updated successfully in account table with ID: {id}")
    except mysql.connector.Error as e:
        print(f"Error updating record with ID {id}: {e}")

def delete_account(**kwargs):
    try:
        with mc.connect_to_database() as conn:
            with conn.cursor() as cursor:
                conditions = ' AND '.join([f"{key} = %s" for key in kwargs])
                values = tuple(kwargs.values())
                sql = f"DELETE FROM account WHERE {conditions}"
                cursor.execute(sql, values)
                conn.commit()  # Commit the transaction
                print(f"Record(s) deleted successfully from account table")
    except mysql.connector.Error as e:
        print(f"Error deleting record(s): {e}")


def select_account(**kwargs):
    try:
        with mc.connect_to_database() as conn:
            with conn.cursor() as cursor:
                conditions = ' AND '.join([f"{key} = %s" for key in kwargs])
                values = tuple(kwargs.values())
                sql = f"SELECT * FROM account WHERE {conditions}"
                cursor.execute(sql, values)
                row = cursor.fetchone()

                if row:
                    # Fetch column names from cursor description
                    columns = [column[0] for column in cursor.description]
                    # Create a dictionary mapping column names to row values
                    result = dict(zip(columns, row))
                    print("Record found:")
                    print(result)
                else:
                    print("No record found for the given criteria")

                return result if row else None  # Return the result dictionary or None
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None  # Return None in case of an error


# Example usage:
# insert_account(username='john_doe', password='password123', token='xyztoken', token_invalid=1234567890, verification='1234', verification_invalid=1234567890)
# print("1" * 50)
# update_account(1, username='new_username', password='new_password', token='new_token', token_invalid=9876543210, verification='5678', verification_invalid=9876543210)
# print("1" * 50)
# delete_account(id=1)
# print("1" * 50)
# select_account(username='john_doe', password='password123')
# print("1" * 50)
