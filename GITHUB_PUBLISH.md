# Ghid Publicare pe GitHub

## ⚠️ IMPORTANT: Verificare Secrete

Înainte de publicare, verifică că **NICIUN** fișier nu conține:

- ❌ IP-uri de server
- ❌ Parole SSH sau Catalog
- ❌ Token-uri sau credențiale
- ❌ Fișiere `config.env` cu valori reale
- ❌ `authorized_users.json` cu date reale

## 📋 Pași pentru Publicare

### 1. Inițializare Repository Git

```powershell
cd C:\Users\necul\GITHUB_32BIT

# Inițializează repository Git
git init

# Creează branch-ul main
git checkout -b main
```

### 2. Adaugă Toate Fișierele (securizate)

```powershell
# Adaugă toate fișierele (gitignore va exclude automat dist/, build/, etc.)
git add .

# Verifică ce fișiere vor fi comitate
git status

# Dacă vezi orice fișier cu secrete (IP, parole), șterge-l din staging:
# git reset HEAD nume_fisier
```

### 3. Commit Initial

```powershell
git commit -m "Public release: ALEPH Server Monitor (sanitized versions)"
```

### 4. Conectare la Repository GitHub

```powershell
# Adaugă remote repository (înlocuiește cu URL-ul tău real)
git remote add origin https://github.com/ME-SUZY/your-repo-name.git

# Verifică remote
git remote -v
```

### 5. Publicare pe GitHub

```powershell
# Push pe branch-ul main
git push -u origin main
```

## ✅ Checklist Final

- [ ] Toate IP-urile sunt eliminate sau înlocuite cu variabile de mediu
- [ ] Toate parolele sunt eliminate sau în variabile de mediu
- [ ] `.gitignore` exclude `dist/`, `build/`, `*.exe`, `*.log`, `config.env`
- [ ] `config.env.example` nu conține valori reale
- [ ] `README.md` explică cum să seteze variabilele de mediu
- [ ] Nu există fișiere `authorized_users.json` cu date reale

## 🔒 Securitate Token GitHub

**IMPORTANT:** Dacă ai afișat anterior un token GitHub în acest chat:

1. **Revocă token-ul imediat** pe GitHub:
   - Settings → Developer settings → Personal access tokens
   - Șterge token-ul compromis

2. **Creează un token nou** (fine-grained, minim permisiuni):
   - Doar pentru repository-ul specific
   - Permisiuni: Contents (read/write)

3. **Folosește token-ul nou doar local** (NU-l mai publica în chat!)

## 📝 Notițe

- Repository-ul public NU trebuie să conțină niciodată secrete
- Toți utilizatorii trebuie să seteze propriile variabile de mediu
- `config.env.example` servește doar ca template

## 🆘 Probleme?

**"repository not found" sau "authentication failed"**
- Verifică că token-ul GitHub este valid
- Verifică că ai permisiuni de write pe repository

**"refusing to merge unrelated histories"**
- Folosește: `git pull origin main --allow-unrelated-histories`

