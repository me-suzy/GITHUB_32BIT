# ALEPH Server Monitor

Monitor automat pentru serverul ALEPH care verifică periodic statusul serverului și îl repornește automat în caz de cădere.

## ⚠️ IMPORTANT: SECURITY

**Acest repository conține versiuni SANITIZATE ale codului - FĂRĂ secrete, IP-uri sau parole!**

Toate configurațiile sensibile (IP server, credențiale SSH, etc.) trebuie setate prin **variabile de mediu** înainte de rulare.

**NICIODATĂ nu comitați fișiere care conțin:**
- IP-uri de server
- Parole SSH sau Catalog
- Token-uri sau credențiale
- `authorized_users.json` cu date reale

## 📋 Structura Proiectului

### Versiuni Disponibile

1. **32-bit Auto Login** (`monitor-server-autologin-32bit.py`)
   - Versiune pentru sisteme Windows 32-bit
   - Auto-login cu credențiale hardcodate (configurate prin env vars)
   - Executabil: `build_exe_32bit_FIXED.py`

2. **64-bit Auto Login** (`monitor-server-autologin-64bit.py`)
   - Versiune pentru sisteme Windows 64-bit
   - Auto-login cu credențiale hardcodate (configurate prin env vars)
   - Executabil: `build_exe_autologin_64bit.py`

## 🚀 Instalare și Configurare

### Cerințe

- Python 3.8+ (32-bit sau 64-bit, în funcție de versiunea dorită)
- Windows OS
- Dependențe Python:
  ```
  pip install paramiko requests pyautogui pyinstaller pillow
  ```

### Configurare Variabile de Mediu

Înainte de rulare sau build, setează următoarele variabile de mediu:

**Windows PowerShell:**
```powershell
$env:ALEPH_SERVER_IP="your.server.ip"
$env:ALEPH_SSH_USER="your_ssh_user"
$env:ALEPH_SSH_PASS="your_ssh_password"
$env:ALEPH_CATALOG_USER="your_catalog_user"
$env:ALEPH_CATALOG_PASS="your_catalog_password"
```

**Windows CMD:**
```cmd
set ALEPH_SERVER_IP=your.server.ip
set ALEPH_SSH_USER=your_ssh_user
set ALEPH_SSH_PASS=your_ssh_password
set ALEPH_CATALOG_USER=your_catalog_user
set ALEPH_CATALOG_PASS=your_catalog_password
```

**Variabile opționale:**
- `ALEPH_SSH_PORT` - Port SSH (default: 22)
- `ALEPH_CATALOG_EXE` - Calea către Catalog.exe (default: `C:\AL500\catalog\bin\Catalog.exe`)
- `ALEPH_CHECK_INTERVAL` - Interval verificare în secunde (default: 120)
- `ALEPH_TEMP_DATE` - Data temporară pentru licență (default: "12 JAN 2012 08:00:00")

### Configurare Permanentă (Opțional)

Pentru a seta variabilele permanent în Windows:

1. Deschide "Sistem" → "Setări avansate" → "Variabile de mediu"
2. Adaugă variabilele în "Variabile utilizator" sau "Variabile sistem"

Sau creează un fișier `config.env` (NU comitați acest fișier!):
```env
ALEPH_SERVER_IP=your.server.ip
ALEPH_SSH_USER=your_ssh_user
ALEPH_SSH_PASS=your_ssh_password
ALEPH_CATALOG_USER=your_catalog_user
ALEPH_CATALOG_PASS=your_catalog_password
```

Și încarcă-l în script (trebuie adăugat cod pentru a-l citi).

## 🔨 Compilare Executabil

### Versiune 32-bit

**IMPORTANT:** Trebuie să ai Python 32-bit instalat!

```powershell
# Verifică arhitectura Python
python -c "import platform; print(platform.architecture()[0])"

# Dacă nu e 32bit, instalează Python 32-bit de pe python.org
# Apoi:
cd "32 biti"
python build_exe_32bit_FIXED.py
```

Vezi `INSTRUCTIUNI_BUILD_32BIT.md` pentru detalii complete.

### Versiune 64-bit

```powershell
cd "AlephMonitor-AutoLogin 64 biti"
python build_exe_autologin_64bit.py
```

## ▶️ Rulare

### Rulare Script Python (fără executabil)

```powershell
# Setează variabilele de mediu (vezi mai sus)
python monitor-server-autologin-32bit.py  # Pentru 32-bit
python monitor-server-autologin-64bit.py  # Pentru 64-bit
```

### Rulare Executabil

După compilare, executabilul va fi în `dist/`:
```powershell
.\dist\AlephMonitor-AutoLogin-32bit.exe  # 32-bit
.\dist\AlephMonitor-AutoLogin.exe         # 64-bit
```

