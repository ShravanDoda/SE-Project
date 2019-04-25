from spotify_interface import process_metadata



# Fetch the metadata of the current song being played



print("Type help for information about available commands.")
print("Type exit to exit.")
while True:
    command = input(">>")
    if command == "exit":
        break
    elif command == "help":
        help.help()
    elif command == "update":
        print(mechanism)
