import json
import random
import sqlite3
import string
import time
import traceback
from functools import wraps
import re
from flask import Flask, request, Response
from flask_cors import CORS
from flask import jsonify
from flask import Blueprint
import model.account_table as acc
import view.expiringDict as expiringDict
import controller.handle_account as handle_account

account = Blueprint("account", __name__)
exp_dict = expiringDict.ExpiringDict();




@account.route("/get_verification", methods=["Post"])
def getVerification():
    obtain_dict = request.get_json()
    if len(obtain_dict) != 0 and len(obtain_dict) == 1:
        username = obtain_dict["username"]

        if not is_valid_email(username):
            return jsonify({'message': '传入用户名不合法'}), 400
        else:
            print(username)
            verification_code = handle_account.send_verification_code(username);
            exp_dict.set(username, verification_code)
            print(exp_dict.get(username))

            print("a" * 30)
            print(verification_code)
            print(username)

            return jsonify({'message': '验证码发送成功'}), 200
    else:
        return jsonify({'message': '传入参数个数不正确'}), 400


@account.route("/insert")
def insert():
    id = acc.insert_account(username='john_doe', password='password123', token='xyztoken', token_invalid=1234567890,
                            verification='1234', verification_invalid=1234567890)
    print(id)
    print("1" * 50)
    return "success"


@account.route("/update")
def update():
    acc.update_account(id=5, username='new_username', password='new_password', token='new_token',
                       token_invalid=9876543210, verification='5678', verification_invalid=9876543210)
    print("1" * 50)
    return "success"


@account.route("/delete")
def delete():
    acc.delete_account(username='xiao')
    print("1" * 50)
    return "success"


@account.route("/select")
def table():
    acc.select_account(username='xiao@qq.com', password='111111')
    print("1" * 50)
    return "success"


def is_valid_email(email):
    """
    Check if the given email address is valid.

    Parameters:
        email (str): Email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    # Regular expression pattern for a valid email address
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Match the pattern against the email address
    if re.match(pattern, email):
        return True
    else:
        return False


def is_valid_password(password):
    """
    Check if the given password is valid based on specified criteria.
    The password should contain at least one lowercase letter, one uppercase letter,
    one digit, one special character, and should not contain any other characters.

    Parameters:
        password (str): Password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    # Check if password length is between 8 and 50 characters
    if len(password) < 6 or len(password) > 50:
        return False

    # Check if password contains only allowed characters
    allowed_characters = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?"
    )
    if not set(password).issubset(allowed_characters):
        return False

    # Check if password contains at least one digit
    if not any(char.isdigit() for char in password):
        return False

    # All criteria met, password is valid
    return True


# 登录认证模块
@account.route("/login", methods=["POST"])
def login():
    obtain_dict = request.get_json()
    if len(obtain_dict) != 0 and len(obtain_dict) == 2:
        username = obtain_dict["username"]
        password = obtain_dict["password"]

        print(username, password)

        if is_valid_email(username) == False or is_valid_password(password) == False:
            return jsonify({'message': '传入用户名密码不合法'}), 400

        # 查询用户是否存在
        select = acc.select_account(username=username)
        if select is None:
            return jsonify({'message': '用户名不存在'}), 400

        hashed_password, salt = handle_account.hash_password(password, select['salt'].encode())
        print("1" * 20)

        print(hashed_password)

        if select['password'] != hashed_password:
            return jsonify({'message': '密码错误'}), 400

        token = ''.join(random.sample(string.ascii_letters + string.digits, 32))
        time_stamp = int(time.time()) + 1200
        print("1" * 30)
        print(select)
        print(type(select))
        acc.update_account(select['id'], token=token, token_invalid=time_stamp)
        return jsonify({"message": "登陆成功", "token": token}), 200

    else:
        return jsonify({'message': '输入参数不可用'}), 400


# 检查登录状态 token是否过期的装饰器
def login_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("处理登录逻辑部分: {}".format(request.url))

        print("1" * 30)

        print(request.headers)

        print("1" * 30)

        try:
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(' ')[1]

            print("token: ", token)
        except Exception as e:
            return jsonify({'message': '请先登录!abc'}), 401

        local_timestamp = int(time.time())
        select = acc.select_account(token=token)
        if (select is None) or local_timestamp > select['token_invalid']:
            return jsonify({'message': '登录过期，已退出登录，请重新登录'}), 401

        try:
            acc.update_account(select['id'], token_invalid=local_timestamp + 1200)
            return func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return jsonify({'message': '未处理异常'}), 400

    return wrapper


@account.route("/test_login")
@login_check
def test_login():
    return "You are logged in!"


# 用户注册函数
# Modify the Register route to hash the password before inserting into the database
@account.route("/register", methods=["POST"])
def Register():
    if request.method == "POST":
        obtain_dict = request.get_json()
        if len(obtain_dict) != 0 and len(obtain_dict) == 3:
            reg_username = obtain_dict["username"]
            reg_password = obtain_dict["password"]
            reg_verification = obtain_dict["verification"].strip()

            print("saved code")
            print(exp_dict.get(reg_username))
            print("input code")
            print(reg_verification)
            print("input_username")
            print(reg_username)
            print("input_password")
            print(reg_password)
            if (reg_username in exp_dict) == False or exp_dict.get(reg_username) != reg_verification:
                return jsonify({'message': '验证失败'}), 400

            if not is_valid_email(reg_username) or not is_valid_password(reg_password):
                return jsonify({'message': '传入用户名密码不合法'}), 400

            select = acc.select_account(username=reg_username)
            if select is not None:
                return jsonify({'message': '用户名已被注册'}), 400
            else:
                # Hash the password before inserting into the database
                hashed_password, salt = handle_account.hash_password(reg_password)

                print("a"*30)
                print(reg_password)

                insert = acc.insert_account(username=reg_username, password=hashed_password, salt=salt)
                if isinstance(insert, int):
                    return jsonify({'message': '注册成功'}), 200
                else:
                    return jsonify({'message': '注册失败'}), 400
        else:
            return jsonify({'message': '传入参数个数不正确'}), 400
    return jsonify({'message': '未知错误'})


# Modify the passwordChange route to hash the new password before updating in the database
@account.route("/passwordChange", methods=["POST"])
@login_check
def passwordChange():
    if request.method == "POST":
        obtain_dict = request.get_json()
        if len(obtain_dict) != 0 and len(obtain_dict) == 4:
            if obtain_dict["newPassword"] != obtain_dict["confirmNewPassword"]:
                return jsonify({'message': '密码不一致'}), 400
            print("2" * 32)

            reg_username = obtain_dict["email"]
            reg_password = obtain_dict["newPassword"]
            old_password = obtain_dict["oldPassword"]
            print("3" * 32)

            select = acc.select_account(username=reg_username)

            print("41" * 10)

            old_hashed_password, salt = handle_account.hash_password(old_password, select['salt'].encode())

            print("42" * 10)

            if old_hashed_password != select['password']:
                return jsonify({'message': '密码错误'}), 400
            print("4" * 32)

            if not is_valid_email(reg_username) or not is_valid_password(reg_password):
                return jsonify({'message': '传入用户名密码不合法'}), 400

            print("5" * 32)

            # Hash the new password before updating in the database
            hashed_password, new_salt = handle_account.hash_password(reg_password)
            acc.update_account(id=select['id'], password=hashed_password, salt=new_salt)
            return jsonify({'message': '修改成功'}), 200

    return jsonify({'message': '未知错误'}), 400

