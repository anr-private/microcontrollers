import asyncio

# Callback function to handle each new connection
async def handle_client(reader, writer):
    print("New client connected")
    try:
        # Read data from the client
        data = await reader.readline()
        message = data.decode().strip()
        print(f"Received: {message}")

        # Send an echo response back
        response = f"Echo: {message}\n"
        writer.write(response.encode())
        await writer.drain()  # Ensure data is sent
    finally:
        # Close the connection
        print("Closing connection")
        writer.close()
        await writer.wait_closed()

async def main():
    # Start the server on all available interfaces ("0.0.0.0")
    # and listen on port 8080
    print("Starting server on port 8080...")
    server = await asyncio.start_server(handle_client, "0.0.0.0", 8080)
    
    # Use the server object as an asynchronous context manager 
    # or keep it running indefinitely
    async with server:
        await server.serve_forever()

# Run the main event loop
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server stopped")
