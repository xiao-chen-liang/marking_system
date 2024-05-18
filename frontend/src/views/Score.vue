<template>
  <div>
    <div id="detailTableDiv" v-if="detailData">
      <h3>成绩详情表</h3>
      <el-table :data="detailData" :row-class-name="rowClassName" style="width: 1000px;" height="350px">
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="course" label="课程"></el-table-column>
        <el-table-column prop="grade" label="成绩" sortable></el-table-column>
        <el-table-column prop="point" label="绩点" sortable></el-table-column>
        <el-table-column prop="semester" label="学期" sortable></el-table-column>
        <el-table-column prop="type" label="类型" sortable></el-table-column>
        <el-table-column prop="required" label="是否包含" sortable>
          <template #default="{ row }">
            {{ getRequiredText(row.required) }}
          </template>
        </el-table-column>

        <el-table-column label="更改包含" align="center">
          <template #default="{ row }">
            <el-switch
                v-model="row.required"
                :active-value="1"
                :inactive-value="0"
                active-text="包含"
                inactive-text="不包含"
                active-color="#13ce66"
                inactive-color="#ff4949"
                :disabled="disable_switch(row)"
                @change="handleRequiredToggle(row)"
            ></el-switch>
          </template>
        </el-table-column>
      </el-table>
      <el-button @click="exit_table()" type="primary" style="margin-top: 20px">关闭</el-button>
    </div>
    <el-row>

      <el-col :span="4">
        <div>
          <el-cascader :options="options" clearable @change="handleCascaderChange" v-model="selectedValue"
                       size="large"></el-cascader>
        </div>
      </el-col>
      <el-col :span="20">
        <div class="headline">
          <h2>{{ selectedValueHeadline }}</h2>
        </div>
        <div class="grid-content bg-purple" id="report_table">
          <el-table :data="reportData" v-loading="reportData === null" stripe class="centered-table">
            <el-table-column label="" align="center">
              <template #default="{ row }">
                <el-button type="text" @click="showDetail(row)">详情</el-button>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="成绩单导出日期" align="center" sortable></el-table-column>
            <el-table-column prop="name" label="姓名" align="center"></el-table-column>
            <el-table-column prop="sn" label="学号" align="center"></el-table-column>
            <el-table-column prop="score" :label="scoreLabel" align="center" sortable></el-table-column>
            <el-table-column prop="comprehensive" :label="comprehensiveLabel" align="center" sortable></el-table-column>
            <el-table-column prop="sum" label="总成绩" align="center" sortable></el-table-column>
            <el-table-column label="更改综合素质成绩" align="center" width="150px">
              <template #default="{ row }">
                <el-input-number v-model="row.inputValue" class="input_box" style="width: 120px" c></el-input-number>
                <el-button type="primary" :disabled="row.inputValue < 0 || row.inputValue > 100"
                           @click="submitInput(row)">提交
                </el-button>
                <el-alert v-if="row.inputValue < 0 || row.inputValue > 100" type="warning" :closable="false" show-icon
                          title="综合素质成绩需为0到100"></el-alert>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {ElTable, ElTableColumn} from 'element-plus';
import axios from '@/config/axios-config.js';
// import axios from 'axios';
import config from "@/config/config";

