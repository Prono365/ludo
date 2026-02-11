#  CURSED ISLAND

Cursed Island adalah permainan petualangan teks (text-based adventure) berbasis Python. Pemain berperan sebagai karakter utama yang terjebak di sebuah pulau misterius bersama 5 teman lainnya. Tantangan utama adalah melarikan diri dalam batas waktu 48 jam dengan cara mengumpulkan tim, mencari item kunci, dan memecahkan misteri pulau tersebut. 

Proyek ini dibuat sebagai tugas akhir (Proyek Akhir Python CLI - Kelas X RPL 1 SMKN 2 JAKARTA) dan kegabutan para kontributornya.

Download disini ->
https://github.com/Prono365/ludo/releases

Game ini menggunakan antarmuka Command Line Interface (CLI), jadi kontrolnya dilakukan menggunakan keyboard: 

 Membaca Cerita: Baca narasi dan dialog yang muncul di layar. 
 Membuat Pilihan: Setiap adegan akan menampilkan beberapa pilihan (biasanya ditandai dengan angka 1, 2, 3, dst). 
 Input: Ketik angka dari pilihan yang kamu inginkan, lalu tekan [Enter]. 
 Lanjut: Untuk melanjutkan teks yang sedang diketik (efek mengetik) atau menutup jendela informasi, cukup tekan [Enter]. 

Mekanisme Permainan:

 Sistem Waktu (48 Jam):
         Perhatikan Time Bar di bagian atas layar.
         Setiap kali kamu berpindah scene atau melakukan aksi (seperti memeriksa ruangan), waktu akan berkurang (misalnya -1 jam, -2 jam).
         Jangan buang-buang waktu untuk pilihan yang tidak berguna, atau kamu akan kehabisan waktu sebelum sampai ke dermaga!
         
 Sistem Inventory:
         Kamu bisa menemukan item penting selama perjalanan (seperti Kunci Rekreasi, Peta Dermaga, Kalkulator Vio, dll).
         Item tertentu diperlukan untuk membuka jalur cerita spesifik (misalnya butuh Kartu Akses untuk naik Lift).
         Cek inventory secara berkala untuk melihat apa yang kamu miliki.
         
 Bercabang (Branching Story):
         Pilihanmu menentukan nasib. Pilihan yang salah bisa membuat kamu kehilangan teman, membuang waktu, atau berujung pada jalan buntu.
         Ada beberapa Ending yang bisa kamu dapatkan.

Cara Memainkannya:

1. Ekstrak File ZIP 

Pertama, kamu harus mengeluarkan isi file ZIP agar komputer bisa membacanya. 

     

    Windows: 
        Klik kanan pada file ZIP yang kamu download. 
        Pilih Extract All (Ekstrak Semua). 
        Pilih lokasi tempat kamu ingin menyimpan foldernya (contoh: Desktop atau Documents). 
        Klik Extract. 
     

    Mac: 
        Klik dua kali file ZIP. 
        Folder baru yang berisi game akan otomatis terbuka. 
     

    Linux (Ubuntu, Debian, Fedora, dll): 
        Buka File Manager. 
        Klik kanan file ZIP -> pilih Extract Here atau Extract to. 
        Pastikan folder hasil ekstrak sudah siap. 
     

    HP (Android/iOS): 
        Kamu memerlukan aplikasi manajer file (seperti ZArchiver atau Files). 
        Buka file ZIP, lalu pilih menu Extract atau Unzip. 
     

2. Buka Folder Game 

Masuk ke folder yang baru saja diekstrak tadi.
Di dalamnya, kamu wajib melihat dua file penting ini: 

    main.py (Kode program utamanya). 
    story.json (Database ceritanya). 

Jika kamu tidak melihat story.json, kemungkinan game tidak akan berjalan atau akan error. 
3. Cara Menjalankan (Running) 

Setelah folder terbuka, buka Terminal atau Command Prompt di lokasi folder tersebut sesuai sistem operasimu: 
Windows 

    Klik kanan pada ruang kosong di dalam folder game. 
    Pilih "Open in Terminal" atau "Open PowerShell window here". 
    Ketik perintah berikut lalu tekan Enter:
     
      
     
    python main.py
     
     
     
    (Jika error, coba: python3 main.py) 

 Mac 

    Buka aplikasi Terminal. 
    Ketik cd  (spasi), lalu seret dan lepas folder game ke jendela Terminal. 
    Tekan Enter. 
    Ketik perintah:
     
      
     
    python3 main.py
     
     
      

Linux 

    Buka folder game di File Manager. 
    Klik kanan ruang kosong -> pilih "Open in Terminal" (atau "Buka di Terminal"). 
    Ketik perintah berikut lalu tekan Enter:
    bash
     
      
     
    python3 main.py
     
     
     
    (Jika belum ada Python, install dulu: sudo apt install python3) 

HP (Android/iOS) 

    Buka aplikasi menjalankan Python (seperti Pydroid 3 atau Termux). 
    Buka file main.py melalui aplikasi tersebut. 
    Tekan tombol Run atau Play. 

4. Selamat Bermain! 

Setelah kamu menekan Enter/Run, layar hitam (terminal) akan membersihkan diri dan judul CURSED ISLAND akan muncul. 

Cara Bermain: 

     Baca cerita yang muncul di layar.
     Ketik angka dari pilihan yang kamu inginkan (misal: 1 untuk jalan kiri, 2 untuk jalan kanan).
     Tekan Enter.
     Perhatikan Waktu (Jam) di bagian atas. Jangan sampai waktu habis sebelum kamu berhasil kabur!
     
         
     
