import datetime
import requests
from requests.exceptions import ConnectionError

import helper

DB_NAME = 'restaurant_db'
MENU_TABLE = 'menu'
INGREDIENT_TABLE = 'ingredient'
AUTHORS_TABLE = 'authors'

MENU_MAX_NAME_LENGTH = 250
MENU_MAX_LINK_LENGTH = 250

def _get_dish_author_id(db, dish_id):
    cursor = db.cursor()
    sql = "SELECT author_id FROM " + MENU_TABLE + " WHERE id = %s"
    val = (dish_id, )
    cursor.execute(sql, val)
    result = cursor.fetchall()
    
    if len(result) > 0:
        row_headers=[x[0] for x in cursor.description]
        return dict(zip(row_headers, result[0]))["author_id"]
    else:
        return None

def get_dishes(db):
    cursor = db.cursor()
    sql = "SELECT * FROM " + MENU_TABLE
    cursor.execute(sql)
    result = cursor.fetchall()

    row_headers=[x[0] for x in cursor.description]
    rows = []
    for x in result:
        d = dict(zip(row_headers, x))
        d["author"] = get_author(d["author_id"])
        d.pop("author_id")
        rows.append(d)
    
    return helper.to_json(rows)

def get_dish(db, dish_id):
    try:
        dish_id = int(dish_id)
    except TypeError:
        return helper.error_query("dish_id must be convertible to int")
    except ValueError:
        return helper.error_query_404()
    
    cursor = db.cursor()
    sql = "SELECT * FROM " + MENU_TABLE + " WHERE id = %s"
    val = (dish_id, )
    cursor.execute(sql, val)
    result = cursor.fetchall()
    
    if len(result) == 0:
        return helper.error_query_404()
    
    row_headers=[x[0] for x in cursor.description]
    
    d = dict(zip(row_headers, result[0]))
    d["author"] = get_author(d["author_id"])
    d.pop("author_id")

    return helper.to_json(d)

def add_dish(db, price, name, image_link, cooking_time, author_name, author_surname):
    try:
        price = float(price)
    except (ValueError, TypeError):
        return helper.error_query("price must be convertible to number")
    
    if not isinstance(name, str):
        return helper.error_query("name must be string")
    
    if not isinstance(image_link, str):
        return helper.error_query("image_link must be string")
    
    if not isinstance(cooking_time, str):
        return helper.error_query("cooking_time must be string")
    
    if price <= 0:
        return helper.error_query("price can't be negative or 0")
    
    if len(name) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("name can't be longer than " + str(MENU_MAX_NAME_LENGTH))
    
    if len(image_link) > MENU_MAX_LINK_LENGTH:
        return helper.error_query("image link can't be longer than " + str(MENU_MAX_LINK_LENGTH))
    
    try:
        cooking_time = datetime.datetime.strptime(cooking_time, "%H:%M:%S")
    except ValueError:
        return helper.error_query("cooking time must have time format: 'HH:MM:SS'")
    
    if not isinstance(author_name, str):
        return helper.error_query("author['name'] must be string")

    if not isinstance(author_surname, str):
        return helper.error_query("author['surname'] must be string")

    if len(author_name) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("author['name'] can't be longer than " + str(MENU_MAX_NAME_LENGTH))
    
    if len(author_surname) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("author['surname'] can't be longer than " + str(MENU_MAX_NAME_LENGTH))

    author_id = add_author(author_name, author_surname)
    if author_id == None:
        return helper.error_query("internal service error", 500)

    cursor = db.cursor()
    sql = "INSERT INTO " + MENU_TABLE + " (price, name, image_link, cooking_time, ingredients, author_id) VALUES (%s,%s,%s,%s,%s,%s)"
    val = (price, name, image_link, cooking_time, "", author_id)
    cursor.execute(sql, val)
    db.commit()
    
    dish_id = cursor.lastrowid
    
    sql = "UPDATE " + MENU_TABLE + " SET ingredients = %s WHERE id = %s"
    val = ("/dishes/" + str(dish_id) + "/ingredients", dish_id)
    cursor.execute(sql, val)
    db.commit()
    
    return get_dish(db, dish_id)

