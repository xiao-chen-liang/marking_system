// Define base URL and paths
const API_BASE_URL = 'http://localhost:5000'; // base URL
const API_PATHS = {
    upload: '/upload',
    getGradesAndColleges: '/get_grades_and_colleges',
    getRuleData: '/get_rule_data',
    updateRuleData: '/update_rule_data',
    updateRequired: '/update_required',
    getDetailMessages: '/get_detail_messages',
    getOptionsOfGradesCollegesMajors: '/get_options_of_grades_colleges_majors',
    getRuleDataByGradeAndCollege: '/get_rule_data',
    getRuleDataByGradeCollegeMajor: '/get_rule_data_by_grade_college_major',
    updateComprehensive: '/update_comprehensive',
    updateAllocationData: '/update_allocation_data',
    download: '/download',
    getAllocationData: '/get_allocation_data',
    getReportDataByGradeCollege: '/get_report_data_by_grade_college',
    register: '/register',
    login: '/login',
    modify: '/modify',
    test_login: '/test_login',
    getVerification: '/get_verification',
    passwordChange: '/passwordChange'
};

// Export the base URL and paths
export default {
    API_BASE_URL,
    API_PATHS
};
