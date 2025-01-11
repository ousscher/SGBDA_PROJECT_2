-- Drop existing table and keyspace
DROP TABLE IF EXISTS health.patients;
DROP KEYSPACE IF EXISTS health;

-- Create keyspace
CREATE KEYSPACE IF NOT EXISTS health
WITH replication = {
    'class': 'SimpleStrategy', 
    'replication_factor': 1    
};

USE health;

-- Creation of the Patients table
CREATE TABLE IF NOT EXISTS patients (
    patient_id UUID PRIMARY KEY,
    blood_type TEXT,         
    age INT,                 
    patient_info MAP<TEXT, TEXT>,
    medical_history MAP<TEXT, TEXT>,
    medications LIST<FROZEN<MAP<TEXT, TEXT>>>,
    exams LIST<FROZEN<MAP<TEXT, TEXT>>>,
    allergies LIST<FROZEN<MAP<TEXT, TEXT>>>, 
    allergies_count INT
);

-- Medications table to track the medications of a patient 
CREATE TABLE IF NOT EXISTS patient_medications (
    patient_id UUID,
    medication_name TEXT,
    dosage TEXT,
    frequency TEXT,
    start_date TEXT,
    prescribing_doctor TEXT,
    notes TEXT,
    PRIMARY KEY (patient_id, medication_name)
);

CREATE TABLE IF NOT EXISTS patient_medical_history (
    patient_id UUID,
    chronic_disease TEXT,
    surgeries TEXT,
    family_history TEXT,
    PRIMARY KEY (patient_id, chronic_disease)
);

-- Create index on blood_type to accelerate search based on blood_type
CREATE INDEX IF NOT EXISTS idx_blood_type ON patients(blood_type);

-- Create index on age to accelerate Queries
CREATE INDEX IF NOT EXISTS idx_age ON patients(age);

