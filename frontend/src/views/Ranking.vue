<template>
  <div>
    <el-row>
      <el-col :span="8">
        <div>
          <el-cascader :options="options" @change="handleCascaderChange" v-model="selectedValue"
                       size="large" clearable></el-cascader>
        </div>
      </el-col>
      <el-col :span="16">
        <div class="headline">
          <h2>{{ selectedValueHeadline }}</h2>
        </div>

        <el-form :model="formData" :rules="formRules" ref="form" label-width="200px" class="allocation">
          <el-row v-if="allocation && allocation.length > 0" v-for="(item, index) in allocation" :key="index">
            <el-col :span="10" class="input-column">
              <el-form-item :label="item.major" prop="allocationItems">
                <!-- Use el-input-number with min value of 0 and step of 1 -->
                <el-input-number v-model="item.quantity" :min="0" :step="1"
                ></el-input-number>
              </el-form-item>
            </el-col>
            <!--            <el-col :span="4">-->
            <!--              <el-button type="primary" :disabled="!validateSumOfQuantities()" @click="submitAllocationItem(index)">-->
            <!--                Update-->
            <!--              </el-button>-->
            <!--            </el-col>-->
          </el-row>

          <el-row v-if="rule">
            <el-col :span="10" class="input-column">
              <el-form-item :label="getSelectedCollegeLabel()" prop="totality">
                <!-- Use el-input-number for totality input -->
                <el-input-number v-model="totality" :min="0" :step="1"
                ></el-input-number>
              </el-form-item>
            </el-col>
            <!--            <el-col :span="4">-->
            <!--              <el-button type="primary" :disabled="!validateSumOfQuantities()" @click="submitForm">Submit</el-button>-->
            <!--            </el-col>-->
          </el-row>

          <el-row>
            <el-col :span="10">
              <!--                make the el-button to located on the right of its container-->

              <el-button type="primary" v-if="rule" :disabled="!validateSumOfQuantities()" @click="submitAll" style="float: right">
                提交
              </el-button>
            </el-col>
          </el-row>
        </el-form>

        <!-- Display error message with bottom margin -->
        <el-row v-if="rule && !validateSumOfQuantities()">
          <el-col :span="24">
            <el-alert
                title="无效输入"
                type="error"
                show-icon
                closable
                class="error-alert"
            />
          </el-col>
        </el-row>

        <div class="grid-content bg-purple" id="report_table">

          <el-table :data="reportData" class="centered-table" :span-method="objectSpanMethod" :row-class-name="rowClassName">
  <el-table-column prop="major" label="专业" align="center"></el-table-column>
  <el-table-column prop="name" label="姓名" align="center"></el-table-column>
  <el-table-column prop="sn" label="学号" align="center"></el-table-column>
  <el-table-column prop="score" :label="scoreLabel" align="center"></el-table-column>
  <el-table-column prop="comprehensive" :label="comprehensiveLabel" align="center"></el-table-column>
  <el-table-column prop="sum" label="总成绩" align="center"></el-table-column>
</el-table>

        </div>

        <el-row>
          <el-col :span="10">
            <!--                make the el-button to located on the right of its container-->

            <el-button v-if="rule" type="primary" @click="downloadTableAsExcel" style="float: right; margin: 10px">
              下载表格
            </el-button>
          </el-col>
        </el-row>

      </el-col>
    </el-row>
  </div>
</template>

