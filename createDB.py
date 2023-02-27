import functionsDB

def create_database(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("DROP DATABASE IF EXISTS " + functionsDB.DB_NAME)
    mycursor.execute("CREATE DATABASE IF NOT EXISTS " + functionsDB.DB_NAME)
    mycursor.execute("USE " + functionsDB.DB_NAME)

    query = '''
    CREATE TABLE ''' + functionsDB.MENU_TABLE + ''' (
        id int NOT NULL AUTO_INCREMENT,
        price DECIMAL(13, 2) NOT NULL,
        name CHAR(255) NOT NULL,
        PRIMARY KEY (id)
    )'''
    mycursor.execute(query)
    
    functionsDB.add_dish(mydb, '4.20', 'Sea weed')
    functionsDB.add_dish(mydb, '0.69', 'Pop corn')