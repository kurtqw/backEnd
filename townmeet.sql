CREATE DATABASE townmeet;
USE townmeet;
CREATE TABLE news (
  `news_id`   INT          NOT NULL AUTO_INCREMENT,
  `url`       VARCHAR(250) NOT NULL,
  `title`     VARCHAR(250) NOT NULL,
  `type`      VARCHAR(100) NOT NULL ,
  `visit_cnt` INT DEFAULT 0,
  PRIMARY KEY (news_id)
);
CREATE TABLE joke (
  `joke_id` INT  NOT NULL AUTO_INCREMENT,
  `content` TEXT NOT NULL,
  `pop_cnt` INT  NOT NULL DEFAULT 0,
  PRIMARY KEY (joke_id)
);
