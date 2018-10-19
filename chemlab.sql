#Delete and recreate database

DROP DATABASE IF EXISTS `chemlab`;

CREATE DATABASE IF NOT EXISTS `chemlab`;

USE chemlab;

#Create tables

CREATE TABLE IF NOT EXISTS `students` (
  `student_id` CHAR(7) NOT NULL,
  `first_name` VARCHAR(25) NOT NULL,
  `last_name` VARCHAR(25) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  PRIMARY KEY(`student_id`)
);

CREATE TABLE IF NOT EXISTS `courses` (
  `course_id` CHAR(7) NOT NULL,
  `course_name` VARCHAR(25) NOT NULL,
  PRIMARY KEY(`course_id`)
);

CREATE TABLE IF NOT EXISTS `teachers` (
  `teacher_id` CHAR(7) NOT NULL,
  `first_name` VARCHAR(25) NOT NULL,
  `last_name` VARCHAR(25) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  PRIMARY KEY(`teacher_id`)
);

CREATE TABLE IF NOT EXISTS `enrolled` (
  `student_id` CHAR(7) NOT NULL,
  `course_id` CHAR(7) NOT NULL,
  FOREIGN KEY(`student_id`)
    REFERENCES students(`student_id`)
    ON DELETE CASCADE,
  FOREIGN KEY(`course_id`)
    REFERENCES courses(`course_id`)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `teaching` (
  `teacher_id` CHAR(7) NOT NULL,
  `course_id` CHAR(7) NOT NULL,
  FOREIGN KEY(`teacher_id`)
    REFERENCES teachers(`teacher_id`)
    ON DELETE CASCADE,
  FOREIGN KEY(`course_id`)
    REFERENCES courses(`course_id`)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `labs` (
  `course_id` CHAR(7) NOT NULL,
  `lab_num` VARCHAR(3) NOT NULL,
  `lab_name` VARCHAR(25) NOT NULL,
  `answer_key` JSON NOT NULL,
  PRIMARY KEY(`course_id`, `lab_num`),
  FOREIGN KEY(`course_id`)
    REFERENCES courses(`course_id`)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `answers` (
  `student_id` CHAR(7) NOT NULL,
  `course_id` CHAR(7) NOT NULL,
  `lab_num` VARCHAR(3) NOT NULL,
  `answers` JSON NOT NULL,
  FOREIGN KEY(`student_id`)
    REFERENCES students(`student_id`)
    ON DELETE CASCADE,
  FOREIGN KEY(`course_id`,`lab_num`)
    REFERENCES labs(`course_id`, `lab_num`)
    ON DELETE CASCADE
);

#Create procedures

DELIMITER //
CREATE PROCEDURE see_key(IN cid CHAR(7), IN lnum VARCHAR(3))
BEGIN
  SET @j = (SELECT COUNT(JSON_KEYS(answer_key)) AS `length` FROM labs);
  SET @i = 0;
  CREATE TABLE `temp_table` (`key` VARCHAR(50), `answer` VARCHAR(50));
  WHILE @i <= @j DO
    INSERT INTO temp_table
    SELECT
      JSON_UNQUOTE(JSON_EXTRACT(JSON_KEYS(answer_key), CONCAT("$[", @i, "]"))) AS `key`,
      JSON_UNQUOTE(JSON_EXTRACT(JSON_EXTRACT(answer_key, "$.*"), CONCAT("$[", @i, "]"))) AS `answers`
    FROM labs
    WHERE course_id = cid
    AND lab_num = lnum;
    SET @i = @i +1;
  END WHILE;
  SELECT * FROM temp_table;
  DROP TABLE `temp_table`;
END //
DELIMITER ;

#Insert test data

INSERT INTO `students` (`student_id`, `first_name`, `last_name`, `email`) VALUES
('2000001', 'John', 'Doe', 'john.doe@wallawalla.edu');

INSERT INTO `courses` (`course_id`, `course_name`) VALUES
('CHEM101', 'Intro to Chemestry');

INSERT INTO `teachers` (`teacher_id`, `first_name`, `last_name`, `email`) VALUES
('2090001', 'Steven', 'Lee', 'steven.lee@wallawalla.edu');

INSERT INTO `enrolled` (`student_id`, `course_id`) VALUES
('2000001', 'CHEM101');

INSERT INTO `teaching` (`teacher_id`, `course_id`) VALUES
('2090001', 'CHEM101');

INSERT INTO `labs` (`course_id`, `lab_num`, `lab_name`, `answer_key`) VALUES
('CHEM101', '01', 'MgO Developer', JSON_OBJECT('initial_temp', '30', 'final_temp', '45'));

INSERT INTO `answers` (`student_id`, `course_id`, `lab_num`, `answers`) VALUES
('2000001', 'CHEM101', '01', JSON_OBJECT('initial_temp', '21.29', 'final_temp', '45.89'));
