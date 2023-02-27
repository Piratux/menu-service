import mysql.connector
import pandas as pd

import helper

DB_NAME = 'restaurant_db'
MENU_TABLE = 'menu'

MENU_MAX_NAME_LENGTH = 250

def add_dish(mydb, price, name):
    try:
        price = float(price)
    except ValueError:
        return helper.error_query("price must be convertible to float")
    
    if len(name) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("name can't be longer than " + str(MENU_MAX_NAME_LENGTH))
    
    if price <= 0:
        return helper.error_query("price can't be negative or 0")
    
    mycursor = mydb.cursor()
    sql = "INSERT INTO " + MENU_TABLE + " (price, name) VALUES (%s,%s)"
    val = (price, name)
    mycursor.execute(sql, val)
    mydb.commit()
    
    return helper.ok_query()

def delete_dish(mydb, dish_id):
    try:
        dish_id = int(dish_id)
    except ValueError:
        return helper.error_query("dish_id must be convertible to int")
    
    mycursor = mydb.cursor()
    sql = "DELETE FROM " + MENU_TABLE + " WHERE id = %s"
    val = (dish_id, )
    mycursor.execute(sql, val)
    mydb.commit()
    
    return helper.ok_query()

def get_dishes(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM " + MENU_TABLE)
    myresult = mycursor.fetchall()

    rows = []
    for x in myresult:
        rows.append(str(x))
    
    return pd.DataFrame({"result": pd.Series(rows)}).to_json()

def update_dish(mydb, dish_id, price, name):
    try:
        dish_id = int(dish_id)
    except ValueError:
        return helper.error_query("dish_id must be convertible to int")
    
    try:
        price = float(price)
    except ValueError:
        return helper.error_query("price must be convertible to float")
    
    if len(name) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("name can't be longer than " + str(MENU_MAX_NAME_LENGTH))
    
    if price <= 0:
        return helper.error_query("price can't be negative or 0")
    
    mycursor = mydb.cursor()
    sql = "UPDATE " + MENU_TABLE + " SET price = %s, name = %s WHERE id = %s"
    val = (price, name, dish_id)
    mycursor.execute(sql, val)
    mydb.commit()
    
    return helper.ok_query()