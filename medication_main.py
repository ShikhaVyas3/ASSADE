import sqlite3
import pandas as pd
import time
import inquirer
from datetime import date


def show_db(tablename):
    """Leverages pandas to display a sql database"""
    conn = sqlite3.connect('proto_asade.db')
    df = pd.read_sql_query(f"SELECT * FROM ({tablename})", conn) 
    print(df)
    conn.close()

    
    
def fetch_x_from_y(x,y):
    """Fetches x column from y table"""
    conn =sqlite3.connect('proto_asade.db')
    c = conn.cursor()
    c.execute(f"SELECT {x} FROM {y}")
    fetch = c.fetchall() 
    fetch_list = [x[0] for x in fetch]
    conn.close()
    return fetch_list 

def fetch_x_from_y_same_start(x,y, start_letter, extra_column):
    """Fetches column x and extra_column where column x looks like some string. Returns 'medication: descrption' list"""
    conn =sqlite3.connect('proto_asade.db')
    c = conn.cursor()
    c.execute(f"SELECT {x},{extra_column} FROM {y} WHERE {x} LIKE '{start_letter}%'")
    fetch = c.fetchall()
    fetch_list = [f"{x[0]}: {x[1]}" for x in fetch] 
    conn.close()
    return fetch_list 

def fetch_emp_password(username):
    """Fetches emp password using user name"""
    conn =sqlite3.connect('proto_asade.db')
    c = conn.cursor()
    c.execute("SELECT password FROM empolyees_b WHERE username = (?)", (username,))
    fetch = c.fetchone()[0]
    conn.close()
    return fetch

def fetch_emp_id(username):
    """Fetches emp password using user name"""
    conn =sqlite3.connect('proto_asade.db')
    c = conn.cursor()
    c.execute("SELECT rowid FROM empolyees_b WHERE username = (?)", (username,))
    fetch = c.fetchone()[0]
    conn.close()
    return fetch

 
def inputted_medication():
    """Prompts the user to input a medication name and description. Returns a string 'medication: description'."""
    med_list = fetch_x_from_y('medication', 'medications_b')
    med_name = input('¿Cual es el nombre del medicamento que quiere rasterar?: ') 
    med_name_first_letter = med_name[0]
    if med_name not in med_list: 
        sim_list = fetch_x_from_y_same_start('medication', 'medications_b', med_name_first_letter, 'description') 
        sim_list.append('Ver de la lista completa') 
        print(f'Parece que no hay un medicamento en el base de datos con el nombre {med_name}. ¿Quisiste decir?:')
    else: 
        sim_list = fetch_x_from_y_same_start('medication', 'medications_b', med_name, 'description')
    questions = [
        inquirer.List('choice', 
                    message= '',
                    choices = sim_list)
    ]
    answer  = inquirer.prompt(questions)['choice']
    if answer == 'Ver de la lista completa': 
        sim_list = fetch_x_from_y_same_start('medication', 'medications_b', '', 'description')
        questions = [
        inquirer.List('choice', 
                    message= '',
                    choices = sim_list)
    ]
        answer  = inquirer.prompt(questions)['choice']
    
    med_id = med_id_finder(answer)
    return med_id

    
def med_id_finder(answer):
    """Given a medication and description in from medication: description, returns the id"""
    med_list = answer.split(': ') 
    medication = med_list[0] 
    description = med_list[1] 
    conn =sqlite3.connect('proto_asade.db')
    c = conn.cursor()
    c.execute(f'SELECT rowid FROM medications_b WHERE (medication = (?)) AND (description = (?))', (medication, description)) 
    fetch = c.fetchall() 
    return fetch[0][0] 


  
def dispense_loop(med_name, med_description):
    """Once a medication is chosen, prompts a user to specify a quantity they want to dispense"""
    continueing = True
    while continueing: 
        amount_removed = input('Cuantas unidades le gustaría dispensar?: ')  
        option_list = ['Sí', 'No', 'Salir']
        questions = [
            inquirer.List('choice', 
                        message = f'Está seguro/a que le gustaría dispensar {amount_removed} unidades de {med_name} {med_description}?',
                        choices = option_list)
        ]
        answer = inquirer.prompt(questions)['choice']
        if answer == 'Sí':
            continueing = False
        elif answer == 'Salir':
            continueing = False
    amount = -int(amount_removed)
    return amount

