# Veckodatabaser

Åtta ämnesvisa veckodatabaser (kultur, psykologi, it, religion, sport, ledarskap,
personlig utveckling, katolsk social lära) plus ett sammanslaget flöde.

Varje databas = en JSON (data) + en självständig HTML-dashboard på svenska.
`index.html` är startsidan och länkar till alla databaser samt `flode.html`.

## Publicering

Sidan publiceras med GitHub Pages. Startsidan är `index.html` i repo-roten.

Uppdatering: kör `publish.bat` (eller låt Windows Task Scheduler köra den) efter att
veckokörningen uppdaterat filerna — den committar och pushar ändringarna automatiskt.
