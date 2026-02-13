# simple_async_webserver.py
#
# From google search AI.
# Runs a simple web server using asyncio.
# Connect to it using a browser (firefox,...) and request
#  http://192.168.1.49:8080
# Fix the IP to be the IP of the Pico's wifi connection, which it
# prints when it connects.
# This server always sends back the same thing, regardless of the request.
# The response is the canned reply - see below.
# This is self-contained. But it uses a couple of things from anr libraries
# like dbg and make_mesg_stg_from_template (with some mods)

###ANR import uasyncio as asyncio
import asyncio
import machine
import network
import sys
import urequests
import utime

from details import SSID, PW

ssid = SSID
password = PW

SIMPLE_REPLY_PAGE_HDR = [
    "HTTP/1.1 200 OK",
    "Date: Wed, 23 Oct 2024 12:00:00 GMT",
    "Server: Apache/2.4.1 (Unix)",
    "Content-Type: text/html; charset=UTF-8",
    "Content-Length: {body_length}",
    "Connection: Closed",
    ""
    ]
SIMPLE_REPLY_PAGE_BODY = [
    "<!DOCTYPE html>",
    "<html>",
    "<head>",
    "    <title>Example Page</title>",
    "</head>",
    "<body>",
    "    <h1>Hello, World!</h1>",
    "    <p>This is a simple HTML page. {comment}</p>",
    "</body>",
    "</html>"
    ]

VERBOSE = True
VV = VERBOSE    

def dbg(stg=None):
    """ output a string to the debug output """
    if not VERBOSE: return
    if stg is None: stg = ""
    print(f"DBG:{stg}")

# from utils.py
def make_header_lines_from_template(template_mesg_lines, values={}):
    """ Create a list of header lines that contain an HTTP header using 
    a list of lines (ie strings, the template lines) as the input.
    The values arg is a dict of substition values.
    Each line of the template is processed like this:
        actual_line = template_line.format(**values)
    So the template lines can contain '{value-item-name}' items.
    """
    ###print(f"make_mesg_stg_from_template templet is {type(template_mesg_lines)}   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$444")
    ###for line in template_mesg_lines:
    ###    print(f"MAKE MESG STG $$$$$$$$$$$$$ LINE is {line}")
    hdr_lines = []
    for line in template_mesg_lines:
        # ** unpacks the dict into kw params
        line = line.format(**values)
        hdr_lines.append(line) 
    ##### add the end-of-line chars per HTTP spec
    ####stg = "\r\n".join(actual_lines)
    ##### add the terminator marker
    ####stg = stg + "\r\n\r\n"
    dbg(f"make_header_lines_from_template@79  num-hdr-lines={len(hdr_lines)}")
    return hdr_lines

def make_body_lines_from_template(body_template_lines, values={}):
    """ Makes body lines from template lines, filling in the 
    string format items with actual values. 
    Returns a list of body lines, ready to send to the browser.
    """
    body_lines = []
    for tline in body_template_lines:
        # ** unpacks the dict into kw params
        body_line = tline.format(**values)
        #dbg(f"ssssss@91 {body_line=}")
        body_lines.append(body_line)
    dbg(f"make_body_lines_from_template@93 num-body-lines={len(body_lines)}")
    return body_lines

def determine_expected_body_length(body_lines):
    """ given body lines ready to send to browser, but without end-of-line
    chars. Calculate the body length to include the chars in the body_lines
    PLUS the (not yet present) EOL chars.
    """
    total_length = 0
    for line in body_lines:
        # add 2 to account for the EOL chars
        total_length += len(line) + 2
        #print(f"@@@@ adding {len(line)+2}  {total_length=}")
    return total_length

def make_reply_lines(header_values, body_values):
    if header_values is None: header_values = {}
    if body_values is None: body_values = {}
    #####body_values = {"comment":"123456789."}
    body_lines = make_body_lines_from_template(SIMPLE_REPLY_PAGE_BODY, body_values)
    body_length = determine_expected_body_length(body_lines)
    print(f"@126  response num-body-lines={len(body_lines)}  {body_length=}")
    
    # the header should have a line for content length like this:
    #   "Content-Length: {body_length}",
    header_values["body_length"] = body_length
    header_lines = make_header_lines_from_template(SIMPLE_REPLY_PAGE_HDR, header_values)

    all_lines = header_lines + body_lines
    return all_lines

    ###mesg_bytes = make_message_bytes(header_lines, body_lines)

