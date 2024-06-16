def major_college_and_grade_is_exist(info, cursor):
    """Check if the major, college and grade exist in the database at the same time"""
    try:
        cursor.execute(
            f"SELECT * FROM allocation WHERE major='{info['major']}' AND college='{info['college']}' AND grade='{info['grade']}'")
        if cursor.fetchall():
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred while checking if the major, college and grade exist in the database at the same "
              f"time: {str(e)}")
        raise Exception("An error occurred while checking if the major, college and grade exist in the database at "
                        "the same time")


def add_major_college_and_grade_to_allocation_table(info, cursor):
    """Add the major, college and grade to the allocation table"""
    try:
        cursor.execute(
            f"INSERT INTO allocation (major, college, grade) VALUES ('{info['major']}', '{info['college']}', "
            f"'{info['grade']}')")
    except Exception as e:
        print(f"An error occurred while adding the major, college and grade to the allocation table: {str(e)}")
        raise Exception("An error occurred while adding the major, college and grade to the allocation table")
    else:
        print("Major, college and grade added to the allocation table successfully!")
        return True


def get_majors_and_quantities(grade, college, cursor):
    """Get majors and quantities from the allocation table"""
    try:
        cursor.execute(
            f"SELECT major, grade, college, quantity FROM allocation WHERE grade='{grade}' AND college='{college}'")
        result = cursor.fetchall()
        # Convert the result to a dictionary using cursor.description
        columns = [column[0] for column in cursor.description]
        majors_and_quantities = [{columns[i]: row[i] for i in range(len(columns))} for row in result]
        return majors_and_quantities
    except Exception as e:
        print(f"An error occurred while getting majors and quantities from the allocation table: {str(e)}")
        raise Exception("An error occurred while getting majors and quantities from the allocation table")


def get_allocation_data(grade, college, cursor):
    """Get allocation data based on the selected grade and college"""
    try:
        cursor.execute(
            f"SELECT * FROM allocation WHERE grade='{grade}' AND college='{college}'")
        result = cursor.fetchall()
        if result:
            # Convert all the fetched rows to a list of dictionary
            columns = [desc[0] for desc in cursor.description]
            allocation_data = [{columns[i]: row[i] for i in range(len(columns))} for row in result]
            return allocation_data
    except Exception as e:
        print(f"An error occurred while getting allocation data: {str(e)}")
        raise Exception("An error occurred while getting allocation data")
    return None


# update all fields of one row in the allocation table with the new data according id
# data is a dictionary containing the new data
# reorganize the data to fit the SQL statement
def update_allocation_data(data, cursor):
    """Update allocation data in the allocation table"""
    try:
        # Get the ID of the row to be updated
        allocation_id = data.pop('id')
        # Reorganize the data to fit the SQL statement
        update_data = ', '.join([f"{key} = '{value}'" for key, value in data.items()])
        cursor.execute(f"UPDATE allocation SET {update_data} WHERE id = {allocation_id}")
    except Exception as e:
        print(f"An error occurred while updating allocation data: {str(e)}")
        raise Exception("An error occurred while updating allocation data")
    else:
        print("Allocation data updated successfully!")
        return True



