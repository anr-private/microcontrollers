#Internal File System Use - Example #1
#write a line of text to a file and read it back

#Open, Write, Close a datafile
data_file = open("MyData.txt","w")                          #Creates/Opens a file called MyData.txt for writing
data_file.write("I put this data into the MyData.txt file") #Write data to the file
data_file.close()                                           #Tidy up by closing file
print("Wrote data to file\n\n")

#Open, Read, Close a datafile
data_file = open("MyData.txt","r")   #Opens a file called MyData.txt for reading
Text_Data = data_file.read()         #Read data from the file
print(Text_Data)                     #print out the file data
data_file.close()                    #Tidy up by closing file
print("\n\nAll Done")



