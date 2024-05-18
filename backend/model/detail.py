from mysql.connector.abstracts import MySQLCursorAbstract


def add_detail_message_to_detail_table(detail: list, cursor: MySQLCursorAbstract):
    """Add detail message to the detail table"""
    try:
        # Iterate over the data and insert each line into the table
        for line in detail:
            cursor.execute("""
                        INSERT INTO detail (sn, course, type, point, grade, semester)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, line)
        print(f"Added the detail message to the detail table: {detail}")
        return True
    except Exception as e:
        error_message = f"An error occurred while adding detail message to detail table: {e}"
        print(error_message)
        raise Exception(error_message)


# Delete record from the detail table according to info[sn]
def delete_detail_message_from_detail_table(info: dict, cursor: MySQLCursorAbstract):
    try:
        # Delete data from 'detail' table
        cursor.execute("DELETE FROM detail WHERE sn = %s", (info['sn'],))
        print(f"Deleted the detail message from the detail table: {info}")
        return True
    except Exception as e:
        error_message = f"An error occurred while deleting detail message from detail table: {e}"
        print(error_message)
        raise Exception(error_message)


def modify_detail_message_required_field_by_course(sn: str, course: str, required: int, cursor: MySQLCursorAbstract):
    """modify the required field of detail table according to the sn and the course"""
    try:
        # Update the 'detail' table with the new required
        cursor.execute("UPDATE detail SET required = %s WHERE sn = %s AND course = %s", (required, sn, course))
        print(f"Changed the required field to {required} for the course {course} of sn {sn}")
        return True
    except Exception as e:
        error_message = f"An error occurred while changing required field in detail table: {e}"
        print(error_message)
        raise Exception(error_message)


# modify the required field of detail table according to the sn and the sn and the type
def modify_detail_message_required_field_by_type(sn: str, type: str, required: int, cursor: MySQLCursorAbstract):
    """modify the required field of detail table according to the sn and the sn and the type"""
    try:
        # Update the 'detail' table with the new required
        cursor.execute("UPDATE detail SET required = %s WHERE sn = %s and type = %s", (required, sn, type))
        print(f"Changed the required field to {required} for the sn {sn}")
        return True
    except Exception as e:
        error_message = f"An error occurred while changing required field in detail table: {e}"
        print(error_message)
        raise Exception(error_message)


# get all detail messages from the detail table according to the sn
# return a list
# every item in the list is a dict
def get_sn_detail_from_detail_table(sn: str, cursor: MySQLCursorAbstract):
    try:
        # Query the 'detail' table to get the detail message
        cursor.execute("SELECT * FROM detail WHERE sn = %s", (sn,))
        result = cursor.fetchall()
        # use cursor to make the result to be a list of dict
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in result]
    except Exception as e:
        error_message = f"an error occurred while getting detail messages from the detail table according to the sn: {e}"
        print(error_message)
        raise Exception(error_message)


def modify_detail_message_required_field_by_id(id, required, cursor):
    """modify the required field of detail table according to the id"""
    try:
        # Update the 'detail' table with the new required
        cursor.execute("UPDATE detail SET required = %s WHERE id = %s", (required, id))
        print(f"Changed the required field to {required} for the id {id}")
        return True
    except Exception as e:
        error_message = f"An error occurred while changing required field in detail table: {e}"
        print(error_message)
        raise Exception(error_message)