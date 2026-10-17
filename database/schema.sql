-- Create the database separately if necessary:
-- CREATE DATABASE placement_prediction;
-- Connect to placement_prediction, then run this file.

CREATE TABLE IF NOT EXISTS students (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cgpa NUMERIC(4,2) NOT NULL CHECK (cgpa BETWEEN 0 AND 10),
    aptitude_score NUMERIC(5,2) NOT NULL CHECK (aptitude_score BETWEEN 0 AND 100),
    coding_score NUMERIC(5,2) NOT NULL CHECK (coding_score BETWEEN 0 AND 100),
    communication_score NUMERIC(5,2) NOT NULL CHECK (communication_score BETWEEN 0 AND 100),
    projects INTEGER NOT NULL CHECK (projects >= 0),
    internships INTEGER NOT NULL CHECK (internships >= 0),
    certifications INTEGER NOT NULL CHECK (certifications >= 0),
    attendance NUMERIC(5,2) NOT NULL CHECK (attendance BETWEEN 0 AND 100),
    backlogs INTEGER NOT NULL CHECK (backlogs >= 0),
    placement_status BOOLEAN NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_students_placement ON students(placement_status);
CREATE INDEX IF NOT EXISTS idx_students_cgpa ON students(cgpa);
