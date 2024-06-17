import os
import model.report as report
import model.rule as rule
import model.detail as detail
import model.allocation as allocation
import traceback
import controller.mysql_connection as mysql_connection
from decimal import Decimal
import pandas as pd


def get_grades_and_colleges():
    """Get all grades and colleges from the rule table"""
    conn = mysql_connection.connect_to_database()
    cursor = conn.cursor()
    # Call the get_grades_and_colleges function from rule.py
    res = rule.get_grades_and_colleges(cursor)
    cursor.close()
    return convert_to_cascader_options(res)


# convert the grades and colleges into cascader options format
# sort the data by college and grade
# all labels are string type
# using method similar to the function convert_to_cascader_options_three_layer

def convert_to_cascader_options(data):
    # Sort the data by college and grade
    data_sorted = sorted(data, key=lambda x: (x[1], x[0]))  # Sort by college and grade

    options = []

    # Create a dictionary to store parent nodes based on the college
    parent_dict = {}

    for item in data_sorted:
        grade, college = item
        label = str(f"{grade}级{college}")  # Convert label to string
        value = label  # Use the label as the value

        # Check if the college exists as a parent node
        if college not in parent_dict:
            parent_dict[college] = {'label': str(college), 'value': college, 'children': []}  # Convert label to string

        # Add the grade as a child node under the college
        grade_node = {'label': str(grade), 'value': grade}  # Convert label to string
        parent_dict[college]['children'].append(grade_node)

    # Convert parent_dict values to a list for the cascader options
    options = [{'label': str(v['label']), 'value': v['value'], 'children': v.get('children', [])} for v in
               parent_dict.values()]  # Convert label to string

    return options


def get_rule_data(grade, college):
    """Get rule data based on the selected grade and college"""
    conn = mysql_connection.connect_to_database()
    try:
        cursor = conn.cursor()
        # Call the get_rule_data function from rule.py
        res = rule.get_rule_data(grade, college, cursor)
        return res
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        traceback.print_exc()
        raise e


def update_rule_data(data):
    """Update rule data changed by user in the rule table"""
    conn = mysql_connection.connect_to_database()
    try:
        cursor = conn.cursor()
        # Call the update_rule_data function from rule.py
        id = rule.update_rule_data(data, cursor)
        conn.commit()
        res = {'id': id}
        return res
    except Exception as e:
        conn.rollback()
        raise e


def update_required_score_and_sum(data):
    """Update the required field of the detail table and the score of the report table according to the data changed
    by user"""
    sns = get_sn_by_college_and_grade(data['college'], data['grade'])
    for sn in sns:
        set_required(sn, data)
        score = calculate_score(sn)
        update_score(sn, score)
        sum = calculate_sum(sn, data)
        update_sum(sn, sum)


# select all sn from report table by the college and the grade
def get_sn_by_college_and_grade(college, grade):
    """get all sns from the report table by the college and the grade"""
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            return report.get_sn_by_college_and_grade(college, grade, cursor)


