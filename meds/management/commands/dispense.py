from django.core.management.base import BaseCommand
from meds.models import Medication, Employee, Transaction
from datetime import date
import inquirer

class Command(BaseCommand):
    help = 'Dispense a medication to a patient and log the transaction'

    def handle(self, *args, **kwargs):
        username = self.log_in()
        if not username:
            self.stdout.write(self.style.WARNING("Login failed. Exiting..."))
            return
        
        emp = Employee.objects.get(username=username)
        med = self.select_medication()
        if not med:
            self.stdout.write("No medication selected.")
            return
        
        amount = self.dispense_loop(med)
        patient_name = self.to_whom(amount, med)
        confirm = self.confirm_transaction(med, emp, patient_name, amount)

        if confirm:
            self.save_transaction(med, emp, patient_name, amount, confirm['restock'], confirm['date_change'])
            self.stdout.write(self.style.SUCCESS("Transacción completada y guardada."))

    def log_in(self):
        employees = Employee.objects.values_list('username', flat=True)
        while True:
            username = input("Nombre de usuario: ").strip()
            password = input("Contraseña: ").strip()
            if username in employees:
                emp = Employee.objects.get(username=username)
                if emp.password == password:
                    return username
            print("⚠️  Usuario o contraseña incorrectos.")
            retry = input("¿Intentar de nuevo? (sí/no): ").lower()
            if retry != 'sí':
                return None

    def select_medication(self):
        meds = Medication.objects.all()
        choices = [f"{m.id}: {m.medication} - {m.description}" for m in meds]
        if not choices:
            return None

        questions = [
            inquirer.List('med_choice', message="Seleccione un medicamento:", choices=choices)
        ]
        selected = inquirer.prompt(questions)
        if selected:
            med_id = int(selected['med_choice'].split(":")[0])
            return Medication.objects.get(id=med_id)
        return None

    def dispense_loop(self, med):
        while True:
            try:
                qty = int(input(f"¿Cuántas unidades de '{med.medication} - {med.description}' desea dispensar?: "))
                questions = [
                    inquirer.List('confirm', message=f"¿Está seguro de dispensar {qty} unidades?", choices=['Sí', 'No', 'Salir'])
                ]
                confirm = inquirer.prompt(questions)['confirm']
                if confirm == 'Sí':
                    return -abs(qty)  # Make it negative
                elif confirm == 'Salir':
                    exit()
            except ValueError:
                print("⚠️  Ingrese un número válido.")

    def to_whom(self, qty, med):
        while True:
            name = input("¿A quién va dirigido el medicamento?: ")
            questions = [
                inquirer.List('confirm', message=f"¿Está seguro de que desea dispensar {abs(qty)} unidades de {med.medication} a {name}?", choices=['Sí', 'No'])
            ]
            if inquirer.prompt(questions)['confirm'] == 'Sí':
                return name

    def confirm_transaction(self, med, emp, patient_name, qty):
        restock = 'No' if qty < 0 else 'Sí'
        action = "Dispensa" if qty < 0 else "Reposición"
        today = date.today()

        print("\nResumen de la transacción:")
        print(f"Acción: {action}")
        print(f"Empleado: {emp.first_names} {emp.apellido_paterno or ''} {emp.appelido_materno or ''}".strip())
        print(f"Paciente: {patient_name}")
        print(f"Medicamento: {med.medication} - {med.description}")
        print(f"Cantidad: {qty}")
        print(f"Fecha: {today}\n")

        confirm = inquirer.prompt([
            inquirer.List('final', message="¿Confirmar esta transacción?", choices=['Realizar acción', 'Cancelar'])
        ])

        if confirm['final'] == 'Realizar acción':
            return {'restock': restock, 'date_change': today}
        else:
            print("❌ Transacción cancelada.")
            return None

    def save_transaction(self, med, emp, patient_name, qty, restock, date_change):
        Transaction.objects.create(
            med_name=med.medication,
            med_description=med.description,
            emp_name=f"{emp.first_names} {emp.apellido_paterno or ''} {emp.appelido_materno or ''}".strip(),
            to_whom=patient_name,
            ammount=qty,
            restock=restock,
            date_change=date_change
        )
        med.num_units_in_stock += qty
        med.save()
