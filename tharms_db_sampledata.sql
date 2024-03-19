-- Inserting the users information into the user table for the database
INSERT INTO `tharms_db`.`users` (`user_id`, `username`, `password`, `first_name`, `last_name`, `access_level`, `email`, `last_update`)
VALUES
(1, 'testingjimmy', 'itsatest', 'Jimmy', 'Tester', 'Administrator', 'testeremail@gmail.com', CURRENT_TIMESTAMP),
(2, 'bestbaseballplayer', 'STLFAN#1', 'Albert', 'Pujols', 'Student', 'albertpujols@stlouiscardinals.com', CURRENT_TIMESTAMP),
(3, 'bobby_jones', 'jonesymebob!', 'Bob', 'Jones', 'Student', 'bobjones@aol.com', CURRENT_TIMESTAMP),
(4, 'galacticbounty', 'clanfett4life', 'Jango', 'Fett', 'Student', 'mandalorian_jango@gmail.com', CURRENT_TIMESTAMP),
(5, 'Roger', 'rogerrogerrorger', 'Roger', 'Roger', 'Student', 'RogerRoger@roger.com', CURRENT_TIMESTAMP),
(6, 'tjharms', 'secure789', 'Tyler', 'Harms', 'Student', 'tj@gmail.com', CURRENT_TIMESTAMP),
(7, 'emmywhite', 'myp@ssword', 'Emily', 'White', 'Instructor', 'emmywhite@yahoo.com', CURRENT_TIMESTAMP),
(8, 'james_stewart', 'p@ss123', 'James', 'Stewart', 'Administrator', 'frank.thomas@gmail.com', CURRENT_TIMESTAMP),
(9, 'gracy_hilly_top', 'frog123', 'Grace', 'Hill', 'Student', 'gracegirl@gmail.com', CURRENT_TIMESTAMP),
(10, 'greenHEN', 'pancakes11', 'Henry', 'Green', 'Instructor', 'hgreen@yahoo.com', CURRENT_TIMESTAMP),
(11, 'isabel_smith', 'randompasswordnumber#3000', 'Isabel', 'Smith', 'Administrator', 'isasmith@gmail.com', CURRENT_TIMESTAMP),
(12, 'theeaglesfan', 'jasonkelcesbiggestfan', 'Jason', 'Brown', 'Student', 'jason.brown@gmail.com', CURRENT_TIMESTAMP),
(13, 'karen_carter', 'karen_pass', 'Karen', 'Carter', 'Instructor', 'karen.carter@email.com', CURRENT_TIMESTAMP),
(14, 'leonardD', 'chenalismyfavorite!_', 'Leo', 'Davis', 'Administrator', 'mynameisntleonard@gmail.com', CURRENT_TIMESTAMP),
(15, 'morgan_hall', 'morganlefaye299!', 'Morgan', 'Hall', 'Student', 'morgan.hall@rocketmail.com', CURRENT_TIMESTAMP),
(16, 'nina_jones', 'ninapass', 'Nina', 'Jones', 'Instructor', 'nina.jones@hotmail.com', CURRENT_TIMESTAMP),
(17, 'vietphan', 'Irun365247', 'Viet', 'Phan', 'Administrator', 'vphan@outlook.com', CURRENT_TIMESTAMP),
(18, 'pamela_scott', 'ilovetheofficeMICHAEL', 'Pamela', 'Scott', 'Student', 'pamela.scott@gmail.com', CURRENT_TIMESTAMP),
(19, 'quincy_rivera', 'quincyflorida???', 'Quincy', 'Rivera', 'Instructor', 'quincy.rivera@gmail.com', CURRENT_TIMESTAMP),
(20, 'rachel_hughes', 'itsnotmypasswordimjustborrowingit', 'Rachel', 'Hughes', 'Administrator', 'rachel.hughes@gmail.com', CURRENT_TIMESTAMP),
(21, 'samwiseturner', 'sampass', 'Samuel', 'Turner', 'Student', 'sammyturnergemail.com', CURRENT_TIMESTAMP),
(22, 'tina_wilson', 'SOMUCHDATA__', 'Tina', 'Wilson', 'Instructor', 'tina.wilsongmail.com', CURRENT_TIMESTAMP),
(23, 'USS_GRANT', 'hewasapresidentyknow', 'Ulysses', 'Grant', 'Administrator', 'ulysses.young@gmail.com', CURRENT_TIMESTAMP),
(24, 'vivian_garcia', 'vivvy288189!', 'Vivian', 'Garcia', 'Student', 'vivian.garcia@gmail.com', CURRENT_TIMESTAMP),
(25, 'bartles_j', 'supersafe!', 'Jamie', 'Bartle', 'Administrator', 'bartleby@gmail.com', CURRENT_TIMESTAMP);

