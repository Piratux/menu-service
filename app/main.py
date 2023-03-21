import mysql.connector
import cherrypy

import createDB
import functionsDB
import helper

class WebService(object):
    def __init__(self, _db):
        self.db = _db

    @cherrypy.tools.json_out()
    def get_dishes(self):
        cherrypy.response.status = 200
        return functionsDB.get_dishes(self.db)
    
    @cherrypy.tools.json_out()
    def delete_dishes(self):
        cherrypy.response.status = 204
        functionsDB.delete_dishes(self.db)
        if cherrypy.response.status != 204:
            return result
    
    @cherrypy.tools.json_out()
    def get_dish(self, dish_id):
        cherrypy.response.status = 200
        return functionsDB.get_dish(self.db, dish_id)
    
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def add_dish(self):
        cherrypy.response.status = 200
        query = cherrypy.request.json
        if not all(k in query for k in ("price", "name", "image_link", "cooking_time", "ingredients")):
            return helper.error_query("payload must contain arguments: 'price', 'name', 'image_link', 'cooking_time', 'ingredients'")
        
        return functionsDB.add_dish(self.db, query["price"], query["name"], query["image_link"], query["cooking_time"], query["ingredients"])
    
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def update_dish(self, dish_id):
        cherrypy.response.status = 200
        query = cherrypy.request.json
        if not all(k in query for k in ("price", "name", "image_link", "cooking_time")):
            return helper.error_query("payload must contain arguments: 'price', 'name', 'image_link', 'cooking_time'")
        
        return functionsDB.update_dish(self.db, dish_id, query["price"], query["name"], query["image_link"], query["cooking_time"])
    
    @cherrypy.tools.json_out()
    def delete_dish(self, dish_id):
        cherrypy.response.status = 204
        result = functionsDB.delete_dish(self.db, dish_id)
        if cherrypy.response.status != 204:
            return result
    
    @cherrypy.tools.json_out()
    def get_dish_ingredients(self, dish_id):
        cherrypy.response.status = 200
        return functionsDB.get_dish_ingredients(self.db, dish_id)
    
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def add_dish_ingredient(self, dish_id):
        cherrypy.response.status = 200
        query = cherrypy.request.json
        if not all(k in query for k in ("name", )):
            return helper.error_query("payload must contain arguments: 'name'")
        
        return functionsDB.add_dish_ingredient(self.db, dish_id, query["name"])
    
    @cherrypy.tools.json_out()
    def delete_dish_ingredients(self, dish_id):
        cherrypy.response.status = 204
        result = functionsDB.delete_dish_ingredients(self.db, dish_id)
        if cherrypy.response.status != 204:
            return result

@cherrypy.tools.json_out()
def jsonify_error(status, message, traceback, version):
    return helper.error_query(message, status)

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
            action='get_dishes',
            controller=WebService(db),
            conditions={'method': ['GET']}
        )
        
        dispatcher.connect(
            name='dishes',
            route='/dishes',
            action='delete_dishes',
            controller=WebService(db),
            conditions={'method': ['DELETE']}
        )
        
        dispatcher.connect(
            name='dishes',
            route='/dishes/{dish_id}',
            action='get_dish',
            controller=WebService(db),
            conditions={'method': ['GET']}
        )
        
        dispatcher.connect(
            name='dishes',
            route='/dishes',
            action='add_dish',
            controller=WebService(db),
            conditions={'method': ['POST']}
        )
        
        dispatcher.connect(
            name='dishes',
            route='/dishes/{dish_id}',
            action='update_dish',
            controller=WebService(db),
            conditions={'method': ['PATCH']}
        )
        
        dispatcher.connect(
            name='dishes',
            route='/dishes/{dish_id}',
            action='delete_dish',
            controller=WebService(db),
            conditions={'method': ['DELETE']}
        )
        
        dispatcher.connect(
            name='dishes',
            route='/dishes/{dish_id}/ingredients',
            action='get_dish_ingredients',
            controller=WebService(db),
            conditions={'method': ['GET']}
        )
        
        dispatcher.connect(
            name='dishes',
            route='/dishes/{dish_id}/ingredients',
            action='add_dish_ingredient',
            controller=WebService(db),
            conditions={'method': ['POST']}
        )
        
        dispatcher.connect(
            name='dishes',
            route='/dishes/{dish_id}/ingredients',
            action='delete_dish_ingredients',
            controller=WebService(db),
            conditions={'method': ['DELETE']}
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
    