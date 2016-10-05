CREATE DATABASE townmeet;
USE townmeet;
CREATE TABLE news (
  `id`       INT          NOT NULL AUTO_INCREMENT,
  `url`      VARCHAR(50)  NOT NULL,
  `title` text NOT NULL,
  `visit_cnt`       INT                   DEFAULT 0,
  PRIMARY KEY (id)
);