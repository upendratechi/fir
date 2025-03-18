# filepath: c:\Users\Admin\Desktop\FIR_PRO\psnapp\generate_pdf.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_device_repair_request_pdf(data, file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, height - 1 * inch, "Device Repair Request")

    # Header
    c.setFont("Helvetica", 12)
    c.drawString(1 * inch, height - 1.5 * inch, f"Name: {data['name']}")
    c.drawString(4 * inch, height - 1.5 * inch, f"Jira SRN ID: {data['jira_srn_id']}")
    c.drawString(1 * inch, height - 1.75 * inch, f"Customer: {data['customer']}")
    c.drawString(4 * inch, height - 1.75 * inch, f"Format Req. No.: {data['format_req_no']}")
    c.drawString(1 * inch, height - 2 * inch, f"Document by: {data['document_by']}")
    c.drawString(4 * inch, height - 2 * inch, f"Date: {data['date']}")

    # Table
    table_data = [
        ["SL No", "Description", "Details"],
        ["1", "Service Request Number", data['service_request_number']],
        ["2", "Date of communication failure", data['date_of_communication_failure']],
        ["3", "Device Model", data['device_model']],
        ["4", "Defective device PSN", data['defective_device_psn']],
        ["5", "VIN Number", data['vin_number']],
        ["6", "Device IMEI", data['device_imei']],
        ["7", "Device CCID", data['device_ccid']],
        ["8", "Date of Sale of Device", data['date_of_sale_of_device']],
        ["9", "S Trigger Date", data['s_trigger_date']],
        ["10", "C Trigger Date", data['c_trigger_date']],
        ["11", "Commercial Expiry date", data['commercial_expiry_date']],
        ["12", "Active Profile (BSNL/Airtel/Dual)", data['active_profile']],
        ["13", "Vehicle Type / Model", data['vehicle_type']],
        ["14", "Failure Location Plant/ Field- Customer Address", data['failure_location']],
        ["15", "Kilometers/Hours", data['kilometers_hours']],
        ["16", "Main Battery Voltage", data['main_battery_voltage']],
        ["17", "Service Engineer Name", data['service_engineer_name']],
        ["18", "Service Engineer Comment", data['service_engineer_comment']],
        ["19", "Reason for Replacement/Repair", data['reason_for_replacement']],
        ["20", "Engineering Team Comment", data['engineering_team_comment']],
        ["21", "DEAL Plant Team Comment", data['deal_plant_team_comment']],
        ["22", "Darby Last communication date", data['darby_last_communication_date']],
        ["23", "Updated request in Darby", data['updated_request_in_darby']],
        ["24", "Device Replacement request Initiation date", data['device_replacement_request_date']],
        ["25", "Returnable / Non-Returnable", data['returnable_non_returnable']],
    ]

    table = c.beginText(1 * inch, height - 2.5 * inch)
    table.setFont("Helvetica", 10)
    for row in table_data:
        table.textLine(f"{row[0]:<5} {row[1]:<50} {row[2]}")
    c.drawText(table)

    # Footer
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1 * inch, 1.5 * inch, "Approved By:")
    c.setFont("Helvetica", 10)
    c.drawString(1 * inch, 1.25 * inch, f"Initiated by- Service Eng.: {data['initiated_by']} {data['initiated_by_date']} {data['initiated_by_signature']}")
    c.drawString(1 * inch, 1 * inch, f"Recommended by- Engineering: {data['recommended_by']} {data['recommended_by_date']} {data['recommended_by_signature']}")
    c.drawString(1 * inch, 0.75 * inch, f"Service Manager: {data['service_manager']} {data['service_manager_date']} {data['service_manager_signature']}")
    c.drawString(1 * inch, 0.5 * inch, f"Sales & Service Head: {data['sales_service_head']} {data['sales_service_head_date']} {data['sales_service_head_signature']}")

    c.save()

# Example usage
data = {
    'name': 'DL545',
    'jira_srn_id': 'ACS-6583-1127',
    'customer': 'AL',
    'format_req_no': 'ASS/011/08/21 Ver-2',
    'document_by': 'After Sales Support Team',
    'date': '13-03-2025',
    'service_request_number': 'ACS-6583',
    'date_of_communication_failure': '13-03-2025',
    'device_model': 'DL545',
    'defective_device_psn': '2207222006',
    'vin_number': 'MB1NEKLD9NPBU1435',
    'device_imei': '867624067250414',
    'device_ccid': '89916420534722378909',
    'date_of_sale_of_device': '23-07-22 11:53',
    's_trigger_date': '03-01-23 0:01',
    'c_trigger_date': '13-02-23 13:33',
    'commercial_expiry_date': '01-07-25 5:30',
    'active_profile': 'Single Airtel',
    'vehicle_type': 'G91 sleeper suspended non tilt',
    'failure_location': 'WM-Rabinarayan behera-97771 40132\nSHREE GANESH AUTOMOBILES, NH5,RATHIA,DHARMASALA,JAJPUR,755024',
    'kilometers_hours': '139788 KM',
    'main_battery_voltage': '24',
    'service_engineer_name': 'Gayadhar',
    'service_engineer_comment': 'Sim Issue',
    'reason_for_replacement': 'Sim Issue',
    'engineering_team_comment': '',
    'deal_plant_team_comment': '',
    'darby_last_communication_date': '20-02-25 10:46',
    'updated_request_in_darby': '',
    'device_replacement_request_date': '13-03-25',
    'returnable_non_returnable': 'Returnable',
    'initiated_by': 'Gayadhar',
    'initiated_by_date': '13-03-2025',
    'initiated_by_signature': 'Gayadhar',
    'recommended_by': '',
    'recommended_by_date': '',
    'recommended_by_signature': '',
    'service_manager': 'Kunal',
    'service_manager_date': '13-Mar-25',
    'service_manager_signature': 'Kunal',
    'sales_service_head': 'Rajendran Subramanian',
    'sales_service_head_date': '16-Mar-25',
    'sales_service_head_signature': '',
}

generate_device_repair_request_pdf(data, "device_repair_request.pdf")