def make_message_bytes(raw_mesg_lines):
    """ raw_mesg_lines is a list of the lines of the message,
    including header lines, header separator line,
    and body lines. 
    These lines DO NOT HAVE and EOL char(s) on them (CR or LF)
    Adds the EOL chars per HTTP spec and then
    creates a byte-string from the lines, ready to send 
    out the socket.
    """

    dbg(f"make_message_bytes raw_mesg_lines.len={len(raw_mesg_lines)}")
    mesg_lines = []
    for raw_line in raw_mesg_lines:
        mesg_lines.append(raw_line + "\r\n")
    mesg_stg = "".join(mesg_lines)
    dbg(f"make_message_bytes {len(mesg_stg)=}")
    mesg_bytes = mesg_stg.encode("utf-8")
    dbg(f"make_message_bytes {len(mesg_bytes)=}")
    return mesg_bytes




def TEST_for_making_the_reply():
    header_values = {}
    header_values["body_length"] = 999

    if 0:
        header_lines = make_header_lines_from_template(SIMPLE_REPLY_PAGE_HDR, header_values)
        print(f"@@@152 header lines len={len(header_lines)}")
        if 1:
            for line in header_lines:
                print(f"  HDR {line}")

    body_values = {"comment":"12345comment6789."}

    if 0:
        body_lines = make_body_lines_from_template(SIMPLE_REPLY_PAGE_BODY, body_values)
        print(f"@@@160 body lines len={len(body_lines)}")
        if 1:
            for line in body_lines:
                print(f"  BODY {line}")

    lines = make_reply_lines(header_values, body_values)

    print(f"@@@175  all lines len = {len(lines)}")
    if 1:
        print("@@@177 all lines:")
        for line in lines:
            print(f"  LINE: {line}")

    mesg_bytes = make_message_bytes(lines)
    print(f"@@@182  mesg_bytes len = {len(mesg_bytes)}")
    


def OLD_TEST():
    body_lines = make_body_lines_from_template(SIMPLE_REPLY_PAGE_BODY, values)
    body_length = determine_expected_body_length(body_lines)
    print(f"@@@  {body_length=}")


def connect_to_wifi(show_details=True):
    """ Connect to the WIFI WLAN.
    Return a wlan obj if successful.
    Else raises exception
    """
    
    dbg(f"CONNECT_TO_WIFI  ++++++++++++++++++++++++++++++")
    
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    dbg(f"  Connect to wifi: ssid='{ssid}'")
    wlan.connect(ssid, password)

    max_wait = 30 # Timeout in seconds
    num_tries = 0
    while num_tries < max_wait:
        wlan_status = wlan.status()
        dbg(f"waiting...  wlan_status={wlan_status}")
        if wlan_status < 0 or wlan_status >= 3:
            break
        num_tries += 1
        print(f"Waiting for connection...   num_tries={num_tries}  max={max_wait}")
        utime.sleep(1)
    dbg(f"wlan.status() = {wlan.status()}")
    
    if wlan.status() != 3:
        wlan.disconnect() # ignored if not connected
        raise RuntimeError(f"Network connection failed. wlan.status={wlan_status}")

    if show_details:
        print(f"Connected to wlan {ssid}")
        info = wlan.ifconfig()
        ip_addr = info[0]
        print(f"  IP={ip_addr}")
        # typical output: INFO: ('192.168.1.49', '255.255.255.0', '192.168.1.1', '192.168.1.1')
        ###print(f"  INFO: {info}")
    
    return wlan, ip_addr


