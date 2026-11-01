#!/usr/bin/env python3
"""Render the two static marketing pages; no build service or dependencies needed."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://flovflo.github.io/reelfin-site/'
STORE = 'https://apps.apple.com/app/reelfin/id6762079357'
DOWNLOAD = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M24 6v25m-9-9 9 9 9-9M10 32v9h28v-9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICONS = {
 'mobile': '<rect x="5" y="5" width="20" height="31" rx="3"/><path d="M12 31h6"/><rect x="27" y="13" width="12" height="25" rx="2"/>',
 'tv': '<rect x="3" y="6" width="36" height="24" rx="3"/><path d="M15 36h12m-6-6v6"/>',
 'mac': '<rect x="7" y="6" width="28" height="23" rx="2"/><path d="m7 29-4 7h36l-4-7M17 33h8"/>'
}
COPY = {
'en': {
 'path':'index.html', 'prefix':'', 'title':'ReelFin — Your cinema. Your way.',
 'description':'Your Jellyfin library on iPhone, iPad and Apple TV. Resume your favourites, explore your collection and take compatible downloads with you. Native. Independent. Yours.',
 'skip':'Skip to content', 'nav':'Primary navigation', 'app':'The app', 'faq':'FAQ', 'menu':'Open navigation',
 'h1':'Your cinema.', 'h1b':'Your way.',
 'intro':'A native Jellyfin experience, made for iPhone Duo.<br>Your library on iPhone, iPad and Apple TV.',
 'download':'Download on the App Store', 'credit':'Demonstration library · Fictional artwork · Movies and shows not included',
 'benefit':'Less browsing.', 'benefitb':'More watching.', 'benefitintro':'From one more episode to a new favourite. Everything you came to watch, one tap away.',
 'resume':'Pick up the story.', 'resumebody':'Your Continue Watching, synced with Jellyfin. Get back to the film or episode you left behind.',
 'library':'Your collection, within reach.', 'librarybody':'Your films, your shows, your collections. Find them on your own Jellyfin server.',
 'downloads':'Take the next episode.', 'downloadsbody':'Download compatible films and shows on iPhone and iPad. Your library travels with you.',
 'downloadlabel':'Ready for the journey', 'downloadsmall':'Compatible media · iPhone & iPad',
 'tvtitle':'Made for the<br>big screen.', 'tvbody':'A home for your library.<br>Built for the remote.',
 'tv1':'Remote-first navigation', 'tv1body':'Clear focus, generous artwork and a native experience designed for the couch.',
 'tv2':'Your audio. Your subtitles.', 'tv2body':'Choose from the tracks available for your title, right where you watch.',
 'tv3':'Direct Play when compatible', 'tv3body':'Play your original media when the file and device support it. Jellyfin can help when needed.',
 'everywhere':'At home.<br>On the move.', 'future':'In development',
 'duotitle':'Made for<br><span class="muted">iPhone Duo.</span>', 'duobody':'Your library on the big inner screen.<br>Your next episode on the outer screen.',
 'duolink':'Explore the iPhone Duo experience', 'duoplatform':'Made for iPhone Duo',
 'duo1':'Room for your library.', 'duo1body':'Open iPhone Duo to browse your Home and library rows on the larger inner screen.',
 'duo2':'Navigation within reach.', 'duo2body':'Main sections and back controls stay accessible, with layouts that respect the screen’s usable space.',
 'duo3':'Back to your episode.', 'duo3body':'Open a series and find the episode you were watching, with your progress ready to resume.',
 'duoalt':'Native ReelFin demonstration Home on the large inner screen of iPhone Duo, with the device open.',
 'duoouteralt':'Native ReelFin demonstration movie detail on the compact iPhone Duo outer screen.',
 'duoseriesalt':'Native ReelFin demonstration series detail and Resume action on the iPhone Duo outer screen, with the device closed.',
 'duocaption':'iPhone Duo open and closed · Demonstration library · Content not included',
 'duohomelabel':'Open · Your library', 'duoserieslabel':'Closed · Resume your series',
 'faqtitle':'A few things<br>to know.',
 'questions':[
  ('Do I need a Jellyfin server?', 'Yes. ReelFin is a client for your own Jellyfin server, or a server you are authorised to use. Enter the server address and sign in to your Jellyfin account.'),
  ('Does ReelFin include movies or shows?', 'No. You bring your library. The screenshots and poster artwork on this page use a fictional demonstration collection; no movies or shows are supplied with the app.'),
  ('Will every file Direct Play?', 'Direct Play depends on the file, codecs, subtitles and device. ReelFin uses native Apple playback, and Jellyfin may remux or transcode a file when it needs help.'),
  ('Can I watch offline?', 'On iPhone and iPad, you can download compatible titles when your Jellyfin account allows downloads. File compatibility and available storage still apply. Downloads are not available on Apple TV.'),
  ('How does ReelFin handle privacy?', 'Your session token is stored in Apple Keychain. ReelFin does not sell your personal data or use cross-app tracking. Optional crash diagnostics may be enabled in a production build. <a href="{prefix}privacy.html">Read the privacy policy</a>.'),
  ('Is ReelFin available on Mac?', 'A dedicated Mac experience is in development. It is not available for public download yet. ReelFin is currently available for iPhone, iPad and Apple TV.')
 ],
 'closing':'Press play on<br>your library.', 'closingbody':'On the App Store. Connect your own Jellyfin server.',
 'support':'Support', 'beta':'Join the beta', 'privacy':'Privacy', 'terms':'Terms',
 'applecredit':'Apple, Apple TV, iPhone, iPad, Mac, App Store and TestFlight are trademarks of Apple Inc., registered in the U.S. and other countries.',
 'footer':'An independent client for your own Jellyfin library. Not affiliated with Jellyfin.',
 'tvalt':'ReelFin Apple TV home screen, using a fictional demonstration library.',
 'phonealt':'ReelFin on iPhone, with Continue Watching and films from a fictional demonstration library.',
 'tvdetailalt':'ReelFin Apple TV movie detail page, using a fictional demonstration library.',
 'detailalt':'ReelFin on iPhone shows a fictional series, episode progress and the Resume action.',
 'mosaicphone':'Your server.<br>Your library.', 'mosaiccentral':'Mac · In development',
 'mosaictag':'A native client for your Jellyfin.', 'mosaicduo':'Made for iPhone Duo',
 'mosaicdirect':'Native playback.<br>Your original file.', 'mosaicdirectbody':'Direct Play when the file and device support it.',
 'mosaicserver':'Your media.<br>Your Jellyfin.', 'mosaicserverbody':'Connect your own server. No catalogue included.',
 'storytitle':'One library.<br>Across your screens.',
 'storybody':'Your library, one screen at a time. Scroll through ReelFin.',
 'storynav':'Explore the app',
 'storytvalt':'ReelFin on Apple TV, using a fictional demonstration library.',
 'storyphonealt':'ReelFin on iPhone, using a fictional demonstration library.',
 'storychapters':[
  ('library','Library','Your server.<br>Your cinema.','Find your library rows and Continue Watching on Apple TV. Your own Jellyfin server supplies the collection.'),
  ('series','Series','Find<br>your series.','Its episodes and your progress, in a detail page made for the big screen.'),
  ('resume','Resume','The next episode.<br>On iPhone.','Find the episode you were watching and pick up where you left off.')
 ],
 'platformlabel':'Supported platforms'
},
'fr': {
 'path':'fr/index.html', 'prefix':'../', 'title':'ReelFin — Votre cinéma. À vous.',
 'description':'Votre médiathèque Jellyfin sur iPhone, iPad et Apple TV. Reprenez vos favoris, explorez vos collections et emportez vos téléchargements compatibles. Natif. Indépendant. À vous.',
 'skip':'Aller au contenu', 'nav':'Navigation principale', 'app':'L’app', 'faq':'FAQ', 'menu':'Ouvrir la navigation',
 'h1':'Votre cinéma.', 'h1b':'À vous.',
 'intro':'L’expérience Jellyfin native, optimisée pour iPhone Duo.<br>Votre médiathèque sur iPhone, iPad et Apple TV.',
 'download':'Télécharger sur l’App Store', 'credit':'Bibliothèque de démonstration · Affiches fictives · Films et séries non inclus',
 'benefit':'Moins chercher.', 'benefitb':'Plus regarder.', 'benefitintro':'Un épisode de plus ou un nouveau coup de cœur. Tout ce que vous aimez regarder, à portée de main.',
 'resume':'Retrouvez le fil.', 'resumebody':'Votre reprise de lecture, synchronisée avec Jellyfin. Reprenez le film ou l’épisode que vous aviez laissé.',
 'library':'Votre collection, à portée de main.', 'librarybody':'Vos films, vos séries, vos collections. Retrouvez-les depuis votre serveur Jellyfin.',
 'downloads':'La suite vous accompagne.', 'downloadsbody':'Téléchargez les films et séries compatibles sur iPhone et iPad. Votre médiathèque voyage avec vous.',
 'downloadlabel':'Prêt pour le voyage', 'downloadsmall':'Médias compatibles · iPhone et iPad',
 'tvtitle':'Pensé pour<br>le grand écran.', 'tvbody':'Votre médiathèque prend ses aises.<br>La télécommande aussi.',
 'tv1':'La télécommande en tête', 'tv1body':'Un focus visible, de grandes images et une expérience native pensée pour le canapé.',
 'tv2':'Votre son. Vos sous-titres.', 'tv2body':'Choisissez parmi les pistes disponibles pour votre film ou votre épisode, pendant la lecture.',
 'tv3':'Direct Play si compatible', 'tv3body':'Lisez le fichier original lorsque le média et l’appareil le permettent. Jellyfin prend le relais si nécessaire.',
 'everywhere':'Chez vous.<br>Et partout.', 'future':'En préparation',
 'duotitle':'Optimisé pour<br><span class="muted">iPhone Duo.</span>', 'duobody':'Votre médiathèque sur le grand écran intérieur.<br>La suite de votre série sur l’écran extérieur.',
 'duolink':'Découvrir l’expérience iPhone Duo', 'duoplatform':'Optimisé pour iPhone Duo',
 'duo1':'De la place pour votre médiathèque.', 'duo1body':'Ouvrez l’iPhone Duo et retrouvez votre accueil et vos rangées sur le grand écran intérieur.',
 'duo2':'Les commandes à portée de main.', 'duo2body':'Navigation et retour restent accessibles, dans une interface qui respecte l’espace utile de l’écran.',
 'duo3':'Retrouvez votre épisode.', 'duo3body':'Ouvrez une série et retrouvez l’épisode en cours, avec votre progression pour reprendre la suite.',
 'duoalt':'Accueil natif ReelFin en démonstration sur le grand écran intérieur de l’iPhone Duo ouvert.',
 'duoouteralt':'Fiche native ReelFin en démonstration sur l’écran extérieur compact de l’iPhone Duo.',
 'duoseriesalt':'Fiche de série native ReelFin en démonstration avec l’action Reprendre sur l’écran extérieur de l’iPhone Duo fermé.',
 'duocaption':'iPhone Duo ouvert et fermé · Bibliothèque de démonstration · Contenus non inclus',
 'duohomelabel':'Ouvert · Votre médiathèque', 'duoserieslabel':'Fermé · Reprendre votre série',
 'faqtitle':'Avant<br>de lancer.',
 'questions':[
  ('Faut-il un serveur Jellyfin ?', 'Oui. ReelFin se connecte à votre propre serveur Jellyfin ou à un serveur que vous êtes autorisé à utiliser. Saisissez son adresse puis connectez-vous à votre compte Jellyfin.'),
  ('ReelFin fournit-il des films ou séries ?', 'Non. Vous apportez votre médiathèque. Les captures et les affiches présentées ici utilisent une collection de démonstration fictive ; aucun film ni aucune série ne sont fournis avec l’app.'),
  ('Tous les fichiers passent-ils en Direct Play ?', 'Direct Play dépend du fichier, des codecs, des sous-titres et de l’appareil. ReelFin utilise la lecture native Apple ; Jellyfin peut remuxer ou transcoder les fichiers qui en ont besoin.'),
  ('Peut-on regarder hors ligne ?', 'Sur iPhone et iPad, vous pouvez télécharger des titres compatibles si votre compte Jellyfin autorise les téléchargements. La compatibilité et l’espace disponible restent nécessaires. Les téléchargements ne sont pas disponibles sur Apple TV.'),
  ('Comment mes données sont-elles traitées ?', 'Votre jeton de session est conservé dans le trousseau Apple. ReelFin ne vend pas vos données et ne fait pas de suivi entre les apps. Des diagnostics de plantage facultatifs peuvent être activés dans une version de production. <a href="{prefix}privacy.html">Lire la politique de confidentialité (en anglais)</a>.'),
  ('ReelFin est-il disponible sur Mac ?', 'Une expérience dédiée au Mac est en préparation. Elle n’est pas encore disponible au téléchargement public. ReelFin est actuellement disponible sur iPhone, iPad et Apple TV.')
 ],
 'closing':'Votre médiathèque.<br>Appuyez sur lecture.', 'closingbody':'Sur l’App Store. Connectez votre propre serveur Jellyfin.',
 'support':'Assistance', 'beta':'Rejoindre la bêta', 'privacy':'Confidentialité', 'terms':'Conditions',
 'applecredit':'Apple, Apple TV, iPhone, iPad, Mac, App Store et TestFlight sont des marques d’Apple Inc., déposées aux États-Unis et dans d’autres pays.',
 'footer':'Un client indépendant pour votre médiathèque Jellyfin. Sans affiliation avec Jellyfin.',
 'tvalt':'Accueil ReelFin sur Apple TV, avec une bibliothèque fictive de démonstration.',
 'phonealt':'ReelFin sur iPhone, avec la reprise de lecture et une bibliothèque de démonstration fictive.',
 'tvdetailalt':'Fiche d’un film fictif de démonstration dans ReelFin sur Apple TV.',
 'detailalt':'Fiche native ReelFin sur iPhone avec une série fictive, sa progression et l’action Reprendre.',
 'mosaicphone':'Votre serveur.<br>Votre bibliothèque.', 'mosaiccentral':'Mac · En préparation',
 'mosaictag':'Votre client Jellyfin natif.', 'mosaicduo':'Optimisé pour iPhone Duo',
 'mosaicdirect':'Lecture native.<br>Fichier original.', 'mosaicdirectbody':'Direct Play si le média et l’appareil le permettent.',
 'mosaicserver':'Vos médias.<br>Votre Jellyfin.', 'mosaicserverbody':'Connectez votre serveur. Aucun catalogue inclus.',
 'storytitle':'Une médiathèque.<br>D’un écran à l’autre.',
 'storybody':'Votre médiathèque, d’un écran à l’autre. Parcourez ReelFin en faisant défiler la page.',
 'storynav':'Parcourir l’app',
 'storytvalt':'ReelFin sur Apple TV, avec une bibliothèque fictive de démonstration.',
 'storyphonealt':'ReelFin sur iPhone, avec une bibliothèque fictive de démonstration.',
 'storychapters':[
  ('library','Médiathèque','Votre serveur.<br>Votre cinéma.','Retrouvez vos rangées et votre reprise de lecture sur Apple TV. Votre serveur Jellyfin fournit la collection.'),
  ('series','Séries','Retrouvez<br>votre série.','Ses épisodes et votre progression, dans une fiche pensée pour le grand écran.'),
  ('resume','Reprise','La suite,<br>sur iPhone.','Retrouvez l’épisode en cours et reprenez là où vous l’aviez laissé.')
 ],
 'platformlabel':'Plateformes compatibles'
}}


MEDIA_SIZES = {
 'tv': '(max-width: 760px) 100vw, (max-width: 1100px) 78vw, 930px',
 'iphone': '(max-width: 760px) 190px, 240px',
 'duo-open': '(max-width: 760px) 100vw, 750px',
 'duo-closed': '(max-width: 760px) 51vw, 382px',
 'story-tv': '(min-width: 1100px) 52vw, 100vw',
 'story-phone': '(min-width: 1100px) 15vw, 190px',
}

def mockup(prefix, name, alt, kind, eager=False):
 data=json.loads((ROOT/'assets/media/devices/provenance.json').read_text())
 item=next(m for m in data['mockups'] if m['file']==name+'.webp')
 variants=item.get('responsive',[])+[item]
 srcset=', '.join(f"{prefix}assets/media/devices/{v['file']} {v['width']}w" for v in variants)
 first=variants[0]['file']
 loading='fetchpriority="high"' if eager else 'loading="lazy"'
 return f'<img src="{prefix}assets/media/devices/{first}" srcset="{srcset}" sizes="{MEDIA_SIZES[kind]}" alt="{alt}" width="{item["width"]}" height="{item["height"]}" {loading} decoding="async">'


def mac_preview(prefix, lang):
 meta=json.loads((ROOT/'assets/media/devices/mac-preview.json').read_text())
 variants=meta['variants']
 srcset=', '.join(f"{prefix}assets/media/devices/{v['file']} {v['width']}w" for v in variants)
 alt='Native ReelFin Home preview on Mac, in development, with a fictional demonstration library.' if lang=='en' else 'Aperçu natif de l’accueil ReelFin sur Mac, en préparation, avec une bibliothèque fictive de démonstration.'
 return f'<img src="{prefix}assets/media/devices/{variants[0]["file"]}" srcset="{srcset}" sizes="(max-width: 599px) 320px, (max-width: 1099px) 55vw, 600px" alt="{alt}" width="1600" height="1150" fetchpriority="high" decoding="async">'

def screen_overlay(prefix, name, kind, css):
 data=json.loads((ROOT/'assets/media/devices/provenance.json').read_text())
 item=next(m for m in data['mockups'] if m['file']==name+'.webp')
 overlay=item['uiOnlyOverlay']
 variants=overlay.get('responsive',[])+[dict(overlay,width=item['width'])]
 srcset=', '.join(f"{prefix}assets/media/devices/{v['file']} {v['width']}w" for v in variants)
 return f'<img class="story__screen {css}" data-story-src="{prefix}assets/media/devices/{variants[0]["file"]}" data-story-srcset="{srcset}" sizes="{MEDIA_SIZES[kind]}" width="{item["width"]}" height="{item["height"]}" alt="" aria-hidden="true" hidden>'

def render(lang, c):
 p=c['prefix']
 brand=f'<span class="brand__mark" aria-hidden="true"><img src="{p}assets/media/NEW/reelfin-mark.png" alt="" width="400" height="240"></span><span>ReelFin</span>'
 cta=f'<a class="button button--primary" href="{STORE}"><span>{c["download"]}</span><span class="arrow" aria-hidden="true">↗</span></a>'
 story_nav=''.join(f'<a href="#story-{key}" data-story-link="{i}"><span>0{i+1}</span>{label}</a>' for i,(key,label,heading,body) in enumerate(c['storychapters']))
 story_chapters=''
 for i,(key,label,heading,body) in enumerate(c['storychapters']):
  name,kind,alt=('tv-home','tv',c['tvalt']) if i==0 else ('tv-series','tv',c['storytvalt']) if i==1 else ('iphone-series','iphone',c['detailalt'])
  story_chapters+=f'<article class="story__chapter" id="story-{key}"><div class="story__chapter-copy"><span class="story__number">0{i+1}</span><h3>{heading}</h3><p>{body}</p></div><figure class="story__chapter-visual story__chapter-visual--{kind} device-artwork">{mockup(p,name,alt,kind)}</figure></article>'
 questions='\n'.join(f'<details><summary>{q}</summary><p>{a.format(prefix=p)}</p></details>' for q,a in c['questions'])
 page=f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{c['title']}</title>
  <meta name="description" content="{c['description']}">
  <meta name="theme-color" content="#101113">
  <meta name="apple-itunes-app" content="app-id=6762079357">
  <link rel="canonical" href="{BASE}{'' if lang=='en' else 'fr/'}">
  <link rel="alternate" hreflang="en" href="{BASE}">
  <link rel="alternate" hreflang="fr" href="{BASE}fr/">
  <link rel="alternate" hreflang="x-default" href="{BASE}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{c['title']}">
  <meta property="og:description" content="{c['description']}">
  <meta property="og:url" content="{BASE}{'' if lang=='en' else 'fr/'}">
  <meta property="og:locale" content="{'en_US' if lang=='en' else 'fr_FR'}">
  <meta property="og:image" content="{BASE}assets/media/cinema/social-{lang}.jpg">
  <meta property="og:image:alt" content="{c['title']}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="{p}assets/media/NEW/reelfin-mark.png">
  <link rel="stylesheet" href="{p}assets/site.css?v=cinema-19">
  <script defer src="{p}assets/site.js?v=cinema-19"></script>
  <script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@type':'MobileApplication','name':'ReelFin','operatingSystem':'iOS 26+, iPadOS 26+, tvOS 26+','applicationCategory':'EntertainmentApplication','description':c['description'],'url':BASE,'downloadUrl':STORE,'author':{'@type':'Person','name':'Florian Taffin'}},ensure_ascii=False)}</script>
</head>
<body>
  <a class="skip-link" href="#main-content">{c['skip']}</a>
  <header class="site-header site-header--marketing">
    <div class="site-header__inner">
      <a class="brand" href="#top" aria-label="ReelFin">{brand}</a>
      <nav class="site-nav" aria-label="{c['nav']}"><a href="#story">{c['app']}</a><a href="#duo">iPhone Duo</a><a href="#tvos">Apple TV</a><a href="#faq">{c['faq']}</a></nav>
      <nav class="language-switch" aria-label="{'Language' if lang=='en' else 'Langue'}"><a href="{p}index.html" lang="en" hreflang="en" {'aria-current="page"' if lang=='en' else ''}>EN</a><span aria-hidden="true">/</span><a href="{p}fr/index.html" lang="fr" hreflang="fr" {'aria-current="page"' if lang=='fr' else ''}>FR</a></nav>
      <a class="button button--primary site-header__cta" href="{STORE}">App Store <span class="arrow" aria-hidden="true">↗</span></a>
      <button class="menu-toggle" aria-expanded="false" aria-controls="mobile-menu" aria-label="{c['menu']}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 8h16M4 16h16"/></svg></button>
    </div>
    <nav class="mobile-menu" id="mobile-menu" aria-label="{c['nav']}" hidden><a href="#story">{c['app']}</a><a href="#duo">iPhone Duo</a><a href="#tvos">Apple TV</a><a href="#faq">{c['faq']}</a><a href="{STORE}">{c['download']} ↗</a></nav>
  </header>
  <main id="main-content">
    <section class="hero container" id="top" aria-labelledby="hero-title">
      <div class="hero__mosaic">
        <div class="mosaic__tile mosaic__phone">
          <p class="mosaic__statement">{c['mosaicphone']}</p>
          <figure class="device-artwork">{mockup(p,'iphone-home',c['phonealt'],'iphone',eager=True)}</figure>
        </div>
        <figure class="mosaic__tile mosaic__screen">
          <figcaption>{c['mosaiccentral']}</figcaption>
          <div class="native-mac-preview">{mac_preview(p,lang)}</div>
        </figure>
        <div class="mosaic__tile mosaic__brand">
          <div class="hero-emblem" aria-hidden="true"><img src="{p}assets/media/NEW/reelfin-mark.png" alt="" width="400" height="240"></div>
          <div class="mosaic__brand-copy"><h1 id="hero-title">ReelFin</h1><p>{c['mosaictag']}</p><p class="hero__platforms">iPhone · iPad · Apple TV</p></div>
        </div>
        <div class="mosaic__tile mosaic__duo">
          <figure class="device-artwork">{mockup(p,'duo-closed-series',c['duoseriesalt'],'duo-closed',eager=True)}</figure>
          <a href="#duo">{c['mosaicduo']} <span aria-hidden="true">↓</span></a>
        </div>
        <article class="mosaic__tile mosaic__direct"><h2>{c['mosaicdirect']}</h2><p>{c['mosaicdirectbody']}</p></article>
        <article class="mosaic__tile mosaic__server"><h2>{c['mosaicserver']}</h2><p>{c['mosaicserverbody']}</p></article>
      </div>
      <p class="image-credit">{c['credit']}</p>
    </section>
    <section class="section container product-story" id="story" aria-labelledby="story-title">
      <div class="section-heading"><h2 id="story-title">{c['storytitle']}</h2><p>{c['storybody']}</p></div>
      <nav class="story__nav" aria-label="{c['storynav']}">{story_nav}</nav>
      <div class="story__layout">
        <div class="story__stage">
          <div class="story__devices">
            <figure class="story__tv device-artwork">{mockup(p,'tv-home',c['storytvalt'],'story-tv')}{screen_overlay(p,'tv-series','story-tv','story__screen--tv')}</figure>
            <figure class="story__phone device-artwork">{mockup(p,'iphone-home',c['storyphonealt'],'story-phone')}{screen_overlay(p,'iphone-series','story-phone','story__screen--phone')}</figure>
          </div>
          <div class="story__position" aria-hidden="true"><span class="story__position-line"></span><span class="story__counter">01 / 03</span></div>
          <p class="image-credit">{c['credit']}</p>
        </div>
        <div class="story__chapters">{story_chapters}</div>
      </div>
    </section>
    <section class="section container duo" id="duo" aria-labelledby="duo-title">
      <div class="section-heading"><h2 id="duo-title">{c['duotitle']}</h2><p>{c['duobody']}</p></div>
      <div class="duo-stage">
        <figure class="duo-stage__open"><div class="device-artwork">{mockup(p,'duo-open-home',c['duoalt'],'duo-open',eager=False)}</div><figcaption>{c['duohomelabel']}</figcaption></figure>
        <figure class="duo-stage__closed"><div class="device-artwork">{mockup(p,'duo-closed-series',c['duoseriesalt'],'duo-closed',eager=False)}</div><figcaption>{c['duoserieslabel']}</figcaption></figure>
      </div>
      <p class="image-credit">{c['duocaption']}</p>
      <div class="tv-benefits"><article><h3>{c['duo1']}</h3><p>{c['duo1body']}</p></article><article><h3>{c['duo2']}</h3><p>{c['duo2body']}</p></article><article><h3>{c['duo3']}</h3><p>{c['duo3body']}</p></article></div>
    </section>
    <section class="download-band container" id="overview" aria-labelledby="downloads-title"><h2 id="downloads-title">{c['downloads']}</h2><div><p>{c['downloadsbody']}</p><p class="download-band__note">{c['downloadsmall']}</p></div></section>
    <section class="section container tvos" id="tvos" aria-labelledby="tv-title">
      <div class="section-heading"><h2 id="tv-title">{c['tvtitle']}</h2><p>{c['tvbody']}</p></div>
      <figure class="device-artwork">{mockup(p,'tv-detail',c['tvdetailalt'],'tv',eager=False)}</figure>
      <div class="tv-benefits"><article><h3>{c['tv1']}</h3><p>{c['tv1body']}</p></article><article><h3>{c['tv2']}</h3><p>{c['tv2body']}</p></article><article><h3>{c['tv3']}</h3><p>{c['tv3body']}</p></article></div>
    </section>
    <section class="compatibility container" aria-label="{c['platformlabel']}">
      <h2>{c['everywhere']}</h2>
      <div class="platform"><svg viewBox="0 0 42 42" fill="none" stroke="currentColor" aria-hidden="true">{ICONS['mobile']}</svg><h3>iPhone &amp; iPad</h3><p>iOS / iPadOS 26+</p></div>
      <div class="platform"><svg viewBox="0 0 42 42" fill="none" stroke="currentColor" aria-hidden="true">{ICONS['tv']}</svg><h3>Apple TV</h3><p>tvOS 26+</p></div>
      <div class="platform platform--future"><svg viewBox="0 0 42 42" fill="none" stroke="currentColor" aria-hidden="true">{ICONS['mac']}</svg><h3>Mac</h3><p>{c['future']}</p></div>
    </section>
    <section class="section container faq" id="faq" aria-labelledby="faq-title"><h2 id="faq-title">{c['faqtitle']}</h2><div>{questions}</div></section>
    <section class="final-cta container" id="support" aria-labelledby="download-title"><div class="cta-emblem" aria-hidden="true"><img src="{p}assets/media/NEW/reelfin-mark.png" alt="" width="400" height="240"></div><h2 id="download-title">{c['closing']}</h2>{cta}<p>{c['closingbody']}</p><div class="final-cta__support"><a href="{p}support.html">{c['support']} ↗</a><a href="https://testflight.apple.com/join/TkVVXmU2">{c['beta']} ↗</a></div></section>
  </main>
  <footer class="site-footer" id="privacy"><div><a class="brand brand--footer" href="#top">{brand}</a><p>{c['footer']}</p><p class="site-footer__credit">{c['applecredit']}</p></div><nav class="site-footer__links" aria-label="{'Footer' if lang=='en' else 'Pied de page'}"><a href="{p}support.html">{c['support']}</a><a href="{p}privacy.html">{c['privacy']}</a><a href="{p}terms.html">{c['terms']}</a></nav></footer>
</body>
</html>
'''
 target=ROOT/c['path']; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(page)

if __name__=='__main__':
 for lang,copy in COPY.items(): render(lang,copy)
 print('Rendered index.html and fr/index.html')
