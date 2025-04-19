from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse
from meds.models import Medication, Employee, Transaction
from django.utils import timezone

def home(request):
    return render(request, 'meds/home.html')

def list_medications(request):
    meds = Medication.objects.all()
    return render(request, 'meds/med_list.html', {'medications': meds})

def dispense_form(request, med_id):
    med = Medication.objects.get(id=med_id)
    if request.method == 'POST':
        qty = int(request.POST.get('quantity'))
        patient_name = request.POST.get('patient_name')
        emp = Employee.objects.get(username='admin_jaime')  # TEMP: Replace with logged-in user later

        Transaction.objects.create(
            med_name=med.medication,
            med_description=med.description,
            emp_name=f"{emp.first_names} {emp.apellido_paterno or ''} {emp.appelido_materno or ''}".strip(),
            to_whom=patient_name,
            ammount=-abs(qty),
            restock='No',
            date_change=timezone.now().date()
        )
        med.num_units_in_stock -= qty
        med.save()
        return redirect('meds:list_medications')
    
    return render(request, 'meds/dispense_form.html', {'medication': med})

