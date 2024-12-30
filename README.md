<div align="center">
  <h1>Biometric Integration</h1>
  <p>Integrate Biometric Attendance Data with ERPNext</p>
</div>

---

### License

MIT

---

## Overview

This project integrates biometric data from **Essl Software** into **ERPNext**. The system fetches attendance and employee check-in data directly from the biometric device and creates records in ERPNext.

---

### Features

- **Biometric Settings Doctype**:
  - Includes three configurable options:
    - **Employee Checkin**
    - **Attendance**
    - **Attendance Request**
  - Data is fetched based on the selected checkbox.

- **Manual Fetch Attendance**:
  - Includes a **Manual Fetch Attendance** button.
  - Allows specifying a date range using "From Date" and "To Date".
  - Fetches and displays data for the selected range.

---

## How It Works

1. Set up the **Biometric Settings Doctype** in ERPNext.
2. Enable the required checkboxes:  
   - Employee Checkin  
   - Attendance  
   - Attendance Request  
3. Use the "Manual Fetch Attendance" button to fetch attendance data for a specific date range.

