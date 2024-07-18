import os
from charm.toolbox.pairinggroup import PairingGroup, GT

def file_to_group_element(group, file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    try:
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        hashed_file = group.hash(file_bytes, GT)
        return hashed_file
    except Exception as e:
        raise IOError(f"An error occurred while reading or hashing the file: {e}")

def group_element_to_file(group_element, output_path):
    try:
        file_bytes = bytes(group_element)
        with open(output_path, 'wb') as f:
            f.write(file_bytes)
    except Exception as e:
        raise IOError(f"An error occurred while writing the group element to the file: {e}")
