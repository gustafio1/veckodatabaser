#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_flode.py
Bygger en enda scrollbar "flöde"-sida (flode.html) som blandar nyheter från
alla ämnesdatabaser med bilder från bild-databasen (bilder.json).

Körs lokalt i mappen där ämnes-JSON-filerna och bilder/ ligger.
1. Läser alla ämnes-JSON (it, kultur, ...).
2. Skannar bilder/ efter bildfiler, uppdaterar bilder.json
   (behåller manuellt redigerade bildtexter, lägger till nya bilder).
3. Slår ihop alla nyheter + bilder, blandar dem (magasinstil).
4. Skriver self-contained flode.html med data mellan markörer.
"""
import json, os, re, random, datetime, html, email.utils

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://www.veckodatabaser.se"

# slug -> (ikon, kort etikett, färg)
TOPICS = {
    "it":                    ("\U0001F4BB", "IT",                  "#4f8cff"),
    "katolsk-social-lara":   ("⛪",     "Katolsk social lära", "#c9a227"),
    "kultur":                ("\U0001F3AD", "Kultur",              "#ff7ab8"),
    "ledarskap":             ("\U0001F9ED", "Ledarskap",           "#19c3a6"),
    "personlig-utveckling":  ("\U0001F331", "Personlig utveckling","#5fd35f"),
    "psykologi":             ("\U0001F9E0", "Psykologi",           "#b07cff"),
    "religion":              ("✝️","Religion",            "#e0aa3e"),
    "sport":                 ("⚽",     "Sport",               "#ff924c"),
}

IMG_EXTS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".bmp")
WEEK = datetime.date.today().isocalendar()
WEEK_STR = f"{WEEK[0]}-W{WEEK[1]:02d}"
TODAY = datetime.date.today().isoformat()


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def scan_pictures():
    """Skanna bilder/-mappen och synka bilder.json. Returnera bild-items."""
    bdir = os.path.join(HERE, "bilder")
    os.makedirs(bdir, exist_ok=True)
    bjson_path = os.path.join(HERE, "bilder.json")

    if os.path.exists(bjson_path):
        db = load_json(bjson_path)
    else:
        db = {
            "topic": "Bilder",
            "description": "Bilddatabas. Lägg bildfiler i mappen bilder/. "
                           "Redigera gärna titel, datum, kategori och källa nedan.",
            "schema_version": 1,
            "last_updated": TODAY,
            "item_count": 0,
            "items": [],
        }

    existing = {it.get("image"): it for it in db.get("items", []) if it.get("image")}

    files = sorted(f for f in os.listdir(bdir)
                   if f.lower().endswith(IMG_EXTS) and not f.startswith("."))

    items = []
    for fn in files:
        if fn in existing:
            it = existing[fn]  # behåll manuella redigeringar
        else:
            mtime = datetime.date.fromtimestamp(
                os.path.getmtime(os.path.join(bdir, fn))).isoformat()
            pretty = re.sub(r"[._-]+", " ", os.path.splitext(fn)[0]).strip().capitalize()
            it = {
                "id": "bild-" + re.sub(r"[^a-z0-9]+", "-", os.path.splitext(fn)[0].lower()).strip("-"),
                "title": pretty or "Bild",
                "category": "Bild",
                "date": mtime,
                "location": "",
                "summary": "",
                "source": "",
                "url": "",
                "image": fn,
                "added_on": TODAY,
                "collected_week": WEEK_STR,
            }
        it["image"] = fn
        items.append(it)

    db["items"] = items
    db["item_count"] = len(items)
    db["last_updated"] = TODAY
    with open(bjson_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    return items


def collect_news():
    feed = []
    for slug in TOPICS:
        path = os.path.join(HERE, f"{slug}.json")
        if not os.path.exists(path):
            continue
        db = load_json(path)
        for it in db.get("items", []):
            feed.append({
                "kind": "news",
                "slug": slug,
                "title": it.get("title", ""),
                "category": it.get("category", ""),
                "date": it.get("date", ""),
                "location": it.get("location", ""),
                "summary": it.get("summary", ""),
                "source": it.get("source", ""),
                "url": it.get("url", ""),
            })
    return feed


def build_feed():
    news = collect_news()
    pics = scan_pictures()
    feed = list(news)
    for p in pics:
        feed.append({
            "kind": "image",
            "slug": "bild",
            "title": p.get("title", ""),
            "category": p.get("category", "Bild"),
            "date": p.get("date", ""),
            "location": p.get("location", ""),
            "summary": p.get("summary", ""),
            "source": p.get("source", ""),
            "url": p.get("url", ""),
            "image": "bilder/" + p.get("image", ""),
        })
    # Blanda (magasinstil) – seedat på dagen så det är stabilt inom en dag
    random.seed(int(datetime.date.today().strftime("%Y%m%d")))
    random.shuffle(feed)
    return feed, len(news), len(pics)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Flödet – Veckodatabaser</title>
<link rel="alternate" type="application/rss+xml" title="Veckodatabaser – RSS" href="rss.xml">
<style>
  :root{--bg:#0f1226;--card:#1a1f3a;--card-h:#222848;--accent:#7c6cff;--accent2:#ff7ab8;--text:#eef0ff;--muted:#9aa0c7;--border:#2b3160;}
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:linear-gradient(160deg,#0f1226,#161a35);color:var(--text);min-height:100vh;padding:32px 18px 72px;}
  .wrap{max-width:1180px;margin:0 auto;}
  .eyebrow{color:var(--accent2);font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:12px;}
  h1{font-size:34px;margin:6px 0 8px;}
  .sub{color:var(--muted);font-size:15px;max-width:680px;line-height:1.55;}
  .bar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:22px 0 6px;}
  #search{flex:1;min-width:220px;background:var(--card);border:1px solid var(--border);color:var(--text);padding:11px 15px;border-radius:10px;font-size:15px;}
  #search::placeholder{color:var(--muted);}
  button.act{background:var(--card);border:1px solid var(--border);color:var(--text);padding:11px 16px;border-radius:10px;font-size:14px;cursor:pointer;transition:.15s;white-space:nowrap;}
  button.act:hover{border-color:var(--accent);background:var(--card-h);}
  .meta{color:var(--muted);font-size:13px;margin-top:4px;}
  .feed{column-width:330px;column-gap:18px;margin-top:22px;}
  .item{break-inside:avoid;margin:0 0 18px;background:var(--card);border:1px solid var(--border);border-radius:16px;overflow:hidden;transition:.15s;display:block;text-decoration:none;color:inherit;}
  .item:hover{background:var(--card-h);border-color:var(--accent);transform:translateY(-2px);}
  .item .body{padding:18px 18px 16px;}
  .chip{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:4px 10px;border-radius:999px;background:#2a2f55;color:#fff;}
  .item h3{font-size:17px;line-height:1.3;margin:11px 0 8px;}
  .item .summ{color:var(--text);opacity:.88;font-size:13.5px;line-height:1.55;}
  .foot{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:13px;color:var(--muted);font-size:12px;}
  .foot .src{font-weight:600;color:var(--text);opacity:.8;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
  .item.image .imgwrap{position:relative;line-height:0;}
  .item.image img{width:100%;height:auto;display:block;}
  .item.image .cap{padding:14px 18px 16px;}
  .item.image .cap h3{margin:9px 0 0;}
  .empty{color:var(--muted);text-align:center;padding:48px;}
  footer.page{margin-top:42px;color:var(--muted);font-size:12px;text-align:center;line-height:1.6;}
  a.back{color:var(--accent2);text-decoration:none;font-size:13px;}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <a class="back" href="index.html">← Till översikten</a>
    <div class="eyebrow" style="margin-top:10px;">Veckodatabaser</div>
    <h1>🌊 Flödet</h1>
    <p class="sub">Alla nyheter från dina ämnesdatabaser – blandade med bilder – i ett enda scrollbart flöde. Klicka på ett kort för att öppna källan.</p>
  </header>
  <div class="bar">
    <input id="search" type="text" placeholder="Sök i flödet…">
    <button class="act" id="shuffle">🔀 Blanda om</button>
  </div>
  <p class="meta" id="meta"></p>
  <section class="feed" id="feed"></section>
  <footer class="page">
    Automatiskt uppdaterad varje vecka · nyheter + bilder<br>
    Oberoende privat icke-kommersiellt projekt. Innehållet är korta egna sammanfattningar med länk till respektive originalkälla; all upphovsrätt tillhör respektive källa. Sidan är inte affilierad med, eller godkänd av, de personer, varumärken eller organisationer som omnämns. Bilder publiceras endast om de är egna, public domain eller licensierade.<br>
    Kontakt / rättelse av uppgift: gustaf.magaard@mdphd.se
  </footer>
</div>
<script>
const TOPICS = /*__TOPICS__*/{}/*__END_TOPICS__*/;
const FEED = /*__DATA__*/[]/*__END_DATA__*/;
const MONTHS=["jan","feb","mar","apr","maj","jun","jul","aug","sep","okt","nov","dec"];
function fmtDate(d){if(!d)return"";const p=d.split("-");if(p.length<3)return d;return parseInt(p[2],10)+" "+MONTHS[parseInt(p[1],10)-1]+" "+p[0];}
function esc(s){return (s||"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]));}
let order = FEED.map((_,i)=>i);
let query = "";

function shuffle(){
  for(let i=order.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[order[i],order[j]]=[order[j],order[i]];}
  render();
}
function matches(it){
  if(!query) return true;
  const t=(it.title+" "+it.summary+" "+it.category+" "+it.source+" "+(TOPICS[it.slug]?TOPICS[it.slug].label:"")).toLowerCase();
  return t.includes(query);
}
function card(it){
  const meta = TOPICS[it.slug] || {icon:"📰",label:it.category||"",color:"#7c6cff"};
  const chip = `<span class="chip" style="background:${meta.color}">${meta.icon} ${esc(meta.label)}</span>`;
  const date = fmtDate(it.date);
  const src = it.source ? esc(it.source) : "";
  const foot = `<div class="foot"><span class="src">${src}</span><span>${date}</span></div>`;
  const href = it.url ? ` href="${esc(it.url)}" target="_blank" rel="noopener"` : "";
  if(it.kind==="image"){
    return `<a class="item image"${href}>
      <div class="imgwrap"><img loading="lazy" src="${esc(it.image)}" alt="${esc(it.title)}"></div>
      <div class="cap">${chip}${it.title?`<h3>${esc(it.title)}</h3>`:""}${it.summary?`<p class="summ">${esc(it.summary)}</p>`:""}${(src||date)?foot:""}</div>
    </a>`;
  }
  return `<a class="item"${href}>
    <div class="body">${chip}<h3>${esc(it.title)}</h3><p class="summ">${esc(it.summary)}</p>${foot}</div>
  </a>`;
}
function render(){
  const feed=document.getElementById("feed");
  const list=order.map(i=>FEED[i]).filter(matches);
  document.getElementById("meta").textContent =
    list.length+" inlägg" + (query?" (filtrerade)":"") + " · " +
    FEED.filter(x=>x.kind==="news").length+" nyheter, " +
    FEED.filter(x=>x.kind==="image").length+" bilder";
  feed.innerHTML = list.length ? list.map(card).join("") :
    '<div class="empty">Inga inlägg matchar din sökning.</div>';
}
document.getElementById("search").addEventListener("input",e=>{query=e.target.value.toLowerCase().trim();render();});
document.getElementById("shuffle").addEventListener("click",shuffle);
render();
</script>
</body>
</html>
"""


