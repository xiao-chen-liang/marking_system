<template>
  <div>
    <el-upload
      class="upload-demo"
      drag
      :before-upload="beforeUpload"
      :file-list="fileList"
      multiple>
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">拖动文件或<em>点击这里</em></div>
    </el-upload>

    <el-table
      :data="tableData"
      style="width: 100%"
      :row-class-name="rowClassName"
      height="400px">
      <el-table-column type="index"></el-table-column>
      <el-table-column
        prop="filename"
        label="文件名称"
        width="180">
      </el-table-column>
      <el-table-column
        prop="message"
        label="信息">
      </el-table-column>
      <el-table-column
        sortable
        prop="status"
        label="状态"
        width="100">
      </el-table-column>
    </el-table>

    <el-button @click="clearTableData" type="danger" style="margin-top: 20px;">清除</el-button>
  </div>
</template>

<script>
import axios from '@/config/axios-config.js';
// import axios from 'axios';
import config from "@/config/config";

export default {
  data() {
    return {
      fileList: [],
      tableData: [],
      isUploading: false,
      i: 0
    };
  },
  created() {
    const testUrl = `${config.API_BASE_URL}${config.API_PATHS.test_login}`;
      axios.get(testUrl)
          .then(response => {
            console.log('Test successful:', response.data);
          })
          .catch(error => {
            console.error('Test failed:', error);
          });

    // Retrieve tableData from local storage when the component is created
    const storedTableData = localStorage.getItem('tableData');
    if (storedTableData) {
      this.tableData = JSON.parse(storedTableData);
    }
  },
  methods: {
    clearTableData() {
      // Clear tableData and remove from local storage
      this.tableData = [];
      localStorage.removeItem('tableData');
      this.i = 0; // Reset count
    },

    rowClassName({ row }) {
      // Check if 'row' is undefined or null
      if (!row) {
        return ''; // Return empty string for no class
      }

      // Determine row class based on 'status' property
      if (row.status === '成功') {
        return 'blue-row'; // Apply 'blue-row' class for success status
      } else if (row.status === '失败') {
        return 'red-row'; // Apply 'red-row' class for error status
      }

      return ''; // Default case: return empty string if no specific class is needed
    },

    async beforeUpload(file) {
      const isPDF = file.type === 'application/pdf';
      const isLt500K = file.size / 1024 < 500;

      if (!isPDF) {
        this.$message.error(file.name + ': 请上传PDF格式成绩单');
        const mes = {count: this.i++, filename: file.name, message: '请上传PDF格式成绩单', status: "失败"};
        this.tableData.unshift(mes);
        return false;
      }
      if (!isLt500K) {
        this.$message.error(file.name + ': 文件大于500KB');
        const mes = {count: this.i++, filename: file.name, message: '文件大于500KB', status: "失败"};
        this.tableData.unshift(mes);
        return false;
      }

      // Add the file to the fileList to display in the UI
      this.fileList.unshift(file);

      // Prevent automatic upload by returning false
      return false;
    },

    async handleFileUpload() {
      // Set isUploading to true
      this.isUploading = true;

      // Iterate through fileList sequentially
      for (let i = 0; i < this.fileList.length; i++) {
        const file = this.fileList[i];

        try {
          const formData = new FormData();
          formData.append('file', file);

          const upload_url = `${config.API_BASE_URL}${config.API_PATHS.upload}`;

          // Use axios to send the file to Flask backend
          const response = await axios.post(upload_url, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });

          // Display success message for the uploaded file
          this.$message.success(`${file.name} ${response.data}`);
          const mes = {count: this.i++, filename: file.name, message: response.data, status: "成功"};
          this.tableData.unshift(mes);

          // Remove the uploaded file from fileList
          // this.removeFile(file);
        } catch (error) {
          // Handle upload error
          if (error.response && error.response.data && error.response.data.error) {
            // Display error message from backend response
            const errorMessage = error.response.data.error;
            this.$message.error(`${file.name}: ${errorMessage}`);
            const mes = {count: this.i++, filename: file.name, message: error.response.data.error, status: "失败"};
            this.tableData.unshift(mes);
          } else {
            // Generic error message for other types of errors
            this.$message.error(`${file.name}: Error uploading file`);
            const mes = {count: this.i++, filename: file.name, message: 'Error uploading file', status: "error"};
            this.tableData.unshift(mes);
          }

          // If an error occurs, do not remove the file from fileList
          continue; // Skip to the next file in case of error
        }
      }

      // Clear fileList after all files are uploaded or processed
      this.fileList = [];

      // Set isUploading to false
      this.isUploading = false;
    },

    removeFile(file) {
      const index = this.fileList.indexOf(file);
      if (index !== -1) {
        this.fileList.splice(index, 1);
      }
    }
  },
  watch: {
    // Watch for changes in tableData and update local storage accordingly
    tableData: {
      handler(newTableData) {
        localStorage.setItem('tableData', JSON.stringify(newTableData));
      },
      deep: true
    },
    fileList: {
      handler() {
        // Trigger file upload when fileList changes and isUploading is false
        if (this.fileList.length > 0 && !this.isUploading) {
          this.handleFileUpload();
        }
      },
      deep: true
    }
  },

};
</script>

<style scoped>
::v-deep .blue-row {
  background-color: #5ea8f6 !important;
}

::v-deep .red-row {
  background-color: #c6a145 !important;
}
</style>
