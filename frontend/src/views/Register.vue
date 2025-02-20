<template>
  <div class="register-container">
    <h1 class="register-header">西南林业大学保研评分系统</h1>
    <h1 class="register-header">注册新账号</h1>
    <el-form :model="registerForm" :rules="rules" ref="registerForm" label-width="100px" class="register-form">
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="registerForm.email" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="registerForm.password" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input type="password" v-model="registerForm.confirmPassword" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="验证码" prop="verification">
        <el-input v-model="registerForm.verification" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="getVerification">获取验证码</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleRegister">注册</el-button>
        <el-button type="primary" @click="goToLoginPage" class="login-button">返回登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios';
import config from "@/config/config";

export default {
  name: 'Register',
  data() {
    const validateEmail = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入邮箱地址')); // Error message for empty email field
      } else if (!this.is_valid_email(value)) {
        callback(new Error('请输入有效的邮箱地址')); // Error message for invalid email format
      } else {
        callback();
      }
    };

    const validatePassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入密码')); // Error message for empty password field
      } else if (value.length < 6) {
        callback(new Error('密码长度不能少于6位')); // Error message for minimum password length
      } else if (value.length > 50) {
        callback(new Error('密码长度不能多于50位')); // Error message for maximum password length
      } else if (!this.isStrongPassword(value)) {
        callback(new Error('密码必须包含至少一个小写字母、一个大写字母、一个数字和一个特殊字符')); // Error message for weak password
      } else {
        callback();
      }
    };

    const validateConfirmPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请再次输入密码')); // Error message for empty confirm password field
      } else if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致')); // Error message for password mismatch
      } else {
        callback();
      }
    };

    return {
      registerForm: {
        email: '',
        password: '',
        confirmPassword: '',
        verification: ''
      },
      rules: {
        email: [
          {required: true, message: '请输入邮箱地址', trigger: 'blur'},
          {validator: validateEmail, trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          {validator: validatePassword, trigger: 'blur'}
        ],
        confirmPassword: [
          {required: true, message: '请再次输入密码', trigger: 'blur'},
          {validator: validateConfirmPassword, trigger: 'blur'}
        ]
      }
    };
  },
  methods: {
    is_valid_email(email) {
      const emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
      return emailPattern.test(email);
    },
    getVerification() {
      if (!this.is_valid_email(this.registerForm.email)) {
        this.$message.warning("邮箱地址格式有误");
        return;
      }
      const formData = {
        username: this.registerForm.email
      };

      const getVerificationUrl = `${config.API_BASE_URL}${config.API_PATHS.getVerification}`;
      // const registerUrl = `${config.API_BASE_URL}${config.API_PATHS.register}`;
      console.log(getVerificationUrl);
      axios.post(getVerificationUrl, formData)
          .then(response => {
            if (response.status === 200) {
              this.$message.success('发送成功');
            }
          })
          .catch(error => {
            if (error.response && error.response.status === 400) {
              // Registration failed, handle the error
              console.error('User registration failed:', error.response.data);
              this.$message.error('发送失败');
            } else {
              // Handle other errors
              console.error('An error occurred:', error);
              this.$message.error('发生了一个错误，请稍后重试'); // Display generic error message
            }
          });
    },
    handleRegister() {
      // Validate the form using the built-in validation of the form component
      this.$refs.registerForm.validate((valid) => {
        if (valid) {
          // Form data is valid, proceed to register the user
          const formData = {
            username: this.registerForm.email, // Assuming 'username' in the backend corresponds to 'email'
            password: this.registerForm.password,
            verification: this.registerForm.verification
          };

          // Send an HTTP POST request to register the user
          const registerUrl = `${config.API_BASE_URL}${config.API_PATHS.register}`;
          console.log(registerUrl);
          axios.post(registerUrl, formData)
              .then(response => {
                if (response.status === 200) {
                  // Registration successful, handle the response
                  console.log('User registration successful:', response.data);
                  this.$message.success('注册成功'); // Display success message
                  this.registerForm = {
                    email: '',
                    password: '',
                    confirmPassword: '',
                    verification: ' ',
                  };
                  // Redirect the user to the login page or perform other actions as needed
                  // this.$router.push({ name: 'login' });
                }
              })
              .catch(error => {
                if (error.response && error.response.status === 400) {
                  // Registration failed, handle the error
                  console.error('User registration failed:', error.response.data);
                  this.$message.error('注册失败: ' + error.response.data.message); // Display error message
                  this.registerForm = {
                    email: '',
                    password: '',
                    confirmPassword: '',
                    verification: ' ',
                  };
                } else {
                  // Handle other errors
                  console.error('An error occurred:', error);
                  this.$message.error('发生了一个错误，请稍后重试'); // Display generic error message
                }
              });
        } else {
          // Form data is invalid, do nothing as the validation messages will be displayed
          console.log('Validation failed');
          return false;
        }
      });
    },
    isStrongPassword(password) {
      const lowerCasePattern = /[a-z]/;
      const upperCasePattern = /[A-Z]/;
      const digitPattern = /\d/;
      const specialCharPattern = /[!@#$%^&*(),.?":{}|<>]/;

      // return lowerCasePattern.test(password) &&
      //     upperCasePattern.test(password) &&
      //     digitPattern.test(password) &&
      //     specialCharPattern.test(password);

      return digitPattern.test(password)
    },
    goToLoginPage() {
      this.$router.push({name: 'login'}); // Navigate to the login page
    }
  }
};
</script>


<style scoped>
.register-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.register-header {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.register-form {
  width: 400px;
  padding: 20px;
  border: 2px solid #ebeef5;
  border-radius: 4px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-button {
  margin-left: 149px; /* Adjusted margin for spacing between buttons */
}

/* Override Element UI default styles for form items */
.el-form-item {
  margin-bottom: 40px; /* Add spacing between form items */
}
</style>
