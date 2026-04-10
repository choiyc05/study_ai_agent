USE edu;

DROP TABLE `edu`.`movie`;
CREATE TABLE `edu`.`movie` (
	`imdbID` TEXT UNIQUE KEY COMMENT 'imdb사이트 영화 고유 id',
	`title` TEXT COMMENT '영화제목',
	`poster` TEXT COMMENT '포스터 사진',
	`year` TEXT COMMENT '개봉 연도',
	`type` TEXT COMMENT '타입(영화)',
	`plot` TEXT,
	`regDate` DATETIME DEFAULT CURRENT_TIMESTAMP,
	`modDate` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
  COMMENT='imdb api로부터 info ai agent가 저장';