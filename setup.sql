
CREATE DATABASE IF NOT EXISTS telemedicine;
USE telemedicine;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50),
  password VARCHAR(50),
  role ENUM('patient', 'doctor', 'admin'),
  name VARCHAR(100),
  specialization VARCHAR(100)
);

CREATE TABLE patients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50),
  name VARCHAR(100),
  mobile VARCHAR(15),
  age INT,
  problem TEXT,
  last_visit DATE
);

CREATE TABLE prescriptions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patient VARCHAR(50),
  doctor VARCHAR(50),
  note TEXT
);

CREATE TABLE appointments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patient VARCHAR(50),
  doctor VARCHAR(50),
  time VARCHAR(50)
);

INSERT INTO users (username, password, role, name, specialization) VALUES
('alice', 'pass123', 'patient', 'Alice', ''),
('bob', 'pass123', 'patient', 'Bob', ''),
('drharish', 'doc123', 'doctor', 'Harish', 'Cardiologist'),
('drkrithik', 'doc123', 'doctor', 'Krithik', 'Neurologist'),
('admin', 'admin123', 'admin', 'Admin', '');

INSERT INTO patients (username, name, mobile, age, problem, last_visit) VALUES
('alice', 'Alice', '9876543210', 28, 'Recurring migraines and fatigue', '2024-12-15'),
('bob', 'Bob', '9123456780', 35, 'Cholesterol imbalance and dizziness', '2025-06-01');

INSERT INTO prescriptions (patient, doctor, note) VALUES
('alice', 'Harish', 'Blood Pressure Normal. Continue Amlodipine 5mg daily.'),
('alice', 'Krithik', 'Mild migraine detected. Prescribed Naproxen.'),
('bob', 'Harish', 'High cholesterol. Recommended diet and Atorvastatin 10mg.'),
('bob', 'Krithik', 'Vitamin D deficiency. Prescribed D3 shots weekly.');
