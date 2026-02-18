# read_a_file.py
#
# Example: Reading a file
#
# All of these work:
#  assumes the files exist:
#    /wsp_log.txt
#    /lib/utils.py
#file_path = "/lib/utils.py"
file_path = "lib/utils.py"
#file_path = "wsp_log.txt"

try:
    # Open the file in read mode ('r' is the default)
    with open(file_path, 'r') as file:
        # Read the entire content of the file
        content = file.read()
        print("File content:")
        print(content)

except OSError as e:
    print(f"Error reading file: {e}")
    print("Please ensure the 'data_folder' exists and 'config.txt' is inside it.")


###