def to_whom(num_units, med_name, med_description):
    """Prompts the user to input the name of the patient they are dispensing the medication to. Returns patient name"""
    continueing = True
    while continueing is True:
        patient_name = input('¿A quién le gustaría dispensar el medicamento?: ')
        option_list = ['Sí', 'No']
        questions = [
        inquirer.List('choice', 
                            message = f'Está seguro/a de que desea dispensar {num_units} de {med_name} {med_description} a {patient_name}?',
                            choices = option_list)
        ]
        answer = inquirer.prompt(questions)['choice']
        if answer == 'Sí':
            continueing = False
    return patient_name

    
def get_med_name(med_id):
    """Retrieves the name of a medication given its id"""
    med_id = str(med_id)
    conn = sqlite3.connect('proto_asade.db')
    c = conn.cursor()
    c.execute('SELECT medication FROM medications_b WHERE rowid = ?',(med_id,))
    fetch = c.fetchall()[0][0]
    print(f"Med_id: {med_id}")
    conn.close()
    return fetch
    
def get_med_description(med_id):
    """Retrieves the name of a medication given its id"""
    med_id = str(med_id)
    conn = sqlite3.connect('proto_asade.db')
    c = conn.cursor()
    c.execute('SELECT description FROM medications_b WHERE rowid = ?',(med_id,))
    fetch = c.fetchall()[0][0]
    conn.close()
    return fetch

def get_emp_name(emp_id):
    emp_id = str(emp_id)
    conn = sqlite3.connect('proto_asade.db')
    c = conn.cursor()
    c.execute('SELECT first_names, apellido_paterno, appelido_materno FROM empolyees_b WHERE rowid = ?',(emp_id))
    fetch = c.fetchall()[0]
    name = f"{fetch[0]} {fetch[1]} {fetch[2]}"
    conn.close()
    return name

def get_privlages(emp_id):
    emp_id = str(emp_id)
    conn = sqlite3.connect('proto_asade.db')
    c = conn.cursor()
    c.execute('SELECT privlages FROM empolyees_b WHERE rowid = ?',(emp_id))
    fetch = c.fetchall()[0][0]
    conn.close()
    return fetch

def display_pre_transaction(med_id, emp_id, to_whom, ammount):
    """Verifies that the user wants to make the transaction. If yes, returns string to be inputed into transaction table. If note, returns None"""
    med_name = get_med_name(med_id)
    med_description = get_med_description(med_id)
    emp_name = get_emp_name(emp_id)
    if ammount > 0:
        restock = 'Sí'
        action = 'Dispensa'
    else:
        restock = 'No'
        action = 'Reposición de inventario'
    date_change = date.today()
    print(f"""
          Acción: {action}
          Paciente: {to_whom}
          Medicamento: {med_name} {med_description}
          Empleado: {emp_name}
          Fecha: {date_change}
          Número de unidades (negativo cuando se trata de una dispensación): {ammount}
          """)
    option_list = ['Realizar acción', 'Salir']
    questions = [
    inquirer.List('choice', 
                        message = f'',
                        choices = option_list)
    ]
    answer = inquirer.prompt(questions)['choice']
    if answer == "Realizar acción":
        return (med_id, emp_name, to_whom, ammount, restock, date_change)
    else:
        return exit()
    
    
def new_transaction(med_id,emp_name,to_whom,amount,restock,date_change):
    """"Makes an addition to the transaction table."""
    conn =sqlite3.connect('proto_asade.db')
    c = conn.cursor()
    med_id = str(med_id)
    med_name = get_med_name(med_id)
    med_description = get_med_description(med_id)
    c.execute("INSERT INTO transaction_tracker_b VALUES(?,?,?,?,?,?,?)", (med_name, med_description,emp_name,to_whom,amount,restock,date_change))
    c.execute("""UPDATE medications_b  
                SET num_units_in_stock = num_units_in_stock + (?)
                WHERE rowid = (?)""",
              (int(amount), med_id))
    conn.commit()
    conn.close()
    print('Transación rastreada')
    show_db('transaction_tracker_b')
        
def log_in():
    continueing = True
    
    user_list = fetch_x_from_y('username', 'empolyees_b')
    """Prompts the user to type in a username and password. Returns the username which will give unique privlages"""
    while continueing is True:
        user = input('Nombre de usario: ')
        password = input('Contraseña: ')
        real_pass = 'fn1208vff1230f8hxmjaedf0asdf812u13r081nasdfasdfhiadf1032e40182e4u13nksvas'
        if user in user_list:
            real_pass = fetch_emp_password(user)
        if user not in user_list or real_pass != password:
            print(f'Usuario o contraseña no coinciden')  
            want_to_continue = input("¿Le gustaría intentar de nuevo?: ") 
            if want_to_continue.lower() == 'no': 
                continueing = False
        else:
            continueing = False
    return user