def update_dish(db, dish_id, price, name, image_link, cooking_time, author_name, author_surname):
    try:
        dish_id = int(dish_id)
    except TypeError:
        return helper.error_query("dish_id must be convertible to int")
    except ValueError:
        return helper.error_query_404()

    try:
        price = float(price)
    except (ValueError, TypeError):
        return helper.error_query("price must be convertible to number")
    
    if not isinstance(name, str):
        return helper.error_query("name must be string")
    
    if not isinstance(image_link, str):
        return helper.error_query("image_link must be string")
    
    if not isinstance(cooking_time, str):
        return helper.error_query("cooking_time must be string")
    
    if price <= 0:
        return helper.error_query("price can't be negative or 0")
    
    if len(name) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("name can't be longer than " + str(MENU_MAX_NAME_LENGTH))
    
    if len(image_link) > MENU_MAX_LINK_LENGTH:
        return helper.error_query("image link can't be longer than " + str(MENU_MAX_LINK_LENGTH))
    
    try:
        cooking_time = datetime.datetime.strptime(cooking_time, "%H:%M:%S")
    except ValueError:
        return helper.error_query("cooking time must have time format: 'HH:MM:SS'")
    
    if not isinstance(author_name, str):
        return helper.error_query("author['name'] must be string")

    if not isinstance(author_surname, str):
        return helper.error_query("author['surname'] must be string")

    if len(author_name) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("author['name'] can't be longer than " + str(MENU_MAX_NAME_LENGTH))
    
    if len(author_surname) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("author['surname'] can't be longer than " + str(MENU_MAX_NAME_LENGTH))
    
    author_id = _get_dish_author_id(db, dish_id)
    if author_id == None:
        return helper.error_query_404()
        
    result = update_author(author_id, author_name, author_surname)
    if result == None:
        return helper.error_query("internal service error", 500)
    
    cursor = db.cursor()
    sql = "UPDATE " + MENU_TABLE + " SET price = %s, name = %s, image_link = %s, cooking_time = %s WHERE id = %s"
    val = (price, name, image_link, cooking_time, dish_id)
    cursor.execute(sql, val)
    db.commit()
    
    return get_dish(db, dish_id)

def delete_dish(db, dish_id):
    try:
        dish_id = int(dish_id)
    except TypeError:
        return helper.error_query("dish_id must be convertible to int")
    except ValueError:
        return helper.error_query_404()
    
    author_id = _get_dish_author_id(db, dish_id)
    if author_id == None:
        return None
    
    result = delete_author(author_id)
    if author_id == -1:
        return helper.error_query("internal service error", 500)

    cursor = db.cursor()
    sql = "DELETE FROM " + MENU_TABLE + " WHERE id = %s"
    val = (dish_id, )
    cursor.execute(sql, val)
    db.commit()

def _dish_exists(db, dish_id):
    cursor = db.cursor()
    sql = "SELECT * FROM " + MENU_TABLE + " WHERE id = %s"
    val = (dish_id, )
    cursor.execute(sql, val)
    result = cursor.fetchall()
    
    return len(result) > 0

def add_dish_ingredient(db, dish_id, name, amount):
    try:
        dish_id = int(dish_id)
    except TypeError:
        return helper.error_query("dish_id must be convertible to int")
    except ValueError:
        return helper.error_query_404()
    
    if not _dish_exists(db, dish_id):
        return helper.error_query_404()
    
    if not isinstance(name, str):
        return helper.error_query("name must be string")
    
    if not isinstance(amount, str):
        return helper.error_query("amount must be string")
    
    if len(name) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("name can't be longer than " + str(MENU_MAX_NAME_LENGTH))
    
    if len(amount) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("amount can't be longer than " + str(MENU_MAX_NAME_LENGTH))
    
    cursor = db.cursor()
    sql = "INSERT INTO " + INGREDIENT_TABLE + " (name, amount, dish_id) VALUES (%s,%s,%s)"
    val = (name, amount, dish_id)
    cursor.execute(sql, val)
    db.commit()
    
    ingredient_id = cursor.lastrowid
    
    return get_dish_ingredient(db, dish_id, ingredient_id)

def get_dish_ingredients(db, dish_id):
    try:
        dish_id = int(dish_id)
    except TypeError:
        return helper.error_query("dish_id must be convertible to int")
    except ValueError:
        return helper.error_query_404()
    
    if not _dish_exists(db, dish_id):
        return helper.error_query_404()
    
    cursor = db.cursor()
    sql = "SELECT id, name, amount FROM " + INGREDIENT_TABLE + " WHERE dish_id = %s"
    val = (dish_id, )
    cursor.execute(sql, val)
    result = cursor.fetchall()

    row_headers=[x[0] for x in cursor.description]
    rows = []
    for x in result:
        d = dict(zip(row_headers, x))
        rows.append(d)
    
    return helper.to_json(rows)

