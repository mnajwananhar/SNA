import pandas as pd

# Ganti nama file sesuai hasil export dari Gephi Data Laboratory
FILE = "sna3.csv"  # atau nama file export lu

df = pd.read_csv(FILE)

# Cari nama kolom modularity (bisa "modularity_class" atau "Modularity Class" dll)
mod_col = [c for c in df.columns if 'modularity' in c.lower() or 'modularity' in c.lower()]
degree_col = [c for c in df.columns if c.lower() == 'degree']
label_col = [c for c in df.columns if c.lower() in ['label', 'id']]

if not mod_col:
    print("Kolom modularity tidak ditemukan!")
    print("Kolom yang tersedia:", list(df.columns))
    exit()

mod_col = mod_col[0]
degree_col = degree_col[0] if degree_col else None
label_col = label_col[0] if label_col else 'Id'

total_nodes = len(df)
print(f"Total Node: {total_nodes}")
print(f"Total Komunitas: {df[mod_col].nunique()}")
print()

# Hitung jumlah anggota per komunitas
komunitas = df.groupby(mod_col).agg(
    Jumlah_Anggota=(label_col, 'count'),
).reset_index()

komunitas['Persentase'] = (komunitas['Jumlah_Anggota'] / total_nodes * 100).round(2)

# Cari aktor utama (degree tertinggi) per komunitas
if degree_col:
    aktor = df.loc[df.groupby(mod_col)[degree_col].idxmax()][[mod_col, label_col, degree_col]]
    aktor.columns = [mod_col, 'Aktor_Utama', 'Degree_Tertinggi']
    komunitas = komunitas.merge(aktor, on=mod_col)

# Sort dari terbesar
komunitas = komunitas.sort_values('Jumlah_Anggota', ascending=False)

print("=" * 70)
print("TOP 10 KOMUNITAS TERBESAR")
print("=" * 70)
for i, row in komunitas.head(10).iterrows():
    print(f"Komunitas {row[mod_col]:>4} | "
          f"Anggota: {row['Jumlah_Anggota']:>4} | "
          f"Persentase: {row['Persentase']:>6}%", end="")
    if degree_col:
        print(f" | Aktor Utama: {row['Aktor_Utama']} (Degree: {row['Degree_Tertinggi']})")
    else:
        print()

print()
print("=" * 70)
print("UNTUK COPY KE LAPORAN:")
print("=" * 70)
for i, row in komunitas.head(5).iterrows():
    aktor = row['Aktor_Utama'] if degree_col else '-'
    print(f"| {int(row[mod_col]):<9} | {int(row['Jumlah_Anggota']):<14} | {row['Persentase']}%{'':<5} | {aktor:<27} |")
