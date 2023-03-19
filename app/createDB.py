import functionsDB

def create_database(mydb):
    cursor = mydb.cursor()
    cursor.execute("DROP DATABASE IF EXISTS " + functionsDB.DB_NAME)
    cursor.execute("CREATE DATABASE IF NOT EXISTS " + functionsDB.DB_NAME)
    cursor.execute("USE " + functionsDB.DB_NAME)

    query = '''
    CREATE TABLE ''' + functionsDB.MENU_TABLE + ''' (
        id int NOT NULL AUTO_INCREMENT,
        price DECIMAL(13, 2) NOT NULL,
        name CHAR(255) NOT NULL,
        PRIMARY KEY (id)
    )'''
    cursor.execute(query)

    query = '''
    CREATE TABLE ''' + functionsDB.INGREDIENT_TABLE + ''' (
        id int NOT NULL AUTO_INCREMENT,
        name CHAR(255) NOT NULL,
        dish_id int NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (dish_id)
            REFERENCES ''' + functionsDB.MENU_TABLE + ''' (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )'''
    cursor.execute(query)
    
    functionsDB.add_dish(mydb, '4.20', 'Sea weed', ['Water', 'Weed'])
    functionsDB.add_dish(mydb, '0.69', 'Pop corn', ['Corn'])