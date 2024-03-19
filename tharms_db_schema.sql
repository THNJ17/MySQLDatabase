-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema tharms_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema tharms_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tharms_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `tharms_db` ;

-- -----------------------------------------------------
-- Table `tharms_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tharms_db`.`users` (
  `user_id` INT UNSIGNED NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `access_level` VARCHAR(45) NOT NULL COMMENT 'Student or Instructor or Administrator',
  `email` VARCHAR(45) NULL,
  `last_update` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `UserID_UNIQUE` (`user_id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tharms_db`.`students`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tharms_db`.`students` (
  `student_id` INT UNSIGNED NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `enrollment_date` DATE NOT NULL,
  PRIMARY KEY (`student_id`),
  INDEX `fk_students_users1_idx` (`user_id` ASC) VISIBLE,
  UNIQUE INDEX `student_id_UNIQUE` (`student_id` ASC) VISIBLE,
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_students_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `tharms_db`.`users` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tharms_db`.`instructors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tharms_db`.`instructors` (
  `instructor_id` INT UNSIGNED NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `last_update` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`instructor_id`),
  INDEX `fk_instructors_users1_idx` (`user_id` ASC) VISIBLE,
  UNIQUE INDEX `instructor_id_UNIQUE` (`instructor_id` ASC) VISIBLE,
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_instructors_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `tharms_db`.`users` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tharms_db`.`admins`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tharms_db`.`admins` (
  `admin_id` INT UNSIGNED NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `last_update` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`admin_id`),
  INDEX `fk_admins_users1_idx` (`user_id` ASC) VISIBLE,
  UNIQUE INDEX `admin_id_UNIQUE` (`admin_id` ASC) VISIBLE,
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_admins_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `tharms_db`.`users` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tharms_db`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tharms_db`.`courses` (
  `course_id` VARCHAR(45) NOT NULL,
  `course_name` VARCHAR(45) NOT NULL,
  `course_subject` VARCHAR(45) NULL,
  `instructor_id` INT UNSIGNED,
  PRIMARY KEY (`course_id`),
  UNIQUE INDEX `course_id_UNIQUE` (`course_id` ASC) VISIBLE,
  INDEX `fk_courses_instructors1_idx` (`instructor_id` ASC) VISIBLE,
  UNIQUE INDEX `course_name_UNIQUE` (`course_name` ASC) VISIBLE,
  CONSTRAINT `fk_courses_instructors1`
    FOREIGN KEY (`instructor_id`)
    REFERENCES `tharms_db`.`instructors` (`instructor_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tharms_db`.`compensations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tharms_db`.`compensations` (
  `compensation_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `instructor_id` INT UNSIGNED NOT NULL,
  `enrollment_bonus` FLOAT NULL,
  `coursesuccess_bonus` FLOAT NULL,
  `last_update` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`compensation_id`),
  UNIQUE INDEX `compensation_id_UNIQUE` (`compensation_id` ASC) VISIBLE,
  INDEX `instructor_id_idx` (`instructor_id` ASC) VISIBLE,
  CONSTRAINT `instructor_id`
    FOREIGN KEY (`instructor_id`)
    REFERENCES `tharms_db`.`instructors` (`instructor_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tharms_db`.`enrollments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tharms_db`.`enrollments` (
  `student_id` INT UNSIGNED NOT NULL,
  `course_id` VARCHAR(45) NOT NULL,
  `progress_percent` FLOAT UNSIGNED NULL,
  `completion_status` TINYINT NULL,
  `last_update` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`student_id`, `course_id`),
  INDEX `course_id_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_student_id`
    FOREIGN KEY (`student_id`)
    REFERENCES `tharms_db`.`students` (`student_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `course_id`
    FOREIGN KEY (`course_id`)
    REFERENCES `tharms_db`.`courses` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- This is a trigger to prevent incorrect enrollments for progress, say a user inputs a progress of 95.0 (95%) and also sets the completion_status as 1, or true, meaning complete. 
-- This would not be true. The trigger prevents that from happening by setting the completion_status to 0 (false) This includes nulls, which set to 0
DELIMITER //
CREATE TRIGGER completion_check
BEFORE INSERT ON tharms_db.enrollments
FOR EACH ROW
BEGIN
    IF NEW.progress_percent < 100 OR NEW.completion_status IS NULL THEN
        SET NEW.completion_status = 0;
    ELSE
        SET NEW.completion_status = 1;
    END IF;
END;
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER completion_status_update_check
BEFORE UPDATE ON tharms_db.enrollments
FOR EACH ROW
BEGIN
    IF NEW.completion_status = 1 AND NEW.progress_percent < 100 THEN
        SET NEW.completion_status = 0;
    END IF;
END;
//
DELIMITER ;


-- This trigger makes sure that when new data is entered, if it is null then it gets set to 0.
DELIMITER //
CREATE TRIGGER progress_check
BEFORE INSERT ON tharms_db.enrollments
FOR EACH ROW
BEGIN
    IF NEW.progress_percent IS NULL THEN
        SET NEW.progress_percent = 0;
    END IF;
END;
//
DELIMITER ;


-- this trigger is for when a new user is created, depending on the access level a new student id, admin id, or instructor id is created to their respective table
/* 
I have commented out this trigger due to the project assignment requiring the ability to create individual entities such as student and instructor.
With this trigger in place, when a new user entity is created it would automatically a insert a new corresponding id to the respective access level. Which while certainly useful, does not allow the manual assignment
of new student, instructor, and admin ids unfortunately.
Essentially, if you want to automatically create an id after a specific access level is assigned, use this. 


DELIMITER //
CREATE TRIGGER new_user
AFTER INSERT ON users FOR EACH ROW
BEGIN
    DECLARE is_student, is_admin, is_instructor BOOLEAN;
    SET is_student = FALSE;
    SET is_admin = FALSE;
    SET is_instructor = FALSE;

    IF NEW.access_level IN ('student', 'Student') THEN
        SET is_student = TRUE;
    END IF;

    IF NEW.access_level IN ('Administrator', 'administrator') THEN
        SET is_admin = TRUE;
    END IF;

    IF NEW.access_level IN ('Instructor', 'instructor') THEN
        SET is_instructor = TRUE;
    END IF;

    IF is_student THEN
        INSERT INTO students (student_id, user_id, enrollment_date)
        SELECT COALESCE(MAX(student_id) + 1, 1), NEW.user_id, NOW() FROM students;
    END IF;

    IF is_admin THEN
        INSERT INTO admins (admin_id, user_id, last_update)
        SELECT COALESCE(MAX(admin_id) + 1, 1), NEW.user_id, NOW() FROM admins;
    END IF;

    IF is_instructor THEN
        INSERT INTO instructors (instructor_id, user_id, last_update)
        SELECT COALESCE(MAX(instructor_id) + 1, 1), NEW.user_id, NOW() FROM instructors;
    END IF;
END;
//
DELIMITER ;

--how to drop the trigger
-- drop trigger new_user;
*/




SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
