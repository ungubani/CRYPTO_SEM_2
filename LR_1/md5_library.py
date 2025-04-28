import hashlib

def lib_md5(string: str):
    md5_hash = hashlib.new('md5')
    data = bytearray(string, 'utf-8')
    md5_hash.update(data)

    md5_hex = md5_hash.hexdigest()
    return md5_hex


if __name__ == "__main__":
    md5_hash = hashlib.new('md5')
    data = b"BILIBERDA INCOMPORATED"
    md5_hash.update(data)

    md5_hex = md5_hash.hexdigest()

    print(f"MD5-хеш (LIBRARY) строки '{data}': {md5_hex}")
