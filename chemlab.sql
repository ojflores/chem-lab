CREATE DATABASE IF NOT EXISTS `chemlab`;

USE chemlab;

CREATE TABLE IF NOT EXISTS `students` (
  `student_id` INT(7) NOT NULL,
  `first_name` VARCHAR(25) NOT NULL,
  `last_name` VARCHAR(25) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`student_id`)
);

INSERT INTO `students` (`student_id`, `first_name`, `last_name`, `email`) VALUES
('2000001', 'John', 'Doe', 'john.doe@wallawalla.edu');
