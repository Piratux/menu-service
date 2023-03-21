import requests
from requests.exceptions import ConnectionError
import json

endpoint = 'http://127.0.0.1:5000/'

commands = {
    "get_dishes": {
        "com_description": "Get all dishes",
        "arg_description": "",
    },
    "delete_dishes": {
        "com_description": "Delete all dishes",
        "arg_description": "",
    },
    "get_dish": {
        "com_description": "Get dish",
        "arg_description": "[dish_id]",
    },
    "add_dish": {
        "com_description": "Add dish",
        "arg_description": "[price, name, image_link, cooking_time]",
    },
    "update_dish": {
        "com_description": "Update dish",
        "arg_description": "[id, price, name, image_link, cooking_time]",
    },
    "delete_dish": {
        "com_description": "Delete dish",
        "arg_description": "[id]",
    },
    "dish_ingredients": {
        "com_description": "Get dish ingredients",
        "arg_description": "[id]",
    },
    "add_ingredient": {
        "com_description": "Add dish ingredient",
        "arg_description": "[id, name]",
    },
    "delete_ingredients": {
        "com_description": "Delete dish ingredients",
        "arg_description": "[id]",
    },
    "exit": {
        "com_description": "Exit app",
        "arg_description": "",
    }
}

def print_all_commands():
    longest_com_desc = 0
    longest_com_name = 0
    for command in commands:
        longest_com_desc = max([longest_com_desc, len(commands[command]["com_description"])])
        longest_com_name = max([longest_com_name, len(command)])
    
    print(
        "INFO".ljust(longest_com_desc+3, ' ') +
        "COMMANDS".ljust(longest_com_name+2, ' ') +
        "PARAMETERS"
    )
    for command in commands:
        print(
            (commands[command]["com_description"] + ":").ljust(longest_com_desc+3, ' ') +
            command.ljust(longest_com_name+2, ' ') +
            commands[command]["arg_description"]
        )

def get(string):
    return requests.get(endpoint + string)

def post(string, obj):
    return requests.post(endpoint + string, json=obj)

def put(string, obj):
    return requests.put(endpoint + string, json=obj)

def patch(string, obj):
    return requests.patch(endpoint + string, json=obj)

def delete(string):
    return requests.delete(endpoint + string)

def prettified_json(json_str):
    if type(json_str) == str:
        return json.dumps(json.loads(json_str), indent=4)
    elif type(json_str) == dict:
        return json.dumps(json_str, indent=4)
    else:
        return "prettified_json error: argument can't be turned to prettified json"

def print_response(response):
    print("http status code: " + str(response.status_code))
    if response.status_code != 204:
        print(prettified_json(response.json()))
    else:
        print(response.text)

while True:
    try:
        print("\n\n")
        print_all_commands()
        print("\n")
        command = input("Please enter your command: ")
        
        if False:
            print("")
            # empty
        
        elif command == "get_dishes":
            print_response(get("dishes"))
        
        elif command == "delete_dishes":
            print_response(delete("dishes"))
        
        elif command == "get_dish":
            dish_id = input("Enter dish id: ")
            print_response(get("dishes/" + str(dish_id)))
        
        elif command == "add_dish":
            price = input("Enter dish price: ")
            name = input("Enter dish name: ")
            image_link = input("Enter image link: ")
            cooking_time = input("Enter cooking time: ")
            ingredients = input("Enter ingredient names seperated by ',': ").split(",")
            ingredients = [s.strip() for s in ingredients if s != ""]
            print_response(post("dishes", {"price": price, "name": name, "image_link": image_link, "cooking_time": cooking_time, "ingredients": ingredients}))
        
        elif command == "update_dish":
            dish_id = input("Enter dish id: ")
            price = input("Enter dish price: ")
            name = input("Enter dish name: ")
            image_link = input("Enter image link: ")
            cooking_time = input("Enter cooking time: ")
            print_response(patch("dishes/" + str(dish_id), {"price": price, "name": name, "image_link": image_link, "cooking_time": cooking_time}))
        
        elif command == "delete_dish":
            dish_id = input("Enter dish id: ")
            print_response(delete("dishes/" + str(dish_id)))
        
        elif command == "dish_ingredients":
            dish_id = input("Enter dish id: ")
            print_response(get("dishes/" + str(dish_id) + "/ingredients"))
        
        elif command == "add_ingredient":
            dish_id = input("Enter dish id: ")
            name = input("Enter ingredient name: ")
            print_response(post("dishes/" + str(dish_id) + "/ingredients", {"name": name}))
        
        elif command == "delete_ingredients":
            dish_id = input("Enter dish id: ")
            print_response(delete("dishes/" + str(dish_id) + "/ingredients"))
        
        elif command == "exit":
            break;
        
        else:
            print("Invalid command");
    
    except ConnectionError:
        print("Can't connect to server")