DROP TABLE `metro_db`.`seoul_metro`;
TRUNCATE TABLE `metro_db`.`seoul_metro`;

CREATE TABLE `test`.`seoul_metro` (
	`날짜` VARCHAR(20),
	`역번호` INT(10),
	`역명` VARCHAR(20),
	`구분` VARCHAR(3),
	`05~06` VARCHAR(10),
	`06~07` VARCHAR(10) ,
	`07~08` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`08~09` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`09~10` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`10~11` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`11~12` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`12~13` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`13~14` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`14~15` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`15~16` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`16~17` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`17~18` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`18~19` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`19~20` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`20~21` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`21~22` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`22~23` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`23~24` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`24~25` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`합계` VARCHAR(10)
)
;

LOAD DATA LOCAL INFILE 'D:\\IDE\\Study\\subway\\2008.csv'
INTO TABLE `edu`.`seoul_metro` 
CHARACTER SET euckr 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES 
(
 @날짜,@역번호, @역명, @구분, 
 @v05, @v06, @v07, @v08, @v09, @v10, @v11, @v12, 
 @v13, @v14, @v15, @v16, @v17, @v18, @v19, @v20, 
 @v21, @v22, @v23, @v24, @v합계
)
SET 
 `날짜`   = TRIM(REPLACE(@날짜, '"', '')),
 `역번호` = TRIM(REPLACE(@역번호, '"', '')),
 `역명`   = TRIM(REPLACE(@역명, '"', '')),
 `구분`   = TRIM(REPLACE(@구분, '"', '')),
 `05~06` = REPLACE(@v05, ',', ''),
 `06~07` = REPLACE(@v06, ',', ''),
 `07~08` = REPLACE(@v07, ',', ''),
 `08~09` = REPLACE(@v08, ',', ''),
 `09~10` = REPLACE(@v09, ',', ''),
 `10~11` = REPLACE(@v10, ',', ''),
 `11~12` = REPLACE(@v11, ',', ''),
 `12~13` = REPLACE(@v12, ',', ''),
 `13~14` = REPLACE(@v13, ',', ''),
 `14~15` = REPLACE(@v14, ',', ''),
 `15~16` = REPLACE(@v15, ',', ''),
 `16~17` = REPLACE(@v16, ',', ''),
 `17~18` = REPLACE(@v17, ',', ''),
 `18~19` = REPLACE(@v18, ',', ''),
 `19~20` = REPLACE(@v19, ',', ''),
 `20~21` = REPLACE(@v20, ',', ''),
 `21~22` = REPLACE(@v21, ',', ''),
 `22~23` = REPLACE(@v22, ',', ''),
 `23~24` = REPLACE(@v23, ',', ''),
 `24~` = REPLACE(@v24, ',', '');