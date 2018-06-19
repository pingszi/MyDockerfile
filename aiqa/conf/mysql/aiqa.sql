/*
 Navicat Premium Data Transfer

 Source Server         : zsbd_30
 Source Server Type    : MySQL
 Source Server Version : 50635
 Source Host           : 192.168.180.30:3306
 Source Schema         : tax_kbase_test

 Target Server Type    : MySQL
 Target Server Version : 50635
 File Encoding         : 65001

 Date: 11/06/2018 10:25:37
*/
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissions_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 84 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add group', 2, 'add_group');
INSERT INTO `auth_permission` VALUES (6, 'Can change group', 2, 'change_group');
INSERT INTO `auth_permission` VALUES (7, 'Can delete group', 2, 'delete_group');
INSERT INTO `auth_permission` VALUES (8, 'Can add permission', 3, 'add_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can change permission', 3, 'change_permission');
INSERT INTO `auth_permission` VALUES (10, 'Can delete permission', 3, 'delete_permission');
INSERT INTO `auth_permission` VALUES (11, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (12, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (13, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (14, 'Can view group', 2, 'view_group');
INSERT INTO `auth_permission` VALUES (15, 'Can view permission', 3, 'view_permission');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add User Setting', 7, 'add_usersettings');
INSERT INTO `auth_permission` VALUES (26, 'Can change User Setting', 7, 'change_usersettings');
INSERT INTO `auth_permission` VALUES (27, 'Can delete User Setting', 7, 'delete_usersettings');
INSERT INTO `auth_permission` VALUES (28, 'Can add User Widget', 8, 'add_userwidget');
INSERT INTO `auth_permission` VALUES (29, 'Can change User Widget', 8, 'change_userwidget');
INSERT INTO `auth_permission` VALUES (30, 'Can delete User Widget', 8, 'delete_userwidget');
INSERT INTO `auth_permission` VALUES (31, 'Can add log entry', 9, 'add_log');
INSERT INTO `auth_permission` VALUES (32, 'Can change log entry', 9, 'change_log');
INSERT INTO `auth_permission` VALUES (33, 'Can delete log entry', 9, 'delete_log');
INSERT INTO `auth_permission` VALUES (34, 'Can add Bookmark', 10, 'add_bookmark');
INSERT INTO `auth_permission` VALUES (35, 'Can change Bookmark', 10, 'change_bookmark');
INSERT INTO `auth_permission` VALUES (36, 'Can delete Bookmark', 10, 'delete_bookmark');
INSERT INTO `auth_permission` VALUES (37, 'Can view Bookmark', 10, 'view_bookmark');
INSERT INTO `auth_permission` VALUES (38, 'Can view log entry', 9, 'view_log');
INSERT INTO `auth_permission` VALUES (39, 'Can view User Setting', 7, 'view_usersettings');
INSERT INTO `auth_permission` VALUES (40, 'Can view User Widget', 8, 'view_userwidget');
INSERT INTO `auth_permission` VALUES (41, 'Can add revision', 11, 'add_revision');
INSERT INTO `auth_permission` VALUES (42, 'Can change revision', 11, 'change_revision');
INSERT INTO `auth_permission` VALUES (43, 'Can delete revision', 11, 'delete_revision');
INSERT INTO `auth_permission` VALUES (44, 'Can add version', 12, 'add_version');
INSERT INTO `auth_permission` VALUES (45, 'Can change version', 12, 'change_version');
INSERT INTO `auth_permission` VALUES (46, 'Can delete version', 12, 'delete_version');
INSERT INTO `auth_permission` VALUES (47, 'Can view revision', 11, 'view_revision');
INSERT INTO `auth_permission` VALUES (48, 'Can view version', 12, 'view_version');
INSERT INTO `auth_permission` VALUES (49, 'Can add 扩展问题', 13, 'add_taxextendquestionheader');
INSERT INTO `auth_permission` VALUES (50, 'Can change 扩展问题', 13, 'change_taxextendquestionheader');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 扩展问题', 13, 'delete_taxextendquestionheader');
INSERT INTO `auth_permission` VALUES (52, 'Can add 知识', 14, 'add_taxknowledge');
INSERT INTO `auth_permission` VALUES (53, 'Can change 知识', 14, 'change_taxknowledge');
INSERT INTO `auth_permission` VALUES (54, 'Can delete 知识', 14, 'delete_taxknowledge');
INSERT INTO `auth_permission` VALUES (55, 'Can add 关键字', 15, 'add_taxbaskeyword');
INSERT INTO `auth_permission` VALUES (56, 'Can change 关键字', 15, 'change_taxbaskeyword');
INSERT INTO `auth_permission` VALUES (57, 'Can delete 关键字', 15, 'delete_taxbaskeyword');
INSERT INTO `auth_permission` VALUES (58, 'Can add 问答会话', 16, 'add_taxsolveunsolve');
INSERT INTO `auth_permission` VALUES (59, 'Can change 问答会话', 16, 'change_taxsolveunsolve');
INSERT INTO `auth_permission` VALUES (60, 'Can delete 问答会话', 16, 'delete_taxsolveunsolve');
INSERT INTO `auth_permission` VALUES (61, 'Can add 基础数据', 17, 'add_taxbasdata');
INSERT INTO `auth_permission` VALUES (62, 'Can change 基础数据', 17, 'change_taxbasdata');
INSERT INTO `auth_permission` VALUES (63, 'Can delete 基础数据', 17, 'delete_taxbasdata');
INSERT INTO `auth_permission` VALUES (64, 'Can add 同义词', 18, 'add_taxbassynonym');
INSERT INTO `auth_permission` VALUES (65, 'Can change 同义词', 18, 'change_taxbassynonym');
INSERT INTO `auth_permission` VALUES (66, 'Can delete 同义词', 18, 'delete_taxbassynonym');
INSERT INTO `auth_permission` VALUES (67, 'Can add 停用词', 19, 'add_taxbasstopword');
INSERT INTO `auth_permission` VALUES (68, 'Can change 停用词', 19, 'change_taxbasstopword');
INSERT INTO `auth_permission` VALUES (69, 'Can delete 停用词', 19, 'delete_taxbasstopword');
INSERT INTO `auth_permission` VALUES (70, 'Can add 扩展问题明细', 20, 'add_taxextendquestion');
INSERT INTO `auth_permission` VALUES (71, 'Can change 扩展问题明细', 20, 'change_taxextendquestion');
INSERT INTO `auth_permission` VALUES (72, 'Can delete 扩展问题明细', 20, 'delete_taxextendquestion');
INSERT INTO `auth_permission` VALUES (73, 'Can view 基础数据', 17, 'view_taxbasdata');
INSERT INTO `auth_permission` VALUES (74, 'Can view 关键字', 15, 'view_taxbaskeyword');
INSERT INTO `auth_permission` VALUES (75, 'Can view 停用词', 19, 'view_taxbasstopword');
INSERT INTO `auth_permission` VALUES (76, 'Can view 同义词', 18, 'view_taxbassynonym');
INSERT INTO `auth_permission` VALUES (77, 'Can view 扩展问题明细', 20, 'view_taxextendquestion');
INSERT INTO `auth_permission` VALUES (78, 'Can view 扩展问题', 13, 'view_taxextendquestionheader');
INSERT INTO `auth_permission` VALUES (79, 'Can view 知识', 14, 'view_taxknowledge');
INSERT INTO `auth_permission` VALUES (80, 'Can view 问答会话', 16, 'view_taxsolveunsolve');
INSERT INTO `auth_permission` VALUES (81, 'Can add 专家调整', 14, 'add_taxknowledgeproxy');
INSERT INTO `auth_permission` VALUES (82, 'Can change 专家调整', 14, 'change_taxknowledgeproxy');
INSERT INTO `auth_permission` VALUES (83, 'Can delete 专家调整', 14, 'delete_taxknowledgeproxy');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$100000$VIDmoLQCN3Bj$zrIV6UXHPseTgG39DiQgM0pLF4Tm1rK4UteOpx5shAQ=', '2018-05-31 02:17:16.278595', 1, 'admin', '', '', '275598139@qq.com', 1, 1, '2018-04-20 01:26:13.861107');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permissions_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_ibfk_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (17, 'mgbase', 'taxbasdata');
INSERT INTO `django_content_type` VALUES (15, 'mgbase', 'taxbaskeyword');
INSERT INTO `django_content_type` VALUES (19, 'mgbase', 'taxbasstopword');
INSERT INTO `django_content_type` VALUES (18, 'mgbase', 'taxbassynonym');
INSERT INTO `django_content_type` VALUES (20, 'mgbase', 'taxextendquestion');
INSERT INTO `django_content_type` VALUES (13, 'mgbase', 'taxextendquestionheader');
INSERT INTO `django_content_type` VALUES (14, 'mgbase', 'taxknowledge');
INSERT INTO `django_content_type` VALUES (21, 'mgbase', 'taxknowledgeproxy');
INSERT INTO `django_content_type` VALUES (16, 'mgbase', 'taxsolveunsolve');
INSERT INTO `django_content_type` VALUES (11, 'reversion', 'revision');
INSERT INTO `django_content_type` VALUES (12, 'reversion', 'version');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (10, 'xadmin', 'bookmark');
INSERT INTO `django_content_type` VALUES (9, 'xadmin', 'log');
INSERT INTO `django_content_type` VALUES (7, 'xadmin', 'usersettings');
INSERT INTO `django_content_type` VALUES (8, 'xadmin', 'userwidget');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for reversion_revision
-- ----------------------------
DROP TABLE IF EXISTS `reversion_revision`;
CREATE TABLE `reversion_revision`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `comment` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `reversion_revision_user_id_17095f45_fk_auth_user_id`(`user_id`) USING BTREE,
  INDEX `reversion_revision_date_created_96f7c20c`(`date_created`) USING BTREE,
  CONSTRAINT `reversion_revision_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for reversion_version
-- ----------------------------
DROP TABLE IF EXISTS `reversion_version`;
CREATE TABLE `reversion_version`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` varchar(191) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `format` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `serialized_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `object_repr` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `revision_id` int(11) NOT NULL,
  `db` varchar(191) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `reversion_version_db_content_type_id_objec_b2c54f65_uniq`(`db`, `content_type_id`, `object_id`, `revision_id`) USING BTREE,
  INDEX `reversion_version_content_type_id_7d0ff25c_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `reversion_version_revision_id_af9f6a9d_fk_reversion_revision_id`(`revision_id`) USING BTREE,
  CONSTRAINT `reversion_version_ibfk_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `reversion_version_ibfk_2` FOREIGN KEY (`revision_id`) REFERENCES `reversion_revision` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for tax_bas_data
-- ----------------------------
DROP TABLE IF EXISTS `tax_bas_data`;
CREATE TABLE `tax_bas_data`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` decimal(10, 2) NULL DEFAULT NULL,
  `sort` int(11) NULL DEFAULT NULL,
  `desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `type` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type_desc` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `add_who` int(11) NULL DEFAULT NULL,
  `add_time` datetime(6) NOT NULL,
  `edit_who` int(11) NULL DEFAULT NULL,
  `edit_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of tax_bas_data
-- ----------------------------
INSERT INTO `tax_bas_data` VALUES (3, 'MODIFY_STEP', '专家调整步长', 0.10, NULL, NULL, 'PARAM_SETTINGS', '参数设置类', NULL, '2018-04-17 03:28:12.594064', NULL, '2018-05-03 02:01:01.177149');
INSERT INTO `tax_bas_data` VALUES (4, 'THRESHOLD_MAX', '上限阈值', 0.70, NULL, NULL, 'PARAM_SETTINGS', '参数设置类', NULL, '2018-04-17 03:44:52.160851', NULL, '2018-05-22 03:35:04.647589');
INSERT INTO `tax_bas_data` VALUES (5, 'THRESHOLD_MIN', '下限阈值', 0.10, NULL, NULL, 'PARAM_SETTINGS', '参数设置类', NULL, '2018-04-17 03:45:31.041863', NULL, '2018-05-22 03:14:57.481952');
INSERT INTO `tax_bas_data` VALUES (6, 'THRESHOLD_MIN_ADJUST', '专家调整下限阈值', 0.00, NULL, '专家调整功能下限阈值', 'PARAM_SETTINGS', '参数设置类', NULL, '2018-05-22 05:55:17.858051', NULL, '2018-05-22 05:56:21.896051');

-- ----------------------------
-- Table structure for tax_bas_keyword
-- ----------------------------
DROP TABLE IF EXISTS `tax_bas_keyword`;
CREATE TABLE `tax_bas_keyword`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `amplification` decimal(10, 2) NOT NULL,
  `add_who` int(11) NULL DEFAULT NULL,
  `add_time` datetime(6) NOT NULL,
  `edit_who` int(11) NULL DEFAULT NULL,
  `edit_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `keyword`(`keyword`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7307 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;


-- ----------------------------
-- Table structure for tax_bas_stopword
-- ----------------------------
DROP TABLE IF EXISTS `tax_bas_stopword`;
CREATE TABLE `tax_bas_stopword`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_who` int(11) NULL DEFAULT NULL,
  `add_time` datetime(6) NOT NULL,
  `edit_who` int(11) NULL DEFAULT NULL,
  `edit_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `word`(`word`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2608 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;


-- ----------------------------
-- Table structure for tax_bas_synonym
-- ----------------------------
DROP TABLE IF EXISTS `tax_bas_synonym`;
CREATE TABLE `tax_bas_synonym`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_who` int(11) NULL DEFAULT NULL,
  `add_time` datetime(6) NOT NULL,
  `edit_who` int(11) NULL DEFAULT NULL,
  `edit_time` datetime(6) NOT NULL,
  `keyword` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `word`(`word`) USING BTREE,
  INDEX `tax_bas_synonym_keyword_a38cf756_fk_tax_bas_keyword_keyword`(`keyword`) USING BTREE,
  CONSTRAINT `tax_bas_synonym_ibfk_1` FOREIGN KEY (`keyword`) REFERENCES `tax_bas_keyword` (`keyword`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of tax_bas_synonym
-- ----------------------------
INSERT INTO `tax_bas_synonym` VALUES (4, '个税', NULL, '2018-04-26 00:58:15.892693', NULL, '2018-04-26 00:58:15.892760', '个人所得税');

-- ----------------------------
-- Table structure for tax_extend_question
-- ----------------------------
DROP TABLE IF EXISTS `tax_extend_question`;
CREATE TABLE `tax_extend_question`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tf_value` decimal(10, 6) NOT NULL,
  `idf_value` decimal(10, 6) NOT NULL,
  `weighted_value` decimal(10, 6) NOT NULL,
  `amplification` decimal(10, 2) NOT NULL,
  `add_who` int(11) NULL DEFAULT NULL,
  `add_time` datetime(6) NOT NULL,
  `edit_who` int(11) NULL DEFAULT NULL,
  `edit_time` datetime(6) NOT NULL,
  `extend_question_id` int(11) NOT NULL,
  `keyword` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tax_extend_question_extend_question_id_de70d43d_fk_tax_exten`(`extend_question_id`) USING BTREE,
  CONSTRAINT `tax_extend_question_ibfk_1` FOREIGN KEY (`extend_question_id`) REFERENCES `tax_extend_question_header` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10605 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for tax_extend_question_header
-- ----------------------------
DROP TABLE IF EXISTS `tax_extend_question_header`;
CREATE TABLE `tax_extend_question_header`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_who` int(11) NULL DEFAULT NULL,
  `add_time` datetime(6) NOT NULL,
  `edit_who` int(11) NULL DEFAULT NULL,
  `edit_time` datetime(6) NOT NULL,
  `knowledge_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tax_extend_question__knowledge_id_da57696b_fk_tax_knowl`(`knowledge_id`) USING BTREE,
  CONSTRAINT `tax_extend_question_header_ibfk_1` FOREIGN KEY (`knowledge_id`) REFERENCES `tax_knowledge` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1436 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for tax_knowledge
-- ----------------------------
DROP TABLE IF EXISTS `tax_knowledge`;
CREATE TABLE `tax_knowledge`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `counter` int(10) UNSIGNED NOT NULL,
  `sd_question` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sd_answer` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_who` int(11) NULL DEFAULT NULL,
  `add_time` datetime(6) NOT NULL,
  `edit_who` int(11) NULL DEFAULT NULL,
  `edit_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1283 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for tax_solve_unsolve
-- ----------------------------
DROP TABLE IF EXISTS `tax_solve_unsolve`;
CREATE TABLE `tax_solve_unsolve`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_key` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `question` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `solve` int(10) UNSIGNED NOT NULL,
  `add_who` int(11) NULL DEFAULT NULL,
  `add_time` datetime(6) NOT NULL,
  `edit_who` int(11) NULL DEFAULT NULL,
  `edit_time` datetime(6) NOT NULL,
  `is_knowledge` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33738 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;


-- ----------------------------
-- Table structure for xadmin_bookmark
-- ----------------------------
DROP TABLE IF EXISTS `xadmin_bookmark`;
CREATE TABLE `xadmin_bookmark`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `url_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `query` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_share` tinyint(1) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `xadmin_bookmark_content_type_id_60941679_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `xadmin_bookmark_user_id_42d307fc_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `xadmin_bookmark_ibfk_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `xadmin_bookmark_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for xadmin_log
-- ----------------------------
DROP TABLE IF EXISTS `xadmin_log`;
CREATE TABLE `xadmin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `ip_addr` char(39) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id`(`content_type_id`) USING BTREE,
  INDEX `xadmin_log_user_id_bb16a176_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `xadmin_log_ibfk_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `xadmin_log_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for xadmin_usersettings
-- ----------------------------
DROP TABLE IF EXISTS `xadmin_usersettings`;
CREATE TABLE `xadmin_usersettings`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `xadmin_usersettings_user_id_edeabe4a_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `xadmin_usersettings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of xadmin_usersettings
-- ----------------------------
INSERT INTO `xadmin_usersettings` VALUES (1, 'dashboard:home:pos', '', 1);
INSERT INTO `xadmin_usersettings` VALUES (2, 'site-theme', '/static/xadmin/css/themes/bootstrap-theme.css', 1);
INSERT INTO `xadmin_usersettings` VALUES (3, 'mgbase_taxknowledge_editform_portal', 'box-0,extend_question-group,,,,,', 1);
INSERT INTO `xadmin_usersettings` VALUES (4, 'mgbase_taxbaskeyword_editform_portal', 'box-0,taxbassynonym_set-group,', 1);
INSERT INTO `xadmin_usersettings` VALUES (5, 'dashboard:home:pos', '', 3);

-- ----------------------------
-- Table structure for xadmin_userwidget
-- ----------------------------
DROP TABLE IF EXISTS `xadmin_userwidget`;
CREATE TABLE `xadmin_userwidget`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `page_id` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `widget_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `xadmin_userwidget_user_id_c159233a_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `xadmin_userwidget_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
