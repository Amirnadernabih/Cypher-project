from flask import Flask, render_template, request

app = Flask(__name__)

# First Layer: Caesar Cipher
def caesar_cipher_encrypt(plaintext, shift):
    encrypted_text = ""
    for char in plaintext:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encrypted_text += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted_text += char
    return encrypted_text

# Second Layer: Monoalphabetic Cipher
def monoalphabetic_cipher_encrypt(plaintext, key):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key_map = dict(zip(alphabet, key))
    encrypted_text = ''
    for char in plaintext.upper():
        if char in alphabet:
            encrypted_text += key_map[char]
        else:
            encrypted_text += char
    return encrypted_text

# Third Layer: Rail Fence Cipher
def rail_fence_encrypt(plaintext, num_rails):
    rail = ['' for _ in range(num_rails)]
    direction_down = False
    row = 0

    for char in plaintext:
        rail[row] += char
        if row == 0 or row == num_rails - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1

    return ''.join(rail)

# Main function to run the multi-layered encryption
def multi_layered_encryption(plaintext, shift, mono_key, num_rails):
    caesar_encrypted = caesar_cipher_encrypt(plaintext, shift)
    mono_encrypted = monoalphabetic_cipher_encrypt(caesar_encrypted, mono_key)
    final_encrypted = rail_fence_encrypt(mono_encrypted, num_rails)
    return final_encrypted

@app.route('/', methods=['GET', 'POST'])
def home():
    encrypted_text = ""
    if request.method == 'POST':
        plaintext = request.form['message']
        shift = 4  # Shift value for Caesar Cipher
        mono_key = 'QWERTYUIOPASDFGHJKLZXCVBNM'  # Key for Monoalphabetic Cipher
        num_rails = 3  # Number of rails for Rail Fence Cipher

        encrypted_text = multi_layered_encryption(plaintext, shift, mono_key, num_rails)

    return render_template('index.html', encrypted_text=encrypted_text)

if __name__ == "__main__":
    app.run(debug=True)
