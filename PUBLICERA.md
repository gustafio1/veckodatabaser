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
3. Trigger: **Dagligen**, kl. **08:00** (efter att flödesbygget körts ~07:35).
4. Åtgärd: **Starta ett program** → Bläddra till
   `C:\backup\Leisure - Claude\Leisure\publish.bat`.
5. Slutför.

   (Flödet `flode.html` byggs nu om dagligen 07:35, så daglig publicering håller
   den publika sidan aktuell. `publish.bat` pushar bara när något faktiskt
   ändrats, så dagar utan nytt innehåll skapar inga tomma commits.)

För att schemalagd push ska fungera utan att du loggar in varje gång måste
GitHub-inloggningen vara sparad — det sker automatiskt efter den första
manuella pushen i steg 2.

---

## Steg 5 – Koppla egen domän (www.veckodatabaser.se)

Filen `CNAME` (innehåll: `www.veckodatabaser.se`) ligger redan i mappen och
pushas automatiskt. Gör så här:

**1. Köp domänen** hos en svensk registrar, t.ex. Loopia
(https://www.loopia.se/domannamn/) eller One.com. Du behöver bara själva
domänen `veckodatabaser.se` — inget webbhotell, GitHub hostar sidan gratis.
Pris `.se`: ofta någon krona–~99 kr första året, därefter ca 219 kr/år.

**2. Lägg in DNS-poster** hos registraren (under "DNS" / "Egna pekare").
www är primär adress; toppdomänen omdirigeras automatiskt dit av GitHub:

| Typ   | Namn / Värd | Pekar på            |
|-------|-------------|---------------------|
| A     | @           | 185.199.108.153     |
| A     | @           | 185.199.109.153     |
| A     | @           | 185.199.110.153     |
| A     | @           | 185.199.111.153     |
| CNAME | www         | gustafio1.github.io |

(`@` = toppdomänen `veckodatabaser.se`. Toppdomänen måste använda A-poster –
en CNAME går inte att lägga på `@`, bara på `www`.)

**3. Pusha CNAME-filen** – kör `publish.bat` så den hamnar på GitHub.

**4. Aktivera i GitHub:** **Settings → Pages → Custom domain** → skriv
`www.veckodatabaser.se` → **Save**. Vänta tills DNS-kollen blir grön (några
minuter upp till 24 h), kryssa sedan i **Enforce HTTPS** för gratis SSL.

Ordning: pusha CNAME + lägg DNS-posterna INNAN du fyller i domänen i GitHub,
annars klagar GitHub på att DNS inte stämmer. DNS kan ta upp till 24 h att slå
igenom, men går ofta på minuter.

---

## Bra att veta

- Sidan blir **offentlig** och kan hittas via sökmotorer. Innehållet här är
  nyhetsbevakning, så det är okej — men lägg inget privat i mappen.
- Bilder: filer du lägger i `bilder/` följer med och visas i flödet. Lägg bara
  in bilder du har rätt att publicera – se `bilder/LÄS-MIG.txt`.
- Juridisk checklista för den publika sidan finns i `JURIDIK.md`.
