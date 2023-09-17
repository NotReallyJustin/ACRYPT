from cryptography.fernet import Fernet

def generateKey():
  key = Fernet.generate_key()
  return key

def encryption(api_key: str, key:str):
  key = Fernet(key)
  enc_message = key.encrypt(api_key.encode())
  return enc_message

def decryption(enc_key: str, key:str):
  key = Fernet(key)
  decMessage = key.decrypt(enc_key).decode()
  return decMessage

if __name__ == '__main__':
  pass