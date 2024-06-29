import os

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        try:
            os.makedirs(folder_name)
            print(f"Folder '{folder_name}' created successfully.")
        except OSError as e:
            print(f"Error creating folder '{folder_name}': {e}")
    else:
        print(f"Folder '{folder_name}' already exists.")

# if __name__ == "__main__":
#     folder_name = input("Enter the folder name: ")
#     create_folder(folder_name)
