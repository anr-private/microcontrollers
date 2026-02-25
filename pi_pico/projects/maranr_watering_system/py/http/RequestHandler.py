# RequestHandler.py

import asyncio

from utils import *
from lib.FileUtils import FileUtils
from http.HttpParser import HttpParser
from http.ReplyBuilder import ReplyBuilder

# Content-Type values
# application/x-www-form-urlencoded  - posting a FORM(?)
# application/json  - posting JSON data
# multipart/form-data; boundary=--------------------------833994107218074559113347

class RequestHandler:

    def __init__(self):
        self.default_file = "/pages/index.html"
        self.default_subdir = "pages"

    def handle_client_request(self, header):
        # header is str containing the header lines """
        # returns a reply, suitable for sending back to the client

        httpParser = HttpParser()

        parsed_http = httpParser.parse_header_data(header)

        if parsed_http is None:
            print(f"RH@30 REQUEST PARSE ERROR: {httpParser.latest_error()}")
            #@@@@@ handle an error
            
        m1 = f"RHS@23 CLIENT REQUEST {httpParser.latest_error()=}"
        m2 = f"RHS@24 {parsed_http.long_string()}"
        print(m1)
        print(m2)
        log(m1)
        log(m2)

        if parsed_http.method == "GET":
            reply = self._handle_get_request(parsed_http)
            if reply:
                print(f"RH@43 {str(reply)=}")
                return reply

        print(f"RH@46  @@@@@@@ RequestHandler @ 34 CANNOT HANDLE REQ {parsed_http=}")
        return None #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            

    def _handle_get_request(self, parsed_http):
        req_url = parsed_http.request_url

        if req_url == "/data":#@@@@@@@@@@@@@@@@@@
            pass
        else:
            reply = self._handle_file_request(parsed_http)
            if reply:
                return reply
        print(f"RH@59  @@@@@@@@ RequestHandler @ 56 SENDING 404 -- CANNOT HANDLE GET-REQ {parsed_http=}")
        rb = ReplyBuilder()
        reply = rb.build_reply_404(req_url)
        dbg(f"RH@62 REPLY WITH 404.  DONT KNOW HOW TO HANDLE THIS: {parsed_http}")
        return reply
            

    def _handle_file_request(self, parsed_http):
        """ """
        file_path = parsed_http.url_path

        if file_path is None or len(file_path) <= 0 or file_path == "/":
            log(f"RH@71 Default file requested") 
            file_path = self.default_file
        
        dbg(f"RH@74 {file_path=}")

        # See if file exists - maybe in /pages/ or etc
        # Don't worry about what type of file yet - do binary read.
        # Try the default_subdir as well.
        fu = FileUtils()
        if not fu.obtain_input_file(file_path, binary=True, prefix_dir=self.default_subdir, w="RH@80"):
            rb = ReplyBuilder()
            m = f"Requested item {file_path} not found (as a file)"
            reply = rb.build_reply_404(m)
            dbg(f"RH@84 REPLY WITH 404. '{m}' {file_path=}  len={show_len(reply)}")
            ###print(f"RH@85  @@@@@@@@@@@   ERROR - NO PAGE FILE FOUND {file_path=}  NOT HANDLED YET !!!!!!!!!!!!!")
            return reply


        # OK the file exists. What kind of file is it?
        content_type = self._guess_file_content_type(file_path)

        if not content_type:
            rb = ReplyBuilder()
            m = f"Requested item {file_path}: Cannot determine Content-Type"
            reply = rb.build_reply_404(m)
            dbg(f"RH@96 REPLY WITH 404. '{m}' {file_path=}  len={show_len(reply)}")
            return reply

        # handle the file depending on its Content-Type
        if content_type in ["text/html","text/css", "text/javascript" ]:
            reply = self._handle_textual_file_request(file_path, content_type)
        elif content_type in ["image/x-icon","image/png", "image/gif", "image/jpeg"]:
            reply = self._handle_binary_file_request(file_path, content_type)
        else:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to build a Reply."
            reply = rb.build_reply_404(m)
            dbg(f"RH@108 REPLY WITH 404.  {file_path=}  {content_type=}")
            dbg(f"RH@109 {m=}")
            ###print(f"RH@110  @@@@@@@@@@@   ERROR - NO PAGE FILE FOUND {file_path=}  NOT HANDLED YET !!!!!!!!!!!!!")
            return reply

        return reply


    def _handle_textual_file_request(self, file_path, content_type):

        #@@@@@@file_content = self.read_the_page_file(file_path)
        # Read the file
        fu = FileUtils()
        file_content = fu.obtain_input_file(file_path, read_contents=True, 
                prefix_dir=self.default_subdir, w="RH@122")

        if file_content is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            dbg(f"RH@128 REPLY WITH 404.  {file_path=}  len={show_len(reply)}")
            dbg(f"RH@129 {m=}")
            ###print(f"RH@130  @@@@@@@@@@@   ERROR - NO PAGE FILE FOUND {file_path=}  NOT HANDLED YET !!!!!!!!!!!!!")
            return reply

        dbg(f"RH@133  {file_path=} {content_type=}  len={show_len(file_content)}")
        
        # Build a reply that provides the file
        rb = ReplyBuilder()

        reply = rb.build_textual_file_reply(content_type, file_content)

        print(f"RH@140 RequestHandler._handle_file_request REPLY is ...")
        print(f"RH@141: {reply}")
        return reply


    def _handle_binary_file_request(self, file_path, content_type):

        #@@@@@@file_content = self.read_the_page_file(file_path)
        # Read the file
        fu = FileUtils()
        file_content = fu.obtain_input_file(file_path, 
                binary=True, read_contents=True, 
                prefix_dir=self.default_subdir, w="RH@152")

        if file_content is None:
            rb = ReplyBuilder()
            m = f"{file_path=} {content_type=} Failed to read the file."
            reply = rb.build_reply_404(m)
            dbg(f"RH@158 REPLY WITH 404.  {file_path=}  len={show_len(reply)}")
            dbg(f"RH@159 {m=}")
            ###print(f"RH@160  @@@@@@@@@@@   ERROR - NO PAGE FILE FOUND {file_path=}  NOT HANDLED YET !!!!!!!!!!!!!")
            return reply

        dbg(f"RH@163  {file_path=} {content_type=}  len={show_len(file_content)}")
        
        # Build a reply that provides the file
        rb = ReplyBuilder()

        reply = rb.build_textual_file_reply(content_type, file_content)

        print(f"RH@170 RequestHandler._handle_file_request REPLY is ...")
        print(f"RH@171: {reply}")
        return reply


    def OLD__read_the_page_file(self, file_path):
        if not file_path:
            file_path = "/"
        if file_path[0] != '/':
            file_path = "/" + file_path

        file_content = self.read_a_text_file(file_path)

        if file_content is None:
            dbg(f"RH@184 did not find file {file_path=}; adding the pages dir")
            sep = ""
            if file_path[0] != "/":
                # add / between /pages and filepath
                sep = "/"            
            new_file_path = "/" + self.default_subdir + sep + file_path
            file_path = new_file_path
            dbg(f"RH@191 2nd try filename: {file_path}")
            file_content = self.read_a_text_file(file_path)
        return file_content


    def OLD__read_a_text_file(self, file_path):
        dbg(f"RH@197  read_a_text_file  {file_path=}")

        try:
            # Open the file in read mode ('r' is the default)
            with open(file_path, 'r') as file:
                # Read the entire content of the file
                dbg(f"RH@203 Opened text file '{file_path}' ")
                content = file.read()
                dbg(f"RH@205  text-file='{file_path}' len={show_len(content)}")
                return content
    
        except OSError as ex:
            print(f"RH@209 Error reading text file '{file_path}'  exc={ex}")
        except Exception as ex:
            print(f"RH@211 Error reading text file '{file_path}'  exc={repr(ex)}  exc='{ex}'")
        return None


    def OLD__read_a_binary_file(self, file_path):
        dbg(f"RH@216  read_a_binary_file  {file_path=}")

        try:
            # Open the file in read mode ('r' is the default)
            with open(file_path, 'rb') as file:
                # Read the entire content of the file
                dbg(f"RH@222 Opened binary file '{file_path}' ")
                content = file.read()
                dbg(f"RH@224  binary-file='{file_path}' len={show_len(content)}")
                return content
    
        except OSError as ex:
            print(f"RH@228 Error reading binary file '{file_path}'  exc={ex}")
        except Exception as ex:
            print(f"RH@230 Error reading binary file '{file_path}'  exc={repr(ex)}  exc='{ex}'")
        return None



    def _guess_file_content_type(self, file_path):
        # parts is ".../filename", "html" etc
        parts = file_path.rsplit(".", 1)
        #dbg(f"RH@238 _guess_file_content_type {parts=} {file_path=} ")
        if len(parts) < 2:
            # no extension found
            return None
        ext = parts[1].lower()
        #dbg(f"RH@243 _guess_file_content_type {ext=} {file_path=} ")
        if ext in ["html", "htm"]:
            #@@@@ maybe use "text/html; charset=UTF-8"?
            t = "text/html"
        elif ext in ["js",]:
            t = "text/javascript"
        elif ext in ["css",]:
            t = "text/css"
        elif ext in ["ico",]:
            t = "image/x-icon"
        elif ext in ["png",]:
            t = "image/png"
        elif ext in ["jpeg", "jpg"]:
            t = "image/jpeg"
        elif ext in ["gif",]:
            t = "image/gif"
        else:
            log(r"RH@254 **ERROR** Unknow Content-Type for file '{file_path}'")
            t = None
        dbg(f"RH@256 _guess_file_content_type {ext=} {file_path=} guessed-type='{t}'")
        return t


###

