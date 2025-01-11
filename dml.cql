USE health;

-- some pratical examples to test the efficency of our db
-- Find all patients with a specific blood type
SELECT patient_info['name'], blood_type 
FROM patients 
WHERE blood_type = 'B+';

-- Find patients over 60 years old
SELECT patient_info['name'], age 
FROM patients 
WHERE age > 60
ALLOW FILTERING;

-- Find patients with specific medication

SELECT patient_id 
FROM patient_medications 
WHERE medication_name = 'Aspirin'
ALLOW FILTERING;

-- Find patients with multiple allergies 
SELECT patient_info['name'], allergies 
FROM patients 
WHERE allergies_count > 1
ALLOW FILTERING;

-- Find patients with specific chronic diseases

SELECT patient_id 
FROM patient_medical_history 
WHERE chronic_disease = 'Hypertension'
ALLOW FILTERING;


-- Get all medications for a specific patient
SELECT patient_info['name'], medications 
FROM patients 
WHERE patient_info['name'] = 'Cindy Holt'
ALLOW FILTERING;


-- Get emergency contacts for all patients

SELECT patient_info['name'], patient_info['emergency_contact'] 
FROM patients 
WHERE patient_info CONTAINS KEY 'emergency_contact'
ALLOW FILTERING;

