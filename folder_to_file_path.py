import os

def get_files_with_extension(folder_path, file_extension):
    # Ensure the file extension starts with a dot
    if not file_extension.startswith('.'):
        file_extension = '.' + file_extension

    # List to store the paths of matching files
    matching_files = []

    # Walk through the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(file_extension.lower()):
                matching_files.append(os.path.join(root, file))
    
    return matching_files

# Example usage:
# folder_path = 'ex'
# file_extension = 'mp4'
# files = get_files_with_extension(folder_path, file_extension)
# for file in files:
#     print(file)
