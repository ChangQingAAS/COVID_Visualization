DROP TABLE details,hotsearch,history,risk_area ;

CREATE TABLE  if not EXISTS  `details` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `update_time` datetime DEFAULT NULL COMMENT '数据最后更新时间',
    `province` varchar(50) DEFAULT NULL COMMENT '省',
    `city` varchar(50) DEFAULT NULL COMMENT '市',
    `confirm` int(11) DEFAULT NULL COMMENT '累计确诊',
    `confirm_add` int(11) DEFAULT NULL COMMENT '新增治愈',
    `heal` int(11) DEFAULT NULL COMMENT '累计治愈',
    `dead` int(11) DEFAULT NULL COMMENT '累计死亡',
    PRIMARY KEY (`id`)  USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE if not EXISTS  `hotsearch` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `dt` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    `content` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`)  USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE if not EXISTS `history` (
    `ds` datetime NOT NULL COMMENT '日期',
    `confirm` int(11) DEFAULT NULL COMMENT '累计确诊',
    `confirm_add` int(11) DEFAULT NULL COMMENT '当日新增确诊',
    `suspect` int(11) DEFAULT NULL COMMENT '剩余疑似',
    `suspect_add` int(11) DEFAULT NULL COMMENT '当日新增疑似',
    `heal` int(11) DEFAULT NULL COMMENT '累计治愈',
    `heal_add` int(11) DEFAULT NULL COMMENT '当日新增治愈',
    `dead` int(11) DEFAULT NULL COMMENT '累计死亡',
    `dead_add` int(11) DEFAULT NULL COMMENT '当日新增死亡',
    PRIMARY KEY (`ds`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE if not EXISTS `risk_area` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `end_update_time` VARCHAR(31) NOT NULL ,
    `province` VARCHAR(11) DEFAULT NULL  ,
    `city` varchar(11) DEFAULT NULL ,
    `county` varchar(11) DEFAULT NULL  ,
    `address` VARCHAR(111) DEFAULT NULL ,
    `type` VARCHAR(11) DEFAULT NULL,
    PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;