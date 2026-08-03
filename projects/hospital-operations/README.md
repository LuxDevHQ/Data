### **Hospital Operations Analytics Project Instructions**

### **Project Overview**
In this project, you will work with a hospital operations dataset containing several related tables. The goal is to upload the dataset into a PostgreSQL database using DBeaver, write SQL queries to explore and analyze the data, and later connect the database to Power BI for dashboard development.

[Download the project workbook](./hospital_operations_powerbi_sql_dataset.xlsx).

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
- Upload the data from the worksheet and use it to answer the questions below. 

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
- Which service type generates the highest revenue?

--- 

**Power BI Questions for Hospital Operations Analytics Project**

1. Which county has the highest number of patients?

2. Which gender has the highest number of hospital visits?

3. What is the total number of patients registered in the hospital?

4. What is the total number of appointments recorded?

5. What is the total number of admissions recorded?

6. Which department has the highest number of admissions?

7. Which department has the lowest number of admissions?

8. What is the monthly trend of appointments?

9. Which month recorded the highest number of appointments?

10. Which appointment status appears most frequently?

11. What percentage of appointments were completed?

12. What percentage of appointments were cancelled?

13. Which doctors handled the highest number of appointments?

14. Which doctors handled the lowest number of appointments?

15. Which doctor has the highest number of completed appointments?

16. Which specialization appears most frequently among doctors?

17. Which lab test was requested the most?

18. Which lab test was requested the least?

19. What percentage of lab test results were normal, abnormal, or pending?

20. Which doctors requested the highest number of lab tests?

21. Which drug was prescribed the most?

22. Which doctor issued the highest number of prescriptions?

23. What is the total prescription cost?

24. What is the average prescription cost per patient?

25. Which department has the highest number of recovered patients?

26. Which department has the highest number of referred patients?

27. What is the average length of hospital stay?

28. Which admission type is most common: Emergency, Referral, or Routine?

29. What percentage of patients were admitted through emergency cases?

30. What is the total amount charged by the hospital?

31. What is the total amount paid by patients?

32. What is the total outstanding balance?

33. What is the payment collection rate?

34. Which payment method is used most frequently?

35. Which payment method generated the highest amount paid?

36. Which service type generated the highest revenue?

37. Which service type generated the lowest revenue?

38. What percentage of bills are fully paid, partially paid, or pending?

39. Which patients have the highest outstanding balances?

40. Which counties generate the highest hospital revenue?

41. How does revenue change month by month?

42. Which insurance provider covers the highest number of patients?

43. What percentage of patients have active insurance?

44. How many insurance policies are expired?

45. Which county has the highest number of insured patients?

46. What is the relationship between insurance status and payment status?

47. Which department has the highest bed capacity?

48. Which departments appear to be under the highest pressure based on admissions?

49. Which age group has the highest number of patients?

50. What recommendations can you give hospital management based on the dashboard insights?
  
