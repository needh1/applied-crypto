# sha256_demo.py
import hashlib

def sha256_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    return sha256.hexdigest()

if __name__ == "__main__":
    input_data = input("Enter a message to hash: ")
    print("SHA-256 Hash:", sha256_hash(input_data))
