import functionsDB

def create_database(db):
    cursor = db.cursor()
    cursor.execute("DROP DATABASE IF EXISTS " + functionsDB.DB_NAME)
    cursor.execute("CREATE DATABASE IF NOT EXISTS " + functionsDB.DB_NAME)
    cursor.execute("USE " + functionsDB.DB_NAME)

    query = '''
    CREATE TABLE ''' + functionsDB.MENU_TABLE + ''' (
        id int NOT NULL AUTO_INCREMENT,
        price DECIMAL(13, 2) NOT NULL,
        name CHAR(255) NOT NULL,
        image_link CHAR(255) NOT NULL,
        ingredients CHAR(255) NOT NULL,
        cooking_time TIME NOT NULL,
        PRIMARY KEY (id)
    )'''
    cursor.execute(query)

    query = '''
    CREATE TABLE ''' + functionsDB.INGREDIENT_TABLE + ''' (
        id int NOT NULL AUTO_INCREMENT,
        name CHAR(255) NOT NULL,
        amount CHAR(255) NOT NULL,
        dish_id int NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (dish_id)
            REFERENCES ''' + functionsDB.MENU_TABLE + ''' (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )'''
    cursor.execute(query)
    
    functionsDB.add_dish(db, '4.20', 'Sea weed', 'http://myimagestorage.com/sea_weed.png', '00:15:00')
    functionsDB.add_dish(db, '0.69', 'Pop corn', 'http://myimagestorage.com/pop_corn.png', '00:03:15')
    
    functionsDB.add_dish_ingredient(db, 1, 'Water', '150ml')
    functionsDB.add_dish_ingredient(db, 1, 'Weed', '40g')
    
    functionsDB.add_dish_ingredient(db, 2, 'Corn', '230g')
    functionsDB.add_dish_ingredient(db, 2, 'Water', '90ml')