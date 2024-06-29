import os

def delete_file(file_path):
    try:
        # Check if the file exists
        if os.path.isfile(file_path):
            # Delete the file
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted successfully.")
        else:
            print(f"File '{file_path}' does not exist.")
    except Exception as e:
        print(f"Error deleting file '{file_path}': {e}")