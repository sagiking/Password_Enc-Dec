
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from hashlib import md5
import random
import argparse
import string
import os

CHUNK_SIZE = 16 * 1024


def main():
   
    parser = argparse.ArgumentParser(description='AES Password Encrypter / Decrypter Tool')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-m', '--mode', help = "Would you like to Encrypt or Decrypt?",
    action='store', type=str, required=True)
    parser.add_argument('-f', '--file', help = "Insert the full file path",
    action='store', type=str, required=True)
    group.add_argument('-p', '--password', help = "Insert the password",
    action='store', type=str)
    group.add_argument('-P', '--password_file', help = "Insert the path where the password stored",
    action='store', type=str)
    parser.add_argument('-d', '--delete', help = "Deleting the Original File", action='store_true')
    parser.add_argument('-s', '--shadow', help = "Deleting the Shadow Copies, only worked in Administrator mode", action='store_true')

    args = parser.parse_args()

    # Does the user chose to read the password from a file?
    if args.password_file:
        with open(fr'{args.password_file}', 'r') as file:
            password = file.read()
    else:
        password = args.password

    hash = md5(password.encode('utf-8')).hexdigest()
    key = bytes(str(hash), 'utf-8')
   
    # Did he choose to encrypt?
    if (args.mode).lower() == "encrypt":
        print('Starting to encrypt the data')
        encrypt_file(args.file, key, args.delete, args.shadow)
    
    # Did he choose to decrypt?
    elif (args.mode).lower() == "decrypt":
        print('Starting to decrypt the data')
        decrypt_file(args.file, key)
    
    # Invaild Method option
    else:
        raise Exception('WRONG Method Input!')


def shred(file_path, shadow_copy):
    file_size = os.path.getsize(file_path)

    with open(file_path, 'wb') as file:
        # Overwrite the file content with random data
        for _ in range(file_size):
            random_byte = random.choice(string.ascii_letters).encode()
            file.write(random_byte)
    
    os.remove(file_path)

    # If the user chose to delete shadow copies
    if shadow_copy:
        os.system('vssadmin delete shadows /for=c: /all /quiet > null')

    print('File Deleted Successfully')
    return


def encrypt_file(file_path, key, delete_file, shadow_copy):

    # Generate a random initialization vector (IV)
    iv = get_random_bytes(16)
    
    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Open input and output files
    with open(file_path, 'rb') as infile, open(file_path + '.enc', 'wb') as outfile:

        # Write the IV to the output file
        outfile.write(iv)

        # Encrypt the file chunk by chunk
        while True:
            chunk = infile.read(CHUNK_SIZE)
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                # If the chunk size is not a multiple of 16, pad it
                chunk = pad(chunk, 16)

            # Encrypt the chunk and write it to the output file
            encrypted_chunk = cipher.encrypt(chunk)
            outfile.write(encrypted_chunk)

    # If the user choose to delete the original file
    if delete_file:
        shred(file_path, shadow_copy)

    print("Encryption completed.")
    return


def decrypt_file(file_path, key):
    dec_file = os.path.splitext(file_path)

     # Open input and output files
    with open(file_path, 'rb') as infile, open(dec_file[0] + '.dec', 'wb') as outfile:

        # Read the IV from the input file
        iv = infile.read(16)

        # Create AES cipher object
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt the file chunk by chunk
        while True:
            chunk = infile.read(CHUNK_SIZE)
            if len(chunk) == 0:
                break
            
             # Decrypt the chunk unpad it and write it to the output file
            elif len(chunk) % 16 != 0:
                decrypted_chunk = cipher.decrypt(chunk)
                outfile.write(unpad(decrypted_chunk, 16))
                
            # Decrypt the chunk and write it to the output file
            decrypted_chunk = cipher.decrypt(chunk)
            outfile.write(decrypted_chunk)
           
           
    print("Decryption completed.")
    return


if __name__ == '__main__' :
    main()

