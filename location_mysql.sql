/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : localhost:3306
 Source Schema         : location

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 06/04/2022 18:07:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for locationcountdb
-- ----------------------------
DROP TABLE IF EXISTS `locationcountdb`;
CREATE TABLE `locationcountdb`  (
  `uname` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mobile` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `lat_count` int(11) NOT NULL,
  `lat_rate` double NOT NULL,
  `trajectory_count` int(11) NOT NULL,
  `trajectory_rate` double NOT NULL,
  `enclosure_count` int(11) NOT NULL,
  `enclosure_rate` int(11) NOT NULL
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of locationcountdb
-- ----------------------------
INSERT INTO `locationcountdb` VALUES ('王瑞', '18265477564', 2, 0, 0, 0, 0, 0);
INSERT INTO `locationcountdb` VALUES ('郑凯', '18265477568', 0, 0, 0, 0, 0, 0);

-- ----------------------------
-- Table structure for objectdb
-- ----------------------------
DROP TABLE IF EXISTS `objectdb`;
CREATE TABLE `objectdb`  (
  `user_key` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `uname` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mobile` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ugroup` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `service_mobile` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `message_name` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_auth` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of objectdb
-- ----------------------------
INSERT INTO `objectdb` VALUES ('1f3dsgf9834r98ug', '王瑞', '18265477564', '测试组', '67882254', 'test', '已授权用户');
INSERT INTO `objectdb` VALUES ('1f3dsgf9834r98ug', '郑凯', '18265477568', '开发组', '67882254', 'test', '未授权用户');

-- ----------------------------
-- Table structure for trajectoryhistorytabledb
-- ----------------------------
DROP TABLE IF EXISTS `trajectoryhistorytabledb`;
CREATE TABLE `trajectoryhistorytabledb`  (
  `mobile` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `start_time` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `end_time` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `local_time` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `x` double NOT NULL,
  `y` double NOT NULL
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of trajectoryhistorytabledb
-- ----------------------------

-- ----------------------------
-- Table structure for trajectorytaskdb
-- ----------------------------
DROP TABLE IF EXISTS `trajectorytaskdb`;
CREATE TABLE `trajectorytaskdb`  (
  `uid` int(11) NOT NULL,
  `task_name` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mobile` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `start_time` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `end_time` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `count` int(11) NOT NULL,
  `rate` double NOT NULL
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of trajectorytaskdb
-- ----------------------------

-- ----------------------------
-- Table structure for userdb
-- ----------------------------
DROP TABLE IF EXISTS `userdb`;
CREATE TABLE `userdb`  (
  `username` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_key` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of userdb
-- ----------------------------
INSERT INTO `userdb` VALUES ('lyshark', '123456', '1f3dsgf9834r98ug');
INSERT INTO `userdb` VALUES ('admin', '1233', 'cef45f9f8480gfi5');

-- ----------------------------
-- Table structure for verificationcodedb
-- ----------------------------
DROP TABLE IF EXISTS `verificationcodedb`;
CREATE TABLE `verificationcodedb`  (
  `mobile` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `code` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `time_stamp` int(11) NOT NULL
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of verificationcodedb
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
