DROP DATABASE IF EXISTS mydb;
CREATE DATABASE mydb;
USE mydb;

DROP TABLE IF EXISTS BitPropertyPDFs;

CREATE TABLE `BitPropertyPDFs` (
	`id` BIGINT NOT NULL AUTO_INCREMENT,
	`created‗at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
	`updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
	`prefecturesId` VARCHAR(4) NOT NULL COMMENT '都道府県コード',
	`courtId` VARCHAR(10) NOT NULL COMMENT '裁判所コード',
	`saleUnitId` VARCHAR(20) NOT NULL COMMENT '物件識別コード',
	`savedRoot` VARCHAR(256) NULL COMMENT '保存先ルート',
	`savedPath` VARCHAR(256) NULL COMMENT '保存先パス',
	`savedFile` VARCHAR(256) NULL COMMENT 'PDFファイル名',
	`savedSize` BIGINT NULL DEFAULT NULL COMMENT 'PDFファイルサイズ',
	PRIMARY KEY (`id`),
	UNIQUE INDEX `courtId_saleUnitId` (`courtId`, `saleUnitId`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


DROP TABLE IF EXISTS BitResults;

CREATE TABLE `BitResults` (
	`id` BIGINT(19) NOT NULL AUTO_INCREMENT,
	`created‗at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`document` LONGTEXT NULL DEFAULT NULL COMMENT 'HTMLドキュメント',
	`prefecturesId` VARCHAR(4) NULL DEFAULT NULL COMMENT '都道府県コード',
	`courtId` VARCHAR(10) NULL DEFAULT NULL COMMENT '裁判所コード',
	`saleScdId` VARCHAR(20) NULL DEFAULT NULL,
	`saleType` INT(10) NULL DEFAULT NULL COMMENT '売却区分(1:期間入札,2:特別売却)',
	`saleClsDisp` VARCHAR(50) NULL DEFAULT NULL COMMENT '売却種別',
	`caseNoText` VARCHAR(50) NULL DEFAULT NULL COMMENT '事件番号',
	`saleStandardAmountDisp` VARCHAR(50) NULL DEFAULT NULL COMMENT '売却基準価額',
	`saleStandardAmount` DECIMAL(20,0) NULL DEFAULT NULL,
	`saleAmountDisp` VARCHAR(50) NULL DEFAULT NULL COMMENT '売却価額',
	`saleAmount` DECIMAL(20,0) NULL DEFAULT NULL,
	`thingNoList` VARCHAR(500) NULL DEFAULT NULL COMMENT '物件番号',
	`thingNoKey` VARCHAR(50) NULL DEFAULT NULL COMMENT '物件番号キー',
	`saleStatusDisp` VARCHAR(50) NULL DEFAULT NULL COMMENT '落札結果',
	`saleStatus` INT(10) NULL DEFAULT NULL,
	`bitUsers` INT(10) NULL DEFAULT NULL COMMENT '入札者数（人）',
	`bitUserClsDisp` VARCHAR(50) NULL DEFAULT NULL COMMENT '落札者資格',
	`bitUserCls` INT(10) NULL DEFAULT NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `courtId_caseNoText_thingNoKey` (`courtId`, `caseNoText`, `thingNoKey`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

