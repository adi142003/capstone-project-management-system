DROP DATABASE IF EXISTS capstone_db;
CREATE DATABASE capstone_db;
USE capstone_db;

DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
	username VARCHAR(50),
    pass_word VARCHAR(50)
);

DROP TABLE IF EXISTS Student;
CREATE TABLE Student (
    SRN INT PRIMARY KEY,
    fname VARCHAR(50),
    lname VARCHAR(50),
    cgpa DECIMAL(3, 2),
    date_of_birth DATE,
    team_id INT,
    department_name VARCHAR(50),
    email VARCHAR(50)
);

DROP TABLE IF EXISTS Student_interests;
CREATE TABLE Student_interests (
    interests VARCHAR(50),
    SRN INT
);

DROP TABLE IF EXISTS Department;
CREATE TABLE Department (
    department_name VARCHAR(50) PRIMARY KEY,
    no_of_faculty INT,
    chairperson VARCHAR(50)
);

DROP TABLE IF EXISTS Team;
CREATE TABLE Team (
    team_id INT PRIMARY KEY,
    no_of_girls INT,
    no_of_boys INT,
    project_id INT,
    faculty_id INT
);

DROP TABLE IF EXISTS Faculty;
CREATE TABLE Faculty (
    faculty_id INT PRIMARY KEY,
    fname VARCHAR(50),
    lname VARCHAR(50),
    start_date DATE,
    qualification VARCHAR(50),
    email VARCHAR(50),
    department varchar(50)
);

DROP TABLE IF EXISTS Project;
CREATE TABLE Project (
    project_id INT PRIMARY KEY,
    problem_statement TEXT,
    description TEXT,
    start_date DATE,
    submission_date DATE
);

DROP TABLE IF EXISTS Faculty_tracks_project;
CREATE TABLE Faculty_tracks_project (
    project_id INT,
    faculty_id INT
);

DROP TABLE IF EXISTS Faculty_field_of_interest;
CREATE TABLE Faculty_field_of_interest (
    field_of_interest VARCHAR(50),
    faculty_id INT
);

drop table if exists grade;
create table grade (
team_id int primary key, 
project_id int, 
phase1 varchar(2), 
phase2 varchar(2), 
phase3 varchar(2)
);


ALTER TABLE Student ADD FOREIGN KEY(team_id) REFERENCES TEAM(team_id);
ALTER TABLE Student ADD FOREIGN KEY(department_name) REFERENCES Department(department_name);
ALTER TABLE Student_interests ADD FOREIGN KEY(SRN) REFERENCES Student(SRN);
ALTER TABLE Team ADD FOREIGN KEY(project_id) REFERENCES Project(project_id);
ALTER TABLE Team ADD FOREIGN KEY(faculty_id) REFERENCES Faculty(faculty_id);
ALTER TABLE Faculty_tracks_project ADD FOREIGN KEY(project_id) REFERENCES Project(project_id);
ALTER TABLE Faculty_tracks_project ADD FOREIGN KEY(faculty_id) REFERENCES Faculty(faculty_id);
ALTER TABLE Faculty_field_of_interest ADD FOREIGN KEY(faculty_id) REFERENCES Faculty(faculty_id);
alter table grade add foreign key (team_id) references team(team_id);
alter table grade add foreign key (project_id) references project(project_id);
alter table faculty add foreign key (department) references Department(department_name); 

-- encryption of passwords -> trigger
CREATE TRIGGER password_hasher BEFORE INSERT ON Users FOR EACH ROW
SET
    NEW.pass_word = MD5 (NEW.pass_word);
    
