/*
Navicat MySQL Data Transfer

Source Server         : 本地MySQL
Source Server Version : 100113
Source Host           : localhost:3306
Source Database       : rename

Target Server Type    : MYSQL
Target Server Version : 100113
File Encoding         : 65001

Date: 2017-08-24 00:41:31
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for rn_content
-- ----------------------------
DROP TABLE IF EXISTS `rn_content`;
CREATE TABLE `rn_content` (
  `wid` int(11) NOT NULL,
  `content` varchar(500) NOT NULL,
  PRIMARY KEY (`wid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
-- Table structure for rn_person
-- ----------------------------
DROP TABLE IF EXISTS `rn_person`;
CREATE TABLE `rn_person` (
  `pid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `did` int(5) NOT NULL,
  `name` varchar(50) NOT NULL,
  `uri` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=12877 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for rn_poem
-- ----------------------------
DROP TABLE IF EXISTS `rn_poem`;
CREATE TABLE `rn_poem` (
  `wid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `uri` varchar(100) NOT NULL,
  PRIMARY KEY (`wid`)
) ENGINE=InnoDB AUTO_INCREMENT=284753 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for rn_poem_content
-- ----------------------------
DROP TABLE IF EXISTS `rn_poem_content`;
CREATE TABLE `rn_poem_content` (
  `wid` int(11) NOT NULL,
  `decade` varchar(30) NOT NULL,
  `poet` varchar(50) NOT NULL,
  `poem` varchar(100) NOT NULL,
  `content` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`wid`),
  UNIQUE KEY `index_wid` (`wid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for rn_word
-- ----------------------------
DROP TABLE IF EXISTS `rn_word`;
CREATE TABLE `rn_word` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wid` int(10) DEFAULT NULL,
  `word` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4788010 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for rn_word_unique
-- ----------------------------
DROP TABLE IF EXISTS `rn_word_unique`;
CREATE TABLE `rn_word_unique` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wid` int(10) DEFAULT NULL,
  `word` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4788010 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for rn_wuxing
-- ----------------------------
DROP TABLE IF EXISTS `rn_wuxing`;
CREATE TABLE `rn_wuxing` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(10) NOT NULL,
  `word` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7150 DEFAULT CHARSET=utf8;

-- ----------------------------
-- View structure for vw_decade_poet_count
-- ----------------------------
DROP VIEW IF EXISTS `vw_decade_poet_count`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER  VIEW `vw_decade_poet_count` AS SELECT b.did, b.decade decade, COUNT(a.`name`) amount
FROM `rn_person` a, rn_decade b
WHERE a.did = b.did
GROUP BY b.decade ;

-- ----------------------------
-- View structure for vw_word_list
-- ----------------------------
DROP VIEW IF EXISTS `vw_word_list`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost`  VIEW `vw_word_list` AS SELECT word, count(word) count FROM `rn_word`
group by word
ORDER BY count(word) desc ;
SET FOREIGN_KEY_CHECKS=1;
