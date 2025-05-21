/*
 Navicat Premium Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80040
 Source Host           : localhost:3306
 Source Schema         : xjtu

 Target Server Type    : MySQL
 Target Server Version : 80040
 File Encoding         : 65001

 Date: 20/05/2025 16:27:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for datasets
-- ----------------------------
DROP TABLE IF EXISTS `datasets`;
CREATE TABLE `datasets`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `dataset` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of datasets
-- ----------------------------
INSERT INTO `datasets` VALUES (1, 'douban');
INSERT INTO `datasets` VALUES (2, 'ppi');

-- ----------------------------
-- Table structure for experiment
-- ----------------------------
DROP TABLE IF EXISTS `experiment`;
CREATE TABLE `experiment`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `outcome_id` int NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of experiment
-- ----------------------------
INSERT INTO `experiment` VALUES (1, 'admin', 7, '2025-05-10 10:28:35');
INSERT INTO `experiment` VALUES (2, 'admin', 8, '2025-05-30 10:28:51');
INSERT INTO `experiment` VALUES (6, 'zmjkk', 51, '2025-05-10 13:16:36');
INSERT INTO `experiment` VALUES (7, 'zmjkk', 52, '2025-05-10 13:18:24');
INSERT INTO `experiment` VALUES (8, 'zmjkk', 53, '2025-05-10 13:22:55');
INSERT INTO `experiment` VALUES (9, 'zmjkk', 54, '2025-05-10 13:24:56');
INSERT INTO `experiment` VALUES (10, 'zmjkk', 55, '2025-05-10 13:27:16');
INSERT INTO `experiment` VALUES (11, 'zmjkk', 56, '2025-05-10 13:28:33');
INSERT INTO `experiment` VALUES (12, 'zmjkk', 57, '2025-05-10 13:30:06');
INSERT INTO `experiment` VALUES (13, 'zmjkk', 58, '2025-05-10 13:41:16');
INSERT INTO `experiment` VALUES (14, 'zmjkk', 59, '2025-05-10 13:42:59');
INSERT INTO `experiment` VALUES (15, 'zmjkk', 60, '2025-05-14 11:49:21');
INSERT INTO `experiment` VALUES (16, 'zmjkk', 61, '2025-05-14 13:25:49');
INSERT INTO `experiment` VALUES (17, 'zmjkk', 62, '2025-05-14 13:28:10');
INSERT INTO `experiment` VALUES (18, 'zmjkk', 63, '2025-05-14 13:28:42');
INSERT INTO `experiment` VALUES (19, 'zmjkk', 64, '2025-05-14 13:29:16');
INSERT INTO `experiment` VALUES (20, 'zmjkk', 65, '2025-05-14 13:31:47');
INSERT INTO `experiment` VALUES (21, 'zmjkk', 66, '2025-05-14 13:34:48');
INSERT INTO `experiment` VALUES (22, 'zmjkk', 67, '2025-05-14 13:36:41');
INSERT INTO `experiment` VALUES (23, 'admin', 68, '2025-05-14 16:22:41');
INSERT INTO `experiment` VALUES (24, 'admin', 69, '2025-05-14 16:24:41');
INSERT INTO `experiment` VALUES (25, 'admin', 70, '2025-05-14 16:25:35');
INSERT INTO `experiment` VALUES (26, 'admin', 71, '2025-05-14 16:26:34');
INSERT INTO `experiment` VALUES (27, 'admin', 72, '2025-05-14 16:29:46');
INSERT INTO `experiment` VALUES (28, 'admin', 73, '2025-05-14 16:31:21');
INSERT INTO `experiment` VALUES (29, 'admin', 74, '2025-05-14 16:32:57');
INSERT INTO `experiment` VALUES (30, 'zmjkk', 75, '2025-05-16 13:38:49');
INSERT INTO `experiment` VALUES (31, 'admin', 76, '2025-05-18 11:52:18');
INSERT INTO `experiment` VALUES (32, 'admin', 77, '2025-05-20 12:59:06');

-- ----------------------------
-- Table structure for outcome
-- ----------------------------
DROP TABLE IF EXISTS `outcome`;
CREATE TABLE `outcome`  (
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `args` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `evaluation` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 79 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of outcome
-- ----------------------------
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0054\',  \'AUC\'= \' 0.5978\',  \'Running time\'= \' 14.226978540420532\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0047\', \'Accuracy\'= \' 0.0000\'}', 7);
INSERT INTO `outcome` VALUES ('GAlign', '--embedding_dim 1 --GAlign_epochs 10', '{ \'Precision_10\'= \' 0.2809\',  \'AUC\'= \' 0.8957\',  \'Running time\'= \' 12.394763469696045\',  \'Precision_5\'= \' 0.1950\',  \'MAP\'= \' 0.1450\', \'Accuracy\'= \' 0.0778\'}', 8);
INSERT INTO `outcome` VALUES ('BigAlign', '--lamb 0.3', '{ \'Precision_10\'= \' 0.0072\',  \'AUC\'= \' 0.8087\',  \'Running time\'= \' 3.412177562713623\',  \'Precision_5\'= \' 0.0036\',  \'MAP\'= \' 0.0066\', \'Accuracy\'= \' 0.0036\'}', 9);
INSERT INTO `outcome` VALUES ('DeepLink', '--embedding_dim 10 --embedding_epochs 20', '{ \'Precision_10\'= \' 0.0018\',  \'AUC\'= \' 0.4967\',  \'Running time\'= \' 167.196715593338\',  \'Precision_5\'= \' 0.0018\',  \'MAP\'= \' 0.0020\', \'Accuracy\'= \' 0.0000\'}', 10);
INSERT INTO `outcome` VALUES ('GTCAlign', '--r_epochs 20 --top_k 5', '{ \'Precision_10\'= \' 0.7630\',  \'AUC\'= \' 0.9928\',  \'Running time\'= None,  \'Precision_5\'= \' 0.5465\',  \'MAP\'= \' 0.6190\', \'Accuracy\'= \' 0.5456\'}', 11);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.6040\',  \'Running time\'= \' 15.756458044052124\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0047\', \'Accuracy\'= \' 0.0000\'}', 12);
INSERT INTO `outcome` VALUES ('GTCAlign', '--r_epochs 30 --top_k 3', '{ \'Precision_10\'= \' 0.7925\',  \'AUC\'= \' 0.9939\',  \'Running time\'= None,  \'Precision_5\'= \' 0.5751\',  \'MAP\'= \' 0.6489\', \'Accuracy\'= \' 0.5751\'}', 13);
INSERT INTO `outcome` VALUES ('REGAL', '', '{ \'Precision_10\'= \' 0.1762\',  \'AUC\'= \' 0.9155\',  \'Running time\'= \' 12.208355903625488\',  \'Precision_5\'= \' 0.1351\',  \'MAP\'= \' 0.0973\', \'Accuracy\'= \' 0.0492\'}', 14);
INSERT INTO `outcome` VALUES ('GAlign', '--GAlign_epochs 30', '{ \'Precision_10\'= \' 0.7701\',  \'AUC\'= \' 0.9899\',  \'Running time\'= \' 35.39320731163025\',  \'Precision_5\'= \' 0.6771\',  \'MAP\'= \' 0.5442\', \'Accuracy\'= \' 0.4311\'}', 15);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0072\',  \'AUC\'= \' 0.6086\',  \'Running time\'= \' 40.729289293289185\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0009\'}', 16);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0072\',  \'AUC\'= \' 0.6037\',  \'Running time\'= \' 17.027602195739746\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0000\'}', 17);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.6012\',  \'Running time\'= \' 16.06363081932068\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0000\'}', 18);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0054\',  \'AUC\'= \' 0.6065\',  \'Running time\'= \' 15.787222146987915\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0047\', \'Accuracy\'= \' 0.0000\'}', 19);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.6001\',  \'Running time\'= \' 16.170696020126343\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0047\', \'Accuracy\'= \' 0.0000\'}', 20);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0072\',  \'AUC\'= \' 0.6026\',  \'Running time\'= \' 15.722263097763062\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0047\', \'Accuracy\'= \' 0.0000\'}', 21);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.6077\',  \'Running time\'= \' 15.434177875518799\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0000\'}', 22);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0045\',  \'AUC\'= \' 0.5929\',  \'Running time\'= \' 16.646034955978394\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0027\'}', 23);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0072\',  \'AUC\'= \' 0.6028\',  \'Running time\'= \' 15.762038469314575\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0000\'}', 24);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.6104\',  \'Running time\'= \' 16.870494842529297\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0047\', \'Accuracy\'= \' 0.0000\'}', 25);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.6035\',  \'Running time\'= \' 16.95035743713379\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0000\'}', 26);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0072\',  \'AUC\'= \' 0.6012\',  \'Running time\'= \' 16.20776081085205\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0000\'}', 27);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0054\',  \'AUC\'= \' 0.5969\',  \'Running time\'= \' 15.178049325942993\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0018\'}', 28);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.6050\',  \'Running time\'= \' 16.523510217666626\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0018\'}', 29);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.5946\',  \'Running time\'= \' 16.042386293411255\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0000\'}', 30);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.5937\',  \'Running time\'= \' 15.250410079956055\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0047\', \'Accuracy\'= \' 0.0000\'}', 31);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.6013\',  \'Running time\'= \' 31.413629055023193\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0018\'}', 40);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.6036\',  \'Running time\'= \' 16.699037075042725\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0047\', \'Accuracy\'= \' 0.0000\'}', 41);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.6007\',  \'Running time\'= \' 15.264742374420166\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0047\', \'Accuracy\'= \' 0.0009\'}', 42);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.6007\',  \'Running time\'= \' 16.676578998565674\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0000\'}', 46);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0072\',  \'AUC\'= \' 0.5963\',  \'Running time\'= \' 16.713284730911255\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0000\'}', 47);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0054\',  \'AUC\'= \' 0.6012\',  \'Running time\'= \' 16.889915466308594\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0046\', \'Accuracy\'= \' 0.0009\'}', 48);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0072\',  \'AUC\'= \' 0.5893\',  \'Running time\'= \' 17.02775001525879\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0047\', \'Accuracy\'= \' 0.0000\'}', 49);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0063\',  \'AUC\'= \' 0.5987\',  \'Running time\'= \' 39.1143217086792\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0047\', \'Accuracy\'= \' 0.0009\'}', 50);
INSERT INTO `outcome` VALUES ('GTCAlign', '--r_epochs 30', '{ \'Precision_10\'= \' 0.7889\',  \'AUC\'= \' 0.9939\',  \'Running time\'= None,  \'Precision_5\'= \' 0.5742\',  \'MAP\'= \' 0.6497\', \'Accuracy\'= \' 0.5760\'}', 51);
INSERT INTO `outcome` VALUES ('GTCAlign', '--top_k 20', '{ \'Precision_10\'= \' 0.8354\',  \'AUC\'= \' 0.9933\',  \'Running time\'= None,  \'Precision_5\'= \' 0.6047\',  \'MAP\'= \' 0.6837\', \'Accuracy\'= \' 0.6064\'}', 52);
INSERT INTO `outcome` VALUES ('GAlign', '--GAlign_epochs 30', '{ \'Precision_10\'= \' 0.7692\',  \'AUC\'= \' 0.9901\',  \'Running time\'= \' 93.07301020622253\',  \'Precision_5\'= \' 0.6771\',  \'MAP\'= \' 0.5424\', \'Accuracy\'= \' 0.4293\'}', 53);
INSERT INTO `outcome` VALUES ('GAlign', '--GAlign_epochs 30', '{ \'Precision_10\'= \' 0.7648\',  \'AUC\'= \' 0.9896\',  \'Running time\'= \' 84.4347198009491\',  \'Precision_5\'= \' 0.6771\',  \'MAP\'= \' 0.5462\', \'Accuracy\'= \' 0.4329\'}', 54);
INSERT INTO `outcome` VALUES ('REGAL', '', '{ \'Precision_10\'= \' 0.1798\',  \'AUC\'= \' 0.9060\',  \'Running time\'= \' 30.68363118171692\',  \'Precision_5\'= \' 0.1324\',  \'MAP\'= \' 0.0942\', \'Accuracy\'= \' 0.0411\'}', 55);
INSERT INTO `outcome` VALUES ('GTCAlign', '--r_epochs 10', '{ \'Precision_10\'= \' 0.6968\',  \'AUC\'= \' 0.9905\',  \'Running time\'= None,  \'Precision_5\'= \' 0.4651\',  \'MAP\'= \' 0.5451\', \'Accuracy\'= \' 0.4669\'}', 56);
INSERT INTO `outcome` VALUES ('GAlign', '--GAlign_epochs 60', '{ \'Precision_10\'= \' 0.7692\',  \'AUC\'= \' 0.9902\',  \'Running time\'= \' 72.37016320228577\',  \'Precision_5\'= \' 0.6780\',  \'MAP\'= \' 0.5483\', \'Accuracy\'= \' 0.4374\'}', 57);
INSERT INTO `outcome` VALUES ('REGAL', '', '{ \'Precision_10\'= \' 0.1592\',  \'AUC\'= \' 0.9153\',  \'Running time\'= \' 7.620827913284302\',  \'Precision_5\'= \' 0.1082\',  \'MAP\'= \' 0.0813\', \'Accuracy\'= \' 0.0304\'}', 58);
INSERT INTO `outcome` VALUES ('FINAL', '', '{ \'Precision_10\'= \' 0.1208\',  \'AUC\'= \' 0.8641\',  \'Running time\'= \' 71.70072317123413\',  \'Precision_5\'= \' 0.0760\',  \'MAP\'= \' 0.0601\', \'Accuracy\'= \' 0.0268\'}', 59);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= None,  \'AUC\'= None,  \'Running time\'= None,  \'Precision_5\'= None,  \'MAP\'= None, \'Accuracy\'= None}', 61);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= None,  \'AUC\'= None,  \'Running time\'= None,  \'Precision_5\'= None,  \'MAP\'= None, \'Accuracy\'= None}', 62);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= None,  \'AUC\'= None,  \'Running time\'= None,  \'Precision_5\'= None,  \'MAP\'= None, \'Accuracy\'= None}', 63);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= None,  \'AUC\'= None,  \'Running time\'= None,  \'Precision_5\'= None,  \'MAP\'= None, \'Accuracy\'= None}', 64);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= None,  \'AUC\'= None,  \'Running time\'= None,  \'Precision_5\'= None,  \'MAP\'= None, \'Accuracy\'= None}', 65);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0057\',  \'AUC\'= \' 0.5075\',  \'Running time\'= \' 11.236568927764893\',  \'Precision_5\'= \' 0.0028\',  \'MAP\'= \' 0.0048\', \'Accuracy\'= \' 0.0017\'}', 66);
INSERT INTO `outcome` VALUES ('FINAL', '', '{ \'Precision_10\'= \' 0.1896\',  \'AUC\'= \' 0.7317\',  \'Running time\'= \' 15.389431953430176\',  \'Precision_5\'= \' 0.0905\',  \'MAP\'= \' 0.0675\', \'Accuracy\'= \' 0.0158\'}', 67);
INSERT INTO `outcome` VALUES ('GTCAlign', '--r_epochs 10', '{ \'Precision_10\'= \' 0.6968\',  \'AUC\'= \' 0.9905\',  \'Running time\'= None,  \'Precision_5\'= \' 0.4651\',  \'MAP\'= \' 0.5451\', \'Accuracy\'= \' 0.4669\'}', 68);
INSERT INTO `outcome` VALUES ('GAlign', '--GAlign_epochs 30', '{ \'Precision_10\'= \' 0.7630\',  \'AUC\'= \' 0.9891\',  \'Running time\'= \' 36.03279232978821\',  \'Precision_5\'= \' 0.6717\',  \'MAP\'= \' 0.5381\', \'Accuracy\'= \' 0.4249\'}', 69);
INSERT INTO `outcome` VALUES ('IsoRank', '', '{ \'Precision_10\'= \' 0.0072\',  \'AUC\'= \' 0.6000\',  \'Running time\'= \' 36.51524233818054\',  \'Precision_5\'= \' 0.0027\',  \'MAP\'= \' 0.0048\', \'Accuracy\'= \' 0.0018\'}', 70);
INSERT INTO `outcome` VALUES ('FINAL', '', '{ \'Precision_10\'= \' 0.1154\',  \'AUC\'= \' 0.8637\',  \'Running time\'= \' 100.37810373306274\',  \'Precision_5\'= \' 0.0769\',  \'MAP\'= \' 0.0614\', \'Accuracy\'= \' 0.0250\'}', 71);
INSERT INTO `outcome` VALUES ('GTCAlign', '--r_epochs 30', '{ \'Precision_10\'= \' 0.7889\',  \'AUC\'= \' 0.9939\',  \'Running time\'= None,  \'Precision_5\'= \' 0.5742\',  \'MAP\'= \' 0.6497\', \'Accuracy\'= \' 0.5760\'}', 72);
INSERT INTO `outcome` VALUES ('GAlign', '--GAlign_epochs 50', '{ \'Precision_10\'= \' 0.7701\',  \'AUC\'= \' 0.9902\',  \'Running time\'= \' 56.84196376800537\',  \'Precision_5\'= \' 0.6717\',  \'MAP\'= \' 0.5443\', \'Accuracy\'= \' 0.4356\'}', 73);
INSERT INTO `outcome` VALUES ('FINAL', '--max_iter 60', '{ \'Precision_10\'= \' 0.1216\',  \'AUC\'= \' 0.8739\',  \'Running time\'= \' 70.70499014854431\',  \'Precision_5\'= \' 0.0850\',  \'MAP\'= \' 0.0641\', \'Accuracy\'= \' 0.0215\'}', 74);
INSERT INTO `outcome` VALUES ('GAlign', '', '{ \'Precision_10\'= \' 0.7594\',  \'AUC\'= \' 0.9895\',  \'Running time\'= \' 45.732532024383545\',  \'Precision_5\'= \' 0.6753\',  \'MAP\'= \' 0.5436\', \'Accuracy\'= \' 0.4365\'}', 75);
INSERT INTO `outcome` VALUES ('REGAL', '', '{ \'Precision_10\'= \' 0.1404\',  \'AUC\'= \' 0.8068\',  \'Running time\'= \' 30.507498502731323\',  \'Precision_5\'= \' 0.0990\',  \'MAP\'= \' 0.0792\', \'Accuracy\'= \' 0.0628\'}', 76);
INSERT INTO `outcome` VALUES ('IsoRank', '', NULL, 77);
INSERT INTO `outcome` VALUES ('GTCAlign', '', NULL, 78);
INSERT INTO `outcome` VALUES ('GTCAlign', '', NULL, 79);

-- ----------------------------
-- Table structure for outcome_dataset
-- ----------------------------
DROP TABLE IF EXISTS `outcome_dataset`;
CREATE TABLE `outcome_dataset`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `outcome_id` int NOT NULL,
  `dataset_type` int NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of outcome_dataset
-- ----------------------------
INSERT INTO `outcome_dataset` VALUES (1, 62, 2);
INSERT INTO `outcome_dataset` VALUES (2, 63, 2);
INSERT INTO `outcome_dataset` VALUES (3, 64, 2);
INSERT INTO `outcome_dataset` VALUES (4, 65, 2);
INSERT INTO `outcome_dataset` VALUES (5, 66, 2);
INSERT INTO `outcome_dataset` VALUES (6, 67, 2);
INSERT INTO `outcome_dataset` VALUES (7, 68, 1);
INSERT INTO `outcome_dataset` VALUES (8, 69, 1);
INSERT INTO `outcome_dataset` VALUES (9, 70, 1);
INSERT INTO `outcome_dataset` VALUES (10, 71, 1);
INSERT INTO `outcome_dataset` VALUES (11, 72, 1);
INSERT INTO `outcome_dataset` VALUES (12, 73, 1);
INSERT INTO `outcome_dataset` VALUES (13, 74, 1);
INSERT INTO `outcome_dataset` VALUES (14, 75, 1);
INSERT INTO `outcome_dataset` VALUES (15, 76, 2);
INSERT INTO `outcome_dataset` VALUES (16, 77, 1);

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role` int NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `account`(`account` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, 'admin', 0);
INSERT INTO `role` VALUES (2, 'XA0qUhDkd7', 1);
INSERT INTO `role` VALUES (3, 'ABWeSUmpN1', 1);
INSERT INTO `role` VALUES (4, 'vkvD2ycBVn', 1);
INSERT INTO `role` VALUES (5, 'bGc7P2XZXM', 1);
INSERT INTO `role` VALUES (6, 'XI9zdkcjjx', 1);
INSERT INTO `role` VALUES (7, 'nv2nPNWppi', 1);
INSERT INTO `role` VALUES (8, 'GMuAfjx8di', 1);
INSERT INTO `role` VALUES (9, '296qRV2ajS', 1);
INSERT INTO `role` VALUES (10, 'rlg4PaZOma', 1);
INSERT INTO `role` VALUES (12, 'mhr', 0);
INSERT INTO `role` VALUES (13, 'zyy', 1);
INSERT INTO `role` VALUES (14, 'zmj', 1);
INSERT INTO `role` VALUES (15, 'abc', 1);
INSERT INTO `role` VALUES (16, 'ddd', 1);
INSERT INTO `role` VALUES (17, 'dda', 1);
INSERT INTO `role` VALUES (18, 'zmjkk', 1);
INSERT INTO `role` VALUES (19, 'zmjkk2', 1);

-- ----------------------------
-- Table structure for role_dict
-- ----------------------------
DROP TABLE IF EXISTS `role_dict`;
CREATE TABLE `role_dict`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role_dict
-- ----------------------------
INSERT INTO `role_dict` VALUES (1, 'admin', 0);
INSERT INTO `role_dict` VALUES (2, 'user', 1);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `pwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `account`(`account` ASC) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1024 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'admin', '123', '');
INSERT INTO `user` VALUES (2, 'XA0qUhDkd7', 'aaa', '123@123.com');
INSERT INTO `user` VALUES (3, 'ABWeSUmpN1', 'aH1MeNiKPH', 'tri@outlook.com');
INSERT INTO `user` VALUES (4, 'vkvD2ycBVn', 'nZa1qXCwe0', 'waihantse@gmail.com');
INSERT INTO `user` VALUES (6, 'XI9zdkcjjx', 'S5c5MY52tY', 'ikkm@yahoo.com');
INSERT INTO `user` VALUES (1016, 'mhr', '123', '2312!23@123.com');
INSERT INTO `user` VALUES (1017, 'zyy', '123', 'test@123.com');
INSERT INTO `user` VALUES (1018, 'zmj', '123', 'test2');
INSERT INTO `user` VALUES (1019, 'abc', '123', '999@9.com');
INSERT INTO `user` VALUES (1020, 'ddd', '123', '9299@9.com');
INSERT INTO `user` VALUES (1021, 'dda', '321', '15091076006@162.com');
INSERT INTO `user` VALUES (1023, 'zmjkk', '123', '15091076006@3.com');
INSERT INTO `user` VALUES (1024, 'zmjkk2', '123', '2158405639@qq.com');

SET FOREIGN_KEY_CHECKS = 1;
