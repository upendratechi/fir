import random
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from .models import PSNEntry  # Correct import
from .forms import PSNEntryForm, EngineerResponseForm  # Correct imports
from django.contrib import messages
import csv
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
import logging
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)

def generate_unique_number():
    last_entry = PSNEntry.objects.order_by('-unique_number').first()
    if last_entry:
        return last_entry.unique_number + 1
    else:
        return 10000  # Starting point if no entries exist

def home(request):
    entries = PSNEntry.objects.all()
    return render(request, 'psnapp/home.html', {'entries': entries})

def entry_detail(request, id):
    entry = get_object_or_404(PSNEntry, id=id)
    if entry.is_processed:
        return HttpResponse('This request has already been processed.', status=400)
    if request.method == 'POST':
        form = EngineerResponseForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            entry.is_processed = True
            entry.save()
            messages.success(request, 'The form has been submitted successfully.')
            return redirect('home')
    else:
        form = EngineerResponseForm(instance=entry)
    return render(request, 'psnapp/entry_detail.html', {'form': form, 'entry': entry})

def psn_form(request):
    if request.method == 'POST':
        form = PSNEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.unique_id = generate_unique_id(entry)
            entry.save()
            if entry.resolved_or_not == 'No':
                send_summary_email(entry)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PSNEntryForm()
    return render(request, 'psnapp/psn_form.html', {'form': form})

def send_summary_email(entry):
    subject = f'New FIR Entry Submitted - Request No: {entry.unique_id}'
    message = render_to_string('psnapp/manager_email.html', {
        'entry': entry,
        'approve_url': f"http://127.0.0.1:8000/approve_request/{entry.id}/",
        'reject_url': f"http://127.0.0.1:8000/reject_request/{entry.id}/",
        'view_details_url': f"http://127.0.0.1:8000/request_details/{entry.id}/"
    })
    recipient_list = [entry.manager_email]
    cc_list = [settings.HOD_EMAIL, entry.engineer_email]
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, cc=cc_list)
    email.content_subtype = 'html'  # To indicate the email content is HTML
    email.send()

def thank_you(request):
    return render(request, 'psnapp/thank_you.html')

def approve_request(request, id):
    entry = get_object_or_404(PSNEntry, id=id)
    
    # Check if the request has already been processed
    if entry.manager_approval_status in ['Approved', 'Rejected']:
        return HttpResponse('This request has already been processed.', status=400)

    entry.manager_approval_status = 'Approved'
    entry.save()

    # Generate CSRF token
    csrf_token = get_token(request)

    # Send email to the engineer
    engineer_email = entry.engineer_email
    subject = f'FIR Request Approved - Action Required - Request No: {entry.unique_id}'
    message = render_to_string('psnapp/engineer_email.html', {
        'entry': entry,
        'csrf_token': csrf_token,
        'form_url': f"http://127.0.0.1:8000/engineer_response/{entry.id}/"
    })

    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [engineer_email])
    email.content_subtype = 'html'  # To indicate the email content is HTML
    email.send()

    # Send email to the HOD
    hod_email = settings.HOD_EMAIL  # Email address of the HOD
    subject = 'FIR Request Approved by Manager - HOD Approval Required'
    message = render_to_string('psnapp/hod_email.html', {
        'entry': entry,
        'csrf_token': csrf_token,
        'approve_url': f"http://127.0.0.1:8000/approve_hod_request/{entry.id}/",
        'reject_url': f"http://127.0.0.1:8000/reject_hod_request/{entry.id}/",
         'view_details_url': f"http://127.0.0.1:8000/request_details/{entry.id}/"
    })
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [hod_email], cc=[engineer_email, entry.manager_email])
    email.content_subtype = 'html'
    email.send()

    return HttpResponse('The request has been approved by the manager and sent to the HOD for approval. Mail has been sent to HOD, Once HOD approves, you and the Engineer will get an email.')

def reject_request(request, id):
    entry = get_object_or_404(PSNEntry, id=id)
    
    # Check if the request has already been processed
    if entry.manager_approval_status in ['Approved', 'Rejected']:
        return HttpResponse('This request has already been processed.', status=400)

    entry.manager_approval_status = 'Rejected'
    entry.save()

    # Send email to the engineer
    engineer_email = entry.engineer_email
    subject = 'PSN Request Rejected'
    message = render_to_string('psnapp/engineer_rejection_email.html', {
        'entry': entry,
    })

    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [engineer_email], cc=[entry.manager_email, settings.HOD_EMAIL])
    email.content_subtype = 'html'  # To indicate the email content is HTML
    email.send()

    return HttpResponse('The request has been rejected and the engineer has been notified. Action has been sent to the engineer.')