<script>
import {ElTable, ElTableColumn, ElAlert, ElInputNumber} from 'element-plus';
import axios from '@/config/axios-config.js';
// import axios from 'axios';
import config from "@/config/config";
export default {
  components: {
    ElTable,
    ElTableColumn,
    ElAlert,
    ElInputNumber
  },
  data() {
    return {
      options: null,
      selectedValue: null,
      reportData: null,
      rule: null,
      allocation: null,
      totality: null,
      formData: {
        totality: ''
      },
      formRules: {}
    };
  },
  computed: {
    selectedValueHeadline() {
      if (!this.selectedValue || this.selectedValue.length === 0) {
        return '未选择';
      } else {
        return this.selectedValue.join(' > ');
      }
    },
    scoreLabel() {
      if (this.rule && this.rule.score !== null) {
        return '智育成绩 ' + (this.rule.score * 100).toFixed(2) + '%';
      } else {
        return '智育成绩';
      }
    },
    comprehensiveLabel() {
      if (this.rule && this.rule.comprehensive !== null) {
        return '综合素质 ' + (this.rule.comprehensive * 100).toFixed(2) + '%';
      } else {
        return '综合素质';
      }
    }
  },

  async created() {
    await this.getOptions();
    if (this.options && this.options.length > 0) {
      const defaultGrade = this.options[0].value;
      const defaultCollege = this.options[0].children[0].value;
      this.selectedValue = [defaultGrade, defaultCollege];
      await this.handleCascaderChange(this.selectedValue);
    }
  },

  methods: {
    rowClassName({ row }) {
    // If the row is null or undefined, return immediately
    if (row == null) {
      return;
    }

    // If the row only has the 'major' key
    if (Object.keys(row).length === 1 && 'major' in row) {
      return 'blue-row'; // Return the class name
    }
  },

   objectSpanMethod({ row, column, rowIndex, columnIndex }) {
  // If the row is null or undefined, return immediately
  if (row == null) {
    return;
  }

  // If the row only has the 'major' key
  if (Object.keys(row).length === 1 && 'major' in row) {
    if (columnIndex === 0) {
      return [1, 6]; // Span 6 columns
    } else {
      return [0, 0]; // Hide other cells in the row
    }
  }
},

    async submitAllocationItem(index) {
      try {
        if (!this.validateSumOfQuantities()) {
          console.error('Sum of quantities exceeds totality.');
          return;
        }

        const itemToUpdate = this.allocation[index];
        const response = await axios.put('http://127.0.0.1:5000/update_allocation_data', itemToUpdate);
        console.log(response.data);

      } catch (error) {
        console.error('Error updating allocation item:', error);
      }
    },

    async submitForm() {
      try {
        this.rule.totality = this.totality;
        const url_getRuleData = `${config.API_BASE_URL}${config.API_PATHS.updateRuleData}`;
        const response = await axios.post(url_getRuleData, this.rule);
        console.log(response.data);

      } catch (error) {
        console.error('Error updating allocation item:', error);
      }
    },

    async submitAll() {
      try {
        for (let i = 0; i < this.allocation.length; i++) {
          await this.submitAllocationItem(i);
        }
        await this.submitForm();

        const [grade, college] = this.selectedValue;

        try {
          const url_getReportData = `${config.API_BASE_URL}${config.API_PATHS.getReportDataByGradeCollege}/${grade}/${college}`;
          const [reportResponse] = await Promise.all([

            axios.get(url_getReportData)
          ]);

          this.reportData = reportResponse.data || null;

          if (this.reportData) {
            this.sortReportDataBySum(); // Sort reportData by 'Sum' column before displaying
          }
        } catch (error) {
          console.error('Error fetching data:', error);
          return ;
        }

        this.$message({
          message: '上传成功',
          type: 'success'
        });
      } catch (error) {
        console.error('Error submitting data:', error);
        this.$message({
          message: 'Error submitting data',
          type: 'error'
        });
      }
    },

    downloadTableAsExcel() {
      const url_download = `${config.API_BASE_URL}${config.API_PATHS.download}`;
      axios({
        url: url_download,
        method: 'POST',
        responseType: 'blob', // Important
        data: {
          reportData: this.reportData,
          rule: this.rule,
          allocation: this.allocation
        }
      })
          .then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', this.rule.college + "_" + this.rule.grade.toString() + "_ranking.xlsx"); //or any other extension
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
          })
          .catch((error) => {
            console.error('Error downloading the file:', error);
          });
    },

    async getOptions() {
      try {
        const url_getGradesAndColleges = `${config.API_BASE_URL}${config.API_PATHS.getGradesAndColleges}`
        const response = await axios.get(url_getGradesAndColleges);
        console.log(response.data)
        this.options = response.data;
      } catch (error) {
        console.error('Error fetching options:', error);

      }
    },

    async handleCascaderChange(selectedValues) {
      if (!selectedValues || selectedValues.length === 0) {
        this.rule = null;
        this.reportData = null;
        this.allocation = null;
        return;
      }

      const [grade, college] = selectedValues;
      try {
        const url_getRuleData = `${config.API_BASE_URL}${config.API_PATHS.getRuleData}/${grade}/${college}`;
        const url_getReportData = `${config.API_BASE_URL}${config.API_PATHS.getReportDataByGradeCollege}/${grade}/${college}`;
        const url_getAllocationData = `${config.API_BASE_URL}${config.API_PATHS.getAllocationData}/${grade}/${college}`;

        const [ruleResponse, reportResponse, allocationResponse] = await Promise.all([
          axios.get(url_getRuleData),
          axios.get(url_getReportData),
          axios.get(url_getAllocationData)
        ]);

        this.rule = ruleResponse.data || null;
        this.reportData = reportResponse.data || null;
        this.allocation = allocationResponse.data || null;

        if (this.reportData) {
          this.sortReportDataBySum(); // Sort reportData by 'Sum' column before displaying
        }

        if (this.rule) {
          this.totality = this.rule.totality;
          this.formData.totality = this.rule.totality;
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },

    sortReportDataBySum() {
      const empty_row = null;
      let qualified = 0;
      const tempData = [];
      let temp_count = 0;
      let allocation_already = 0;

      if (this.reportData && this.reportData.length > 0) {
        this.reportData.sort((a, b) => {
          return a.sum - b.sum; // Sort by 'Sum' column
        });

        for (let item of this.allocation) {
          tempData.unshift(empty_row);
          let count = item.quantity;
          allocation_already += count;
          for (let i = this.reportData.length - 1; i >= 0 && count > 0; i--) {
            if (item.major === this.reportData[i].major) {
              tempData.unshift(this.reportData.splice(i, 1)[0]); // Move matched item to tempData
              qualified++;
              count--;
              temp_count++;
            }
          }
          tempData.unshift({"major": this.rule.grade + " " + this.rule.college + " " + item.major + "  分配名额：" + item.quantity + "  合格人数：" + temp_count});

          temp_count = 0;
        }

        let count = this.rule.totality - qualified;
        tempData.unshift(empty_row);
        for (let i = this.reportData.length - 1; i >= 0 && count > 0; i--) {
          tempData.unshift(this.reportData.splice(i, 1)[0]); // Move unmatched item to tempData
          count--;
          console.log('count:', count);
          temp_count++;
        }
        tempData.unshift({"major": this.rule.grade + " " + this.rule.college+ " 总名额：" + this.rule.totality + "  剩余名额：" + (this.rule.totality - allocation_already) + "  合格人数：" + temp_count});

        temp_count = 0;
        tempData.unshift(empty_row);
        for (let i = this.reportData.length - 1; i >= 0; i--) {
          tempData.unshift(this.reportData.splice(i, 1)[0]);
          temp_count++;
        }
        tempData.unshift({"major": this.rule.grade + " " + this.rule.college + " 不合格：" + temp_count});


        this.reportData = tempData.reverse(); // Reverse the order of tempData

        let j = 0;
        for (let i = 0; i < this.reportData.length; i++) {
          if (this.reportData[i] == null){
            for (j = i + 1; j < this.reportData.length; j++){
              if (!('sn' in this.reportData[j])){
                let t = this.reportData[i];
                this.reportData[i] = this.reportData[j];
                this.reportData[j] = t;
                break;
              }
            }
            i = j;
          }
        }

        console.log(this.reportData)
      }
    },


    getSelectedCollegeLabel() {
      if (this.selectedValue && this.selectedValue.length === 2) {
        const [, college] = this.selectedValue;
        return college;
      }
      return 'College';
    },

    validateSumOfQuantities() {

      console.log("this.allocation", this.allocation, "this.totality", this.totality);
      if (!this.allocation || this.allocation.length === 0 || this.totality === null) {
        console.log("1")
        return false;
      }
      for (let item of this.allocation) {
        if (item.quantity === null){
          console.log("2")
          return false;
        }
      }
      if(this.totality < 0){
        console.log("3")
        return false;
      }
      for (let item of this.allocation) {
        if (item.quantity < 0){
          console.log("4")
          return false;
        }
      }
      let sum = 0;
      for (let item of this.allocation) {
        sum += item.quantity;
      }
      if (sum > this.totality) {
        console.log("5")
        return false;
      }
      if (!Number.isInteger(this.totality)){
        console.log("6")
        return false;
      }
      for (let item of this.allocation) {
        if (!Number.isInteger(item.quantity)){
          console.log("7")
          return false;
        }
      }
      return true;
    }
  }
};
</script>

<style scoped>
  ::v-deep .blue-row {
    background-color: #5ea8f6 !important;
  }

.el-input-number {
  width: 200px;
}

.input-column {
  margin-bottom: 10px;
}

.headline {
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: bold;
}

.centered-table {
  margin: 0 auto;
  max-width: 100%;
}

.el-form-item__label {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  width: 200px;
}

.el-form-item__error {
  white-space: nowrap;
  width: auto;
}

.error-alert {
  margin-bottom: 10px;
}

.el-button {
  margin-bottom: 10px;
}


</style>