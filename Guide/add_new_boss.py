import subprocess
import binascii

# Step 1: Decrypt the monsterscript.gcf file using mcfcoder
def decrypt_gcf(input_file, output_file):
    subprocess.run(["mcfcoder", "-d", input_file, "-o", output_file])

# Step 2: Open the decrypted file and find the monster's name and ID
def find_monster_id(decrypted_file, monster_name, marker=b'\xDD\x6D'):
    with open(decrypted_file, 'rb') as file:
        content = file.read()
    
    # Convert monster name to binary
    monster_name_bytes = monster_name.encode('utf-8')
    
    # Find the marker and monster name
    marker_index = content.find(marker)
    monster_name_index = content.find(monster_name_bytes)
    
    if marker_index == -1 or monster_name_index == -1:
        raise ValueError("Marker or monster name not found in the file.")
    
    # Find the monster ID in front of the marker
    monster_id_index = marker_index - 4  # Assuming monster ID is 4 bytes before the marker
    monster_id_bytes = content[monster_id_index:marker_index]
    monster_id_hex = binascii.hexlify(monster_id_bytes).decode('utf-8')
    
    return monster_id_hex

# Step 3: Edit the monsterscript.txt file to insert the monster's information
def edit_monsterscript(txt_file, monster_id, monster_info):
    with open(txt_file, 'r') as file:
        lines = file.readlines()
    
    # Find the line with the monster ID
    for i, line in enumerate(lines):
        if line.startswith(monster_id):
            lines[i] = f"{monster_id} {monster_info}\n"
            break
    else:
        # If not found, append the new monster info
        lines.append(f"{monster_id} {monster_info}\n")
    
    with open(txt_file, 'w') as file:
        file.writelines(lines)

# Main function to execute the steps
def main():
    input_file = 'monsterscript.gcf'
    decrypted_file = 'monsterscript_decrypted.gcf'
    txt_file = 'monsterscript.txt'
    monster_name = 'sakan'
    monster_info = 'sakan x .. .....'  # Replace with the actual hydra information
    
    decrypt_gcf(input_file, decrypted_file)
    monster_id = find_monster_id(decrypted_file, monster_name)
    edit_monsterscript(txt_file, monster_id, monster_info)

if __name__ == "__main__":
    main()
