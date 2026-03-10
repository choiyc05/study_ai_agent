create view db_to_air.weeks as 
select * from 
(
	select 1 as 코드, '월요일' as 요일
	union all 
	select 2 as 코드, '화요일' as 요일
	union all 
	select 3 as 코드, '수요일' as 요일
	union all 
	select 4 as 코드, '목요일' as 요일
	union all 
	select 5 as 코드, '금요일' as 요일
	union all 
	select 6 as 코드, '토요일' as 요일
	union all 
	select 7 as 코드, '일요일' as 요일
) as t;

use db_to_air;

select 
	   STR_TO_DATE(CONCAT(CAST(a.년도 AS CHAR), CAST(a.월 AS CHAR), CAST(a.일 AS CHAR)), '%Y%m%d') as 날짜, 
	   w.요일, 
	   a.`항공편번호`, c1.설명 as 항공편명, 
	   a.`항공사코드`, c2.설명 as 항공사명,
	   a.`출발공항코드`, a1.`도시` as 출발도시, a1.`국가` as 출발국가,
	   a.`도착지공항코드`, a2.`도시` as 도착도시, a2.`국가` as 도착국가
  from db_air.`비행` as a 
  left outer join db_to_air.weeks as w
  on (a.요일 = w.코드)
  left outer join db_air.`운반대` as c1
  on (a.`항공편번호` = c1.`코드`)
  left outer join db_air.`운반대` as c2
  on (a.`항공사코드` = c2.`코드`)
  left outer join db_air.`항공사` as a1
  on (a.`출발공항코드` = a1.`항공사코드`)
  left outer join db_air.`항공사` as a2
  on (a.`도착지공항코드` = a2.`항공사코드`)
  where a.월 = 10 and a.`출발공항코드` = 'ATL'
  limit 5
;

select 
	   STR_TO_DATE(CONCAT(CAST(a.년도 AS CHAR), CAST(a.월 AS CHAR), CAST(a.일 AS CHAR)), '%Y%m%d') as 날짜, 
	   w.요일, 
	   a.`항공사코드`, c.설명 as 항공사명, a.`항공편번호`, 	   
	   a.`출발공항코드`, a1.`도시` as 출발도시, a1.`국가` as 출발국가,
	   a.`도착지공항코드`, a2.`도시` as 도착도시, a2.`국가` as 도착국가,
	   a.`비행거리`,
	   case when a.`우회여부` = 1 then '우회' else '직항' end as 우회여부
  from db_air.`비행` as a 
  left outer join db_to_air.weeks as w
  on (a.요일 = w.코드)
  left outer join db_air.`운반대` as c
  on (a.`항공사코드` = c.`코드`)
  left outer join db_air.`항공사` as a1
  on (a.`출발공항코드` = a1.`항공사코드`)
  left outer join db_air.`항공사` as a2
  on (a.`도착지공항코드` = a2.`항공사코드`)
  where a.월 = 10 
    and a.`항공사코드` = 'AA'
  	and a.`출발공항코드` = 'LAX'
  	and a.`도착지공항코드` = 'SFO'
  order by a.`비행거리` desc
;

select 
	   c.설명 as 항공사명,
	   sum(case when a.`우회여부` = 1 then 1 else 0 end) as 우회,
	   sum(case when a.`우회여부` = 1 then 0 else 1 end) as 직항
  from db_air.`비행` as a 
  left outer join db_to_air.weeks as w
  on (a.요일 = w.코드)
  left outer join db_air.`운반대` as c
  on (a.`항공사코드` = c.`코드`)
  left outer join db_air.`항공사` as a1
  on (a.`출발공항코드` = a1.`항공사코드`)
  left outer join db_air.`항공사` as a2
  on (a.`도착지공항코드` = a2.`항공사코드`)
  where a.월 = 10 
    and a.일 in (1,2,3,4,5,6,7)
    and a.`항공사코드` in (select `항공사코드` from db_air.`비행` t  group by `항공사코드`) 
  group by 항공사명
  order by 3 desc
  limit 10
;

select `항공사코드`, max(TIMEDIFF(실제출발시간, 예정출발시간)) as 최대출발지연시간 
from (
	select 
		`항공사코드`,
		STR_TO_DATE(LPAD(`예정출발시간`,4,'0'), '%H%i') as 예정출발시간,
		STR_TO_DATE(LPAD(`실제출발시간`,4,'0'), '%H%i') as 실제출발시간
	from db_air.`비행` where 일 = 1 
) as t
group by `항공사코드`
order by 2 desc
;

select 
	`항공사코드`,
	STR_TO_DATE(LPAD(`예정출발시간`,4,'0'), '%H%i') as 예정출발시간,
	STR_TO_DATE(LPAD(`실제출발시간`,4,'0'), '%H%i') as 실제출발시간,
	TIMEDIFF(실제출발시간, 예정출발시간)
from db_air.`비행` 
WHERE 일 = 1 and `항공사코드` = 'CO'
order by 4 desc
;
