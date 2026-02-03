from tkinter import *
from tkinter import ttk, messagebox
import base64
from tkinter import font as tkfont

# ==============================================
# KONFIGURASI WARNA
# ==============================================
BG_COLOR = "#f0f0f0"          # Warna latar belakang utama
PRIMARY_COLOR = "#4a6fa5"      # Warna primer (biru tua)
SECONDARY_COLOR = "#166088"    # Warna sekunder (biru sedang)
ACCENT_COLOR = "#4fc3f7"       # Warna aksen (biru muda)
ERROR_COLOR = "#ff5252"        # Warna untuk error (merah)
SUCCESS_COLOR = "#4caf50"      # Warna untuk sukses (hijau)

# ==============================================
# FUNGSI UTAMA
# ==============================================

def reset():
    """
    Fungsi untuk mereset/mengosongkan semua input:
    - Mengosongkan area pesan
    - Mengosongkan field password
    - Mengembalika n status ke 'Ready'
    """
    text1.delete("1.0", END)       # Hapus semua teks di text area
    code.set("")                   # Kosongkan password
    status_label.config(text="Ready", fg="black")  # Reset status

def validate_password():
    """
    Fungsi untuk validasi password:
    - Memeriksa apakah password sudah diisi
    - Memeriksa apakah password benar (default: '1234')
    - Mengembalikan True jika valid, False jika tidak
    """
    password = code.get()          # Ambil nilai password
    
    # Validasi 1: Password tidak boleh kosong
    if not password:
        messagebox.showerror("Error", "Harap masukkan password", parent=screen)
        return False
    
    # Validasi 2: Password harus '1234' (default)
    if password != "1234":
        messagebox.showerror("Error", "Password salah", parent=screen)
        return False
    
    return True  # Jika semua validasi terpenuhi

def encrypt():
    """
    Fungsi untuk enkripsi pesan menggunakan base64:
    1. Validasi password terlebih dahulu
    2. Memeriksa apakah ada pesan yang dimasukkan
    3. Mengenkripsi pesan menggunakan base64
    4. Menampilkan hasil dalam window baru
    5. Memberikan feedback ke user
    """
    # Langkah 1: Validasi password
    if not validate_password():
        return
        
    # Langkah 2: Ambil pesan dan pastikan tidak kosong
    message = text1.get("1.0", END).strip()
    if not message:
        messagebox.showwarning("Warning", "Harap masukkan pesan untuk dienkripsi", parent=screen)
        return
    
    try:
        # Langkah 3: Proses enkripsi
        encode_message = message.encode("ascii")       # Konversi ke bytes
        base64_bytes = base64.b64encode(encode_message) # Enkripsi base64
        encrypted = base64_bytes.decode("ascii")       # Konversi ke string
        
        # Langkah 4: Tampilkan hasil dalam window baru
        result_window = Toplevel(screen)
        result_window.title("Hasil Enkripsi")
        result_window.geometry("500x300")
        result_window.configure(bg=BG_COLOR)
        result_window.resizable(False, False)
        
        # Frame untuk hasil enkripsi
        frame = ttk.Frame(result_window, style="Card.TFrame")
        frame.pack(pady=20, padx=20, fill=BOTH, expand=True)
        
        # Label judul
        Label(frame, text="PESAN TERENKRIPSI", font=("Arial", 12, "bold"), 
              bg=BG_COLOR).pack(pady=(10, 5))
        
        # Text area untuk menampilkan hasil
        result_text = Text(frame, font=("Consolas", 10), wrap=WORD, 
                         height=8, padx=10, pady=10)
        result_text.pack(fill=BOTH, expand=True, padx=10, pady=5)
        result_text.insert(END, encrypted)  # Tampilkan hasil
        result_text.config(state="disabled") # Non-aktifkan edit
        
        # Tombol untuk menyalin hasil
        ttk.Button(frame, text="Salin ke Clipboard", 
                  command=lambda: copy_to_clipboard(encrypted)).pack(pady=10)
        
        # Langkah 5: Update status
        status_label.config(text="Pesan berhasil dienkripsi", fg=SUCCESS_COLOR)
        
    except Exception as e:
        # Tangani error jika enkripsi gagal
        messagebox.showerror("Error", f"Gagal mengenkripsi: {str(e)}", parent=screen)
        status_label.config(text="Enkripsi gagal", fg=ERROR_COLOR)

def decrypt():
    """
    Fungsi untuk dekripsi pesan menggunakan base64:
    1. Validasi password terlebih dahulu
    2. Memeriksa apakah ada pesan yang dimasukkan
    3. Mendekripsi pesan menggunakan base64
    4. Menampilkan hasil dalam window baru
    5. Memberikan feedback ke user
    """
    # Langkah 1: Validasi password
    if not validate_password():
        return
        
    # Langkah 2: Ambil pesan dan pastikan tidak kosong
    message = text1.get("1.0", END).strip()
    if not message:
        messagebox.showwarning("Warning", "Harap masukkan pesan untuk didekripsi", parent=screen)
        return
    
    try:
        # Langkah 3: Proses dekripsi
        encode_message = message.encode("ascii")       # Konversi ke bytes
        base64_bytes = base64.b64decode(encode_message) # Dekripsi base64
        decrypted = base64_bytes.decode("ascii")       # Konversi ke string
        
        # Langkah 4: Tampilkan hasil dalam window baru
        result_window = Toplevel(screen)
        result_window.title("Hasil Dekripsi")
        result_window.geometry("500x300")
        result_window.configure(bg=BG_COLOR)
        result_window.resizable(False, False)
        
        # Frame untuk hasil dekripsi
        frame = ttk.Frame(result_window, style="Card.TFrame")
        frame.pack(pady=20, padx=20, fill=BOTH, expand=True)
        
        # Label judul
        Label(frame, text="PESAN TERDEKRIPSI", font=("Arial", 12, "bold"), 
              bg=BG_COLOR).pack(pady=(10, 5))
        
        # Text area untuk menampilkan hasil
        result_text = Text(frame, font=("Arial", 10), wrap=WORD, 
                         height=8, padx=10, pady=10)
        result_text.pack(fill=BOTH, expand=True, padx=10, pady=5)
        result_text.insert(END, decrypted)  # Tampilkan hasil
        result_text.config(state="disabled") # Non-aktifkan edit
        
        # Tombol untuk menyalin hasil
        ttk.Button(frame, text="Salin ke Clipboard", 
                  command=lambda: copy_to_clipboard(decrypted)).pack(pady=10)
        
        # Langkah 5: Update status
        status_label.config(text="Pesan berhasil didekripsi", fg=SUCCESS_COLOR)
        
    except Exception as e:
        # Tangani error jika dekripsi gagal
        messagebox.showerror("Error", f"Gagal mendekripsi: {str(e)}", parent=screen)
        status_label.config(text="Dekripsi gagal", fg=ERROR_COLOR)

