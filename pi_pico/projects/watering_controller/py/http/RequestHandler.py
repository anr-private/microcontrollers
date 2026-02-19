# RequestHandler.py

import asyncio

from utils import *
from http.HttpParser import HttpParser
from http.ReplyBuilder import ReplyBuilder


class RequestHandler:

    def __init__(self):
        self.default_file = "/pages/index.html"
        # True if we are running under Py3/Linux vs Micropython/Pico
        self._py3sim = False

    def handle_client_request(self, header):
        # header is str containing the header lines """
        # returns a reply, suitable for sending back to the client

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
            reply = self.handle_get_request(parsed_http)
            if reply:
                print(f"RH@39  reply len={len(reply)}")
                return reply

        print(f"@@@@@@@@ RequestHandler @ 34 CANNOT HANDLE REQ {parsed_http=}")
        return None #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            

    def handle_get_request(self, parsed_http):
        req_url = parsed_http.request_url

        if req_url == "/data":#@@@@@@@@@@@@@@@@@@
            pass
        else:
            reply = self.handle_file_request(parsed_http)
            if reply:
                return reply
        print(f"@@@@@@@@ RequestHandler @ 56 SENDING 404 -- CANNOT HANDLE GET-REQ {parsed_http=}")
        rb = ReplyBuilder()
        reply = rb.build_reply_404()
        dbg(f"RH@58 REPLY WITH 404.  DONT KNOW HOW TO HANDLE THIS: {parsed_http}")
        return reply
            

    def OLD___handle_get_request(self, parsed_http): #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        req_url = parsed_http.request_url

        if req_url == "/data":#@@@@@@@@@@@@@@@@@@
            pass
        elif req_url == "/":
            reply = self.handle_file_request(parsed_http)
            if reply:
                return reply
        else:
            print(f"@@@@@@@@ RequestHandler @ 56 SENDING 404 -- CANNOT HANDLE GET-REQ {parsed_http=}")
        if file_content is None:
            rb = ReplyBuilder()
            reply = rb.build_reply_404()
            dbg(f"RH@73 REPLY WITH 404.  {file_path=}  len={show_len(reply)}")
            ###print(f"@@@@@@@@@@@ RH@65  ERROR - NO PAGE FILE FOUND {file_path=}  NOT HANDLED YET !!!!!!!!!!!!!")
            return reply
            

    def handle_file_request(self, parsed_http):
        """ """
        file_path = parsed_http.url_path

        if file_path is None or len(file_path) <= 0 or file_path == "/":
            log(f"RH@52 Default file requested") 
            file_path = self.default_file
        
        dbg(f"RH@58 {file_path=}")

        file_content = self.read_a_page_file(file_path)

        if file_content is None:
            rb = ReplyBuilder()
            reply = rb.build_reply_404()
            dbg(f"RH@73 REPLY WITH 404.  {file_path=}  len={show_len(reply)}")
            ###print(f"@@@@@@@@@@@ RH@65  ERROR - NO PAGE FILE FOUND {file_path=}  NOT HANDLED YET !!!!!!!!!!!!!")
            return reply

        # Build a reply that provides the file
        rb = ReplyBuilder()

        reply = rb.build_page_file_reply(file_content)

        print(f"RequestHandler.handle_file_request REPLY is ...")
        print(f"{reply}")

        return reply


    def read_a_page_file(self, file_path):
        dbg(f"RH@66  read_a_page_file  {file_path=}")

        if self._py3sim:
            print(f"@@@ RequestHandler.read_a_page_file  **** SIMULATING THIS PAGE FILE '{file_path}'")
            if file_path.startswith("/"):
                file_path = file_path[1:]
            print(f"@@@ RequestHandler.read_a_page_file  **** USING SIMULATED PAGE FILE '{file_path}'")

        try:
            # Open the file in read mode ('r' is the default)
            with open(file_path, 'r') as file:
                # Read the entire content of the file
                content = file.read()
                print(f"Page-file '{file_path}'  len={len(content)}")
                ###print(content)
                return content
    
        except OSError as ex:
            print(f"RH@78 Error reading page file '{file_path}'  exc={ex}")
        return None

###
