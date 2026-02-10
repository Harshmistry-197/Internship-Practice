import pyodbc

try:
    # Connect
    print("Building Connection")
    con_string = (
        "driver={ODBC Driver 17 for SQL Server};"
        "server=1R-76;"
        "database=harsh;"
        "trusted_connection=yes;"
    )
    conn = pyodbc.connect(con_string)
    print("Successfully Connected")


    # Creating cursor
    print("Creating cursor")
    cursor = conn.cursor()
    print("Successfully Created cursor")


    # # Single Insert into table
    try:
        insert_query = "INSERT INTO INTERNS (NAME, AGE, EMAIL, CITY, PHONE_NUMBER) VALUES (?,?,?,?,?);"
        cursor.execute(insert_query, ('Jane Smith', 21, 'jane.smith@email.com', 'Mumbai', '+91 9878755456'))
        conn.commit()
        print("Single record inserted successfully")

    except pyodbc.Error as e:
        print("Insertion failed", e)


    # Multiple Insertion into table
    try:
        val = [
            ('Alice Brown', 23, 'alice.b@email.com', 'Vapi', '+91 9775485545'),
            ('Bob Miller', 22, 'bob.m@email.com', 'Valsad', '+91 8785554456'),
            ('Charlie Davis', 24, 'charlie.d@email.com', 'Navsari', '+91 6485785123')
        ]
        insert_query = "INSERT INTO INTERNS (NAME, AGE, EMAIL, CITY, PHONE_NUMBER) VALUES (?,?,?,?,?);"
        cursor.executemany(insert_query, val)
        conn.commit()
        print("Multiple record inserted successfully")

    except pyodbc.Error as e:
        print("Multiple Insertion failed", e)


    # Read all Records
    try:
        read_query = "SELECT * FROM INTERNS;"
        cursor.execute(read_query)
        data = cursor.fetchall()
        for row in data:
            print(row)

    except pyodbc.Error as e:
        print("Reading Records from table Failed ", e)


    # Update Records in table
    try:
        update_query = "UPDATE INTERNS SET age = age + 1 WHERE NAME = 'Bob Miller';"
        cursor.execute(update_query)
        conn.commit()
        print("Successfully Updated")

    except pyodbc.Error as e:
        print("Updating Records into table Failed ", e)


    # Deleting the records
    try:
        delete_query = "DELETE FROM INTERNS WHERE INTERN_ID = 2;"
        cursor.execute(delete_query)
        conn.commit()
        print("Successfully Deleted")
        cursor.close()
        conn.close()

    except pyodbc.Error as e:
        print("Deleting Records into table Failed ", e)

except pyodbc.Error as e:
    print("Failed to connect to database",e)
except Exception as e:
    print("Unrecognised error occurred", e)

