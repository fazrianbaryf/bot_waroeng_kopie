# ☕ Bot Waroeng Kopie (Discord)

**Bot Waroeng Kopie** adalah asisten Discord interaktif bergaya tongkrongan brutal dan savage! Bot ini mengusung sistem ekonomi unik berupa **"Biji Kopie"** ☕. Cocok untuk server komunitas gaming dan tempat nongkrong virtual supaya anggota server makin aktif berinteraksi, main game bareng, atau bahkan judi-judian koin.

Bot ini tidak menggunakan bahasa formal yang kaku, melainkan menggunakan bahasa umpatan ala tongkrongan (bujang, anjing, dsb.) dipadu dengan emotikon absurd (👽, 🤡, 💩, 🐒, ☕) agar suasana server Discord jadi lebih hidup, kocak, dan tidak membosankan.

---

## 🎯 Fitur & Cara Mendapatkan Biji Kopie (Poin Ekonomi)

Poin di dalam bot ini disebut sebagai **Biji Kopie**. Anggota server bisa mendapatkannya dengan cara-cara berikut:

1. **Ngajak Mabar (Chat Keyword)**
   - Jika anggota server mengetik pesan yang mengandung kata kunci ajakan main seperti: `mabar`, `r`, `login`, `ready`, `gas`, `ayo`, `main`, `party`, `rank`, `push`, `ayok`, `skuy`, `kuy`, `s`, atau `v`...
   - Atau jika ada anggota yang secara langsung nge-**tag (mention)** teman di pesan mereka (contoh: *"oi @Pais"*)...
   - **Hadiah:** Bot akan membalas dengan ucapan semangat secara savage, dan memberikan bonus **+2 Biji Kopie**! Sekaligus akan me-react pesan dengan stiker ☕.

2. **Nongkrong di Voice Channel (AFK / Aktif)**
   - Anggota yang berada di Voice Channel (kanal suara) mana pun akan otomatis diberikan gaji setiap 10 menit sekali.
   - **Hadiah:** Tambahan **+5 Biji Kopie** setiap 10 menit diam di channel suara.

3. **Bermain Game (Discord Activity)**
   - Bot ini akan mengecek status/aktivitas setiap pengguna di Discord setiap 5 menit. Jika ada yang terdeteksi sedang bermain game (misal: "Playing Valorant", "Playing Dota 2", dsb).
   - **Hadiah:** Tambahan pasif **+1 Biji Kopie** setiap 5 menit selama game dimainkan.

---

## 🎖️ Sistem Pangkat Otomatis (Auto-Role)

Bot secara otomatis akan mempromosikan pangkat pengguna dengan menugaskan role Discord jika jumlah Biji Kopie mereka sudah mencapai target tertentu.
- 🥉 Poin menyentuh **50 Biji Kopie** = Mendapatkan Role **"Pelanggan Tetap"**
- 🥈 Poin menyentuh **200 Biji Kopie** = Mendapatkan Role **"Juragan Gorengan"**
- 🥇 Poin menyentuh **500 Biji Kopie** = Mendapatkan Role **"Sultan Kopi"**

> **Catatan Admin:** Pastikan role Discord dengan nama-nama persis seperti di atas (`Pelanggan Tetap`, `Juragan Gorengan`, `Sultan Kopi`) telah dibuat di Server Settings > Roles agar fitur ini berjalan. Pastikan juga urutan Role Bot Waroeng Kopie berada di atas ketiga role pangkat tersebut agar bot bisa memberikannya ke member.

---

## 📜 Daftar Perintah (Commands)

Berikut adalah perintah (`/`) yang dapat diketik oleh member di server chat:

- **/cek**
  Untuk mengecek jumlah dompet / saldo Biji Kopie pribadi beserta sindirannya.
  *Contoh Balasan:* `"🐒 Lu @User cuma punya 10 Biji Kopie, kismin amat anjir! 💩"`
  
- **/top_juragan**
  Untuk melihat peringkat (Leaderboard) atau daftar 10 Sengkuni dengan Biji Kopie paling banyak di server. 
  
- **/transfer @user [jumlah]**
  Untuk mentransfer/memberi sedekah Biji Kopie dari saldo pribadi kepada teman (member lain). Jika tidak punya saldo cukup, bot akan menolak dan meledek pengguna.
  *Contoh:* `/transfer @Andi 50`

- **/slot [jumlah]**
  Sistem taruhan mesin judi **"Lingkaran Setan"**. Pengguna bisa mempertaruhkan Biji Kopie mereka. Mesin akan melakukan animasi putaran 🔄 dengan frame-by-frame lock yang realistis.
  - **Aturan Menang:**
    - Jika dapat **3 gambar kombinasi unik (☕, 🐒, 👽, 🤡) yang sama persis** *(JACKPOT!)* = Menang **5x lipat** dari jumlah taruhan yang dipasang (Bandar bangkrut!).
    - Jika dapat **minimal 2 gambar yang sama** = Balik modal + tambahan kemenangan **2x lipat** taruhan.
    - Jika **ketiga gambar berbeda semua** = *RUNGKAD!* Taruhan hangus lenyap seketika, dan pemain akan diledek bot habis-habisan.
  *Contoh:* `/slot 10` (Ingin mempertaruhkan 10 Biji Kopie).

---

## 💻 Cara Menjalankan Bot di Komputer Lokal

1. Buka folder bot di Visual Studio Code / Terminal PC Anda.
2. Pastikan file `database.db` terbuat (otomatis oleh `database.py`) untuk menyimpan riwayat koin peserta server.
3. Jalankan bot dengan perintah:
   ```bash
   python main.py
   ```
   > Jika Anda menggunakan virtual environment (venv) seperti struktur file saat ini, pastikan terminalnya berada di path yang benar (seperti `./venv/Scripts/python.exe main.py`).
4. Tunggu sesaat hingga terminal memunculkan notifikasi: `NamaBot siap ngopi!`.
5. Buka aplikasi Discord, dan silakan lakukan testing dengan mengetik kata-kata pancingan atau memanggil commands-nya.