**Notă:** Executabilul trebuie să aibă setate variabilele de mediu sau să le citească din configurație.

## ⚙️ Funcționalități

### Monitorizare Automată

- Verifică serverul la fiecare 2 minute (configurabil)
- Detectează căderi consecutive (2 eșecuri = repornire)
- Repornire automată cu secvența corectă

### Secvența de Repornire

1. Conectare SSH la server
2. Setare dată temporară (pentru licență Aleph)
3. Așteptare inițializare servicii (30s)
4. **Deschidere catalog online în browser** (ORDINE CRITICĂ!)
5. Lansare Catalog.exe local cu autentificare
6. Resetare dată curentă pe server
7. Redeschidere catalog online
8. Verificare finală

### Prevenire Sleep/Hibernate

Aplicația previne automat intrarea calculatorului în sleep sau hibernate cât timp rulează.

### Pauză Backup (22:00 - 03:00)

Monitorul nu efectuează acțiuni (verificări sau reporniri) între orele 22:00 și 03:00 pentru a evita conflictele cu procesele de backup.

## 📁 Structura Fișierelor

```
.
├── README.md                          # Acest fișier
├── config.env.example                 # Template pentru config.env (fără valori reale)
├── .gitignore                         # Exclude secrete, build files, executabile
│
├── monitor-server-autologin-32bit.py  # Script 32-bit (sanitized)
├── monitor-server-autologin-64bit.py  # Script 64-bit (sanitized)
│
├── build_exe_32bit_FIXED.py           # Build script 32-bit
├── build_exe_autologin_64bit.py       # Build script 64-bit
│
├── INSTRUCTIUNI_BUILD_32BIT.md        # Ghid pentru compilare 32-bit
├── diagnoza_executabil.py              # Script diagnostic Python environment
│
└── dist/                               # Output executabile (NU se comite!)
    ├── AlephMonitor-AutoLogin-32bit.exe
    └── AlephMonitor-AutoLogin.exe
```

## 🔒 Securitate

### Checklist înainte de Commit

- [ ] ❌ Nu există IP-uri sau adrese server în cod
- [ ] ❌ Nu există parole sau token-uri în cod
- [ ] ❌ Nu există fișiere `config.env` cu valori reale
- [ ] ❌ Nu există `authorized_users.json` cu date reale
- [ ] ✅ Toate secretele sunt în variabile de mediu sau fișiere `.env` (excluse din git)
- [ ] ✅ `.gitignore` exclude toate fișierele sensibile

### Fișiere Excluse (vezi `.gitignore`)

- `dist/` - Executabile compilate
- `build/` - Fișiere temporare PyInstaller
- `*.exe` - Executabile
- `*.log` - Log-uri
- `config.env` - Configurații cu valori reale
- `authorized_users.json` - Lista utilizatorilor (dacă conține date reale)

## 🐛 Depanare

### "Variabilele de mediu necesare nu sunt setate"

**Soluție:** Setează toate variabilele de mediu necesare (vezi secțiunea "Configurare Variabile de Mediu").

### "not a valid Win32 application" (la 32-bit)

**Cauză:** Executabilul a fost compilat cu Python 64-bit.

**Soluție:** Instalează Python 32-bit și recompilă executabilul. Vezi `INSTRUCTIUNI_BUILD_32BIT.md`.

### Serverul nu se repornește automat

**Verifică:**
1. Variabilele de mediu SSH sunt setate corect
2. Conexiunea SSH este posibilă (testează cu Putty)
3. Aplicația nu este în pauză backup (22:00-03:00)
4. Verifică log-urile în `aleph_monitor.log`

### Catalog.exe nu se lansează

**Verifică:**
1. Path-ul către Catalog.exe este corect (default: `C:\AL500\catalog\bin\Catalog.exe`)
2. Setează `ALEPH_CATALOG_EXE` dacă path-ul este diferit
3. Verifică dacă Catalog.exe există la locația specificată

## 📝 Notițe

- **Ordinea deschiderii este critică:** Catalog online trebuie deschis ÎNAINTE de Catalog.exe din cauza licenței Aleph.
- **Prevenirea sleep-ului** este automată cât timp aplicația rulează.
- **Pauza de backup** este între 22:00 și 03:00 (ora locală România).

## 📄 Licență

Proiect intern pentru monitorizarea serverului ALEPH.

## 👥 Contribuții

**NU comitați secrete, IP-uri sau parole în repository!**

Pentru modificări:
1. Folosește variabile de mediu pentru configurații
2. Verifică că `.gitignore` exclude toate fișierele sensibile
3. Testează înainte de commit