def copy_to_clipboard(text):
    """
    Fungsi untuk menyalin teks ke clipboard sistem:
    1. Membersihkan clipboard terlebih dahulu
    2. Menambahkan teks ke clipboard
    3. Update GUI
    4. Memberikan feedback ke user
    """
    screen.clipboard_clear()       # Bersihkan clipboard
    screen.clipboard_append(text)  # Tambahkan teks ke clipboard
    screen.update()                # Update GUI
    status_label.config(text="Tersalin ke clipboard!", fg=PRIMARY_COLOR)

def main_screen():
    """
    Fungsi utama untuk membuat GUI aplikasi:
    - Mengatur tampilan utama
    - Membuat semua komponen antarmuka
    - Mengatur style dan tata letak
    """
    global screen, code, text1, status_label
    
    # 1. Setup window utama
    screen = Tk()
    screen.title("SecureCrypt - Alat Enkripsi/Decripsi")
    screen.geometry("600x500")
    screen.configure(bg=BG_COLOR)
    screen.resizable(False, False)
    
    # 2. Coba set icon aplikasi
    try:
        screen.iconbitmap("lock.ico")  # File icon aplikasi
    except:
        pass  # Lewati jika file tidak ada
    
    # 3. Konfigurasi style untuk komponen GUI
    style = ttk.Style()
    style.configure("TFrame", background=BG_COLOR)
    style.configure("Card.TFrame", background="white", borderwidth=2, 
                   relief="groove", bordercolor="#e0e0e0")
    style.configure("TButton", font=("Arial", 10), padding=6)
    style.map("TButton",
              foreground=[('pressed', 'white'), ('active', 'white')],
              background=[('pressed', SECONDARY_COLOR), ('active', PRIMARY_COLOR)])
    
    # 4. Membuat header aplikasi
    header_frame = ttk.Frame(screen, style="TFrame")
    header_frame.pack(fill=X, padx=20, pady=(20, 10))
    
    # Judul aplikasi dengan font khusus
    title_font = tkfont.Font(family="Arial", size=16, weight="bold")
    Label(header_frame, text="SecureCrypt", font=title_font, 
          bg=BG_COLOR, fg=PRIMARY_COLOR).pack(side=LEFT)
    
    # 5. Frame utama untuk konten
    main_frame = ttk.Frame(screen, style="Card.TFrame")
    main_frame.pack(padx=20, pady=10, fill=BOTH, expand=True)
    
    # 6. Input area untuk pesan
    Label(main_frame, text="Masukkan pesan:", font=("Arial", 11), 
          bg="white", anchor="w").pack(fill=X, padx=10, pady=(10, 5))
    
    text1 = Text(main_frame, font=("Arial", 10), wrap=WORD, 
                height=10, padx=10, pady=10)
    text1.pack(fill=BOTH, expand=True, padx=10, pady=5)
    
    # 7. Input area untuk password
    Label(main_frame, text="Masukkan kunci enkripsi:", font=("Arial", 11), 
          bg="white", anchor="w").pack(fill=X, padx=10, pady=(10, 5))
    
    code = StringVar()  # Variabel untuk menyimpan password
    password_entry = ttk.Entry(main_frame, textvariable=code, 
                              font=("Arial", 11), show="•")  # Input dengan bullet
    password_entry.pack(fill=X, padx=10, pady=5)
    
    # 8. Frame untuk tombol aksi
    button_frame = ttk.Frame(main_frame, style="TFrame")
    button_frame.pack(fill=X, padx=10, pady=10)
    
    # Tombol-tombol aksi
    ttk.Button(button_frame, text="Enkripsi", style="TButton", 
              command=encrypt).pack(side=LEFT, padx=5)
    ttk.Button(button_frame, text="Dekripsi", style="TButton", 
              command=decrypt).pack(side=LEFT, padx=5)
    ttk.Button(button_frame, text="Reset", style="TButton", 
              command=reset).pack(side=RIGHT, padx=5)
    
    # 9. Status bar di bagian bawah
    status_frame = ttk.Frame(screen, style="TFrame", height=25)
    status_frame.pack(fill=X, padx=20, pady=(0, 20))
    
    status_label = Label(status_frame, text="Ready", font=("Arial", 9), 
                        bg=BG_COLOR, fg="black", anchor="w")
    status_label.pack(fill=X, padx=5)
    
    # 10. Set fokus awal ke area pesan
    text1.focus_set()
    
    # 11. Jalankan aplikasi
    screen.mainloop()

# Jalankan aplikasi jika file di-execute langsung
if __name__ == "__main__":
    main_screen()
