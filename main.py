import json
from charm.toolbox.pairinggroup import PairingGroup, GT
from ABE.ac17 import AC17CPABE
from file_abe import file_to_group_element, group_element_to_file

def main():
    # Load configuration
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Extract configuration
    input_file_path = config['input_file_path']
    output_encrypted_file_path = config['output_encrypted_file_path']
    output_decrypted_file_path = config['output_decrypted_file_path']
    attributes = config['attributes']
    policy_str = config['policy']

    # Instantiate a bilinear pairing map
    pairing_group = PairingGroup('MNT224')

    # AC17 CP-ABE under DLIN (2-linear)
    cpabe = AC17CPABE(pairing_group, 2)

    # Run the set up
    (pk, msk) = cpabe.setup()

    # Generate a key
    key = cpabe.keygen(pk, msk, attributes)

    # Convert the file contents to a group element
    file_element = file_to_group_element(pairing_group, input_file_path)

    # Generate a ciphertext
    ctxt = cpabe.encrypt(pk, file_element, policy_str)

    # Decrypt the file contents
    rec_element = cpabe.decrypt(pk, ctxt, key)

    # Verification and output
    if rec_element == file_element:
        print("Successful decryption.")
        group_element_to_file(rec_element, output_decrypted_file_path)
    else:
        print("Decryption failed.")

if __name__ == "__main__":
    main()