def rfc822(datestr):
    try:
        d = datetime.datetime.strptime(datestr, "%Y-%m-%d").replace(
            tzinfo=datetime.timezone.utc)
    except Exception:
        d = datetime.datetime.now(datetime.timezone.utc)
    return email.utils.format_datetime(d)


def build_rss(news, limit=40):
    """Skriv rss.xml från nyhetsposterna (senaste först)."""
    def x(s):
        return html.escape(s or "", quote=True)

    items = [n for n in news if n.get("title")]
    items.sort(key=lambda n: n.get("date", ""), reverse=True)
    items = items[:limit]

    parts = []
    for n in items:
        label = TOPICS.get(n.get("slug"), (None, n.get("category", ""), None))[1]
        link = n.get("url") or (SITE_URL + "/")
        guid = n.get("url") or (SITE_URL + "/#" + n.get("title", ""))
        desc = n.get("summary", "")
        if n.get("source"):
            desc = (desc + " (Källa: " + n["source"] + ")") if desc else ("Källa: " + n["source"])
        parts.append(
            "    <item>\n"
            f"      <title>{x(n.get('title',''))}</title>\n"
            f"      <link>{x(link)}</link>\n"
            f"      <guid isPermaLink=\"false\">{x(guid)}</guid>\n"
            f"      <category>{x(label)}</category>\n"
            f"      <pubDate>{rfc822(n.get('date',''))}</pubDate>\n"
            f"      <description>{x(desc)}</description>\n"
            "    </item>")

    now = email.utils.format_datetime(datetime.datetime.now(datetime.timezone.utc))
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        '  <channel>\n'
        '    <title>Veckodatabaser</title>\n'
        f'    <link>{SITE_URL}/</link>\n'
        '    <description>Veckovis bevakning: kultur, psykologi, IT, religion, '
        'sport, ledarskap, personlig utveckling och katolsk social lära.</description>\n'
        '    <language>sv-SE</language>\n'
        f'    <lastBuildDate>{now}</lastBuildDate>\n'
        f'    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>\n'
        + "\n".join(parts) + "\n"
        '  </channel>\n'
        '</rss>\n')
    with open(os.path.join(HERE, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(rss)
    return len(items)


def main():
    feed, n_news, n_pics = build_feed()
    data_json = json.dumps(feed, ensure_ascii=False)
    topics_json = json.dumps(
        {slug: {"icon": ico, "label": lab, "color": col}
         for slug, (ico, lab, col) in TOPICS.items()},
        ensure_ascii=False)

    out = HTML_TEMPLATE
    out = out.replace("/*__TOPICS__*/{}/*__END_TOPICS__*/",
                      "/*__TOPICS__*/" + topics_json + "/*__END_TOPICS__*/")
    out = out.replace("/*__DATA__*/[]/*__END_DATA__*/",
                      "/*__DATA__*/" + data_json + "/*__END_DATA__*/")

    with open(os.path.join(HERE, "flode.html"), "w", encoding="utf-8") as f:
        f.write(out)

    n_rss = build_rss(collect_news())
    print(f"flode.html byggd: {n_news} nyheter + {n_pics} bilder = {len(feed)} inlagg")
    print(f"rss.xml byggd: {n_rss} poster")


if __name__ == "__main__":
    main()