async def handle_client_by_lines(reader, writer):
    """
    Coroutine to handle a single client connection.
    Takes StreamReader and StreamWriter instances as arguments.
    """
    print('New client connected...')
    try:
        lno = 0
        lines = []
        while True:
            # Read line by line from the client
            print(f"handle_client_by_lines@82  ======  READ A LINE  =================================")
            new_bytes = await reader.readline()
            if not new_bytes:
                # Client disconnected
                print(f"handle_client_by_lines@86 GOT NO MORE BYTES, client disconnected")
                break
            lno += 1
            print(f"handle_client_by_lines@89 {lno=} got {len(new_bytes)} bytes. ")
            
            # print the last 2 bytes of each line
            s = ""
            if len(new_bytes) >= 2:
                s += f"  2nd-last-byte is {int(new_bytes[-2])} "
            if len(new_bytes) >=1:
                s += f"  last-byte is {int(new_bytes[-1])} "
            if s:
                print(f" {lno=} {s}")
                
            # last 2 bytes are 13 10  ie \r\n
            ###if len(new_bytes) == 2:
            ###    print()
            ###    print(f"handle_client_by_lines@103  2 bytes are {int(new_bytes[0])}  {int(new_bytes[1])} ")
            
            new_line = new_bytes.decode('utf8').strip()
            print(f'Received: {lno=}. {new_line}')

            ###if message.lower() == 'quit':
            ###    break
            lines.append(new_line)
            print(f"  there are now {len(lines)} lines received.")

            # are the last 2 bytes  13 10  ie \r\n
            if len(new_bytes) == 2:
                print()
                print(f"handle_client_by_lines@116  2 bytes are {int(new_bytes[0])}  {int(new_bytes[1])} ")
                if int(new_bytes[0]) == 13 and int(new_bytes[1]) == 10:
                    print(f"  THIS IS THE LAST LINE!!!!!!!!!!! STOP READING!!!!!!!!!")
                break
        if 1:
            header_values = {}
            body_values = {"comment":"this is the comment!."}

            lines = make_reply_lines(header_values, body_values)
        
            print(f"@@@285  all lines len = {len(lines)}")
            if 1:
                print("@@@287 all lines:")
                for line in lines:
                    print(f"  LINE: {line}")
        
            mesg_bytes = make_message_bytes(lines)
            print(f"@@@292  mesg_bytes len = {len(mesg_bytes)}")

            writer.write(mesg_bytes)
            await writer.drain() # Ensure the data is sent


        if 0:
            # Send the response back to the client
            body_values = {"comment":"123456789."}
            body_lines = make_body_lines_from_template(SIMPLE_REPLY_PAGE_BODY, body_values)
            body_length = determine_expected_body_length(body_lines)
            print(f"@212  response {body_length=}")
            header_values = {"body_length":body_length}
            header_lines = make_header_lines_from_template(SIMPLE_REPLY_PAGE_HDR, header_values)
            all_mesg_lines = header_lines + body_lines
           

            ###message = make_mesg_stg_from_template(SIMPLE_REPLY_PAGE)
            mesg_bytes = message.encode("utf-8")
            print(f"@168 SEND RESPONSE. len(mesg_bytes) = {len(mesg_bytes)}")
            writer.write(mesg_bytes)
            await writer.drain() 

        if 0:
            if lines[0][0:3] == "GET":
                print(f"  REPLACE GET with 200 OK")
                lines[0] = "HTTP/1.1 200 OK\r\n"
            message = "".join(lines)
            ###message += "\r\n\r\n"
            # Send the response back to the client
            mesg_bytes = message.encode("utf-8")
            print(f" Write the mesg.  len(mesg_bytes) = {len(mesg_bytes)}")
            ###writer.write(f'Echo: {message}\n'.encode('utf8'))
            writer.write(mesg_bytes)
            # add trailing blank line
            ####writer.write(f"\r\n".encode("utf-8"))  ### ANR
            await writer.drain() # Ensure the data is sent
            
    except Exception as e:
        print(f'Error with client: {e}')
    finally:
        print('Closing connection')
        writer.close()
        await writer.wait_closed() # Wait until the stream is fully closed