export default {
  components: {
    ElTable,
    ElTableColumn
  },
  data() {
    return {
      options: null,
      selectedValue: [],
      reportData: [],
      sn_opened: null,
      rule: {
        college: '',
        comprehensive: 0.15,
        grade: null,
        id: null,
        pe: 1,
        policy: 1,
        public: 1,
        score: 0.85,
        skill: 1,
        specialized: 1,
        theory: 1
      },
      detailData: null
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
      return '智育成绩 ' + this.rule.score * 100 + '%';
    },
    comprehensiveLabel() {
      return '综合素质 ' + this.rule.comprehensive * 100 + '%';
    }
  },
  async created() {
    await this.getOptions();
    if (this.options && this.options.length > 0) {
      const defaultGrade = this.options[0].value;
      const defaultCollege = this.options[0].children[0].value;
      const defaultMajor = this.options[0].children[0].children[0].value;
      this.selectedValue = [defaultGrade, defaultCollege, defaultMajor];
      await this.fetchReportData(defaultGrade, defaultCollege, defaultMajor);
      const [grade, college, major] = this.selectedValue;
      const url_getRuleData = `${config.API_BASE_URL}${config.API_PATHS.getRuleData}/${grade}/${college}`;
      const response = await axios.get(url_getRuleData);
      this.rule = response.data;
    }
  },
  methods: {
    disable_switch(row){
      if(row.required == null){
        return true;
      }
      if (row.type === "选修" || row.type === "公修"){
        return true;
      }

      if(row.course === "体育(1)" || row.course === "体育(2)" || row.course === "体育(3)" || row.course === "体育(4)"){
        return true;
      }
      if(row.course === "形势与政策(1)" || row.course === "形势与政策(2)" || row.course === "形势与政策(3)" || row.course === "形势与政策(4)"){
        return true;
      }
      if(row.course === "形势与政策(5)" || row.course === "形势与政策(6)" || row.course === "形势与政策(7)" || row.course === "形势与政策(8)"){
        return true;
      }
      if(row.course === "军事技能" || row.course === "军事理论"){
        return true;
      }

      return false;
    },
    exit_table() {
      this.detailData = null;
      this.handleCascaderChange(this.selectedValue)
    },
    async handleRequiredToggle(row) {
      try {
        // Toggle the required property between 0 and 1
        // row.required = row.required === 1 ? 0 : 1;

        // Make an API call to update the 'required' property
        const url_updateRequired = `${config.API_BASE_URL}${config.API_PATHS.updateRequired}`;
        const data = {id: row.id, required: row.required, sn: this.sn_opened, grade: this.selectedValue[0], college: this.selectedValue[1]};
        const response = await axios.post(url_updateRequired, data);

        // Check the response status to determine success or failure
        if (response.status === 200) {
          this.$message.success(`${row.course}：包含状态更改成功`);
        } else {
          this.$message.error(`${row.course}：包含状态更改失败`);
        }
      } catch (error) {
        console.error('Error toggling required:', error);
        this.$message.error('An error occurred while updating required status');
      }
    },

    rowClassName({row}) {
      // If the row is null or undefined, return immediately
      if (row == null) {
        return;
      }

      // If the row only has the 'major' key
      if (row.required == 0) {
        return 'blue-row'; // Return the class name
      }
    },
    async showDetail(row) {
      try {
        this.sn_opened = row.sn;
        const sn = row.sn;
        const url_getDetailData = `${config.API_BASE_URL}${config.API_PATHS.getDetailMessages}/${sn}`;
        const response = await axios.get(url_getDetailData);
        this.detailData = response.data;

      } catch (error) {
        console.error('Error fetching detail data:', error);
      }
    },
    async getOptions() {
      try {
        const url_getOptions = `${config.API_BASE_URL}${config.API_PATHS.getOptionsOfGradesCollegesMajors}`;
        const response = await axios.get(url_getOptions);
        this.options = response.data;
      } catch (error) {
        console.error('Error fetching options:', error);
      }
    },
    async handleCascaderChange(selectedValues) {
      if (!selectedValues || selectedValues.length === 0) {
        this.reportData = [];
        this.rule = {
          college: '',
          comprehensive: 0.15,
          grade: null,
          id: null,
          pe: 1,
          policy: 1,
          public: 1,
          score: 0.85,
          skill: 1,
          specialized: 1,
          theory: 1
        };
        return;
      }
      const [grade, college, major] = selectedValues;
      const url_getRuleData = `${config.API_BASE_URL}${config.API_PATHS.getRuleData}/${grade}/${college}`;
      const response = await axios.get(url_getRuleData);
      this.rule = response.data;
      await this.fetchReportData(grade, college, major);
    },
    async fetchReportData(grade, college, major) {
      try {
        const url_getReportData = `${config.API_BASE_URL}${config.API_PATHS.getRuleDataByGradeCollegeMajor}/${grade}/${college}/${major}`;
        const response = await axios.get(url_getReportData);
        this.reportData = response.data || [];
        this.reportData.forEach(item => {
          item.inputValue = item.comprehensive;
        });
      } catch (error) {
        console.error('Error fetching rule data:', error);
      }
    },
    async submitInput(row) {
      try {
        row.comprehensive = row.inputValue;
        if (row.comprehensive !== this.originalComprehensive) {
          this.$message.success(`${row.name}的综合素质成绩更改为${row.inputValue}`);
        }
        const url_updateComprehensive = `${config.API_BASE_URL}${config.API_PATHS.updateComprehensive}`;
        const response = await axios.put(url_updateComprehensive, row);
        await this.fetchReportData(this.selectedValue[0], this.selectedValue[1], this.selectedValue[2]);
      } catch (error) {
        console.error('Error updating comprehensive value:', error);
      }
    },
    getRequiredText(required) {
      return required == true ? '包含' : '不包含';
    },

  }
};
</script>

<style scoped>
::v-deep .blue-row {
  background-color: #5ea8f6 !important;
}

#detailTableDiv {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  padding: 20px;
  background: #56b3e7;
  border: 1px solid #ccc;
  border-radius: 15px;
  align-content: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.input_box {
  width: 200px;
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
</style>
