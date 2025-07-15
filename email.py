import re

def validate_email(email):
    # Pola regex untuk validasi email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    else:
        return False

# Contoh penggunaan
email = input("Masukkan alamat email: ")
if validate_email(email):
    print("✅ Email valid!")
else:
    print("❌ Email tidak valid!")