async def OLD__handle_client_as_bytes(reader, writer):
    """
    Coroutine to handle a single client connection.
    Takes StreamReader and StreamWriter instances as arguments.
    """
    print('New client connected...')
    try:
        all_bytes = bytearray(b"")
        while True:
            # Read line by line from the client
            new_bytes = await reader.readline()
            if not new_bytes:
                # Client disconnected
                print(f"handle_client_by_lines GOT NO MORE BYTES, client disconnected")
                break
            print(f"handle_client_by_lines@122  got {len(new_bytes)} bytes.  len(all)={len(all_bytes)}")
            
            all_bytes.extend(new_bytes)
            print(f"handle_client_by_lines@125  got {len(new_bytes)} bytes.  len(all)={len(all_bytes)}")
            ###message = line.decode('utf8').strip()
            ###print(f'Received: {message}')

            ###if message.lower() == 'quit':
            ###    break

            # Send the response back to the client
            ###writer.write(f'Echo: {message}\n'.encode('utf8'))
            ###await writer.drain() # Ensure the data is sent
            
    except Exception as e:
        print(f'Error with client: {e}')
    finally:
        print('Closing connection')
        writer.close()
        await writer.wait_closed() # Wait until the stream is fully closed

async def OLD__handle_client_all_bytes(reader, writer):
    """
    Coroutine to handle a single client connection.
    Takes StreamReader and StreamWriter instances as arguments.
    """
    print('New client connected...')
    try:
        while True:
            # this stalls until the client/browser is told to give up on the request (press X on browser gui)
            print(f"handle_client_all_bytes read everything!")
            got_bytes = await reader.read(-1)

            print(f"handle_client_all_bytes@112 got {None if got_bytes is None else len(got_bytes)} ")
            if got_bytes is None or len(got_bytes) <= 0:
                print(f"handle_client_all_bytes - got nothing!")
                break
            print(f" @@@@ 116")
            message = got_bytes.decode('utf8').strip()
            print(f'Received: decode.len={len(message)}')
            print(f'Received: {message}')

            if message.lower() == 'quit':
                break

            # Send the response back to the client
            writer.write(f'Echo: {message}\n'.encode('utf8'))
            await writer.drain() # Ensure the data is sent
            
    except Exception as e:
        print(f'Error with client: {e}')
    finally:
        print('Closing connection')
        writer.close()
        await writer.wait_closed() # Wait until the stream is fully closed

async def run_server(host, port):
    """
    Starts the asynchronous server.
    """
    # asyncio.start_server returns a Server object (or a generator in older MicroPython versions)
    ###callbk = handle_client_all_bytes
    callbk = handle_client_by_lines
    server = await asyncio.start_server(callbk, host, port)
    print(f'Listening on {host}:{port}...')
    print(f"Server obj is {type(server)}")
    print(f"server module {server.__module__}")
    print(f"  dir(server)")
    print(f"  {dir(server)}")
    if 0:
        # server.sockets does not exist
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')
    # Use 'async with' to manage the server's lifecycle automatically
    async with server:
        ###ANR not needed, the start_server's task already is running
        ###ANRawait server.serve_forever() # Run the server indefinitely
        while 1:
            print(f"run_server -- just waiting while server runs")
            await asyncio.sleep(10)
            
def main():
    wlan, ip_addr = connect_to_wifi()

    print(f"MAIN  CONNECTED TO WIFI.  {ip_addr=}  wlan={wlan}")

    # You will likely need to replace '0.0.0.0' with your device's actual IP address
    # after connecting it to a network.
    # '0.0.0.0' makes the server listen on all available network interfaces.
    ### ANR host = '0.0.0.0'
    host = ip_addr
    port = 8080

    try:
        # Start the event loop and run the main server coroutine
        asyncio.run(run_server(host, port))
    except KeyboardInterrupt:
        print('Server stopped by user KeyboardInterrupt.')
    finally:
        # Clean up the event loop (optional, but good practice)
        asyncio.new_event_loop()


if __name__ == '__main__':
    main()
    
    #TEST_for_making_the_reply()


    # v = {"bbb": "23"}
    # print(f"{v=}")
    # s = "THIS IS {bbb} BBB".format(**v)
    # print(f"{s=}")

### end ###
        