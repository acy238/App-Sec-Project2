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
# Additionally, we know that from test file 3, that the hashed password is: 18821d89de11ab18488fdc0a01f1ddf4d290e198b0f80cd4974fc031dc2615a3

# If the hashed password from above is saved to a file called: toBrute.txt
# Then, from the commandline, attackers can run: ./john --format=Raw-SHA256 --salts=30930 toBrute.txt
