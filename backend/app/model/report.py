from mysql.connector.abstracts import MySQLCursorAbstract


def add_report_message_to_report_table(info: dict, cursor: MySQLCursorAbstract):
    """Add report message to the report table"""
    try:
        # Insert data into 'report' table
        report_query = "INSERT INTO report (sn, college, major, grade, name, total, required, specialized, public, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        report_data = (
        info['sn'], info.get('college'), info.get('major'), info['grade'], info['name'], info.get('total'),
        info.get('required'), info.get('specialized'), info.get('public'), info.get('date'))
        cursor.execute(report_query, report_data)
        print(f"Added the report message to the report table: {info}")
        return True
    except Exception as e:
        error_message = f"An error occurred while adding report message to report table: {e}"
        print(error_message)
        raise Exception(error_message)


def sn_is_exist(info: dict, cursor: MySQLCursorAbstract):
    """Decide whether the info[sn] exists or not"""
    try:
        # Query the 'report' table to check if the student number already exists
        cursor.execute("SELECT sn FROM report WHERE sn = %s", (info['sn'],))
        result = cursor.fetchone()
        return True if result else False
    except Exception as e:
        error_message = f"An error occurred while checking if sn exists in report table: {e}"
        print(error_message)
        raise Exception(error_message)


def query_date(info: dict, cursor: MySQLCursorAbstract):
    """Query the date according to the info[sn]"""
    try:
        # Query the 'report' table to get the date
        cursor.execute("SELECT date FROM report WHERE sn = %s", (info['sn'],))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        error_message = f"An error occurred while querying date from report table: {e}"
        print(error_message)
        raise Exception(error_message)


def change_date(info: dict, cursor: MySQLCursorAbstract):
    """Change the date to the current date according to the info[sn]"""
    try:
        # Update the 'report' table with the new date
        cursor.execute("UPDATE report SET date = %s WHERE sn = %s", (info['date'], info['sn']))
        print(f"Changed the date to the current date: {info['date']}")
        return True
    except Exception as e:
        error_message = f"An error occurred while changing date in report table: {e}"
        print(error_message)
        raise Exception(error_message)


# get report messages from the detail table according to the sn
# return a dict
def get_sn_report_from_report_table(sn: str, cursor: MySQLCursorAbstract):
    try:
        # Query the 'detail' table to get the detail message
        cursor.execute("SELECT * FROM report WHERE sn = %s", (sn,))
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            # convert the result to a dict using cursor.description
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, result))
    except Exception as e:
        error_message = f"an error occurred while getting report messages from the detail table according to the sn: {e}"
        print(error_message)
        raise Exception(error_message)


# select all sn from the report table by the college and the grade
def get_sn_by_college_and_grade(college: str, grade: int, cursor: MySQLCursorAbstract):
    try:
        # Query the 'report' table to get the sn by college and grade
        cursor.execute("SELECT sn FROM report WHERE college = %s AND grade = %s", (college, grade))
        result = cursor.fetchall()
        return [sn[0] for sn in result]
    except Exception as e:
        error_message = f"An error occurred while getting sn by college and grade from report table: {e}"
        print(error_message)
        raise Exception(error_message)


# update the score of the report table according to the sn
def update_score(info: dict, cursor: MySQLCursorAbstract):
    try:
        # Update the 'report' table with the new score
        cursor.execute("UPDATE report SET score = %s WHERE sn = %s", (info['score'], info['sn']))
        print(f"Changed the score to {info['score']} for the sn {info['sn']}")
        return True
    except Exception as e:
        error_message = f"An error occurred while changing score in report table: {e}"
        print(error_message)
        raise Exception(error_message)


# update the sum of the report table according to the sn
def update_sum(info: dict, cursor: MySQLCursorAbstract):
    try:
        # Update the 'report' table with the new sum
        cursor.execute("UPDATE report SET sum = %s WHERE sn = %s", (info['sum'], info['sn']))
        print(f"Changed the comprehensive to {info['sum']} for the sn {info['sn']}")
        return True
    except Exception as e:
        error_message = f"An error occurred while changing sum in report table: {e}"
        print(error_message)
        raise Exception(error_message)


# delete the report message from the report table according to the sn
def delete_report_message_from_report_table(sn: str, cursor: MySQLCursorAbstract):
    try:
        # Delete the report message from the 'report' table
        cursor.execute("DELETE FROM report WHERE sn = %s", (sn,))
        print(f"Deleted the report message from the report table: {sn}")
        return True
    except Exception as e:
        error_message = f"An error occurred while deleting report message from report table: {e}"
        print(error_message)
        raise Exception(error_message)


# select all grade, college and major from the report table
# every itme is unique
def get_all_grade_college_major(cursor: MySQLCursorAbstract):
    try:
        # Query the 'report' table to get the grade, college and major
        cursor.execute("SELECT DISTINCT grade, college, major FROM report")
        result = cursor.fetchall()
        return result
    except Exception as e:
        error_message = f"An error occurred while getting all grade, college and major from report table: {e}"
        print(error_message)
        raise Exception(error_message)


def get_report_data_by_grade_college_major(grade, college, major, cursor):
    """Get report data based on the selected grade, college and major"""
    try:
        # Query the 'report' table to get the report data based on grade, college and major
        cursor.execute("SELECT * FROM report WHERE grade = %s AND college = %s AND major = %s", (grade, college, major))
        result = cursor.fetchall()
        if result:
            # Convert the fetched row to a dictionary
            columns = [desc[0] for desc in cursor.description]  # Get column names
            report_dict = [dict(zip(columns, row)) for row in result]  # Create dictionary from column names and row data
            return report_dict
    except Exception as e:
        error_message = f"An error occurred while getting report data: {e}"
        print(error_message)
        raise Exception(error_message)


# data = { comprehensive: row.inputValue, sn: row.sn}
# update the comprehensive of the report table according to the sn

def update_comprehensive(data, cursor):
    print(data)
    try:
        # Update the 'report' table with the new comprehensive
        cursor.execute("UPDATE report SET comprehensive = %s WHERE sn = %s", (data['comprehensive'], data['sn']))
        print(f"Changed the comprehensive to {data['comprehensive']} for the sn {data['sn']}")
        return True
    except Exception as e:
        error_message = f"An error occurred while changing comprehensive in report table: {e}"
        print(error_message)
        raise Exception(error_message)


def get_report_data_by_grade_college(grade, college, cursor):
    """Get report data based on the selected grade and college"""
    try:
        # Query the 'report' table to get the report data based on grade and college
        cursor.execute("SELECT * FROM report WHERE grade = %s AND college = %s", (grade, college))
        result = cursor.fetchall()
        if result:
            # Convert the fetched row to a dictionary
            columns = [desc[0] for desc in cursor.description]  # Get column names
            report_dict = [dict(zip(columns, row)) for row in result]  # Create dictionary from column names and row data
            return report_dict
    except Exception as e:
        error_message = f"An error occurred while getting report data: {e}"
        print(error_message)
        raise Exception(error_message)