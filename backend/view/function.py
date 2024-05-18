import traceback
from flask import request, jsonify, send_file
import controller.handle_score as handle_score
import controller.handle_report as handle_report
from flask import Blueprint
import view.account as account

function = Blueprint('function', __name__)
@function.route('/upload', methods=['POST'])
@account.login_check
def upload_file():
    """
     上传文件
        ---
        parameters:
          - name: name
            in: path
            type: string
            required: true
            description: The name to greet.
        responses:
          200:
            description: A greeting message.
            schema:
              type: object
              properties:
                message:
                  type: string

    """
    try:
        if 'file' not in request.files:
            return 'No file part', 400
        files = request.files.getlist('file')
        if len(files) == 0:
            return 'No files uploaded', 400
        for file in files:
            if file.filename == '':
                return 'No selected file', 400
            res = handle_report.handle_file(file)
        return res, 200
    except Exception as e:
        error_message = f"{str(e)}"
        print(error_message)
        traceback.print_exc()
        return jsonify({'error': error_message}), 500

@function.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@function.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@function.route('/get_grades_and_colleges')
@account.login_check
def get_rules():
    """
         获得所有的年级和学院
            ---
            parameters:
              - name: name
                in: path
                type: string
                required: false
                description: The name to greet.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        return jsonify(handle_score.get_grades_and_colleges())
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        traceback.print_exc()
        return jsonify({'error': error_message}), 500

@function.route('/get_rule_data/<string:grade>/<string:college>')
@account.login_check
def get_rule_data(grade, college):
    """
            通过年级，学院获得规则数据
            ---
            parameters:
              - name: name
                in: path
                type: string
                required: true
                description: The name to greet.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        rule_response = handle_score.get_rule_data(grade, college)
        if rule_response:
            return jsonify(rule_response)
        else:
            return jsonify({'error': 'Rule data not found for the selected grade and college'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@function.route('/update_rule_data', methods=['POST'])
@account.login_check
def update_rule_data():
    """
            更新规则数据
            ---
            parameters:
              - name: sn
                in: path
                type: string
                required: true
                description: The name to greet.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        data = request.get_json()
        handle_score.update_rule_data(data)
        handle_score.update_required_score_and_sum(data)
        return "Rule data and detail data updated successfully!", 200
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        traceback.print_exc()
        return jsonify({'error': error_message}), 500

@function.route('/get_options_of_grades_colleges_majors')
@account.login_check
def get_options_of_grades_colleges_majors():
    """
            获得年级学院专业选项
            ---
            parameters:
              - name: name
                in: path
                type: string
                required: true
                description: The name to greet.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        return jsonify(handle_score.get_grade_college_major_options())
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        traceback.print_exc()
        return jsonify({'error': error_message}), 500

@function.route('/get_rule_data_by_grade_college_major/<string:grade>/<string:college>/<string:major>')
@account.login_check
def get_report_data_by_grade_college_major(grade, college, major):
    """
            通过年级，学院，专业获得规则数据
            ---
            parameters:
              - name: name
                in: path
                type: string
                required: true
                description: The name to greet.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        rule_response = handle_score.get_report_data_by_grade_college_major(grade, college, major)
        if rule_response:
            return jsonify(rule_response)
        else:
            return jsonify({'error': 'Rule data not found for the selected grade, college and major'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@function.route('/get_report_data_by_grade_college/<string:grade>/<string:college>')
@account.login_check
def get_report_data_by_grade_college(grade, college):
    """
            通过年级，学院获得成绩单数据
            ---
            parameters:
              - name: name
                in: path
                type: string
                required: true
                description: The name to greet.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        rule_response = handle_score.get_report_data_by_grade_college(grade, college)
        if rule_response:
            return jsonify(rule_response)
        else:
            return jsonify({'error': 'Rule data not found for the selected grade and college'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@function.route('/update_comprehensive', methods=['PUT'])
@account.login_check
def update_comprehensive():
    """
         更新综合成绩
            ---
            parameters:
              - name: name
                in: path
                type: string
                required: true
                description: The name to greet.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        data = request.get_json()
        handle_score.update_comprehensive(data)
        return "Comprehensive scontroller updated successfully!", 200
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        traceback.print_exc()
        return jsonify({'error': error_message}), 500

@function.route('/get_allocation_data/<string:grade>/<string:college>')
@account.login_check
def get_allocation_data(grade, college):
    """
            通过年级，学院获得分配数据
            ---
            parameters:
              - name: name
                in: path
                type: string
                required: true
                description: The name to greet.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        return jsonify(handle_score.get_allocation_data(grade, college))
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        traceback.print_exc()
        return jsonify({'error': error_message}), 500

@function.route('/update_allocation_data', methods=['PUT'])
@account.login_check
def update_allocation_data():
    """
            更新分配数据
            ---
            parameters:
              - name: name
                in: path
                type: string
                required: true
                description: The name to greet.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        data = request.get_json()
        handle_score.update_allocation_data(data)
        return "Allocation data updated successfully!", 200
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        traceback.print_exc()
        return jsonify({'error': error_message}), 500

@function.route('/download', methods=['POST'])
@account.login_check
def download_file():
    """
         下载文件
            ---
            parameters:
              - name: name
                in: path
                type: string
                required: true
                description: The name to greet.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        outputData = request.get_json()
        download_path = handle_score.generate_output_file(outputData)
        return send_file(download_path, as_attachment=True)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        traceback.print_exc()
        return jsonify({'error': error_message}), 500

@function.route('/get_detail_messages/<string:sn>')
@account.login_check
def get_detail_messages(sn):
    """
         获得详细信息
            ---
            parameters:
              - name: sn
                in: path
                type: integer
                required: true
                description: The sn of the student.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        return jsonify(handle_score.get_sn_detail_from_detail_table(sn))
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        traceback.print_exc()
        return jsonify({'error': error_message}), 500

@function.route('/update_required', methods=['POST'])
@account.login_check
def update_required():
    """
         更新是否纳入智育成绩计算
            ---
            parameters:
              - name: name
                in: path
                type: string
                required: true
                description: The name to greet.
            responses:
              200:
                description: A greeting message.
                schema:
                  type: object
                  properties:
                    message:
                      type: string

        """
    try:
        data = request.get_json()
        handle_score.update_required_by_sn(data)
        return "Required updated successfully!", 200
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        traceback.print_exc()
        return jsonify({'error': error_message}), 500

