# 사용자 정의 함수 만들기

DELIMITER //

CREATE FUNCTION add_numbers(a INT, b INT)
RETURNS INT
DETERMINISTIC
BEGIN
   RETURN a + b;
END;
//

DELIMITER ;

SELECT add_numbers(1, 4);