-- Creating the students in the student table
INSERT INTO `tharms_db`.`students` (`student_id`, `user_id`, `enrollment_date`)
VALUES
(100, 2, '2023-04-01'),
(101, 3, '2023-04-01'),
(102, 4, '2023-04-01'),
(103, 5, '2023-04-01'),
(105, 6, '2022-08-15'),
(106, 7, '2022-11-01'),
(107, 8, '2022-09-20'),
(108, 9, '2022-10-10'),
(109, 10, '2022-12-01'),
(110, 11, '2023-01-15'),
(111, 12, '2023-02-20'),
(112, 13, '2022-07-10'),
(113, 14, '2022-11-15'),
(114, 15, '2023-03-01');

-- Inserts into the admin table the instructors for the elearning platform.
INSERT INTO `tharms_db`.`instructors` (`instructor_id`, `user_id`, `last_update`)
VALUES
(205, 16, CURRENT_TIMESTAMP),
(206, 17, CURRENT_TIMESTAMP),
(207, 18, CURRENT_TIMESTAMP),
(208, 19, CURRENT_TIMESTAMP),
(209, 20, CURRENT_TIMESTAMP),
(210, 21, CURRENT_TIMESTAMP),
(211, 22, CURRENT_TIMESTAMP),
(212, 23, CURRENT_TIMESTAMP),
(213, 24, CURRENT_TIMESTAMP),
(214, 25, CURRENT_TIMESTAMP);

-- Inserts into admin table the admins from the elearning platform.
INSERT INTO `tharms_db`.`admins` (`admin_id`, `user_id`, `last_update`)
VALUES
(313, 16, CURRENT_TIMESTAMP),
(314, 17, CURRENT_TIMESTAMP),
(315, 18, CURRENT_TIMESTAMP),
(316, 19, CURRENT_TIMESTAMP),
(317, 20, CURRENT_TIMESTAMP),
(318, 21, CURRENT_TIMESTAMP),
(319, 22, CURRENT_TIMESTAMP),
(320, 23, CURRENT_TIMESTAMP),
(321, 24, CURRENT_TIMESTAMP),
(322, 25, CURRENT_TIMESTAMP);

-- Insert more sample data into tharms_db.courses
INSERT INTO `tharms_db`.`courses` (`course_id`, `course_name`, `course_subject`, `instructor_id`)
VALUES
('MA092', 'Mathematical Literacy', 'Mathematics', 205),
('EN271', 'African American Literature', 'English', 206),
('IS318', 'The Mask', 'Art/Theater', 207),
('RS117', 'World Religions', 'Religion', 208),
('AR181', 'Art Practice', 'Art', 209),
('C120', 'Computer Science Algorithms', 'Computer Science', 210),
('PL101', 'Philosophy Introduction', 'Psychology', 211),
('PY101', 'General Psychology', 'Psychology', 212),
('CS222', 'Data Structures', 'Computer Science', 210),
('BI111', 'Introduction to Biology', 'Biology', 214);

-- Setting compensations for instructors
INSERT INTO `tharms_db`.`compensations` (`instructor_id`, `enrollment_bonus`, `coursesuccess_bonus`, `last_update`)
VALUES
(205, 100, 0, CURRENT_TIMESTAMP),
(206, 50, 0, CURRENT_TIMESTAMP),
(207, 0, 140.00, CURRENT_TIMESTAMP),
(208, 0, 0, CURRENT_TIMESTAMP),
(209, 200, 200, CURRENT_TIMESTAMP),
(210, 10, 1, CURRENT_TIMESTAMP),
(211, 20, 80, CURRENT_TIMESTAMP),
(212, 80, 420, CURRENT_TIMESTAMP),
(213, 69, 1738, CURRENT_TIMESTAMP),
(214, 0, 0, CURRENT_TIMESTAMP);

-- Showing enrollment statuses. 0 means not complete, 1 means complete
INSERT INTO `tharms_db`.`enrollments` (`student_id`, `course_id`, `progress_percent`, `completion_status`, `last_update`)
VALUES
(100, 'EN271', 70.0, 0, CURRENT_TIMESTAMP), 
(101, 'EN271', 80.0, 0, CURRENT_TIMESTAMP), 
(102, 'C120', 90.0, 0, CURRENT_TIMESTAMP), 
(103, 'CS222', 95.0, 0, CURRENT_TIMESTAMP),
(103, 'PL101', 75.0, 0, CURRENT_TIMESTAMP),
(105, 'MA092', 88.5, 0, CURRENT_TIMESTAMP),
(106, 'EN271', 92.0, 0, CURRENT_TIMESTAMP),
(107, 'IS318', 75.5, 0, CURRENT_TIMESTAMP),
(108, 'RS117', 80.0, 0, CURRENT_TIMESTAMP),
(109, 'RS117', 100, 1, CURRENT_TIMESTAMP),
(110, 'C120', 68.5, 0, CURRENT_TIMESTAMP),
(111, 'PY101', 90.0, 0, CURRENT_TIMESTAMP),
(112, 'PL101', 77.5, 0, CURRENT_TIMESTAMP),
(113, 'CS222', 84.5, 0, CURRENT_TIMESTAMP),
(114, 'BI111', 79.0, 0, CURRENT_TIMESTAMP);

