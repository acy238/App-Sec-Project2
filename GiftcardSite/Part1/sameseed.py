import random
import base64
from binascii import hexlify

length = 16

RANDOM_SEED = base64.b64decode("2RUHYAyJWdDdXOicZfnTRw==")

random.seed(RANDOM_SEED)
print(hexlify(random.randint(0, 2**length-1).to_bytes(length, byteorder='big')))
print(random.randint(0, 2**length-1))

# salt (in bytes) from above w/ hexlify = b'000000000000000000000000000078d2'
# salt (in base 10 form) is = 30930
# Therefore, we know that the password is encrypted with sha256 and the SAME salt for every registered user because of the variable: RANDOM_SEED

# This greatly reduces the number of possibilities (search space) for the adversary because:
# The adversary can append '000000000000000000000000000078d2' to the beginning of each word in the dictionary/wordlist and brute force from there.
# Please refer to "bugs.txt" for the complete overview with details on test case 4.
