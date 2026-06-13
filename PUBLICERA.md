# Publicera Veckodatabaser med GitHub Pages

Allt är förberett i den här mappen (`.gitignore`, `README.md`, `publish.bat`,
`bilder/.gitkeep`). Du behöver bara köra stegen nedan **på din egen dator** —
den här miljön kan inte nå GitHub, men det kan din Windows-dator.

Förutsättning: Git är installerat (kolla med `git --version` i en
terminal/PowerShell). Saknas det: ladda ner från https://git-scm.com/download/win

---

## Steg 1 – Skapa ett tomt repo på GitHub

1. Gå till https://github.com/new
2. **Repository name:** t.ex. `veckodatabaser`
3. Välj **Public** (krävs för gratis GitHub Pages).
4. Bocka INTE i "Add a README" — mappen har redan filer.
5. Klicka **Create repository**.

GitHub visar nu en sida med en URL som ser ut så här:
`https://github.com/DITT-ANVANDARNAMN/veckodatabaser.git` — den behövs i steg 2.

---

## Steg 2 – Ladda upp mappen (engångs)

Öppna PowerShell, klistra in raderna en i taget. Byt ut URL:en mot din egen:

```powershell
cd "C:\backup\Leisure - Claude\Leisure"
git init -b main
git add -A
git commit -m "Forsta version: Veckodatabaser"
git remote add origin https://github.com/DITT-ANVANDARNAMN/veckodatabaser.git
git push -u origin main
```

Första `git push` öppnar ett inloggningsfönster mot GitHub — logga in en gång,
så sparas inloggningen för framtida pushar.

---

## Steg 3 – Slå på GitHub Pages

1. På repo-sidan: **Settings** → **Pages** (vänstermenyn).
2. Under **Source**: välj **Deploy from a branch**.
3. Branch: **main**, mapp: **/ (root)**. Klicka **Save**.
4. Vänta ~1 minut. Sidan dyker upp på:

   **https://DITT-ANVANDARNAMN.github.io/veckodatabaser/**

Det är din publika adress. `index.html` blir startsidan automatiskt.

---

## Steg 4 – Automatisk publicering varje vecka

`publish.bat` (ligger i mappen) committar och pushar allt nytt. Tre alternativ:

**A) Manuellt** – dubbelklicka `publish.bat` när du vill uppdatera sajten.

**B) Schemalagt (Windows Task Scheduler):**
1. Öppna *Schemaläggaren* / *Task Scheduler*.
2. **Skapa enkel uppgift** → namn t.ex. "Publicera veckodatabaser".
3. Trigger: **Veckovis**, måndag, kl. **08:00** (efter att veckokörningen
   uppdaterat filerna ~07:35).
4. Åtgärd: **Starta ett program** → Bläddra till
   `C:\backup\Leisure - Claude\Leisure\publish.bat`.
5. Slutför.

För att schemalagd push ska fungera utan att du loggar in varje gång måste
GitHub-inloggningen vara sparad — det sker automatiskt efter den första
manuella pushen i steg 2.

---

## Bra att veta

- Sidan blir **offentlig** och kan hittas via sökmotorer. Innehållet här är
  nyhetsbevakning, så det är okej — men lägg inget privat i mappen.
- Bilder: filer du lägger i `bilder/` följer med och visas i flödet.
- Vill du ha egen domän (t.ex. `veckodata.se`) går det att koppla under
  Settings → Pages → Custom domain. Säg till så hjälper jag dig.
