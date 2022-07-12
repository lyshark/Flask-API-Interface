/*
 Navicat Premium Data Transfer

 Source Server         : database
 Source Server Type    : SQLite
 Source Server Version : 3035005
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005
 File Encoding         : 65001

 Date: 06/04/2022 14:35:20
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for LocationCountDB
-- ----------------------------
DROP TABLE IF EXISTS "LocationCountDB";
CREATE TABLE "LocationCountDB" (
  "uname" char(32) NOT NULL,
  "mobile" char(32) NOT NULL,
  "lat_count" int NOT NULL,
  "lat_rate" float NOT NULL,
  "trajectory_count" int NOT NULL,
  "trajectory_rate" float NOT NULL,
  "enclosure_count" int NOT NULL,
  "enclosure_rate" int NOT NULL,
  UNIQUE ("mobile" ASC)
);

-- ----------------------------
-- Records of LocationCountDB
-- ----------------------------
INSERT INTO "LocationCountDB" VALUES ('王瑞', '18265477564', 2, 0.0, 0, 0.0, 0, 0);
INSERT INTO "LocationCountDB" VALUES ('郑凯', '18265477568', 0, 0.0, 0, 0.0, 0, 0);

-- ----------------------------
-- Table structure for ObjectDB
-- ----------------------------
DROP TABLE IF EXISTS "ObjectDB";
CREATE TABLE "ObjectDB" (
  "user_key" char(128) NOT NULL,
  "uname" char(32) NOT NULL,
  "mobile" char(32) NOT NULL,
  "ugroup" char(32) NOT NULL,
  "service_mobile" char(32) NOT NULL,
  "message_name" char(512) NOT NULL,
  "is_auth" char(32) NOT NULL
);

-- ----------------------------
-- Records of ObjectDB
-- ----------------------------
INSERT INTO "ObjectDB" VALUES ('1f3dsgf9834r98ug', '王瑞', '18265477564', '测试组', '67882254', 'test', '已授权用户');
INSERT INTO "ObjectDB" VALUES ('1f3dsgf9834r98ug', '郑凯', '18265477568', '开发组', '67882254', 'test', '未授权用户');

-- ----------------------------
-- Table structure for TrajectoryHistoryTableDB
-- ----------------------------
DROP TABLE IF EXISTS "TrajectoryHistoryTableDB";
CREATE TABLE "TrajectoryHistoryTableDB" (
  "mobile" char(32) NOT NULL,
  "start_time" char(32) NOT NULL,
  "end_time" char(32) NOT NULL,
  "local_time" char(32) NOT NULL,
  "x" float NOT NULL,
  "y" float NOT NULL
);

-- ----------------------------
-- Records of TrajectoryHistoryTableDB
-- ----------------------------

-- ----------------------------
-- Table structure for TrajectoryTaskDB
-- ----------------------------
DROP TABLE IF EXISTS "TrajectoryTaskDB";
CREATE TABLE "TrajectoryTaskDB" (
  "uid" int NOT NULL,
  "task_name" char(64) NOT NULL,
  "mobile" char(32) NOT NULL,
  "start_time" char(32) NOT NULL,
  "end_time" char(32) NOT NULL,
  "count" int NOT NULL,
  "rate" float NOT NULL,
  UNIQUE ("uid" ASC),
  UNIQUE ("mobile" ASC)
);

-- ----------------------------
-- Records of TrajectoryTaskDB
-- ----------------------------

-- ----------------------------
-- Table structure for UserDB
-- ----------------------------
DROP TABLE IF EXISTS "UserDB";
CREATE TABLE "UserDB" (
  "username" char(32) NOT NULL,
  "password" char(32) NOT NULL,
  "user_key" char(128) NOT NULL
);

-- ----------------------------
-- Records of UserDB
-- ----------------------------
INSERT INTO "UserDB" VALUES ('lyshark', '123456', '1f3dsgf9834r98ug');
INSERT INTO "UserDB" VALUES ('admin', '1233', 'cef45f9f8480gfi5');

-- ----------------------------
-- Table structure for VerificationCodeDB
-- ----------------------------
DROP TABLE IF EXISTS "VerificationCodeDB";
CREATE TABLE "VerificationCodeDB" (
  "mobile" char(32) NOT NULL,
  "code" char(16) NOT NULL,
  "time_stamp" int NOT NULL,
  UNIQUE ("mobile" ASC),
  UNIQUE ("code" ASC)
);

-- ----------------------------
-- Records of VerificationCodeDB
-- ----------------------------

PRAGMA foreign_keys = true;
