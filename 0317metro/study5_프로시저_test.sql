# 프로시저 이용

SET @result = 0;
CALL pl_total_yw('2008-01-01', 150, '서울역(150)', '승차', @result);

SELECT @result;