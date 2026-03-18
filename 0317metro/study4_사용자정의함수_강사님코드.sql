DELIMITER //

CREATE FUNCTION get_total2(
    a VARCHAR(100),
    b VARCHAR(100),
    c VARCHAR(100),
    d VARCHAR(100),
    e VARCHAR(10)
)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE result INT;

    SELECT 
        CASE 
            WHEN e = 'AM' THEN
                (
                    IFNULL(`05~06`,0) + IFNULL(`06~07`,0) + IFNULL(`07~08`,0) +
                    IFNULL(`08~09`,0) + IFNULL(`09~10`,0) + IFNULL(`10~11`,0) +
                    IFNULL(`11~12`,0)
                )
            WHEN e = 'PM' THEN
                (
                    IFNULL(`12~13`,0) + IFNULL(`13~14`,0) + IFNULL(`14~15`,0) +
                    IFNULL(`15~16`,0) + IFNULL(`16~17`,0) + IFNULL(`17~18`,0) +
                    IFNULL(`18~19`,0) + IFNULL(`19~20`,0) + IFNULL(`20~21`,0) +
                    IFNULL(`21~22`,0) + IFNULL(`22~23`,0) + IFNULL(`23~24`,0) +
                    IFNULL(`24~`,0)
                )
            ELSE
                (
                    IFNULL(`05~06`,0) + IFNULL(`06~07`,0) + IFNULL(`07~08`,0) +
                    IFNULL(`08~09`,0) + IFNULL(`09~10`,0) + IFNULL(`10~11`,0) +
                    IFNULL(`11~12`,0) + IFNULL(`12~13`,0) + IFNULL(`13~14`,0) +
                    IFNULL(`14~15`,0) + IFNULL(`15~16`,0) + IFNULL(`16~17`,0) +
                    IFNULL(`17~18`,0) + IFNULL(`18~19`,0) + IFNULL(`19~20`,0) +
                    IFNULL(`20~21`,0) + IFNULL(`21~22`,0) + IFNULL(`22~23`,0) +
                    IFNULL(`23~24`,0) + IFNULL(`24~`,0)
                )
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