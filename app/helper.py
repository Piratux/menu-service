import simplejson
import cherrypy

def error_query(error_msg = '', error_status = 400):
    cherrypy.response.status = error_status
    return {"error": str(error_msg)}

def error_query_404():
    return error_query("resource does not exist", 404)

def to_json(result):
    return result
