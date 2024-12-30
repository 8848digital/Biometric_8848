<div align="center">
  <h1>Biometric Integration</h1>
  <p>Integrate Biometric Attendance Data with ERPNext</p>
</div>

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

1. **Setup Biometric Settings**:
   - Configure the **Biometric Settings Doctype** in ERPNext.
   - Enable the required checkboxes:  
     - Employee Checkin  
     - Attendance  
     - Attendance Request  
   - Use the **Manual Fetch Attendance** button to fetch attendance data for a specific date range.

2. **Trigger Integration**:
   - A dedicated server hosts the Essl Software database.
   - A SQL Trigger named `trg_AfterInsert` is created to send attendance data in real-time.

---

### SQL Trigger Details

Below is the SQL Trigger used to fetch real-time data from the **MasterAttendance** table in the Essl database:

#### Create Trigger
```sql
CREATE TRIGGER trg_AfterInsert
ON MasterAttendance
AFTER INSERT
AS
BEGIN
    BEGIN TRY
        DECLARE @command VARCHAR(8000);
        DECLARE @data VARCHAR(8000);
        SET @data = (
            SELECT
                EmployeeCode,
                DeviceCode,
                LogDateTime,
                LogDate,
                LogTime,
                Direction,
                DownloadDateTime
            FROM inserted
            FOR XML PATH('MasterAttendance')
        );
        SET @data = REPLACE(@data, '''', ''''''); -- Escape single quotes
        SET @command = 'python C:\scripts\script.py "' + @data + '"';
        EXEC xp_cmdshell @command;
    END TRY
    BEGIN CATCH
        DECLARE @errorMessage NVARCHAR(MAX) = ERROR_MESSAGE();
        RAISERROR ('Trigger Error: %s', 16, 1, @errorMessage) WITH LOG;
    END CATCH
END;
'''
