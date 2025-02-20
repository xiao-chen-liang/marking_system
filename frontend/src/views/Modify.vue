<template>
  <div class="password-modify-container">
    <h1 class="password-modify-header">西南林业大学保研评分系统</h1>
    <h1 class="password-modify-header">修改密码</h1>
    <el-form :model="passwordModifyForm" :rules="rules" ref="passwordModifyForm" label-width="100px" class="password-modify-form">
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="passwordModifyForm.email" autocomplete="off" readonly></el-input>
      </el-form-item>
      <el-form-item label="旧密码" prop="oldPassword">
        <el-input type="password" v-model="passwordModifyForm.oldPassword" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="newPassword">
        <el-input type="password" v-model="passwordModifyForm.newPassword" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="确认新密码" prop="confirmNewPassword">
        <el-input type="password" v-model="passwordModifyForm.confirmNewPassword" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handlePasswordChange">修改密码</el-button>
        <el-button type="primary" @click="goToHomePage" class="exit-button">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from '@/config/axios-config.js';
// import axios from 'axios';
import config from "@/config/config";

export default {
  name: 'PasswordModify',
  data() {
    const validateEmail = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入邮箱地址'));
      } else if (!this.is_valid_email(value)) {
        callback(new Error('请输入有效的邮箱地址'));
      } else {
        callback();
      }
    };

    const validateOldPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入旧密码'));
      } else {
        callback();
      }
    };

    const validateNewPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入新密码'));
      } else if (value.length < 6) {
        callback(new Error('密码长度不能少于6位'));
      } else if (value.length > 50) {
        callback(new Error('密码长度不能多于50位'));
      } else if (!this.isStrongPassword(value)) {
        callback(new Error('密码必须包含至少一个小写字母、一个大写字母、一个数字和一个特殊字符'));
      } else {
        callback();
      }
    };

    const validateConfirmNewPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请再次输入新密码'));
      } else if (value !== this.passwordModifyForm.newPassword) {
        callback(new Error('两次输入的密码不一致'));
      } else {
        callback();
      }
    };

    return {
      passwordModifyForm: {
        email: localStorage.getItem('username') || '', // Retrieve email from local storage
        oldPassword: '',
        newPassword: '',
        confirmNewPassword: ''
      },
      rules: {
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { validator: validateEmail, trigger: 'blur' }
        ],
        oldPassword: [
          { required: true, message: '请输入旧密码', trigger: 'blur' },
          { validator: validateOldPassword, trigger: 'blur' }
        ],
        newPassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { validator: validateNewPassword, trigger: 'blur' }
        ],
        confirmNewPassword: [
          { required: true, message: '请再次输入新密码', trigger: 'blur' },
          { validator: validateConfirmNewPassword, trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    is_valid_email(email) {
      const emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
      return emailPattern.test(email);
    },
    isStrongPassword(password) {
      const lowerCasePattern = /[a-z]/;
      const upperCasePattern = /[A-Z]/;
      const digitPattern = /\d/;
      const specialCharPattern = /[!@#$%^&*(),.?":{}|<>]/;

      // return lowerCasePattern.test(password) &&
      //        upperCasePattern.test(password) &&
      //        digitPattern.test(password) &&
      //        specialCharPattern.test(password);

      return digitPattern.test(password)
    },
    handlePasswordChange() {
      this.$refs.passwordModifyForm.validate((valid) => {
        if (valid) {
          const formData = {
            email: this.passwordModifyForm.email,
            oldPassword: this.passwordModifyForm.oldPassword,
            newPassword: this.passwordModifyForm.newPassword,
            confirmNewPassword: this.passwordModifyForm.confirmNewPassword
          };

          const passwordChangeUrl = `${config.API_BASE_URL}${config.API_PATHS.passwordChange}`;
          console.log(passwordChangeUrl);
          axios.post(passwordChangeUrl, formData)
            .then(response => {
              if (response.status === 200) {
                console.log('Password changed successfully:', response.data);
                this.$message.success('密码修改成功');
                localStorage.removeItem('username');
                localStorage.removeItem('token');
                this.$router.push({name: 'login'}); // Redirect to login page
              }
            })
              .catch(error => {
                if (error.response && error.response.status === 400) {
                  console.error('Password change failed:', error.response.data);
                  this.$message.error('密码修改失败: ' + error.response.data.message);
                } else {
                  console.error('An error occurred:', error);
                  this.$message.error('发生了一个错误，请稍后重试');
                }
              });
        } else {
          console.log('Validation failed');
          return false;
        }
      });
    },
    goToHomePage() {
      this.$router.push({name: 'dashboard'});
    }
  }
};
</script>

<style scoped>
.password-modify-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.password-modify-header {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.password-modify-form {
  width: 400px;
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.exit-button {
  margin-left: 149px; /* Adjusted margin for spacing between buttons */
}

/* Override Element UI default styles for form items */
.el-form-item {
  margin-bottom: 40px; /* Add spacing between form items */
}
</style>
