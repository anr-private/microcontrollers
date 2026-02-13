# simple_async_server.py
#
###ANR import uasyncio as asyncio
# You may need to import network specific libraries (like 'network' for Wi-Fi)
# and use them to get the board connected and obtain its IP address.

import asyncio
import machine
import network
import sys
import urequests
import utime

from details import SSID, PW

ssid = SSID
password = PW
    
VERBOSE = True
VV = VERBOSE    

def dbg(stg=None):
    """ output a string to the debug output """
    if not VERBOSE: return
    if stg is None: stg = ""
    print(f"DBG:{stg}")


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

async def handle_client_as_bytes(reader, writer):
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

async def handle_client_all_bytes(reader, writer):
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
            
if __name__ == '__main__':

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


### end ###
        