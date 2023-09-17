from cryptography.fernet import Fernet

def generateKey():
  key = Fernet.generate_key()
  return key.decode()

def encryption(api_key: str, key:str):
  key = Fernet(key)
  enc_message = key.encrypt(api_key.encode())
  return enc_message.decode()

def decryption(enc_key: str, key:str):
  key = Fernet(key)
  decMessage = key.decrypt(enc_key).decode()
  return decMessage

if __name__ == '__main__':
  # key = generateKey()
  # encrypt = encryption("Hello World!", key)
  # decrypt = decryption(encrypt, key)
  # print(decrypt)
  pass