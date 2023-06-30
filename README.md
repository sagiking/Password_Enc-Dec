# Password_Enc-Dec
Simple Python Tool to encrypt/decrypt a file with a given password

With this tool you can encrypt important files with a password of your choice!
The script use AES-CBC (Cipher Block Chaining), in CBC Method each plaintext block gets XOR-ed with the previous ciphertext block prior to encryption.
In addition there is a use of initialization vector to make sure each encryption has a different ciphertext result.



Options:

  -h, --help,             show help message and exit
  
  -m  --mode,             Would you like to Encrypt or Decrypt?
  
  -f  --file,             Insert the full file path (Make Sure the path is correct)
  
  -p  --password,         Insert the password       
  
  -P  --password_file,    Insert the path where the password stored     
  
  -d, --delete,           Deleting the Original File
  
  -s, --shadow,           Deleting the Shadow Copies, only worked in Administrator mode
  


  There are two files in this repository, one is the original python script and the other is a 
  compiled version with pyinstaller.
