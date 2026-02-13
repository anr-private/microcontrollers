# simple_async_server.py
#
###ANR import uasyncio as asyncio
# You may need to import network specific libraries (like 'network' for Wi-Fi)
# and use them to get the board connected and obtain its IP address.

import asyncio
import machine
import network
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


async def handle_client(reader, writer):
    """
    Coroutine to handle a single client connection.
    Takes StreamReader and StreamWriter instances as arguments.
    """
    print('New client connected...')
    try:
        while True:
            # Read line by line from the client
            line = await reader.readline()
            if not line:
                break  # Client disconnected
            
            message = line.decode('utf8').strip()
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
    server = await asyncio.start_server(handle_client, host, port)
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
        