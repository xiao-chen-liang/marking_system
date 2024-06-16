from werkzeug.datastructures import FileStorage
import pdfplumber
import os
import model.report as report
import model.rule as rule
import model.detail as detail
import model.allocation as allocation
import re
import controller.custom_exceptions as ce
import traceback
import controller.mysql_connection as mysql_connection
import controller.handle_score as handle_score


def extract_info(text: str):
    try:
        """extract information from the text of the first page of the report"""
        # Split the multi-line string into lines and select the first 4 lines
        first_4_lines = text.splitlines()[:4]

        info = {}  # Dictionary to store extracted information

        for line in first_4_lines:
            if '学院' in line:
                info['college'] = line.split('学院: ')[1].split(' ')[0]
            if '专业' in line:
                info['major'] = line.split('专业: ')[1].split(' ')[0]
            if '班级' in line:
                info['grade'] = line.split('班级: ')[1].split(' ')[0]
            if '学号' in line:
                info['sn'] = line.split('学号: ')[1].split(' ')[0]
            if '姓名' in line:
                info['name'] = line.split('姓名: ')[1].split(' ')[0]

        # Split the multi-line string into lines and select the last 4 lines
        lines = text.splitlines()
        last_4_lines = lines[-4:]

        for line in last_4_lines:
            if '获得总学分' in line:
                info['total'] = float(line.split('获得总学分 ')[1].split(' ')[0])
                info['required'] = float(line.split('必修 ')[1].split(' ')[0])
                info['specialized'] = float(line.split('专业选修 ')[1].split(' ')[0])
                info['public'] = float(line.split('公共选修 ')[1].split(' ')[0])
            if '打印日期' in line:
                info['date'] = line.split('打印日期:')[1].split(' ')[0]

        # Use regular expression to find four continuous digits
        match = re.search(r'\d{4}', info['grade'])
        info['grade'] = int(match.group()) if match else None

        return info
    except Exception as e:
        raise Exception("成绩单格式有误")


def extract_data(data: list, info: dict):
    try:
        """extract data from the table of the report"""
        # Find the index of the string '毕业论文（设计）题目'
        index = None
        for i, sublist in enumerate(data):
            if '毕业论文(设计)题目' in sublist:
                index = i
                break

        # Cut out the list after the occurrence of the string
        if index is not None:
            data = data[:index]

        del data[0]

        new_data = []
        for row in data:
            new_row = [row[0], row[1], row[2], row[3], row[4], row[5]]
            new_data.append(new_row)

        for row in data:
            new_row = [row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]]
            new_data.append(new_row)

        for row in data:
            new_row = [row[14], row[15], row[16], row[17], row[18], row[19]]
            new_data.append(new_row)

        cleaned_list = [[item for item in sublist if item is not None and item != ''] for sublist in new_data]

        last_score_index = None  # Initialize last_score_index before the loop

        for i, sublist in enumerate(cleaned_list):
            if '必修' in sublist or '选修' in sublist or '公修' in sublist:
                last_score_index = i

        if last_score_index is not None:
            new = cleaned_list[:last_score_index + 1]
        else:
            new = cleaned_list[:]  # If the condition is never satisfied, use the entire cleaned_list

        semester = None
        last_data = []
        for row in new:
            if len(row) == 1:
                semester = row[0]
            else:
                row.append(semester)
                last_data.append(row)

        detail_data = []

        # Write data to the worksheet
        for row_index, row_data in enumerate(last_data):
            row_data = [info['sn']] + row_data
            detail_data.append(row_data)
    except Exception as e:
        raise Exception("成绩单格式有误")

    if not check_all_pass(detail_data):

        # find weather the report need to be updated or not
        if sn_is_exist(info):
            print("The sn is existed")

            # query the date according to the info[sn]
            database_date = query_date(info)
            # formats of database_date and info[date] is something like '2024/04/12'
            # turn the string to date type
            current_date = database_date.split('/')
            info_date = info['date'].split('/')
            # compare the date
            if current_date < info_date:
                print("The report is the newest, so the preview report need to be delete")
                with mysql_connection.connect_to_database() as conn:
                    with conn.cursor() as cursor:
                        detail.delete_detail_message_from_detail_table(info, cursor)
                        report.delete_report_message_from_report_table(info['sn'], cursor)
                        conn.commit()
                        mes = return_message(info) + "此成绩单存在不及格成绩,该学生已上传成绩单已被删除，不上传此成绩单"
                        raise ce.NotAllCoursesPassedError(mes)
            else:
                raise ce.NotAllCoursesPassedError("Not all courses are passed, but the report is not the newest, "
                                                  "so the preview report are reserved")
        else:
            mes = return_message(info) + "此成绩单存在不及格成绩，缺考或补考成绩，不上传此成绩单"
            raise ce.NotAllCoursesPassedError(mes)

    return detail_data


