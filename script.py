from faker import Faker
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import uuid

# Initialize Faker
fake = Faker()

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra IP
session = cluster.connect()

# Create keyspace and table if not exists
session.execute("""
CREATE KEYSPACE IF NOT EXISTS health
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
""")
session.set_keyspace('health')

session.execute("""
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
""")

session.execute("""
CREATE TABLE IF NOT EXISTS patient_medications (
    patient_id UUID,
    patient_name TEXT,
    medication_name TEXT,
    dosage TEXT,
    frequency TEXT,
    start_date TEXT,
    prescribing_doctor TEXT,
    notes TEXT,
    PRIMARY KEY (patient_id, medication_name)
);
""")

session.execute("""
CREATE TABLE IF NOT EXISTS patient_medical_history (
    patient_id UUID,
    patient_name TEXT,
    chronic_disease TEXT,
    surgeries TEXT,
    family_history TEXT,
    PRIMARY KEY (patient_id, chronic_disease)
);
""")

def generate_patient():
    patient_id = uuid.uuid4()
    age = fake.random_int(min=1, max=100)
    blood_type = fake.random_element(elements=['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])
    patient_info = {
        'name': fake.name(),
        'address': fake.address(),
        'age': str(age),
        'gender': fake.random_element(elements=['M', 'F']),
        'phone' : fake.phone_number(),
        'emergency_contact': f"{fake.name()} {fake.phone_number()}",
        'insurance_number': fake.bothify(text='INS#####'),
        'occupation': fake.job()
    }
    medical_history = {
        'chronic_disease': fake.random_element(elements=['Diabetes', 'Hypertension', 'Asthma', 'Heart Disease']),
        'surgeries': fake.random_element(elements=['Appendectomy', 'Knee Surgery', 'Gallbladder Removal', 'Cataract Surgery']),
        'family_history': fake.random_element(elements=['Diabetes in parents', 'Heart issues in siblings', 'Cancer in grandparents', 'No known family history'])
    }
    medications = [
        {
            'medication_name': fake.random_element(elements=['Paracetamol', 'Ibuprofen', 'Amoxicillin', 'Metformin', 'Aspirin']),
            'dosage': f"{fake.random_int(min=1, max=100)}mg",
            'frequency': fake.random_element(elements=['Once daily', 'Twice daily', 'As needed']),
            'start_date': str(fake.date()),  # Convert date to string
            'prescribing_doctor': fake.name(),
            'notes': fake.sentence(nb_words=3)
        }
        for _ in range(2)
    ]
    exams = [
        {
            'exam_type': fake.word(),
            'result': fake.sentence(nb_words=4),
            'exam_date': str(fake.date()),  # Convert date to string
            'laboratory': fake.company(),
            'notes': fake.sentence(nb_words=3)
        }
        for _ in range(2)
    ]
    allergies = [
        {
            'allergy_name': fake.word(),
            'severity': fake.random_element(elements=['Mild', 'Moderate', 'Severe']),
            'diagnosis_date': str(fake.date()),  # Convert date to string
            'symptoms': fake.sentence(nb_words=3),
            'diagnosed_by': fake.name()
        }
        for _ in range(2)
    ]

    return {
        'patient_id': patient_id,
        'age': age,
        'blood_type': blood_type,
        'patient_info': patient_info,
        'medical_history': medical_history,
        'medications': medications,
        'exams': exams,
        'allergies': allergies, 
        'allergies_count': len(allergies)
    }

# Insert data into Cassandra
def insert_patient(patient):
    query = """
    INSERT INTO patients (
        patient_id,
        blood_type,
        age,
        patient_info,
        medical_history,
        medications,
        exams,
        allergies, 
        allergies_count
    ) VALUES (
        %(patient_id)s,
        %(blood_type)s,
        %(age)s,
        %(patient_info)s,
        %(medical_history)s,
        %(medications)s,
        %(exams)s,
        %(allergies)s, 
        %(allergies_count)s
    )
    """
    session.execute(query, patient)

def insert_patient_medications(patient_id,patient_name, medications):
    for med in medications:
        query = """
        INSERT INTO patient_medications (
            patient_id,
            patient_name, 
            medication_name,
            dosage,
            frequency,
            start_date,
            prescribing_doctor,
            notes
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        session.execute(query, (patient_id,patient_name, med['medication_name'], med['dosage'], med['frequency'], med['start_date'], med['prescribing_doctor'], med['notes']))

def insert_patient_medical_history(patient_id,patient_name, medical_history):
    query = """
    INSERT INTO patient_medical_history (
        patient_id,
        patient_name,
        chronic_disease,
        surgeries,
        family_history
    ) VALUES (%s,%s, %s, %s, %s)
    """
    session.execute(query, (patient_id,patient_name, medical_history['chronic_disease'], medical_history['surgeries'], medical_history['family_history']))

for _ in range(1000):  # Generate 1000 patients
    patient = generate_patient()
    try:
        insert_patient(patient)
        insert_patient_medications(patient['patient_id'],patient['patient_info']['name'], patient['medications'])
        insert_patient_medical_history(patient['patient_id'],patient['patient_info']['name'],  patient['medical_history'])
        print(f"Successfully inserted patient with ID: {patient['patient_id']}")
    except Exception as e:
        print(f"Error inserting patient: {e}")

print("Data insertion complete.")

# Close connections
session.shutdown()
cluster.shutdown()