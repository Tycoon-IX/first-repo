"""
Sistem Manajemen Keuangan Pribadi
oleh [Nama Anda]
Menggunakan:
- Class utama untuk semua fungsi
- File handling untuk penyimpanan data
- Exception handling
- Datetime untuk pencatatan transaksi
"""

import json
from datetime import datetime

class ManajemenKeuangan:
    def __init__(self):
        self.data_keuangan = {
            'saldo': 0,
            'pemasukan': [],
            'pengeluaran': [],
            'kategori_pengeluaran': {}
        }
        self.load_data()
    
    def load_data(self):
        """Memuat data dari file JSON"""
        try:
            with open('data_keuangan.json', 'r') as f:
                self.data_keuangan = json.load(f)
            print("Data keuangan berhasil dimuat.")
        except FileNotFoundError:
            print("File data tidak ditemukan, memulai dengan data baru.")
        except Exception as e:
            print(f"Error saat memuat data: {e}")
    
    def save_data(self):
        """Menyimpan data ke file JSON"""
        try:
            with open('data_keuangan.json', 'w') as f:
                json.dump(self.data_keuangan, f, indent=4)
            print("Data berhasil disimpan.")
        except Exception as e:
            print(f"Error saat menyimpan data: {e}")
    
    def catat_pemasukan(self):
        """Mencatat pemasukan baru"""
        print("\n=== CATAT PEMASUKAN ===")
        try:
            jumlah = float(input("Jumlah pemasukan: Rp "))
            if jumlah <= 0:
                print("Jumlah harus lebih dari 0.")
                return
            
            sumber = input("Sumber pemasukan (contoh: Gaji, Bonus, dll): ").strip()
            tanggal = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            transaksi = {
                'jumlah': jumlah,
                'sumber': sumber,
                'tanggal': tanggal
            }
            
            self.data_keuangan['pemasukan'].append(transaksi)
            self.data_keuangan['saldo'] += jumlah
            self.save_data()
            
            print(f"\nPemasukan sebesar Rp {jumlah:,.2f} dari {sumber} berhasil dicatat.")
            print(f"Saldo saat ini: Rp {self.data_keuangan['saldo']:,.2f}")
        except ValueError:
            print("Input jumlah tidak valid. Harap masukkan angka.")
    
    def catat_pengeluaran(self):
        """Mencatat pengeluaran baru"""
        print("\n=== CATAT PENGELUARAN ===")
        try:
            jumlah = float(input("Jumlah pengeluaran: Rp "))
            if jumlah <= 0:
                print("Jumlah harus lebih dari 0.")
                return
            
            if jumlah > self.data_keuangan['saldo']:
                print("Saldo tidak mencukupi untuk pengeluaran ini.")
                return
            
            keterangan = input("Keterangan pengeluaran: ").strip()
            kategori = input("Kategori pengeluaran (contoh: Makanan, Transportasi, Hiburan): ").strip()
            tanggal = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            transaksi = {
                'jumlah': jumlah,
                'keterangan': keterangan,
                'kategori': kategori,
                'tanggal': tanggal
            }
            
            self.data_keuangan['pengeluaran'].append(transaksi)
            self.data_keuangan['saldo'] -= jumlah
            
            # Update kategori pengeluaran
            if kategori in self.data_keuangan['kategori_pengeluaran']:
                self.data_keuangan['kategori_pengeluaran'][kategori] += jumlah
            else:
                self.data_keuangan['kategori_pengeluaran'][kategori] = jumlah
            
            self.save_data()
            
            print(f"\nPengeluaran sebesar Rp {jumlah:,.2f} untuk {keterangan} berhasil dicatat.")
            print(f"Saldo saat ini: Rp {self.data_keuangan['saldo']:,.2f}")
        except ValueError:
            print("Input jumlah tidak valid. Harap masukkan angka.")
    
    def lihat_saldo(self):
        """Menampilkan saldo saat ini"""
        print("\n=== SALDO ANDA ===")
        print(f"Saldo saat ini: Rp {self.data_keuangan['saldo']:,.2f}")
    
    def lihat_laporan(self):
        """Menampilkan laporan keuangan"""
        print("\n=== LAPORAN KEUANGAN ===")
        print(f"\nSaldo Akhir: Rp {self.data_keuangan['saldo']:,.2f}")
        
        # Ringkasan pemasukan
        print("\n=== PEMASUKAN ===")
        total_pemasukan = sum(item['jumlah'] for item in self.data_keuangan['pemasukan'])
        print(f"Total Pemasukan: Rp {total_pemasukan:,.2f}")
        
        if self.data_keuangan['pemasukan']:
            print("\n10 Pemasukan Terakhir:")
            for item in self.data_keuangan['pemasukan'][-10:]:
                print(f"- Rp {item['jumlah']:,.2f} dari {item['sumber']} ({item['tanggal']})")
        
        # Ringkasan pengeluaran
        print("\n=== PENGELUARAN ===")
        total_pengeluaran = sum(item['jumlah'] for item in self.data_keuangan['pengeluaran'])
        print(f"Total Pengeluaran: Rp {total_pengeluaran:,.2f}")
        
        if self.data_keuangan['pengeluaran']:
            print("\n10 Pengeluaran Terakhir:")
            for item in self.data_keuangan['pengeluaran'][-10:]:
                print(f"- Rp {item['jumlah']:,.2f} untuk {item['keterangan']} ({item['kategori']}, {item['tanggal']})")
        
        # Analisis kategori pengeluaran
        print("\n=== ANALISIS PENGELUARAN PER KATEGORI ===")
        if self.data_keuangan['kategori_pengeluaran']:
            for kategori, jumlah in self.data_keuangan['kategori_pengeluaran'].items():
                persentase = (jumlah / total_pengeluaran * 100) if total_pengeluaran > 0 else 0
                print(f"- {kategori}: Rp {jumlah:,.2f} ({persentase:.1f}%)")
    
    def menu_utama(self):
        """Menampilkan menu utama"""
        while True:
            print("\n=== MANAJEMEN KEUANGAN PRIBADI ===")
            print("1. Catat Pemasukan")
            print("2. Catat Pengeluaran")
            print("3. Lihat Saldo")
            print("4. Lihat Laporan Keuangan")
            print("5. Keluar")
            
            pilihan = input("Pilih menu (1-5): ")
            
            if pilihan == '1':
                self.catat_pemasukan()
            elif pilihan == '2':
                self.catat_pengeluaran()
            elif pilihan == '3':
                self.lihat_saldo()
            elif pilihan == '4':
                self.lihat_laporan()
            elif pilihan == '5':
                print("Terima kasih telah menggunakan sistem manajemen keuangan.")
                break
            else:
                print("Pilihan tidak valid. Silakan pilih 1-5.")

if __name__ == "__main__":
    sistem = ManajemenKeuangan()
    sistem.menu_utama()