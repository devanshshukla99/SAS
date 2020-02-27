#Program to generate encryption keys

from numpy import *
import os

print("\n Enter the key file name " , end="")
key_name = input()

enc_key = random.randint(256, size=256)

enc_key = array(enc_key)

save(key_name , enc_key)

os.system("mv " + key_name + ".npy ./" + key_name)
os.system("sudo chmod 400 " + key_name)