def query_date(info):
    """query the date the report is generated according to the info[sn] in the report table"""
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            return report.query_date(info, cursor)


def sn_is_exist(info):
    """decide whether the info[sn] exists or not in the report table"""
    with mysql_connection.connect_to_database() as conn:
        with conn.cursor() as cursor:
            return report.sn_is_exist(info, cursor)


def update_report(info, detail_data):
    """when the sn is existed, update the report and the detail table according to the info and detail_data"""
    with mysql_connection.connect_to_database() as conn:
        try:
            cursor = conn.cursor()
            # Call the delete_detail_message_from_detail_table function from detail.py
            detail.delete_detail_message_from_detail_table(info, cursor)
            # Call the add_detail_message_to_detail_table function from detail.py
            detail.add_detail_message_to_detail_table(detail_data, cursor)
            # Call the change_date function from report.py
            report.change_date(info, cursor)
        except Exception as e:
            conn.rollback()
            raise e
        else:
            res = return_message(info) + "更新成功"
            conn.commit()
            return res
        finally:
            cursor.close()


def upload_report(info, detail_data):
    """when the sn is not existed, add the report and the detail table according to the info and detail_data"""
    with mysql_connection.connect_to_database() as conn:
        try:
            cursor = conn.cursor()
            # Call the add_report_message_to_report_table function from report.py
            report.add_report_message_to_report_table(info, cursor)
            # Call the add_detail_message_to_detail_table function from detail.py
            detail.add_detail_message_to_detail_table(detail_data, cursor)
            # judge the college and grade is existed or not
            # if not existed, add the college and grade to the rule table
            if not rule.college_and_grade_is_exist(info, cursor):
                rule.add_college_and_grade_to_rule_table(info, cursor)
            # judge the major, college and grade is existed or not
            # if not existed, add the major, college and grade to the allocation table
            if not allocation.major_college_and_grade_is_exist(info, cursor):
                allocation.add_major_college_and_grade_to_allocation_table(info, cursor)

        except Exception as e:
            conn.rollback()
            raise e
        else:
            res = return_message(info) + "上传成功"
            conn.commit()
        finally:
            cursor.close()

    try:
        handle_score.update_required_score_and_sum_of_sn(info)
    except Exception as e:
        raise e

    return res


def handle_file(file: FileStorage):
    """Handle the uploaded file and extract the required information"""

    upload_directory = 'src/temp_score_report'
    score_report_directory = 'src/score_report'
    try:
        filename = file.filename
        upload_path = os.path.join(upload_directory, filename)

        file.save(upload_path)

        with pdfplumber.open(upload_path) as pdf:
            text = pdf.pages[0].extract_text()
            data = pdf.pages[0].extract_table()

        info = extract_info(text)

        # find weather the report need to be updated or not
        if sn_is_exist(info):
            print("The sn is existed")

            # query the date according to the info[sn]
            database_date = query_date(info)
            # formats of database_date and info[date] is something like '2024/04/12'
            # turn the string to date type
            current_date = database_date.split('/')
            info_date = info['date'].split('/')
            # compare the date
            if current_date < info_date:
                print("The report need to be updated")
                detail_data = extract_data(data, info)

                res = update_report(info, detail_data)

            else:
                mes = return_message(info) + "不是最新的成绩单，不上传此成绩单"
                raise ce.TheReportIsNotNewestError(mes)

        else:
            detail_data = extract_data(data, info)

            res = upload_report(info, detail_data)

    except ce.TheReportIsNotNewestError as e:
        print(f"The report is not the newest")
        os.remove(upload_path)
        traceback.print_exc()
        raise Exception(e.message)

    except ce.NotAllCoursesPassedError as e:
        print(f"Not all courses are passed")
        os.remove(upload_path)
        traceback.print_exc()
        raise Exception(e.message)

    except Exception as e:
        # delete the file
        os.remove(upload_path)
        traceback.print_exc()
        raise e
    else:
        # rename the file to info.sn.pdf and remove it to the score_report directory
        # if the file is existed in the score_report directory, it will be replaced
        score_report_path = os.path.join(score_report_directory, info['sn'] + '.pdf')
        if os.path.exists(score_report_path):
            os.remove(score_report_path)
        os.rename(upload_path, score_report_path)
        return res


def return_message(info):
    return str(info['grade']) + " " + info['college'] + " " + info["major"] + " " + info['sn'] + " " + info['name'] + " "


def check_all_pass(detail_data):
    """every course must be passed"""
    for row in detail_data:
        if row[4] == "缺考" or row[4] == "合格":
            return False
        if row[4] == "免修":
            # delete this row
            detail_data.remove(row)
            continue
        if float(row[4]) < 60:
            return False
    return True
