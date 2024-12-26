import frappe
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def get_attendance_logs(from_date=None, to_date=None):
    # Enforce strict validation for dates
    if not from_date or not to_date:
        frappe.throw("Both From Date and To Date must be provided.")
    
    try:
        # Update to handle cases where time might be omitted
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
    except ValueError as e:
        frappe.throw("Invalid date format. Dates must be in YYYY-MM-DD format.")

    essl_settings = frappe.get_doc('ESSL Settings')
    base_url = essl_settings.ip
    username = essl_settings.username
    password = essl_settings.password
    devices = [
        device['serial_no']
        for device in frappe.get_all('ESSL Settings Detail', {'is_active': 1}, ['serial_no'])
    ]
    
    url = f"{base_url}/iclock/WebAPIService.asmx?op=GetTransactionsLog"
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://tempuri.org/GetTransactionsLog"
    }
    device_name = "201 MAIN"

    for serial_number in devices:
        body = f"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                       xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                       xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <GetTransactionsLog xmlns="http://tempuri.org/">
            <FromDateTime>{from_date}</FromDateTime>
            <ToDateTime>{to_date}</ToDateTime>
            <SerialNumber>{serial_number}</SerialNumber>
            <UserName>{username}</UserName>
            <UserPassword>{password}</UserPassword>
            <strDataList>EmployeeId,EmployeeName,EmployeeCode,Timestamp,SerialNumber</strDataList>
            <DeviceName>{device_name}</DeviceName>
            </GetTransactionsLog>
        </soap:Body>
        </soap:Envelope>
        """
        try:
            response = requests.post(url, data=body, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            frappe.log_error(message=f"Error fetching data from device {serial_number}: {e}", title="ESSL API Error")
            continue
        try:
            root = ET.fromstring(response.text)
            namespaces = {
                'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
                'tempuri': 'http://tempuri.org/'
            }
            body = root.find('.//soap:Body', namespaces)
            response_data = body.find('.//tempuri:GetTransactionsLogResponse', namespaces)
            str_data_list = response_data.find('tempuri:strDataList', namespaces).text
            records = str_data_list.split("\n")
            for record in records:
                if record.strip():
                    fields = record.split("\t")
                    if len(fields) >= 2:
                        employee_id = fields[0]
                        employee_time = fields[1]
                        emp_id = frappe.db.get_value('Employee', {'attendance_device_id': employee_id}, 'employee')
                        if emp_id:
                            employee_checkin = frappe.get_doc({
                                'doctype': 'Attendance Biometric',
                                'employeecode': emp_id,
                                'devicecode': employee_id,
                                'logdatetime': employee_time
                            })
                            employee_checkin.insert(ignore_permissions=True)
                            frappe.db.commit()
        except Exception as e:
            frappe.log_error(message=f"Error processing response from device {serial_number}: {e}", title="ESSL Parsing Error")
            continue
    return "Attendance logs fetched successfully."