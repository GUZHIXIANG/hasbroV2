from rest_framework.response import Response

class AjaxResponse(object):
    def __init__(self):

        self.error = ""
        self.data = ""
        self.message = ""

    def successMessage(self, data=None, message="success",status=None):
        self.message = message
        if data == None:
            data = ""
        jsondata = {
                    "message":self.message,
                    "status":status,
                    "data":data}
        response = Response(jsondata)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response

    def errorMessage(self, data=None, message="false",status=None, error=""):
        self.error = error
        self.message = message
        if data == None:
            data = ""
        jsondata = {
                    "message":self.message,
                    "status":status,
                    "error":str(self.error),
                    "data":data}
        response = Response(jsondata)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        
        return response
