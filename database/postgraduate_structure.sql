/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3306
 Source Schema         : postgraduate

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 18/05/2024 15:48:17
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for account
-- ----------------------------
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '密码',
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'token\r\n',
  `token_invalid` bigint NULL DEFAULT NULL COMMENT 'token失效时间',
  `verification` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '验证码',
  `verification_invalid` bigint NULL DEFAULT NULL COMMENT '验证码失效时间',
  `salt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '加盐',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '账号管理表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for allocation
-- ----------------------------
DROP TABLE IF EXISTS `allocation`;
CREATE TABLE `allocation`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `major` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '专业',
  `grade` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '年级',
  `college` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学院',
  `quantity` int NULL DEFAULT 0 COMMENT '年度专业最少保研人数',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 177 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '名额分配表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for detail
-- ----------------------------
DROP TABLE IF EXISTS `detail`;
CREATE TABLE `detail`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `sn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学号',
  `course` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '课程',
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '性质',
  `point` decimal(10, 2) NULL DEFAULT NULL COMMENT '学分',
  `grade` int NULL DEFAULT NULL COMMENT '成绩',
  `required` int NULL DEFAULT 1 COMMENT '是否包含该科目',
  `semester` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 40153 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '成绩详情表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for report
-- ----------------------------
DROP TABLE IF EXISTS `report`;
CREATE TABLE `report`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `sn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '学号',
  `college` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学院',
  `major` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '专业',
  `grade` int NULL DEFAULT NULL COMMENT '年级',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '姓名',
  `total` decimal(10, 2) NULL DEFAULT NULL COMMENT '总学分',
  `required` decimal(10, 2) NULL DEFAULT NULL COMMENT '必修学分',
  `specialized` decimal(10, 2) NULL DEFAULT NULL COMMENT '专业选修学分',
  `public` decimal(10, 2) NULL DEFAULT NULL COMMENT '公共选修学分',
  `score` decimal(10, 2) NULL DEFAULT NULL COMMENT '智育成绩',
  `comprehensive` decimal(10, 2) NULL DEFAULT 0.00 COMMENT '综合成绩',
  `sum` decimal(10, 2) NULL DEFAULT NULL COMMENT '总得分',
  `date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '打印日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 588 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '成绩单表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for rule
-- ----------------------------
DROP TABLE IF EXISTS `rule`;
CREATE TABLE `rule`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `college` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学院',
  `grade` int NULL DEFAULT NULL COMMENT '年级',
  `specialized` int NULL DEFAULT 1 COMMENT '是否包含专业选修课',
  `public` int NULL DEFAULT 1 COMMENT '是否包含公共选修课',
  `policy` int NULL DEFAULT 1 COMMENT '是否包含形式与政策',
  `pe` int NOT NULL DEFAULT 1 COMMENT '是否包含体育',
  `skill` int NULL DEFAULT 1 COMMENT '是否包含军事技能',
  `theory` int NULL DEFAULT 1 COMMENT '是否包含军事理论',
  `score` decimal(10, 2) NULL DEFAULT 0.85 COMMENT '智育成绩权重',
  `comprehensive` decimal(10, 2) NULL DEFAULT 0.15 COMMENT '综合成绩权重',
  `totality` int NULL DEFAULT 0 COMMENT '年度学院保研总人数',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 203 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '评分规则表' ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
