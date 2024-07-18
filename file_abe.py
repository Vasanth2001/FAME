from charm.toolbox.pairinggroup import PairingGroup, GT

def file_to_group_element(group, file_path):
    # Read the file content as bytes
    with open(file_path, 'rb') as f:
        file_bytes = f.read()
    # Hash the bytes to an element in the group GT
    hashed_file = group.hash(file_bytes, GT)
    return hashed_file

def group_element_to_file(group_element, output_path):
    # Convert the group element back to bytes
    file_bytes = bytes(group_element)
    # Write the bytes to a file
    with open(output_path, 'wb') as f:
        f.write(file_bytes)
