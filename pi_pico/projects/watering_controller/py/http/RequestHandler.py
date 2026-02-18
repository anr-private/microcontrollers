# RequestHandler.py

import asyncio

from utils import *
from http.HttpParser import HttpParser

class RequestHandler:

    def __init__(self):
        ...

    def handle_client_request(self, header):
        """ header is str containing the header lines """

        httpParser = HttpParser()

        parsed_http = httpParser.parse_header_data(header)

        if parsed_http is None:
            print(f"RH@20 REQUEST PARSE ERROR: {httpParser.latest_error()}")
            #@@@@@ handle an error
            
        m1 = f"RHS@23 CLIENT REQUEST {httpParser.latest_error()=}"
        m2 = f"RHS@24 {parsed_http.long_string()}"
        print(m1)
        print(m2)
        log(m1)
        log(m2)

        if parsed_http.method == "GET":
            self.handle_get_request(parsed_http)
        else:
            print(f"@@@@@@@@ RequestHandler @ 34 CANNOT HANDLE REQ {parsed_http=}")
        return None #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def handle_get_request(self, parsed_http):
        req_url = parsed_http.requested_url 

        if req_url == "/data":#@@@@@@@@@@@@@@@@@@
            pass
        elif req_url== "/":
            self.handle_file_request(None)

        else:
            print(f"@@@@@@@@ RequestHandler @ 40 CANNOT HANDLE GET-REQ {parsed_http=}")
            
    def handle_file_request(self, parsed_http, file_path):
        """ """
        if file_path is None or len(file_path) <= 0:
            log("RH@47 Default file requested") 
            file_path = "/index.html"  #@@@@@@
        



###