CREATE TRIGGER password_hasher_update BEFORE UPDATE ON Users FOR EACH ROW
SET
    NEW.pass_word = MD5 (NEW.pass_word);
    
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetProjectFaculty`(IN p_project_id INT)
BEGIN
    SELECT f.* FROM Faculty f
    JOIN Faculty_tracks_project ftp ON f.faculty_id = ftp.faculty_id
    WHERE ftp.project_id = p_project_id;
END$$
DELIMITER ;

DELIMITER //

DELIMITER $$

CREATE PROCEDURE ChangeStudentPassword(
    IN p_srn varchar(10),
    IN p_new_password VARCHAR(50)
)
BEGIN
    DECLARE is_student_exists INT;

    -- Check if the student with the provided SRN exists
    SELECT COUNT(*) INTO is_student_exists FROM Users WHERE username = p_srn;
    
    -- If the student exists, update the password
    IF is_student_exists > 0 THEN
        UPDATE Users SET pass_word = p_new_password WHERE username = p_srn;
        SELECT 'Password changed successfully.' AS result;
    ELSE
        SELECT 'Student not found. Password change failed.' AS result;
    END IF;
END $$

DELIMITER ;

DELIMITER $$
CREATE FUNCTION UpdateProjectDescription(p_project_id INT, p_description TEXT) RETURNS BOOLEAN
deterministic
BEGIN
    DECLARE rows_affected INT;
    
    UPDATE Project SET description = p_description WHERE project_id = p_project_id;
    GET DIAGNOSTICS rows_affected = ROW_COUNT;
    
    RETURN rows_affected > 0;
END$$
DELIMITER ;




-- Users Data
insert into users(username, pass_word) values
('admin','admin'),
('stu1','stu1'),
('fac1','fac1');

-- Project Data
INSERT INTO Project (project_id, problem_statement, description, start_date, submission_date) VALUES
(1, 'Automated Task Scheduler', 'Develop a system for scheduling and managing tasks automatically.', '2022-01-10', '2022-04-10'),
(2, 'Smart Home Automation', 'Create an intelligent system for automating home tasks and processes.', '2022-02-05', '2022-05-05'),
(3, 'Green Energy Solutions', 'Design eco-friendly solutions for energy conservation and renewable energy.', '2022-03-20','2022-05-05'),
(4, 'Healthcare Management System', 'Develop a comprehensive system for managing healthcare information and services.', '2022-04-15','2022-06-04'),
(5, 'E-commerce Platform', 'Build an advanced e-commerce platform with innovative features.', '2022-05-30', '2022-08-30'),
(6, 'Autonomous Drone Delivery', 'Implement a drone delivery system for efficient and autonomous package delivery.', '2022-06-15', '2022-09-15'),
(7, 'Augmented Reality Gaming', 'Create an augmented reality gaming experience with interactive and immersive features.', '2022-07-10', '2022-10-10'),
(8, 'Smart Traffic Management', 'Develop an intelligent system for optimizing traffic flow and reducing congestion in urban areas.', '2022-08-25', '2022-11-25'),
(9, 'Blockchain-based Voting System', 'Design a secure and transparent voting system using blockchain technology.', '2022-09-20', '2022-12-20'),
(10, 'AI-Powered Personal Assistant', 'Build a virtual assistant using artificial intelligence to help users with daily tasks and information.', '2022-10-15', '2023-01-15');

-- Department Data
INSERT INTO Department (department_name, no_of_faculty, chairperson) VALUES
('Computer Science', 15, 'Dr. Smith'),
('Electrical Engineering', 12, 'Dr. Johnson'),
('Mechanical Engineering', 18, 'Dr. Miller');

-- Faculty Data
INSERT INTO Faculty (faculty_id, fname, lname, start_date, qualification, email,department) VALUES
(101, 'Dr. Richard', 'Smith', '2008-03-15', 'Ph.D.', 'richard.smith@example.com','Computer Science'),
(102, 'Dr. Amanda', 'Johnson', '2010-07-20', 'Ph.D.', 'amanda.johnson@example.com','Electrical Engineering'),
(103, 'Dr. Michael', 'Miller', '2005-11-10', 'Ph.D.', 'michael.miller@example.com','Mechanical Engineering'),
(104, 'Dr. Sarah', 'Williams', '2012-06-25', 'Ph.D.', 'sarah.williams@example.com','Computer Science'),
(105, 'Dr. Kevin', 'Brown', '2007-09-30', 'Ph.D.', 'kevin.brown@example.com','Computer Science'),
(106, 'John', 'Doe', '2022-01-01', 'Ph.D.', 'john.doe@email.com', 'Computer Science'),
(107, 'Jane', 'Smith', '2022-02-15', 'M.Sc.', 'jane.smith@email.com', 'Electrical Engineering'),
(108, 'Robert', 'Johnson', '2022-03-20', 'Ph.D.', 'robert.johnson@email.com', 'Mechanical Engineering'),
(109, 'Emily', 'Wilson', '2022-04-10', 'M.Sc.', 'emily.wilson@email.com', 'Computer Science'),
(110, 'Michael', 'Brown', '2022-05-05', 'Ph.D.', 'michael.brown@email.com', 'Computer Science');

-- Team Data
INSERT INTO Team (team_id, no_of_girls, no_of_boys, project_id, faculty_id) VALUES
(1, 2, 3, 1, 101),
(2, 3, 2, 2, 102), 	
(3, 1, 4, 3, 103),
(4, 4, 1, 4, 101),
(5, 2, 3, 5, 105),
(6, 3, 2, 6, 106),
(7, 2, 4, 7, 107),
(8, 4, 1, 8, 108),
(9, 1, 5, 9, 109),
(10, 3, 2, 10, 110);

-- Student Data
INSERT INTO Student (SRN, fname, lname, cgpa, date_of_birth, team_id, department_name, email) VALUES
(123456, 'John', 'Doe', 8.56, '1998-05-15', 1, 'Computer Science', 'john.doe@example.com'),
(123457, 'Alice', 'Smith', 7.92, '1999-02-20', 2, 'Electrical Engineering', 'alice.smith@example.com'),
(123458, 'Bob', 'Johnson', 9.01, '1997-09-10', 1, 'Computer Science', 'bob.johnson@example.com'),
(123459, 'Eva', 'Williams', 8.25, '1998-11-25', 3, 'Mechanical Engineering', 'eva.williams@example.com'),
(123460, 'Charlie', 'Brown', 7.73, '1999-08-05', 2, 'Electrical Engineering', 'charlie.brown@example.com'),
(123461, 'Sophia', 'Miller', 8.94, '1997-04-30', 3, 'Mechanical Engineering', 'sophia.miller@example.com'),
(123462, 'Daniel', 'Anderson', 9.12, '1998-07-12', 1, 'Computer Science', 'daniel.anderson@example.com'),
(123463, 'Olivia', 'Davis', 7.88, '1999-01-18', 2, 'Electrical Engineering', 'olivia.davis@example.com'),
(123464, 'Liam', 'Moore', 8.75, '1997-06-22', 3, 'Mechanical Engineering', 'liam.moore@example.com'),
(123465, 'Emma', 'Wilson', 7.65, '1998-10-07', 1, 'Computer Science', 'emma.wilson@example.com'),
(123466, 'Ava', 'Jones', 8.42, '1998-03-12', 4, 'Electrical Engineering', 'ava.jones@example.com'),
(123467, 'Noah', 'Thomas', 7.98, '1999-09-28', 4, 'Mechanical Engineering', 'noah.thomas@example.com'),
(123468, 'Mia', 'Taylor', 8.87, '1997-12-05', 5, 'Computer Science', 'mia.taylor@example.com'),
(123469, 'James', 'White', 7.75, '1998-06-18', 5, 'Electrical Engineering', 'james.white@example.com'),
(123470, 'Isabella', 'Clark', 9.05, '1999-04-02', 6, 'Mechanical Engineering', 'isabella.clark@example.com'),
(123471, 'William', 'Hill', 8.15, '1997-11-15', 7, 'Computer Science', 'william.hill@example.com'),
(123472, 'Avery', 'Baker', 7.92, '1998-08-20', 6, 'Electrical Engineering', 'avery.baker@example.com'),
(123473, 'Ethan', 'Fisher', 8.98, '1999-05-10', 6, 'Mechanical Engineering', 'ethan.fisher@example.com'),
(123474, 'Scarlett', 'Moore', 7.83, '1997-10-25', 8, 'Computer Science', 'scarlett.moore@example.com'),
(123475, 'Lucas', 'Hall', 8.54, '1998-04-08', 8, 'Electrical Engineering', 'lucas.hall@example.com');

-- Student Interests Data
INSERT INTO Student_interests (interests, SRN) VALUES
('Programming', 123456),
('Machine Learning', 123462),
('Web Development', 123464),
('Data Science', 123457),
('Artificial Intelligence', 123458),
('Robotics', 123458),
('Networking', 123459),
('Cybersecurity', 123460),
('Database Management', 123461),
('Software Engineering', 123456);

-- Faculty Tracks Project Data
INSERT INTO Faculty_tracks_project (project_id, faculty_id) VALUES
(1, 101),
(2, 101),
(3, 103),
(4, 104),
(5, 105),
(1, 102),
(2, 103),
(3, 104),
(4, 105),
(5, 101);

-- Faculty Field of Interest Data
INSERT INTO Faculty_field_of_interest (field_of_interest, faculty_id) VALUES
('Artificial Intelligence', 101),
('Machine Learning', 102),
('Robotics', 103),
('Data Science', 104),
('Software Engineering', 105),
('Networking', 101),
('Web Development', 102),
('Cybersecurity', 103),
('Database Management', 104),
('Programming Languages', 105);
