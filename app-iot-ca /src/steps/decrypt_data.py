import hashlib
from bson import json_util
import json
# from Crypto.Cipher import AES
# import base64

secret_key = '65592739GTH87694KTY63B3238GD987F'

def _decrypt_data(objet) -> dict:
  encode = hashlib.sha256(objet)
  encode.hexdigest()
  #encode.update(objet, secuty_key)
  encode.digest()

  # cipher = AES.new(secret_key,AES.MODE_ECB) 
  # #encoded = base64.b85encode(cipher.encrypt(objet))
  # decoded = cipher.decrypt(baes64.b85encode(objet))

  resposnse = json_util.dumps(encode)
  return json.loads(resposnse)

def encrypt_data() -> dict:
  return 0