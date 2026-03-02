import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Dashboard Analisis Evaluasi", layout="wide")

st.title("📊 Dashboard Analisis Evaluasi Pembelajaran")
st.write("Data: 50 Siswa - 20 Soal")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("data_simulasi_50_siswa_20_soal.xlsx")

df = load_data()

# Ambil 20 kolom soal pertama
soal = df.iloc[:, :20]

df["Total_Skor"] = soal.sum(axis=1)
df["Rata_Rata"] = soal.mean(axis=1)

# =========================
# 1. DESKRIPSI DESKRIPTIF
# =========================
st.header("1️⃣ Statistik Deskriptif")

col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Siswa", len(df))
col2.metric("Rata-rata Total Skor", round(df["Total_Skor"].mean(),2))
col3.metric("Standar Deviasi", round(df["Total_Skor"].std(),2))

fig1 = plt.figure()
plt.hist(df["Total_Skor"], bins=10)
plt.xlabel("Total Skor")
plt.ylabel("Frekuensi")
st.pyplot(fig1)

# =========================
# 2. ANALISIS PER SOAL
# =========================
st.header("2️⃣ Analisis Per Soal")

rata_soal = soal.mean()
std_soal = soal.std()

analisis_soal = pd.DataFrame({
    "Rata-rata": rata_soal,
    "Standar Deviasi": std_soal
})

st.dataframe(analisis_soal)

fig2 = plt.figure()
rata_soal.plot(kind="bar")
plt.xlabel("Soal")
plt.ylabel("Rata-rata Skor")
st.pyplot(fig2)

# =========================
# 3. SOAL TERBAIK & TERBURUK
# =========================
st.header("3️⃣ Soal Terbaik & Terburuk")

soal_terbaik = rata_soal.idxmax()
soal_terburuk = rata_soal.idxmin()

st.success(f"Soal Termudah: {soal_terbaik}")
st.error(f"Soal Tersulit: {soal_terburuk}")

# =========================
# 4. ANALISIS GAP
# =========================
st.header("4️⃣ Analisis GAP")

nilai_maks = soal.max().max()
gap = nilai_maks - rata_soal

gap_df = pd.DataFrame({"GAP": gap})
st.dataframe(gap_df)

fig3 = plt.figure()
gap.plot(kind="bar")
plt.xlabel("Soal")
plt.ylabel("GAP terhadap skor maksimum")
st.pyplot(fig3)

# =========================
# 5. SEGMENTASI SISWA
# =========================
st.header("5️⃣ Segmentasi Siswa")

mean_total = df["Total_Skor"].mean()
std_total = df["Total_Skor"].std()

def kategori(skor):
    if skor >= mean_total + std_total:
        return "Tinggi"
    elif skor >= mean_total:
        return "Sedang"
    else:
        return "Rendah"

df["Kategori"] = df["Total_Skor"].apply(kategori)

segmentasi = df["Kategori"].value_counts()
st.dataframe(segmentasi)

fig4 = plt.figure()
segmentasi.plot(kind="bar")
plt.xlabel("Kategori")
plt.ylabel("Jumlah Siswa")
st.pyplot(fig4)

# =========================
# 6. KORELASI
# =========================
st.header("6️⃣ Korelasi Antar Soal")

corr_matrix = soal.corr()

fig5 = plt.figure()
plt.imshow(corr_matrix)
plt.colorbar()
plt.title("Matriks Korelasi")
st.pyplot(fig5)

# =========================
# 7. KESIMPULAN OTOMATIS
# =========================
st.header("7️⃣ Kesimpulan")

rata_total = df["Total_Skor"].mean()

if rata_total > (nilai_maks * 20 * 0.7):
    tingkat = "TINGGI"
elif rata_total > (nilai_maks * 20 * 0.5):
    tingkat = "SEDANG"
else:
    tingkat = "RENDAH"

st.write(f"""
Rata-rata total skor siswa adalah {round(rata_total,2)}.
Secara umum tingkat pencapaian berada pada kategori {tingkat}.
Soal termudah adalah {soal_terbaik}, sedangkan soal tersulit adalah {soal_terburuk}.
Distribusi segmentasi menunjukkan variasi performa siswa.
Korelasi antar soal menunjukkan adanya keterkaitan antar indikator kompetensi.
""")

st.divider()
st.subheader("Data Lengkap")
st.dataframe(df)
