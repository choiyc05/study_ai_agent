DELIMITER //

CREATE FUNCTION get_total(a VARCHAR(100), b VARCHAR(100), c VARCHAR(100), d VARCHAR(100) )
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE result INT;
    
    SELECT 
    (
    `05~06` + `06~07` +  `07~08` + `08~09` + `09~10` +  `10~11` +  `11~12` +  `12~13` + 
    `13~14` +  `14~15` + `15~16` +  `16~17` +  `17~18` +  `18~19` +  `19~20` +  `20~21` + 
    `21~22` +  `22~23` +  `23~24` +  `24~`
    ) INTO result
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