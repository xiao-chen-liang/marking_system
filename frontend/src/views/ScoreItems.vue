<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">
        <div>
          <el-cascader :options="options" clearable @change="handleCascaderChange" v-model="selectedValue"
                       size="large"></el-cascader>
        </div>
      </el-col>
      <el-col :span="16">
        <div class="headline">
          <h2>{{ selectedValueHeadline }}</h2>
        </div>
        <div class="grid-content bg-purple">
          <el-form :model="rule" ref="ruleForm" :rules="rules" label-width="120px">
            <el-form-item label="公选">
              <el-radio-group v-model="rule.public">
                <el-radio :label="1">包含</el-radio>
                <el-radio :label="0">不包含</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="选修">
              <el-radio-group v-model="rule.specialized">
                <el-radio :label="1">包含</el-radio>
                <el-radio :label="0">不包含</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="体育">
              <el-radio-group v-model="rule.pe">
                <el-radio :label="1">包含</el-radio>
                <el-radio :label="0">不包含</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="形式与政策">
              <el-radio-group v-model="rule.policy">
                <el-radio :label="1">包含</el-radio>
                <el-radio :label="0">不包含</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="军事技能">
              <el-radio-group v-model="rule.skill">
                <el-radio :label="1">包含</el-radio>
                <el-radio :label="0">不包含</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="军事理论">
              <el-radio-group v-model="rule.theory">
                <el-radio :label="1">包含</el-radio>
                <el-radio :label="0">不包含</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="智育成绩权重">
              <el-input v-model="rule.score" placeholder="Enter score" type="number" :step="0.01" class="input_box"
                        :max="1" :min="0"></el-input>
            </el-form-item>
            <el-form-item label="综合素质权重">
              <el-input v-model="rule.comprehensive" placeholder="Enter comprehensive" type="number" :step="0.01"
                        class="input_box" :max="1" :min="0"></el-input>
            </el-form-item>


            <el-form-item>
              <el-button type="primary" @click="submitForm('ruleForm')" :disabled="isSubmitDisabled">提交</el-button>
              <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from '@/config/axios-config.js';
// import axios from 'axios';
import config from "@/config/config";

export default {
  data() {
    return {
      data: null,
      options: null,
      selectedValue: [],
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
      }, // Define the rule variable
      originalRule: null, // Variable to store original values of rule
      rules: {
        score: [{ required: true, message: 'Score is required', trigger: 'blur' }],
        comprehensive: [{ required: true, message: 'Comprehensive is required', trigger: 'blur' }]
      }
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
    isSubmitDisabled() {
      return !this.selectedValue || this.selectedValue.length === 0;
    }
  },
  methods: {
    areDecimalNumbersEqualToOne(num1, num2) {
      const tolerance = 1; // Define a tolerance level for floating-point comparisons
      const sum = num1 + num2;
      return Math.abs(sum - 1) < tolerance;
    },
    async getOptions() {
      try {
        const url_getGradesAndColleges = `${config.API_BASE_URL}${config.API_PATHS.getGradesAndColleges}`
        const response = await axios.get(url_getGradesAndColleges);
        this.options = response.data;
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async handleCascaderChange(selectedValues) {
      if (!selectedValues || selectedValues.length === 0) {
        this.rule ={
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
        this.originalRule = { ...this.rule }; // Save original values
        this.selectedValueHeadline = 'No selection'; // Update headline
      } else {
        const [grade, college] = selectedValues;
        try {
          const url_getRuleData = `${config.API_BASE_URL}${config.API_PATHS.getRuleData}/${grade}/${college}`;
          const response = await axios.get(url_getRuleData);
          this.rule = response.data;
          this.originalRule = { ...this.rule }; // Save original values
          this.selectedValueHeadline = 'Selected value: ' + selectedValues.join(' > ');
        } catch (error) {
          console.error('Error fetching rule data:', error);
          this.$message.error('Failed to fetch rule data. Please try again later.');
        }
      }
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const scoreNumber = parseFloat(this.rule.score);
          const comprehensiveNumber = parseFloat(this.rule.comprehensive);
          if (!isNaN(scoreNumber) && !isNaN(comprehensiveNumber)) {
            if (scoreNumber + comprehensiveNumber === 1) {
              const url_updateRuleData = `${config.API_BASE_URL}${config.API_PATHS.updateRuleData}`;
              axios.post(url_updateRuleData, this.rule)
                .then(response => {
                  console.log('Server response:', response.data);
                  this.$message.success("提交成功");
                })
                .catch(error => {
                  console.error('Error updating rule data:', error);
                  this.$message.error('Error submitting form. Please try again later.');
                });
              this.originalRule = { ...this.rule };
            } else {
              this.$message.error('权重和需为1');
            }
          } else {
            this.$message.error('请输入有效值');
          }
        } else {
          this.$message.error('请输入有效值');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.rule = { ...this.originalRule }; // Reset to original values
      this.$refs[formName].resetFields();
    }
  },
  created() {
    this.getOptions().then(() => {
      if (this.options && this.options.length > 0) {
        const defaultGrade = this.options[0].value;
        const defaultCollege = this.options[0].children[0].value;
        this.selectedValue = [defaultGrade, defaultCollege];
        this.handleCascaderChange(this.selectedValue);
      }
    });
  }
};
</script>



<style scoped>
/* Your scoped styles here */
.input_box {
  width: 200px;
}

.headline {
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: bold;
}
</style>