def approve_hod_request(request, id):
    entry = get_object_or_404(PSNEntry, id=id)
    if entry.hod_approval_status in ['Approved', 'Rejected']:
        return HttpResponse('This request has already been processed by the HOD.', status=400)
    entry.hod_approval_status = 'Approved'
    entry.save()
    engineer_email = entry.engineer_email
    subject = 'FIR Request Approved by HOD - Action Required'
    message = render_to_string('psnapp/engineer_email.html', {'entry': entry, 'csrf_token': get_token(request)})
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [engineer_email], cc=[entry.manager_email, settings.HOD_EMAIL, 'mupendramzvpsp@gmail.com', 'mulaupendrareddy@gmail.com'])
    email.content_subtype = 'html'
    email.send()
    return HttpResponse('Thanks for approval. Engineer will receive confirmation to fill the additional details.')

def reject_hod_request(request, id):
    entry = get_object_or_404(PSNEntry, id=id)
    if entry.hod_approval_status in ['Approved', 'Rejected']:
        return HttpResponse('This request has already been processed by the HOD.', status=400)
    entry.hod_approval_status = 'Rejected'
    entry.save()
    engineer_email = entry.engineer_email
    subject = 'PSN Request Rejected by HOD'
    message = render_to_string('psnapp/engineer_rejection_email.html', {'entry': entry})
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [engineer_email])
    email.content_subtype = 'html'
    email.send()
    return HttpResponse('The request has been rejected by the HOD and the engineer has been notified.')

def download_data(request):
    # Get the current date and time in Indian Standard Time (IST)
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    formatted_datetime = now.strftime('%d_%m_%Y_%H:%M')

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="FIR_ENTRIES_{formatted_datetime}.csv"'

    writer = csv.writer(response)
    # Write the header row with all fields
    writer.writerow([
        'ID', 'Date of Complaint', 'Date of Sale of Device', 'Issue Raised by Customer', 'Vehicle Sale Date',
        'Active Profile', 'C Trigger Date', 'Commercial Expiry Date', 'Complaint Raised by', 'Complaint Raised Name',
        'Complaint Raised Through', 'Configuration', 'Contact Number', 'Device ICCID', 'Device IMEI', 'Device Model',
        'Device PSN', 'Engineer Recommendation', 'External Modification', 'Firmware', 'First Communication in Darby',
        'HOD Remarks', 'Issue Analysis', 'Issue Description', 'Issue Identified', 'Kilometers Hours',
        'Last Communication on Darby', 'Main Battery Voltage', 'Manager Remarks', 'S Trigger Date',
        'Service Engineer Name', 'Telco Status', 'Vehicle Running Location', 'Vehicle Support Date', 'Vehicle Type',
        'VIN Number', 'Resolved or Not', 'Engineer Email', 'HOD Approval Status', 'Vehicle Run', 'Manager Email',
        'Device to be Sent', 'Call Status', 'Final Action Taken', 'Final Call Status', 'Date of Closure',
        'Manager Approval Status', 'Unique ID'
    ])

    entries = PSNEntry.objects.all()
    for entry in entries:
        writer.writerow([
            entry.id, 
            entry.date_of_complaint.strftime('%Y-%m-%d %H:%M:%S') if entry.date_of_complaint else 'N/A', 
            entry.date_of_sale_of_device.strftime('%Y-%m-%d %H:%M:%S') if entry.date_of_sale_of_device else 'N/A', 

            entry.vehicle_sale_date.strftime('%Y-%m-%d %H:%M:%S') if entry.vehicle_sale_date else 'N/A',
            entry.active_profile, 
            entry.c_trigger_date.strftime('%Y-%m-%d %H:%M:%S') if entry.c_trigger_date else 'N/A', 
            entry.commercial_expiry_date.strftime('%Y-%m-%d %H:%M:%S') if entry.commercial_expiry_date else 'N/A', 
            entry.complaint_raised_by, 
            entry.complaint_raised_name,
            entry.complaint_raised_through, 
            entry.configuration, 
            entry.contact_number, 
            entry.device_ICCID, 
            entry.device_IMEI, 
            entry.device_model,
            entry.device_PSN, 
            entry.engineer_recommendation, 
            entry.external_modification, 
            entry.firmware, 
            entry.first_communication_in_darby.strftime('%Y-%m-%d %H:%M:%S') if entry.first_communication_in_darby else 'N/A',
            entry.hod_remarks, 
            entry.issue_analysis, 
            entry.issue_description, 
            entry.issue_identified, 
            entry.kilometers_hours,
            entry.last_communication_in_darby.strftime('%Y-%m-%d %H:%M:%S') if entry.last_communication_in_darby else 'N/A', 
            entry.main_battery_voltage, 
            entry.manager_remarks, 
            entry.s_trigger_date.strftime('%Y-%m-%d %H:%M:%S') if entry.s_trigger_date else 'N/A',
            entry.service_engineer_name, 
            entry.telco_status, 
            entry.vehicle_running_location, 
            entry.vehicle_support_date.strftime('%Y-%m-%d %H:%M:%S') if entry.vehicle_support_date else 'N/A', 
            entry.vehicle_type,
            entry.VIN_number, 
            entry.resolved_or_not, 
            entry.engineer_email, 
            entry.hod_approval_status, 
            entry.vehicle_run, 
            entry.manager_email,
            entry.device_to_be_sent, 
            entry.call_status, 
            entry.final_action_taken, 
            entry.final_call_status, 
            entry.date_of_closure.strftime('%Y-%m-%d %H:%M:%S') if entry.date_of_closure else 'N/A',
            entry.manager_approval_status, 
            entry.unique_id
        ])

    return response

