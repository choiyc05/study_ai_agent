# 다음 아래의 컬럼의 값을 구하시오.
# 단, 승차합, 하차합은 AM, PM 구분으로 사용자 함수를 사용하시오.

# | 날짜 | 역번호 | 역명 | AM승차합 | PM승차합 | AM하차합 | PM하차합 |

DELIMITER //

CREATE FUNCTION total_yw(a VARCHAR(100), b VARCHAR(100), c VARCHAR(100), d VARCHAR(100), time_type VARCHAR(10) )
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE result INT;
    
    SELECT
    	CASE 
    		WHEN time_type = 'AM' THEN (`05~06` + `06~07` +  `07~08` + `08~09` + `09~10` +  `10~11` +  `11~12` + `24~`)
			WHEN time_type = 'PM' THEN (`12~13` + `13~14` +  `14~15` + `15~16` + `16~17` +  `18~19` +  `20~21` + `21~22` + `22~23` + `23~24`)
			ELSE (`05~06` + `06~07` +  `07~08` + `08~09` + `09~10` +  `10~11` +  `11~12` +  `12~13` + 
			   `13~14` +  `14~15` + `15~16` +  `16~17` +  `17~18` +  `18~19` +  `19~20` +  `20~21` + 
			   `21~22` +  `22~23` +  `23~24` +  `24~`)
		END 
		INTO result
    FROM seoul_metro_08_16
    WHERE `날짜` = a
      AND `역번호` = b
      AND `역명` = c
      AND `구분` = d
    LIMIT 1;
    
    RETURN result;
END;
//

DELIMITER ;