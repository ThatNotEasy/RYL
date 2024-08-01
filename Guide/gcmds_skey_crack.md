# Decrypting `.GCMDS` and `.SKEY` Files

## Overview

You have two types of encrypted files: `.GCMDS` and `.SKEY`. The encryption uses an XOR key, and you need to decrypt these files to determine their format or make use of their content.

## XOR Key

- **Key for Encryption:** `7A 7F 41 4C 4C 7F 61 7F 13 64`

## Decryption Process

To decrypt the files, use the provided XOR key. Below is a sample Python script to perform the decryption.

### Python Script for Decryption

```python
def xor_decrypt(data, key):
    key_length = len(key)
    return bytes([data[i] ^ key[i % key_length] for i in range(len(data))])

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()
    decrypted_data = xor_decrypt(data, key)
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

if __name__ == "__main__":
    xor_key = bytes([0x7A, 0x7F, 0x41, 0x4C, 0x4C, 0x7F, 0x61, 0x7F, 0x13, 0x64])
    
    # Replace 'input.gcmds' and 'input.skey' with your actual file names
    decrypt_file('input.gcmds', 'decrypted.gcmds', xor_key)
    decrypt_file('input.skey', 'decrypted.skey', xor_key)
```
# Instructions for Decrypting `.GCMDS` and `.SKEY` Files

## Instructions

1. **Save the Python Script:**
   - Save the provided Python script to a file (e.g., `decrypt.py`).

2. **Modify File Names:**
   - Replace `input.gcmds` and `input.skey` in the script with your actual file names.

3. **Run the Script:**
   - Execute the script to decrypt your files.

## Identifying the File Format

After decryption, you need to examine the contents of the `.gcmds` and `.skey` files to determine their format:

- **Magic Numbers:** Look for specific headers or magic numbers that might indicate the file format.
- **File Signature:** Compare the contents with known file formats or use file identification tools.

## Additional Steps

- **Search for Existing Tools:** Look for any tools or libraries that might support `.GCMDS` or `.SKEY` files.
- **Contact Developers:** Reach out to the software provider (e.g., Gamsoft) or relevant communities for more information or tools.

## Notes

- **Backup:** Ensure you have backups of your files before running the decryption script.
- **Assistance:** If you encounter issues or need further assistance, providing more context about the files may help in identifying the format or finding appropriate tools.
