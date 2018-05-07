/*
Navicat MySQL Data Transfer

Source Server         : 本地MySQL
Source Server Version : 100129
Source Host           : localhost:3306
Source Database       : rename

Target Server Type    : MYSQL
Target Server Version : 100129
File Encoding         : 65001

Date: 2018-02-09 15:49:10
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for rn_decade
-- ----------------------------
DROP TABLE IF EXISTS `rn_decade`;
CREATE TABLE `rn_decade` (
  `did` int(5) NOT NULL,
  `decade` varchar(20) NOT NULL,
  PRIMARY KEY (`did`,`decade`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of rn_decade
-- ----------------------------
INSERT INTO `rn_decade` VALUES ('1', '先秦');
INSERT INTO `rn_decade` VALUES ('2', '汉朝');
INSERT INTO `rn_decade` VALUES ('3', '魏晋');
INSERT INTO `rn_decade` VALUES ('4', '南北朝');
INSERT INTO `rn_decade` VALUES ('5', '隋朝');
INSERT INTO `rn_decade` VALUES ('6', '唐朝');
INSERT INTO `rn_decade` VALUES ('7', '宋朝');
INSERT INTO `rn_decade` VALUES ('8', '金朝');
INSERT INTO `rn_decade` VALUES ('9', '辽朝');
INSERT INTO `rn_decade` VALUES ('10', '元朝');
INSERT INTO `rn_decade` VALUES ('11', '明朝');
INSERT INTO `rn_decade` VALUES ('12', '清朝');
INSERT INTO `rn_decade` VALUES ('13', '近当代');
SET FOREIGN_KEY_CHECKS=1;
