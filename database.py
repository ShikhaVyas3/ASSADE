#creating database
import sqlite3

conn = sqlite3.connect('proto_asade.db')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS medications_b')

#remove the table if exists

c.execute("""
          CREATE TABLE medications_b(
            medication TEXT NOT NULL,
            description TEXT NOT NULL,
            high_low_mid_use INTEGER, 
            num_units_per_month INTEGER, 
            num_units_in_stock INTEGER, 
            date_of_last_restock TEXT 
          )
          """)

med_list = [
    ("Metformina", "1000mg Tableta", 3, 1000, 321, "2024-12-28"),
    ("Metformina", "500mg Tableta", 3, 1000, 311, "2024-11-05"),
    ("Glyburide", "5mg Tableta", 3, 1000, 74, "2025-01-12"),
    ("Gabapentina", "600mg Tableta", 3, 500, 490, "2024-12-05"),
    ("Cefalexina", "500mg Capsula", 2, 200, 194, "2024-12-30"),
    ("Claritromicina", "500mg Tableta", 2, 200, 389, "2024-12-18"),
    ("Ciprofloxacina", "500mg Tableta", 2, 200, 167, "2025-01-19"),
    ("Levofloxacina", "500mg Tableta", 2, 200, 218, "2025-01-12"),
    ("Amoxicilina", "600mg Suspensión Frasco", 3, 100, 380, "2024-12-20"),
    ("Amoxicilina", "400mg Suspensión Frasco", 3, 100, 194, "2025-01-24"),
    ("Cefalexina", "250mg Suspensión Frasco", 3, 100, 96, "2024-11-12"),
    ("Cefradoxilo", "250mg Suspensión Frasco", 3, 100, 469, "2024-11-12"),
    ("Lisinopril", "20mg Tableta", 3, 500, 53, "2024-11-03"),
    ("Enalapril", "20mg Tableta", 3, 500, 496, "2025-01-23"),
    ("Lansoprazol", "30mg Capsula", 3, 1000, 423, "2024-12-02"),
    ("Omeprazol", "20mg Capsula", 3, 1000, 39, "2025-01-16"),
    ("Clorfeniramina", "Jarabe", 2, 150, 338, "2024-11-24"),
    ("Ibuprofeno", "800mg Tableta", 2, 300, 330, "2024-11-09"),
    ("Metronidazol", "500mg Tableta", 2, 100, 346, "2025-01-07"),
    ("Minociclina", "90mg Tableta", 1, 180, 330, "2025-01-14"),
    ("Cardioaspirina", "81mg Tableta", 3, 500, 417, "2024-12-13"),
    ("Laxantes", "Capsulas", 2, 100, 429, "2025-01-11"),
    ("Triple antibiótico", "Crema Tubo", 3, 75, 208, "2024-11-17"),
    ("Hidrocortisona", "Crema Tubo", 2, 75, 468, "2025-01-11"),
    ("Clotrimazol", "Crema Tubo", 2, 75, 344, "2025-01-07"),
    ("Benzoato de bencilo", "Loción Frasco", 1, 50, 126, "2024-11-28"),
    ("NyQuil", "Jarabe Frasco", 2, 125, 261, "2024-12-12"),
    ("DayQuil", "Jarabe Frasco", 2, 125, 159, "2025-01-14"),
    ("AJ Flujipect", "Jarabe Frasco", 2, 200, 355, "2024-11-14"),
    ("Fluticasona", "Spray Inhalador", 2, 50, 318, "2024-12-21"),
    ("Albuterol", "Spray Inhalador", 2, 50, 18, "2024-12-26"),
    ("Spiriva", "Capsulas + Inhalador (caja)", 2, 25, 39, "2025-01-27"),
    ("Ambroxol", "Jarabe Frasco", 2, 50, 440, "2024-12-23"),
    ("Dexametasona", "Ampolla", 3, 200, 65, "2024-11-03"),
    ("Piroxican", "Ampolla", 3, 200, 10, "2025-01-30"),
    ("Dipirona", "Ampolla", 3, 100, 296, "2025-01-15"),
    ("Ibersartan", "150mg Tableta", 2, 500, 470, "2024-11-15"),
    ("Creon", "Capsulas", 2, 100, 149, "2024-12-02"),
    ("Prednisona", "10mg Tableta", 1, 50, 218, "2025-01-17"),
    ("Fluconazol", "100mg-150mg Tableta", 1, 25, 198, "2024-12-20"),
    ("Terbinafina", "250mg Tableta", 1, 25, 68, "2024-11-27"),
    ("Diclofenaco", "75mg Tableta", 2, 100, 50, "2025-01-24"),
    ("Cloranfenicol", "Gotas oftalmicas", 2, 50, 317, "2024-11-26"),
    ("Ketorolaco", "Gotas oftalmicas", 2, 50, 472, "2024-11-04"),
    ("Otik", "Gotas óticas", 2, 50, 122, "2024-11-25"),
    ("Ibuprofeno", "Jarabe Frasco", 3, 150, 345, "2024-12-30"),
    ("Acetaminofen", "Jarabe Frasco", 3, 200, 188, "2024-11-10")
]

c.executemany('INSERT INTO medications_b VALUES (?,?,?,?,?,?)', med_list)

#creat employee table

c.execute('DROP TABLE IF EXISTS empolyees_b')
c.execute("""
          CREATE TABLE empolyees_b(
              username TEXT UNIQUE NOT NULL, 
              password TEXT UNIQUE NOT NULL, 
              first_names TEXT NOT NULL, 
              apellido_paterno TEXT NULL, 
              appelido_materno TEXT NULL,
              privlages TEXT, 
              job_description TEXT, 
              fecha_de_nacimiento TEXT,
              date_added TEXT
          )
          """)

emp_list = [
    ("nurse_juana", "nursepass", "Ana Sofía", "González", "Méndez", "None", "Nurse", "1990-05-14", "2025-02-01"),
    ("admin_jaime", "adminpass", "Jaime", "Martinez", "Gomez", "Admin", "Clinic Manager", "1985-08-22", "2025-02-01")
]
c.executemany('INSERT INTO empolyees_b VALUES (?,?,?,?,?,?,?,?,?)', emp_list)

#Create patients table
c.execute('DROP TABLE IF EXISTS patients_b')
c.execute("""
          CREATE TABLE patients_b(
              first_names TEXT NOT NULL, 
              apellido_paterno TEXT, 
              appellido_materno TEXT, 
              fecha_de_nacimiento TEXT, 
              doctor_id TEXT, 
              FOREIGN KEY(doctor_id) REFERENCES empolyees_b(rowid) ON DELETE SET NULL
          )
          """)


#Creating transactions table

c.execute('DROP TABLE IF EXISTS transaction_tracker_b')
c.execute("""
          CREATE TABLE transaction_tracker_b(
            med_name TEXT, 
            med_description TEXT,
            emp_name TEXT,
            to_whom TEXT,
            ammount INTEGER, 
            restock TEXT,
            date_change TEXT,
            FOREIGN KEY(med_name) REFERENCES medications_b(medication) ON DELETE SET NULL,
            FOREIGN KEY(med_description) REFERENCES medications_b(description) ON DELETE SET NULL
          )
          """)

conn.commit()
conn.close()