def get_dish_ingredient(db, dish_id, ingredient_id, ignore_dish_id = False):
    if not ignore_dish_id:
        try:
            dish_id = int(dish_id)
        except TypeError:
            return helper.error_query("dish_id must be convertible to int")
        except ValueError:
            return helper.error_query_404()
    
        if not _dish_exists(db, dish_id):
            return helper.error_query_404()
    
    try:
        ingredient_id = int(ingredient_id)
    except TypeError:
        return helper.error_query("ingredient_id must be convertible to int")
    except ValueError:
        return helper.error_query_404()
    
    cursor = db.cursor()
    sql = "SELECT id, name, amount FROM " + INGREDIENT_TABLE + " WHERE id = %s"
    val = (ingredient_id, )
    cursor.execute(sql, val)
    result = cursor.fetchall()
    
    if len(result) == 0:
        return helper.error_query_404()
    
    row_headers=[x[0] for x in cursor.description]
    
    d = dict(zip(row_headers, result[0]))
    
    return helper.to_json(d)

def update_dish_ingredient(db, dish_id, ingredient_id, name, amount, ignore_dish_id = False):
    if not ignore_dish_id:
        try:
            dish_id = int(dish_id)
        except TypeError:
            return helper.error_query("dish_id must be convertible to int")
        except ValueError:
            return helper.error_query_404()

        if not _dish_exists(db, dish_id):
            return helper.error_query_404()
    
    try:
        ingredient_id = int(ingredient_id)
    except TypeError:
        return helper.error_query("ingredient_id must be convertible to int")
    except ValueError:
        return helper.error_query_404()
    
    if not isinstance(name, str):
        return helper.error_query("name must be string")
    
    if not isinstance(amount, str):
        return helper.error_query("amount must be string")
    
    if len(name) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("name can't be longer than " + str(MENU_MAX_NAME_LENGTH))
    
    if len(amount) > MENU_MAX_NAME_LENGTH:
        return helper.error_query("amount can't be longer than " + str(MENU_MAX_NAME_LENGTH))
    
    cursor = db.cursor()
    sql = "UPDATE " + INGREDIENT_TABLE + " SET name = %s, amount = %s WHERE id = %s"
    val = (name, amount, ingredient_id)
    cursor.execute(sql, val)
    db.commit()
    
    return get_dish_ingredient(db, dish_id, ingredient_id, ignore_dish_id)

def delete_dish_ingredient(db, dish_id, ingredient_id, ignore_dish_id = False):
    if not ignore_dish_id:
        try:
            dish_id = int(dish_id)
        except TypeError:
            return helper.error_query("dish_id must be convertible to int")
        except ValueError:
            return helper.error_query_404()

        if not _dish_exists(db, dish_id):
            return helper.error_query_404()
    
    try:
        ingredient_id = int(ingredient_id)
    except TypeError:
        return helper.error_query("ingredient_id must be convertible to int")
    except ValueError:
        return helper.error_query_404()
    
    cursor = db.cursor()
    sql = "DELETE FROM " + INGREDIENT_TABLE + " WHERE id = %s"
    val = (ingredient_id, )
    cursor.execute(sql, val)
    db.commit()

def get_ingredients(db):
    cursor = db.cursor()
    sql = "SELECT id, name, amount FROM " + INGREDIENT_TABLE
    cursor.execute(sql)
    result = cursor.fetchall()

    row_headers=[x[0] for x in cursor.description]
    rows = []
    for x in result:
        d = dict(zip(row_headers, x))
        rows.append(d)
    
    return helper.to_json(rows)

# --------------------------------------------------------
# Wrapper functions for foreign authors service
# --------------------------------------------------------

def add_author(name, surname):
    endpoint = 'http://library_service:80/api/Authors'
    try:
        request_result = requests.post(endpoint, json = {'name': name, 'surname': surname})
        if request_result.status_code == 201:
            return request_result.json()['id']
        else:
            return None
    except ConnectionError:
        return None

def get_author(author_id):
    endpoint = 'http://library_service:80/api/Authors/' + str(author_id)
    try:
        request_result = requests.get(endpoint)
        if request_result.status_code == 200:
            return request_result.json()
        else:
            return None
    except ConnectionError:
        return None

def update_author(author_id, name, surname):
    if author_id == None:
        return None
    
    endpoint = 'http://library_service:80/api/Authors/' + str(author_id)
    try:
        request_result = requests.put(endpoint, json = {'name': name, 'surname': surname})
        if request_result.status_code == 200:
            return request_result.json()
        else:
            return None
    except ConnectionError:
        return None

def delete_author(author_id):
    endpoint = 'http://library_service:80/api/Authors/' + str(author_id)
    try:
        requests.delete(endpoint)
        return 0
    except ConnectionError:
        return -1
    except Exception as e:
        return 0
