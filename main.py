import mysql.connector
import cherrypy
import pandas as pd

import createDB
import functionsDB
import helper

db = mysql.connector.connect(host = 'menu_db', user = 'root', password = 'root', port = 3306)

commands = {
    "add_dish": {
        "param_count": 2,
        "com_description": "Add dish to the menu",
        "arg_description": "[price, name]",
    },
    "delete_dish": {
        "param_count": 1,
        "com_description": "Delete dish from the menu",
        "arg_description": "[dish_id]",
    },
    "get_dishes": {
        "param_count": 0,
        "com_description": "Return all dishes",
        "arg_description": "",
    },
    "update_dish": {
        "param_count": 3,
        "com_description": "Update dish data using dish_id",
        "arg_description": "[dish_id, price, name]",
    },
    "help": {
        "param_count": 0,
        "com_description": "List all commands",
        "arg_description": "",
    }
}

def get_all_commands():
    # auto format commands
    longest_com_desc = 0
    longest_com_name = 0
    for command in commands:
        longest_com_desc = max([longest_com_desc, len(commands[command]["com_description"])])
        longest_com_name = max([longest_com_name, len(command)])
    
    rows = []
    
    for command in commands:
        desc = (commands[command]["com_description"] + ":").ljust(longest_com_desc+3, ' ') + command.ljust(longest_com_name+2, ' ') + commands[command]["arg_description"]
        rows.append(desc)
    
    return pd.DataFrame({"result": pd.Series(rows)}).to_json()

def parse_user_input(command: str, code: str, param_count: int):
    command = command.replace(code, '')
    params = command.split(",")

    if len(params) != param_count:
        # print("ERROR - Incorrect parameter count.")
        return False

    for i, str in enumerate(params):
        params[i] = str.strip()

        if params[i] == '':
            # print("ERROR - missing parameter.")
            return False

    return params

class MyWebService(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def process(self):
        query = cherrypy.request.json
        
        return self.process_query(query)
    
    def process_query(self, query):
        command = query['query']
        print('command: ' + command)
        
        if command.startswith("add_dish"):
            params = parse_user_input(command, "add_dish", commands["add_dish"]["param_count"])

            if params is False:
                return helper.error_query("bad parameters")

            return functionsDB.add_dish(db, params[0], params[1])
        
        elif command.startswith("delete_dish"):
            params = parse_user_input(command, "delete_dish", commands["delete_dish"]["param_count"])

            if params is False:
                return helper.error_query("bad parameters")

            return functionsDB.delete_dish(db, params[0])
        
        elif command == "get_dishes":
            return functionsDB.get_dishes(db)
        
        elif command.startswith("update_dish"):
            params = parse_user_input(command, "update_dish", commands["update_dish"]["param_count"])

            if params is False:
                return helper.error_query("bad parameters")

            return functionsDB.update_dish(db, params[0], params[1], params[2])
        
        elif command == "help":
            return get_all_commands()
        
        else:
            return helper.error_query("query command doesn't exist")

if __name__ == '__main__':
    createDB.create_database(db)
    
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 5000})
    cherrypy.quickstart(MyWebService())
    