def engineer_response(request, id):
    entry = get_object_or_404(PSNEntry, id=id)
    if entry.is_processed:
        return HttpResponse('This request has already been processed.', status=400)
    if request.method == 'POST':
        form = EngineerResponseForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            entry.is_processed = True
            entry.save()
            messages.success(request, 'The form has been submitted successfully.')
            return redirect('home')
    else:
        form = EngineerResponseForm(instance=entry)
    return render(request, 'psnapp/engineer_response.html', {'form': form, 'entry': entry})

def thank_you(request):
    return render(request, 'psnapp/thank_you.html')

def form_submission_view(request):
    if request.method == 'POST':
        form = PSNEntryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Engineer has submitted the form. Your manager is reviewing it soon.')
            return redirect('thank_you')  # Replace with your actual success URL
    else:
        form = PSNEntryForm()
    return render(request, 'form_template.html', {'form': form})

def filter_entries(request):
    filtered_entries = PSNEntry.objects.filter(unique_id__startswith='123')
    return render(request, 'psnapp/filtered_entries.html', {'entries': filtered_entries})

def download_psn_entries(request):
    entries = PSNEntry.objects.all()
    response_content = []

    for entry in entries:
        try:
            date_of_complaint = entry.date_of_complaint.isoformat() if entry.date_of_complaint else 'N/A'

            date_of_sale_of_device = entry.date_of_sale_of_device.isoformat() if entry.date_of_sale_of_device else 'N/A'
            s_trigger_date = entry.s_trigger_date.isoformat() if entry.s_trigger_date else 'N/A'
            c_trigger_date = entry.c_trigger_date.isoformat() if entry.c_trigger_date else 'N/A'
            commercial_expiry_date = entry.commercial_expiry_date.isoformat() if entry.commercial_expiry_date else 'N/A'
            first_communication_on_darby = entry.first_communication_on_darby.isoformat() if entry.first_communication_on_darby else 'N/A'
            last_communication_on_darby = entry.last_communication_on_darby.isoformat() if entry.last_communication_on_darby else 'N/A'
            vehicle_support_date = entry.vehicle_support_date.isoformat() if entry.vehicle_support_date else 'N/A'
            vehicle_sale_date = entry.vehicle_sale_date.isoformat() if entry.vehicle_sale_date else 'N/A'
            date_of_closure = entry.date_of_closure.isoformat() if entry.date_of_closure else 'N/A'
        except AttributeError as e:
            return HttpResponse(f"Error: {e}", status=500)

        response_content.append(f"{date_of_complaint}, {date_of_sale_of_device}, {s_trigger_date}, {c_trigger_date}, {commercial_expiry_date}, {first_communication_on_darby}, {last_communication_on_darby}, {vehicle_support_date}, {vehicle_sale_date}, {date_of_closure}\n")

    response = HttpResponse(response_content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="psn_entries.csv"'
    return response

def success(request):
    return render(request, 'psnapp/success.html')

def request_details(request, id):
    entry = get_object_or_404(PSNEntry, id=id)
    return render(request, 'psnapp/request_details.html', {'entry': entry})

def psn_entry_create(request):
    if request.method == 'POST':
        form = PSNEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('psn_entry_list')
    else:
        form = PSNEntryForm()
    return render(request, 'psnapp/psn_entry_form.html', {'form': form})

def psn_entry_update(request, pk):
    psn_entry = get_object_or_404(PSNEntry, pk=pk)
    if request.method == 'POST':
        form = PSNEntryForm(request.POST, instance=psn_entry)
        if form.is_valid():
            form.save()
            return redirect('psn_entry_list')
    else:
        form = PSNEntryForm(instance=psn_entry)
    return render(request, 'psnapp/psn_entry_form.html', {'form': form})

def psn_entry_list(request):
    psn_entries = PSNEntry.objects.all()
    return render(request, 'psnapp/psn_entry_list.html', {'psn_entries': psn_entries})

def generate_unique_id(entry):
    service_engineer_initial = entry.service_engineer_name[0].upper()
    current_date = timezone.now()
    year = current_date.strftime('%y')
    month = current_date.strftime('%m')
    last_entry = PSNEntry.objects.filter(unique_id__startswith=service_engineer_initial + year + month).order_by('-unique_id').first()
    if last_entry and last_entry.unique_id[6:].isdigit():
        sequence_number = int(last_entry.unique_id[6:]) + 1
    else:
        sequence_number = 0
    unique_id = f"{service_engineer_initial}{year}{month}{sequence_number:04d}"
    return unique_id
