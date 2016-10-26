CREATE DATABASE townmeet;
USE townmeet;
CREATE TABLE user (
  `id`   INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150),
  `sex`  INT NOT NULL,
  PRIMARY KEY (id)
);
CREATE TABLE chat_history (
  `id`       INT NOT NULL AUTO_INCREMENT,
  `user_id1` INT NOT NULL,
  `user_id2` INT NOT NULL,
  `content`  TEXT,
  PRIMARY KEY (id)
);
CREATE TABLE news (
  `news_id`   INT          NOT NULL,
  `url`       VARCHAR(250) NOT NULL,
  `title`     VARCHAR(250) NOT NULL,
  `visit_cnt` INT DEFAULT 0,
  PRIMARY KEY (news_id)
);
CREATE TABLE joke (
  `joke_id` INT  NOT NULL AUTO_INCREMENT,
  `content` TEXT NOT NULL,
  `pop_cnt` INT  NOT NULL DEFAULT 0,
  PRIMARY KEY (joke_id)
);
CREATE TABLE news_chat (
  `id`      INT NOT NULL AUTO_INCREMENT,
  `news_id` INT NOT NULL,
  `content` TEXT,
  PRIMARY KEY (id)
);