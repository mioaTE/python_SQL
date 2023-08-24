import psycopg2

print("Cats and Owners")

hostname = 'localhost'
database = 'demo'
username = 'postgres'
pwd = 'postgres1'
port_id = 5432
conn = None
cur = None

try: 
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    cur = conn.cursor()

    # Create the owner table
    create_owner_script = '''CREATE TABLE IF NOT EXISTS owner (
        owner_id SERIAL PRIMARY KEY,
        owner_name VARCHAR(50) NOT NULL,
        contact_info VARCHAR(100)
    )'''
    
    cur.execute(create_owner_script)
    conn.commit()

     # Alter the owner table to change data type of 'phone_number' column to VARCHAR
    alter_owner_script = '''ALTER TABLE owner
        ALTER COLUMN phone_number TYPE VARCHAR(20)'''
    
    cur.execute(alter_owner_script)
    conn.commit()


    # # Insert data into the owner table
    # insert_owner_script = '''INSERT INTO owner (owner_name, phone_number)
    #     VALUES ('Dorothy', '1234567890'),
    #            ('Andrew', '9876543210'),
    #            ('Nick', '2345678901')'''
    
    # cur.execute(insert_owner_script)
    # conn.commit()

    # Create the cat table with foreign key reference to owner
    create_cat_script = '''CREATE TABLE IF NOT EXISTS cat (
        cat_id SERIAL PRIMARY KEY,
        cat_name VARCHAR(40) NOT NULL,
        breed VARCHAR(40),
        age INT,
        owner_id INT REFERENCES owner(owner_id)
    )'''

    # # Insert data into the cat table
    # insert_cat_script = '''INSERT INTO cat (cat_name, breed, age, owner_id)
    #     VALUES ('Churro', 'Longhair', 3, 1),
    #            ('Anko', 'Shorthair', 2, 1),
    #            ('Pandan', 'Ragdoll', 1, 2),
    #            ('Lucy', 'Siamese', 2, 3)'''
    
    # cur.execute(insert_cat_script)
    # conn.commit()
    
    cur.execute(create_cat_script)
    conn.commit()

     # Retrieve and display data from both owner and cat tables
    select_script = '''SELECT o.owner_name, o.phone_number, c.cat_name, c.breed, c.age
                      FROM owner o
                      JOIN cat c ON o.owner_id = c.owner_id'''
    
    cur.execute(select_script)
    records = cur.fetchall()

    print("Owner Name\tPhone Number\tCat Name\tBreed\tAge")
    print("--------------------------------------------------------")
    for record in records:
        print("\t".join(str(field) for field in record))
    
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()