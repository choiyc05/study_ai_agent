# data01 지연이 많았던 항공사 top5 (기간 1987.10 - 1989.12) - 도착지연시간 기준 (막대 차트)

TRUNCATE db_to_air.data01;

INSERT INTO db_to_air.data01 (`항공사`, `도착지연횟수`)
SELECT 
	b.`설명` AS 항공사, 
	COUNT(a.`항공사코드`) AS 도착지연횟수
FROM 
	db_air.`비행` a
JOIN 
	db_air.`운반대` b ON a.`항공사코드` = b.`코드`
WHERE 
	a.`도착지연시간` REGEXP '^[0-9]+$' 
	AND CAST(a.`도착지연시간` AS UNSIGNED) > 0
GROUP BY 
	b.`설명`
ORDER BY
	도착지연횟수 DESC;


# data02 국제선, 국내선 비율 - 기간별 (파이 차트) // 필요한 컬럼 - 년도, 월, 국내선, 국제선 

TRUNCATE db_to_air.data02;

INSERT INTO db_to_air.data02 (`년도`, `월`, `국내선`, `국제선`)
SELECT
	a.`년도`,
	a.`월`,
	SUM(CASE WHEN ap_start.`국가` = ap_end.`국가` THEN 1 ELSE 0 END) AS 국내선,
	SUM(CASE WHEN ap_start.`국가` <> ap_end.`국가` THEN 1 ELSE 0 END) AS 국제선
FROM
	db_air.`비행` a
JOIN
	db_air.`항공사` ap_start ON a.`출발공항코드` = ap_start.`항공사코드` 
JOIN
	db_air.`항공사` ap_end ON a.`도착지공항코드` = ap_end.`항공사코드` 
GROUP BY 
	a.`년도`,
	a.`월`
ORDER BY
	a.`년도`,
	a.`월`;

# data04 기간 내의 항공사별 결항 비율(비행취소여부에 따른 데이터 적재, 결항횟수/전체 운행 횟수) // 필요한 컬럼 - 년도, 월, 항공사(운반대.설명), 전체비행수, 실제비행수, 취소비행수, 실제비행비율, 취소비행비율

TRUNCATE db_to_air.data04;
## 적재
INSERT INTO db_to_air.data04  (`년도`, `월`, `항공사`, `전체비행수`, `실제비행수`, `취소비행수`, `실제비행비율`, `취소비행비율`)
SELECT
	a.`년도`,
	a.`월`,
	b.`설명` AS 항공사,
	COUNT(*) AS 전체비행수,
	SUM(CASE WHEN a.`비행취소여부` = 0 THEN 1 ELSE 0 END) AS 실제비행수,
	SUM(CASE WHEN a.`비행취소여부` = 1 THEN 1 ELSE 0 END) AS 취소비행수,
	ROUND(SUM(CASE WHEN a.`비행취소여부` = '0' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS 실제비행비율,
	ROUND(SUM(CASE WHEN a.`비행취소여부` = '1' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS 취소비행비율
FROM 
	db_air.`비행` a
JOIN
	db_air.`운반대` b ON a.`항공사코드` = b.`코드`
GROUP BY
	a.`년도`, a.`월`, b.`설명` 
ORDER BY
	a.`년도`, a.`월`, b.`설명`;