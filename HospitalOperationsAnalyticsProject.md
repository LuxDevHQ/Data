### **Hospital Operations Analytics Project Instructions**

### **Project Title**
Hospital Operations Analytics Using SQL and Power BI

### **Project Overview**
In this project, you will work with a hospital operations dataset containing several related tables. The goal is to upload the dataset into a PostgreSQL database using DBeaver, write SQL queries to explore and analyze the data, and later connect the database to Power BI for dashboard development.

The dataset contains information about patients, doctors, departments, appointments, admissions, billing, insurance, lab tests, prescriptions, and patient outcomes.

---

### **Project Tools Required**

You are required to use the following tools:

1. PostgreSQL
2. DBeaver
3. Microsoft Excel
4. Power BI Desktop

---

### **Dataset Tables**

The dataset contains the following tables:

1. Patients
2. Doctors
3. Departments
4. Appointments
5. Admissions
6. Billing
7. Lab Tests
8. Insurance
9. Prescriptions

Each table should be imported separately into PostgreSQL.

---

### **Step 1: Open the Dataset**

1. Open the hospital dataset Excel file.
2. Review all the sheets in the workbook.
3. Confirm that each sheet represents a separate table.
4. Check the column names in each sheet.
5. Identify the ID columns in each table.

---

### **Step 2: Create a PostgreSQL Database**

1. Open DBeaver.
2. Connect to your PostgreSQL server.
3. Right-click on your PostgreSQL connection.
4. Select **Create**.
5. Select **Database**.
6. Name the database:

```sql
hospital_operations_db
```


#### **Use SQL to answer business questions from the dataset.**

**Your SQL queries should help answer questions such as:**
- Which department receives the most patients?
- Which counties have the highest number of patients?
- What is the monthly trend of appointments?
- Which doctors have the highest number of completed appointments?
- What is the average hospital bill per patient?
- What percentage of bills are unpaid or partially paid?
- What is the average length of hospital stay?
- Which lab tests are most commonly requested?
- Which payment method is used most often?
-- Which service type generates the highest revenue?
