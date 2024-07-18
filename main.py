import json
import os
from charm.toolbox.pairinggroup import PairingGroup, GT
from ABE.ac17 import AC17CPABE
from file_abe import file_to_group_element, group_element_to_file

def main():
    try:
        # Load configuration
        if not os.path.isfile('config.json'):
            raise FileNotFoundError("The configuration file 'config.json' does not exist.")
        
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
        
        # Save the ciphertext to a file
        with open(output_encrypted_file_path, 'wb') as f:
            f.write(bytes(ctxt))
        
        # Decrypt the file contents
        rec_element = cpabe.decrypt(pk, ctxt, key)
        
        # Verification and output
        if rec_element == file_element:
            print("Successful decryption.")
            group_element_to_file(rec_element, output_decrypted_file_path)
        else:
            print("Decryption failed.")
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except IOError as e:
        print(f"I/O error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