def set_required(sn):
    """set the required field of the detail table according to the sn"""
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            sn_report = report.get_sn_report_from_report_table(sn, cursor)

    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            sn_rule = rule.get_rule_data(sn_report['grade'], sn_report['college'], cursor)

    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            try:
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(1)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(2)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(3)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(4)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(5)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(6)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(7)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(8)", sn_rule['policy'], cursor)

                detail.modify_detail_message_required_field_by_course(sn, "体育(1)", sn_rule['pe'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "体育(2)", sn_rule['pe'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "体育(3)", sn_rule['pe'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "体育(4)", sn_rule['pe'], cursor)

                detail.modify_detail_message_required_field_by_course(sn, "军事技能", sn_rule['skill'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "军事理论", sn_rule['theory'], cursor)

                detail.modify_detail_message_required_field_by_type(sn, "选修", sn_rule['specialized'], cursor)
                detail.modify_detail_message_required_field_by_type(sn, "共修", sn_rule['public'], cursor)

            except Exception as e:
                conn.rollback()
                raise e
            else:
                res = "The required field is updated"
                conn.commit()
                return res


# set the required field of the detail table according to the sn and sn_rule
def set_required(sn, sn_rule):
    """set the required field of the detail table according to the sn and sn_rule"""
    print(sn_rule)
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            try:
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(1)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(2)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(3)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(4)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(5)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(6)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(7)", sn_rule['policy'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "形势与政策(8)", sn_rule['policy'], cursor)

                detail.modify_detail_message_required_field_by_course(sn, "体育(1)", sn_rule['pe'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "体育(2)", sn_rule['pe'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "体育(3)", sn_rule['pe'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "体育(4)", sn_rule['pe'], cursor)

                detail.modify_detail_message_required_field_by_course(sn, "军事技能", sn_rule['skill'], cursor)
                detail.modify_detail_message_required_field_by_course(sn, "军事理论", sn_rule['theory'], cursor)

                detail.modify_detail_message_required_field_by_type(sn, "选修", sn_rule['specialized'], cursor)
                detail.modify_detail_message_required_field_by_type(sn, "公修", sn_rule['public'], cursor)

            except Exception as e:
                conn.rollback()
                raise e
            else:
                res = "The required field is updated"
                conn.commit()
                return res
            finally:
                cursor.close()


# get all detail messages from the detail table according to the sn
def get_sn_detail_from_detail_table(sn):
    """get all detail messages from the detail table according to the sn"""
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            return detail.get_sn_detail_from_detail_table(sn, cursor)


# calculate the score of the student according to the sn
def calculate_score(sn):
    """calculate the score of the student according to the sn"""
    detail_data = get_sn_detail_from_detail_table(sn)
    total_point = 0
    total_grade = 0
    for row in detail_data:
        if row['required'] == 1:
            total_point += row['point']
            total_grade += row['grade'] * row['point']

    score = total_grade / total_point
    return score


# update the score of the student according to the sn
def update_score(sn, score):
    """update the score of the student according to the sn"""
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            try:
                report.update_score({"sn": sn, "score": score}, cursor)
            except Exception as e:
                conn.rollback()
                raise Exception("An error occurred while updating the score")
            else:
                res = "The score is updated"
                conn.commit()
                return res
            finally:
                cursor.close()


def update_required_score_and_sum_of_sn(info):
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            # update the required field of the detail table according to the sn and the sn_rule
            sn_rule = rule.get_rule_data(info['grade'], info['college'], cursor)
    set_required(info['sn'], sn_rule)
    # calculate the score of the student according to the sn
    score = calculate_score(info['sn'])
    # update the score of the student according to the sn
    update_score(info['sn'], score)
    # calculate the sum of the report table
    sum = calculate_sum(info['sn'], sn_rule)
    # update the comprehensive of the report table according to the info
    update_sum(info['sn'], sum)


# calculate the sum of the report table
def calculate_sum(sn, sn_rule):
    """calculate the sum of the report table"""
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            sn_report = report.get_sn_report_from_report_table(sn, cursor)
    sum = sn_report['score'] * Decimal(sn_rule['score']) + sn_report['comprehensive'] * Decimal(
        sn_rule['comprehensive'])
    return sum


def update_sum(sn, sum):
    """update the sum of the report table according to the info"""
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            try:
                report.update_sum({'sn': sn, 'sum': sum}, cursor)
            except Exception as e:
                conn.rollback()
                raise Exception("An error occurred while updating the sum")
            else:
                res = "The sum is updated"
                conn.commit()
                return res
            finally:
                cursor.close()


# select grade, college and major from the report table
# every itme is unique
def get_grade_college_major_from_report_table():
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            return report.get_all_grade_college_major(cursor)


def convert_to_cascader_options_three_layer(data):
    # Sort the data by year (first element of each tuple)
    data_sorted = sorted(data, key=lambda x: (x[0], x[1], x[2]))  # Sort by year, college, and major

    options = []

    # Create a dictionary to store parent nodes based on the year
    parent_dict = {}

    for item in data_sorted:
        year, college, major = item
        label = f"{college} - {major}"
        value = label  # Use the label as the value

        # Check if the year exists as a parent node
        if year not in parent_dict:
            parent_dict[year] = {'label': str(year), 'value': str(year), 'children': []}

        # Check if the college exists as a child node under the year
        college_node = next((node for node in parent_dict[year]['children'] if node['label'] == college), None)

        if not college_node:
            college_node = {'label': college, 'value': college, 'children': []}
            parent_dict[year]['children'].append(college_node)

        # Add the major as a child node under the college
        major_node = {'label': major, 'value': major}  # Use the major as both label and value
        college_node['children'].append(major_node)

    # Convert parent_dict values to a list for the cascader options
    options = [{'label': v['label'], 'value': v['value'], 'children': v.get('children', [])} for v in
               parent_dict.values()]

    return options


# get the options of grade, college and major
def get_grade_college_major_options():
    """Get the options of grade, college and major"""
    data = get_grade_college_major_from_report_table()
    return convert_to_cascader_options_three_layer(data)


def get_report_data_by_grade_college_major(grade, college, major):
    """Get report data based on the selected grade, college and major"""
    conn = mysql_connection.connect_to_database()
    cursor = conn.cursor()
    try:
        # Call the get_report_data_by_grade_college_major function from report.py
        res = report.get_report_data_by_grade_college_major(grade, college, major, cursor)
        return res
    except Exception as e:
        error_message = f"An error occurred while getting report data by grade, college and major: {e}"
        print(error_message)
        raise Exception(error_message)
    finally:
        cursor.close()


# update comprehensive of the report table according to the sn
def update_comprehensive(data):
    """update the comprehensive of the report table according to the sn"""
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            try:
                report.update_comprehensive(data, cursor)
                conn.commit()
                sn_rule = rule.get_rule_data(data['grade'], data['college'], cursor)
                sum = calculate_sum(data['sn'], sn_rule)
                update_sum(data['sn'], sum)
            except Exception as e:
                conn.rollback()
                raise Exception("An error occurred while updating the comprehensive")
            else:
                res = "The comprehensive is updated"
                conn.commit()
                return res
            finally:
                cursor.close()


def get_report_data_by_grade_college(grade, college):
    """Get report data based on the selected grade and college"""
    conn = mysql_connection.connect_to_database()
    cursor = conn.cursor()
    try:
        # Call the get_report_data_by_grade_college function from report.py
        res = report.get_report_data_by_grade_college(grade, college, cursor)
        return res
    except Exception as e:
        error_message = f"An error occurred while getting report data by grade and college: {e}"
        print(error_message)
        raise Exception(error_message)
    finally:
        cursor.close()


def get_majors_and_quantities(grade, college):
    """Get all majors and quantities from the allocation table based on the selected grade and college"""
    conn = mysql_connection.connect_to_database()
    cursor = conn.cursor()
    try:
        # Call the get_majors_and_quantities function from allocation.py
        res = allocation.get_majors_and_quantities(grade, college, cursor)
        return res
    except Exception as e:
        error_message = f"An error occurred while getting all majors and quantities: {e}"
        print(error_message)
        raise Exception(error_message)
    finally:
        cursor.close()


def get_allocation_data(grade, college):
    """Get allocation data based on the selected grade and college"""
    conn = mysql_connection.connect_to_database()
    cursor = conn.cursor()
    try:
        # Call the get_allocation_data function from allocation.py
        res = allocation.get_allocation_data(grade, college, cursor)
        return res
    except Exception as e:
        error_message = f"An error occurred while getting allocation data: {e}"
        print(error_message)
        raise Exception(error_message)
    finally:
        cursor.close()


def update_allocation_data(data):
    """Update allocation data in the allocation table"""
    conn = mysql_connection.connect_to_database()
    cursor = conn.cursor()
    try:
        # Call the update_allocation_data function from allocation.py
        allocation.update_allocation_data(data, cursor)
        conn.commit()
        res = "Allocation data updated successfully!"
        return res
    except Exception as e:
        conn.rollback()
        error_message = f"An error occurred while updating allocation data: {e}"
        print(error_message)
        raise Exception(error_message)
    finally:
        cursor.close()


def generate_output_file(outputData):
    download_directory = '/backend/app/src/result_table'
    file_name = outputData['rule']['college'] + '_' + str(outputData['rule']['grade']) + '_ranking.xlsx'
    download_path = os.path.join(download_directory, file_name)

    # if the file is existed already, delete it
    if os.path.exists(download_path):
        os.remove(download_path)

    # Replace None entries with an empty dictionary
    processed_data = [item if item is not None else {} for item in outputData['reportData']]

    # Create a DataFrame from the processed data
    df = pd.DataFrame(processed_data)

    # Create an Excel writer using pandas ExcelWriter
    with pd.ExcelWriter(download_path, engine='openpyxl') as writer:
        # Write DataFrame to the Excel file
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    print(f"Excel file '{download_path}' created successfully.")

    return download_path


# change the required field of the detail table according to the id
def update_required_by_sn(data):
    """change the required field of the detail table according to the id"""
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            try:
                detail.modify_detail_message_required_field_by_id(data['id'], data['required'], cursor)
            except Exception as e:
                conn.rollback()
                raise Exception("An error occurred while updating the required field")
            else:
                res = "The required field is updated"
                conn.commit()
            finally:
                cursor.close()

    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            # update the required field of the detail table according to the sn and the sn_rule
            sn_rule = rule.get_rule_data(data['grade'], data['college'], cursor)
    # calculate the score of the student according to the sn
    score = calculate_score(data['sn'])
    # update the score of the student according to the sn
    update_score(data['sn'], score)
    # calculate the sum of the report table
    sum = calculate_sum(data['sn'], sn_rule)
    # update the comprehensive of the report table according to the info
    update_sum(data['sn'], sum)
    return res
