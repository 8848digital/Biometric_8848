<!DOCTYPE html>
<html lang="en">

<body>
  <div align="center">
    <h1>Biometric Integration with ERPNext</h1>
    <p>Automate Attendance Data Sync from Essl Software to ERPNext</p>
  </div>

  <hr>

  <h2>Overview</h2>
  <p>This project automates the integration of biometric attendance data from <strong>Essl Software</strong> into <strong>ERPNext</strong>.
    It uses a database trigger to capture new entries in the biometric system and fetches data into ERPNext using custom scripts and configurations.</p>

  <hr>

  <h2>Features</h2>
  <ul>
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

  <hr>

  <h2>SQL Scripts</h2>

  <h3>1. Create Trigger</h3>
  <pre>
<code>
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

  <h3>2. Drop Trigger</h3>
  <pre>
<code>
DROP TRIGGER trg_AfterInsert;
</code>
  </pre>

  <h3>3. Set Identity Insert</h3>
  <pre>
<code>
SET IDENTITY_INSERT MasterAttendance ON;
</code>
  </pre>

  <h3>4. Insert Sample Data</h3>
  <pre>
<code>
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

  <hr>

  <h2>Python Script Execution</h2>
  <p>The trigger executes a Python script located at <code>C:\scripts\script.py</code>. The script processes the data fetched from the trigger and integrates it into ERPNext.</p>

  <pre>
<code>
python C:\scripts\script.py "<data>"

import sys
import os
import xml.etree.ElementTree as ET
import json
import requests
from datetime import datetime

def xml_to_json(xml_string):
    try:
        root = ET.fromstring(xml_string)
        def xml_element_to_dict(element):
            if len(element) > 0:
                return {child.tag: xml_element_to_dict(child) for child in element}
            else:
                return element.text.strip() if element.text else None
        data = xml_element_to_dict(root)
        return data
    except Exception as e:
        return {"error": str(e)}

def get_biometric_settings():
    settings_url = "http://test-biometric.8848digitalerp.com/api/method/biometric.biometric.api.essl.get_biometric_settings.biometric_settings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "token cb406f2ad6382ed:f1ea5d4364d9687"
    }
    try:
        response = requests.get(settings_url, headers=headers)
        if response.status_code in [200, 201]:
            return response.json().get("message", {})
        else:
            return {}
    except Exception as e:
        return {}

def post_json_to_api(json_data):
    attendance_url = "http://test-biometric.8848digitalerp.com/api/resource/Attendance Biometric"
    error_log_url = "http://test-biometric.8848digitalerp.com/api/resource/Attendance Biometric Error Log"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "token cb406f2ad6382ed:f1ea5d4364d9687"
    }
    biometric_settings = get_biometric_settings()
    attendance_biometric_error_log = biometric_settings.get("attendance_biometric_error_log", 0)

    if isinstance(json_data, dict):
        records_to_process = [json_data]
    else:
        records_to_process = json_data[:1]

    for record in records_to_process:
        try:
            payload = create_payload(record)
            response = requests.post(attendance_url, headers=headers, json=payload)
            if response.status_code not in [200, 201] and attendance_biometric_error_log == 1:
                error_message = f"Failed to post data. Status Code: {response.status_code}. Response: {response.text}"
                log_data = {
                    "title": "Error Attendance Biometric",
                    "time_stamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "message": error_message
                }
                post_error_log_to_api(error_log_url, headers, log_data)
        except Exception as e:
            if attendance_biometric_error_log == 1:
                log_data = {
                    "title": "Error Attendance Biometric",
                    "time_stamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "message": str(e)
                }
                post_error_log_to_api(error_log_url, headers, log_data)

def post_error_log_to_api(url, headers, log_data):
    try:
        requests.post(url, headers=headers, json=log_data)
    except Exception:
        pass

def get_field_map():
    return {
        "EmployeeCode": "employeecode",
        "DeviceCode": "devicecode",
        "LogDateTime": "logdatetime",
        "LogDate": "logdate",
        "LogTime": "logtime",
        "Direction": "direction",
        "DownloadDateTime": "downloaddatetime"
    }

def create_payload(json_data):
    payload = {}
    field_map = get_field_map()
    for key, value in json_data.get("MasterAttendance", {}).items():
        if field_map.get(key):
            if key in ["LogDateTime", "DownloadDateTime"]:
                try:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass
            payload[field_map[key]] = value
    return payload

def get_old_record_data():
    old_record_path = r"C:\\scripts\\old_record.json"
    if os.path.exists(old_record_path):
        with open(old_record_path, "r", encoding="utf-8") as old_file:
            return json.load(old_file)
    return {}

def write_json_to_file(json_data, filename):
    output_folder = r"C:\\scripts\\output\\"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)
    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(json_data, output_file)

if __name__ == "__main__":
    xml_string = sys.argv[1]
    json_data = xml_to_json(xml_string)
    write_json_to_file(json_data, "attendance_data.json")
    post_json_to_api(json_data)
</code>
  </pre>

  <footer class="footer">
    <p>Developed by: 8848 Digital LLP</p>
  </footer>

</body>
</html>
