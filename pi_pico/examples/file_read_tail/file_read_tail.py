import os

def read_last_n_lines(filename, n):
    """Reads the last N lines of a text file efficiently in MicroPython."""
    try:
        with open(filename, 'rb') as f: # Open in binary mode for reliable seeking
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            position = file_size
            lines_found = 0
            lines = []
            fbytes = b""

            while position > 0 and lines_found <= n:
                # Read a chunk from near the end
                chunk_size = 128 # Read in small chunks to save memory
                position = max(0, position - chunk_size)
                f.seek(position)
                chunk = f.read(file_size - position if position == 0 else chunk_size)
                file_size = position # Update file_size for next iteration if needed
                fbytes = chunk + fbytes # Prepend the new chunk to the fbytes
                
                # Count newlines in the fbytes
                while b'\n' in fbytes and lines_found <= n:
                    # Find the last newline
                    last_newline_index = fbytes.rfind(b'\n')
                    if last_newline_index == -1:
                        break
                    
                    line = fbytes[last_newline_index + 1:]
                    if line: # Avoid empty lines if file ends with newline
                        lines.insert(0, line.decode('utf-8')) # Decode and insert at beginning
                        lines_found += 1
                    fbytes = fbytes[:last_newline_index] # Keep the remaining fbytes for the next line

            # If loop finishes and there's still content in fbytes, it's the first line(s)
            if fbytes and lines_found <= n:
                 lines.insert(0, fbytes.decode('utf-8'))
                 lines_found += 1

            return lines[-n:] # Return only the last N lines
    except OSError:
        return []

# Example Usage:
# Create a dummy file for testing
fpath = "junk_test.txt"
with open(fpath, "w") as f:
    for i in range(1, 21):
        f.write(f"This is line {i}.\n")

# Read the last 5 lines
last_lines = read_last_n_lines(fpath, 5)

print("Last 5 lines:")
for line in last_lines:
    print(line.strip())

###

