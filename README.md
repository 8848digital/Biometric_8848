<div align="center" style="font-family: Arial, sans-serif;">
  <h1 style="font-size: 2.5em; color: #4CAF50;">Biometric Integration with ERPNext</h1>
  <p style="font-size: 1.2em; color: #555;">Automate Attendance Data Sync from Essl Software to ERPNext</p>
</div>

<hr style="border: 1px solid #ddd;">

<h2 style="color: #4CAF50;">Overview</h2>
<p style="font-size: 1em; color: #555;">
  This project automates the integration of biometric attendance data from <strong>Essl Software</strong> into <strong>ERPNext</strong>. 
  It uses a database trigger to capture new entries in the biometric system and fetches data into ERPNext using custom scripts and configurations.
</p>

<hr style="border: 1px solid #ddd;">

<h2 style="color: #4CAF50;">Features</h2>
<ul style="font-size: 1em; color: #555; line-height: 1.6;">
  <li><strong>Trigger-Based Data Fetching</strong>: Captures new attendance records from the <em>MasterAttendance</em> table and calls a Python script for data processing.</li>
  <li><strong>Manual Data Fetching</strong>: Includes a button in ERPNext to fetch attendance data for a specified date range.</li>
  <li><strong>Configurable Settings</strong>: Allows toggling data sync for:
    <ul>
      <li>Employee Checkin</li>
      <li>Attendance</li>
      <li>Attendance Request</li>
    </ul>
  </li>
</ul>

<hr style="border: 1px solid #ddd;">

<h2 style="color: #4CAF50;">SQL Scripts</h2>

<h3 style="color: #4CAF50;">1. Create Trigger</h3>
<pre style="background: #f9f9f9; padding: 10px; border: 1px solid #ddd; border-radius: 5px; overflow: auto;">
<code style="color: #000;">
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
</code>
</pre>

<h3 style="color: #4CAF50;">2. Drop Trigger</h3>
<pre style="background: #f9f9f9; padding: 10px; border: 1px solid #ddd; border-radius: 5px; overflow: auto;">
<code style="color: #000;">
DROP TRIGGER trg_AfterInsert;
</code>
</pre>

<h3 style="color: #4CAF50;">3. Set Identity Insert</h3>
<pre style="background: #f9f9f9; padding: 10px; border: 1px solid #ddd; border-radius: 5px; overflow: auto;">
<code style="color: #000;">
SET IDENTITY_INSERT MasterAttendance ON;
</code>
</pre>

<h3 style="color: #4CAF50;">4. Insert Sample Data</h3>
<pre style="background: #f9f9f9; padding: 10px; border: 1px solid #ddd; border-radius: 5px; overflow: auto;">
<code style="color: #000;">
INSERT INTO MasterAttendance (
    EmployeeCode,
    DeviceCode,
    LogDateTime,
    LogDate,
    LogTime,
    Direction,
    DownloadDateTime
)
VALUES (
    'HR-EMP-00081',
    '81',
    '2024-12-26 19:29:08.000',
    '2024-12-26',
    '10:29:08.0000000',
    'in',
    '2024-12-26 19:29:08.000'
);
</code>
</pre>

<hr style="border: 1px solid #ddd;">

<h2 style="color: #4CAF50;">Python Script Execution</h2>
<p style="font-size: 1em; color: #555;">
  The trigger executes a Python script located at <code>C:\scripts\script.py</code>. The script processes the data fetched from the trigger and integrates it into ERPNext.
</p>

<pre style="background: #f9f9f9; padding: 10px; border: 1px solid #ddd; border-radius: 5px; overflow: auto;">
<code style="color: #000;">
python C:\scripts\script.py "<data>"
</code>
</pre>

<hr style="border: 1px solid #ddd;">

<h2 style="color: #4CAF50;">How to Use</h2>
<ol style="font-size: 1em; color: #555; line-height: 1.6;">
  <li><strong>Setup Biometric Integration</strong>: Create the Biometric Settings in ERPNext and enable the required checkboxes.</li>
  <li><strong>Install Trigger</strong>: Use the Create Trigger script to set up the SQL trigger.</li>
  <li><strong>Test with Demo Data</strong>: Insert sample data using the Insert Sample Data script.</li>
  <li><strong>Fetch Attendance Data</strong>: Use the "Manual Fetch Attendance" button in ERPNext for the specified date range.</li>
</ol>

<hr style="border: 1px solid #ddd;">

<h2 style="color: #4CAF50;">License</h2>
<p style="font-size: 1em; color: #555;">This project is licensed under the <strong>MIT License</strong>.</p>

<hr style="border: 1px solid #ddd;">

<div align="center" style="font-size: 1em; color: #777;">
  <p>Developed with ❤️ for seamless attendance management.</p>
</div>
