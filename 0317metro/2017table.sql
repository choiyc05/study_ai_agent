USE edu;

DROP TABLE `seoul_metro_2017`;

CREATE TABLE `seoul_metro_2017` (
	`날짜` VARCHAR(20),
	`근무구분` VARCHAR(10) NULL DEFAULT NULL COMMENT '평,토,휴,신정 등등',
	`호선` VARCHAR(10),
	`역번호` VARCHAR(10),
	`역명` VARCHAR(20),
	`구분` VARCHAR(4),
	`05~06` VARCHAR(10),
	`06~07` VARCHAR(10),
	`07~08` VARCHAR(10),
	`08~09` VARCHAR(10),
	`09~10` VARCHAR(10),
	`10~11` VARCHAR(10),
	`11~12` VARCHAR(10),
	`12~13` VARCHAR(10),
	`13~14` VARCHAR(10),
	`14~15` VARCHAR(10),
	`15~16` VARCHAR(10),
	`16~17` VARCHAR(10),
	`17~18` VARCHAR(10),
	`18~19` VARCHAR(10),
	`19~20` VARCHAR(10),
	`20~21` VARCHAR(10),
	`21~22` VARCHAR(10),
	`22~23` VARCHAR(10),
	`23~24` VARCHAR(10),
	`24~` VARCHAR(10),
	`합계` VARCHAR(10)
)
;

LOAD DATA LOW_PRIORITY LOCAL INFILE 'D:\\IDE\\Study\\subway\\2017.csv'
IGNORE INTO TABLE `edu`.`seoul_metro_2017`
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(
 @v날짜, @v근무구분, @v호선, @v역번호, @v역명, @v구분, 
 @v05, @v06, @v07, @v08, @v09, @v10, @v11, @v12, 
 @v13, @v14, @v15, @v16, @v17, @v18, @v19, @v20, 
 @v21, @v22, @v23, @v24, @v합계
)
SET 
 `날짜`   = TRIM(REPLACE(@v날짜, '"', '')),
 `근무구분` = TRIM(REPLACE(@v근무구분, '"', '')),
 `호선`   = TRIM(REPLACE(@v호선, '"', '')),
 `역번호`   = TRIM(REPLACE(@v역번호, '"', '')),
 `역명`   = TRIM(REPLACE(@v역명, '"', '')),
 `구분`   = TRIM(REPLACE(@v구분, '"', '')),
 `05~06` = TRIM(REPLACE(@v05, ',', '')),
 `06~07` = TRIM(REPLACE(@v06, ',', '')),
 `07~08` = TRIM(REPLACE(@v07, ',', '')),
 `08~09` = TRIM(REPLACE(@v08, ',', '')),
 `09~10` = TRIM(REPLACE(@v09, ',', '')),
 `10~11` = TRIM(REPLACE(@v10, ',', '')),
 `11~12` = TRIM(REPLACE(@v11, ',', '')),
 `12~13` = TRIM(REPLACE(@v12, ',', '')),
 `13~14` = TRIM(REPLACE(@v13, ',', '')),
 `14~15` = TRIM(REPLACE(@v14, ',', '')),
 `15~16` = TRIM(REPLACE(@v15, ',', '')),
 `16~17` = TRIM(REPLACE(@v16, ',', '')),
 `17~18` = TRIM(REPLACE(@v17, ',', '')),
 `18~19` = TRIM(REPLACE(@v18, ',', '')),
 `19~20` = TRIM(REPLACE(@v19, ',', '')),
 `20~21` = TRIM(REPLACE(@v20, ',', '')),
 `21~22` = TRIM(REPLACE(@v21, ',', '')),
 `22~23` = TRIM(REPLACE(@v22, ',', '')),
 `23~24` = TRIM(REPLACE(@v23, ',', '')),
 `24~`   = TRIM(REPLACE(@v24, ',', '')),
 `합계`  = TRIM(REPLACE(@v합계, ',', ''))
 ;