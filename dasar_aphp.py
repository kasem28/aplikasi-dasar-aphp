import streamlit as st
import pandas as pd
import os
import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Dasar-Dasar APHP", page_icon="🌱", layout="wide")

# Fungsi untuk memuat atau membuat database CSV
def load_data(filename, columns):
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)
    return pd.read_csv(filename)

# File penyimpanan
FILE_BAHAN = "log_bahan.csv"
FILE_RENDEMEN = "log_rendemen.csv"
FILE_ALAT = "log_alat.csv"

# Load Data
df_bahan = load_data(FILE_BAHAN, ["Tanggal", "Kelompok", "Nama_Bahan", "Warna", "Aroma", "Tekstur", "Kondisi_Mutu"])
df_rendemen = load_data(FILE_RENDEMEN, ["Tanggal", "Kelompok", "Produk_Olahan", "Berat_Awal", "Berat_Akhir", "Persentase_Rendemen"])
df_alat = load_data(FILE_ALAT, ["Tanggal", "Peminjam", "Nama_Alat", "Kondisi_Pinjam", "Status_Kembali"])

st.title("🌱 Aplikasi Jurnal Praktikum Dasar-Dasar APHP")
st.markdown("**Mata Pelajaran: Dasar-Dasar Agriteknologi Pengolahan Hasil Pertanian (Kelas X)**")
st.divider()

# Sidebar untuk Navigasi Menu
menu = st.sidebar.selectbox("Pilih Menu Praktikum:", 
    ["1. Identifikasi Bahan Baku", "2. Kalkulator Rendemen", "3. Peminjaman Alat", "4. Dashboard Laporan Siswa"]
)

# 1. MENU IDENTIFIKASI BAHAN BAKU
if menu == "1. Identifikasi Bahan Baku":
    st.header("🔍 Form Identifikasi Karakteristik Bahan")
    st.write("Catat hasil pengamatan fisik bahan hasil pertanian sebelum diolah.")
    
    with st.form("form_bahan"):
        col1, col2 = st.columns(2)
        with col1:
            tgl = st.date_input("Tanggal Praktikum")
            kelompok = st.text_input("Nama/Nomor Kelompok (Misal: Kelompok 1)")
            nama_bahan = st.text_input("Nama Bahan (Misal: Daun Nilam, Biji Kakao, Kentang)")
            kondisi = st.selectbox("Kesimpulan Mutu Bahan", ["Sangat Baik (Segar/Layak)", "Baik (Ada sedikit cacat)", "Kurang Baik (Banyak cacat/busuk)"])
        with col2:
            warna = st.text_input("Pengamatan Warna")
            aroma = st.text_input("Pengamatan Aroma")
            tekstur = st.text_input("Pengamatan Tekstur")
            
        submit_bahan = st.form_submit_button("Simpan Data Pengamatan")
        
        if submit_bahan and kelompok != "" and nama_bahan != "":
            data_baru = pd.DataFrame([{
                "Tanggal": tgl, "Kelompok": kelompok, "Nama_Bahan": nama_bahan, 
                "Warna": warna, "Aroma": aroma, "Tekstur": tekstur, "Kondisi_Mutu": kondisi
            }])
            df_bahan = pd.concat([df_bahan, data_baru], ignore_index=True)
            df_bahan.to_csv(FILE_BAHAN, index=False)
            st.success(f"✅ Data pengamatan {nama_bahan} dari {kelompok} berhasil disimpan!")

# 2. MENU KALKULATOR RENDEMEN
elif menu == "2. Kalkulator Rendemen":
    st.header("🧮 Kalkulator Perhitungan Rendemen")
    st.write("Hitung persentase hasil olahan (Contoh: Berapa % minyak atsiri yang dihasilkan dari penyulingan daun sereh wangi).")
    
    with st.form("form_rendemen"):
        tgl_rendemen = st.date_input("Tanggal")
        kelompok_rendemen = st.text_input("Nama/Nomor Kelompok")
        produk = st.text_input("Nama Produk Olahan (Misal: Minyak Atsiri Sereh Wangi, Keripik Kentang)")
        
        col1, col2 = st.columns(2)
        with col1:
            berat_awal = st.number_input("Berat Bahan Awal (Satuannya harus sama, misal Gram)", min_value=0.0, step=1.0)
        with col2:
            berat_akhir = st.number_input("Berat Produk Akhir / Hasil Jadi (Gram)", min_value=0.0, step=1.0)
            
        submit_rendemen = st.form_submit_button("Hitung & Simpan Rendemen")
        
        if submit_rendemen:
            if berat_awal > 0:
                rendemen = (berat_akhir / berat_awal) * 100
                st.info(f"📊 Hasil Perhitungan Rendemen: **{rendemen:.2f} %**")
                
                if kelompok_rendemen != "" and produk != "":
                    data_baru = pd.DataFrame([{
                        "Tanggal": tgl_rendemen, "Kelompok": kelompok_rendemen, "Produk_Olahan": produk, 
                        "Berat_Awal": berat_awal, "Berat_Akhir": berat_akhir, "Persentase_Rendemen": round(rendemen, 2)
                    }])
                    df_rendemen = pd.concat([df_rendemen, data_baru], ignore_index=True)
                    df_rendemen.to_csv(FILE_RENDEMEN, index=False)
                    st.success("✅ Data perhitungan rendemen berhasil dicatat ke laporan!")
            else:
                st.error("Berat awal tidak boleh nol (0)!")

# 3. MENU PEMINJAMAN ALAT
elif menu == "3. Peminjaman Alat":
    st.header("🛠️ Log Peminjaman Alat Praktikum")
    st.write("Catat alat yang dipinjam dari laboran / ruang alat (Terapkan kedisiplinan SOP).")
    
    with st.form("form_alat"):
        tgl_alat = st.date_input("Tanggal")
        peminjam = st.text_input("Nama Peminjam / Kelompok")
        nama_alat = st.text_input("Nama Alat (Misal: Timbangan Analitik, Gelas Ukur 500 mL, Blender)")
        kondisi = st.selectbox("Kondisi Saat Dipinjam", ["Baik & Bersih", "Sedikit Kotor/Kusam", "Ada Retak/Cacat ringan"])
        
        submit_alat = st.form_submit_button("Catat Peminjaman")
        
        if submit_alat and peminjam != "" and nama_alat != "":
            data_baru = pd.DataFrame([{
                "Tanggal": tgl_alat, "Peminjam": peminjam, "Nama_Alat": nama_alat, 
                "Kondisi_Pinjam": kondisi, "Status_Kembali": "Belum Kembali"
            }])
            df_alat = pd.concat([df_alat, data_baru], ignore_index=True)
            df_alat.to_csv(FILE_ALAT, index=False)
            st.success(f"✅ Peminjaman {nama_alat} oleh {peminjam} dicatat.")

# 4. DASHBOARD LAPORAN
elif menu == "4. Dashboard Laporan Siswa":
    st.header("📑 Dashboard Laporan Kelas X APHP")
    st.write("Semua data praktikum siswa akan terekap di sini.")
    
    st.subheader("1. Rekap Nilai Rendemen")
    st.dataframe(df_rendemen, use_container_width=True)
    
    st.subheader("2. Rekap Identifikasi Bahan")
    st.dataframe(df_bahan, use_container_width=True)
    
    st.subheader("3. Status Alat Praktikum (Belum Dikembalikan)")
    if not df_alat.empty:
        alat_belum_kembali = df_alat[df_alat["Status_Kembali"] == "Belum Kembali"]
        st.dataframe(alat_belum_kembali, use_container_width=True)
    else:
        st.write("Belum ada data peminjaman.")
