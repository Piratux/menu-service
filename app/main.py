import mysql.connector
import cherrypy
import simplejson

import createDB
import functionsDB
import helper

class WebService(object):
    def __init__(self, _db):
        self.db = _db

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def dishes(self):
        method = cherrypy.request.method
        if method == 'GET':
            cherrypy.response.status = 200
            return functionsDB.get_dishes(self.db)
            
        elif method == 'POST':
            cherrypy.response.status = 201
            query = cherrypy.request.json
            if not all(k in query for k in ("price", "name", "image_link", "cooking_time")):
                return helper.error_query("payload must contain arguments: 'price', 'name', 'image_link', 'cooking_time'")
            
            result = functionsDB.add_dish(self.db, query["price"], query["name"], query["image_link"], query["cooking_time"])
            if cherrypy.response.status == 201:
                dish_id = result["id"]
                cherrypy.response.headers['Content-Location'] = "/dishes/" + str(dish_id)
            
            return result
            
        elif method == 'DELETE':
            cherrypy.response.status = 204
            functionsDB.delete_dishes(self.db)
            if cherrypy.response.status != 204:
                return result
            
        else:
            return helper.error_query("method not allowed", 405)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def dishes_id(self, dish_id):
        method = cherrypy.request.method
        if method == 'GET':
            cherrypy.response.status = 200
            return functionsDB.get_dish(self.db, dish_id)
            
        elif method == 'PUT':
            cherrypy.response.status = 200
            query = cherrypy.request.json
            if not all(k in query for k in ("price", "name", "image_link", "cooking_time")):
                return helper.error_query("payload must contain arguments: 'price', 'name', 'image_link', 'cooking_time'")
            
            return functionsDB.update_dish(self.db, dish_id, query["price"], query["name"], query["image_link"], query["cooking_time"])
            
        elif method == 'DELETE':
            cherrypy.response.status = 204
            result = functionsDB.delete_dish(self.db, dish_id)
            if cherrypy.response.status != 204:
                return result
            
        else:
            return helper.error_query("method not allowed", 405)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def dishes_id_ingredients(self, dish_id):
        method = cherrypy.request.method
        if method == 'GET':
            cherrypy.response.status = 200
            return functionsDB.get_dish_ingredients(self.db, dish_id)
            
        elif method == 'POST':
            cherrypy.response.status = 201
            query = cherrypy.request.json
            if not all(k in query for k in ("name", "amount")):
                return helper.error_query("payload must contain arguments: 'name', 'amount'")
            
            result = functionsDB.add_dish_ingredient(self.db, dish_id, query["name"], query["amount"])
            if cherrypy.response.status == 201:
                ingredient_id = result["id"]
                cherrypy.response.headers['Content-Location'] = "/dishes/" + str(dish_id) + "/ingredients/" + str(ingredient_id)
            
            return result
            
        else:
            return helper.error_query("method not allowed", 405)
    
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def dishes_id_ingredients_id(self, dish_id, ingredient_id):
        method = cherrypy.request.method
        if method == 'GET':
            cherrypy.response.status = 200
            return functionsDB.get_dish_ingredient(self.db, dish_id, ingredient_id)
            
        elif method == 'PUT':
            cherrypy.response.status = 200
            query = cherrypy.request.json
            if not all(k in query for k in ("name", "amount")):
                return helper.error_query("payload must contain arguments: 'name', 'amount'")
            
            return functionsDB.update_dish_ingredient(self.db, dish_id, ingredient_id, query["name"], query["amount"])
            
        elif method == 'DELETE':
            cherrypy.response.status = 204
            result = functionsDB.delete_dish_ingredient(self.db, dish_id, ingredient_id)
            if cherrypy.response.status != 204:
                return result
            
        else:
            return helper.error_query("method not allowed", 405)
        
            @cherrypy.tools.json_out()
    
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def ingredients(self):
        method = cherrypy.request.method
        if method == 'GET':
            cherrypy.response.status = 200
            return functionsDB.get_ingredients(self.db)
            
        else:
            return helper.error_query("method not allowed", 405)
    
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def ingredients_id(self, ingredient_id):
        method = cherrypy.request.method
        if method == 'GET':
            cherrypy.response.status = 200
            return functionsDB.get_dish_ingredient(self.db, -1, ingredient_id, True)
            
        elif method == 'PUT':
            cherrypy.response.status = 200
            query = cherrypy.request.json
            if not all(k in query for k in ("name", "amount")):
                return helper.error_query("payload must contain arguments: 'name', 'amount'")
            
            return functionsDB.update_dish_ingredient(self.db, -1, ingredient_id, query["name"], query["amount"], True)
            
        elif method == 'DELETE':
            cherrypy.response.status = 204
            result = functionsDB.delete_dish_ingredient(self.db, -1, ingredient_id, True)
            if cherrypy.response.status != 204:
                return result
            
        else:
            return helper.error_query("method not allowed", 405)
    
    
def jsonify_error(status, message, traceback, version):
    return simplejson.dumps(helper.error_query(message, status))

if __name__ == '__main__':
    try:
        db = mysql.connector.connect(host = 'menu_db', user = 'root', password = 'root', port = 3306)
        createDB.create_database(db)
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})
        cherrypy.config.update({'server.socket_port': 5000})
        
        dispatcher = cherrypy.dispatch.RoutesDispatcher()
        
        dispatcher.connect(
            name='dishes',
            route='/dishes',
            action='dishes',
            controller=WebService(db)
        )
        
        dispatcher.connect(
            name='dishes',
            route='/dishes/{dish_id}',
            action='dishes_id',
            controller=WebService(db)
        )
        
        dispatcher.connect(
            name='dishes',
            route='/dishes/{dish_id}/ingredients',
            action='dishes_id_ingredients',
            controller=WebService(db)
        )
        
        dispatcher.connect(
            name='dishes',
            route='/dishes/{dish_id}/ingredients/{ingredient_id}',
            action='dishes_id_ingredients_id',
            controller=WebService(db)
        )
        
        dispatcher.connect(
            name='ingredients',
            route='/ingredients',
            action='ingredients',
            controller=WebService(db)
        )
        
        dispatcher.connect(
            name='ingredients',
            route='/ingredients/{ingredient_id}',
            action='ingredients_id',
            controller=WebService(db)
        )
        
        conf = {
            '/': {
                'request.dispatch': dispatcher,
                'error_page.default': jsonify_error,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
            }
        }
        
        cherrypy.tree.mount(root=None, config=conf)
        
        cherrypy.engine.start()
        cherrypy.engine.block()

    except Exception as e:
        print(e)
    
