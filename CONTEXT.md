# Tonus - CONTEXT

Créée le 2026-11-03. Demande de Simon : une petite PWA avec une UI sympa et un programme d'abdos à
domicile (gainage, crunchs...) et de musculation (pompes avec poignées, haltères), **10 minutes
maximum par jour**. Distincte de `../reprise-sport/` (autre projet, page statique).

## Ce que c'est

Une PWA **une seule page** (`index.html`, ~90 Ko, vanilla JS, zéro build, zéro dépendance) +
`sw.js` + `manifest.json` + `icons/`. Interface en français, thème clair / sombre (auto ou forcé
dans les réglages), pensée téléphone d'abord (colonne de 560 px max).

Quatre onglets en bas :
- **Aujourd'hui** : la séance du jour (carte en dégradé à la couleur de la séance, bonhomme animé,
  durée, niveau, matériel), bascule **10 min / 5 min**, « Changer de séance », bouton Démarrer ;
  semaine en 7 pastilles, série de jours, séances, minutes ; la liste des exercices du jour avec
  un mini bonhomme animé et la charge en kg (« ? kg » tant qu'elle n'est pas notée). Une fois la
  séance faite : « C'est fait ! » et la séance de demain. Carte « Bienvenue » + choix du niveau tant
  qu'il n'y a aucun historique ; bandeau « passer au niveau suivant » après 3 séances « facile ».
- **Programme** : principe (frise des 10 minutes), choix du niveau, les 5 séances avec « Lancer »
  et la pastille « Prochaine », bons réflexes.
- **Exercices** : les 31 exercices animés, filtres par catégorie ; une fiche par exercice
  (consignes, à éviter, plus facile / plus dur, séances où il apparaît, **charge en kg** avec
  boutons +/- et presets 2 à 20 kg, gardée par exercice).
- **Progrès** : série actuelle et record, séances, temps total, calendrier 18 semaines coloré par
  séance, répartition par séance, historique (suppression d'une ligne possible).

**Lecteur de séance** (plein écran) : barre de progression segmentée, phase (Prêt ?,
Échauffement, Exercice n / 8, Récup, Installe-toi, Retour au calme), grand bonhomme animé, nom,
côté et charge, anneau qui se vide avec les secondes, une consigne qui tourne toutes les 6 s,
précédent / pause / suivant, chrono écoulé / total. Pendant la récup, le bonhomme montre
l'exercice suivant (atténué). Bips 3-2-1 (Web Audio), **voix française** (speechSynthesis) qui
annonce l'exercice suivant pendant la récup, vibreur Android, **Wake Lock** (l'écran ne s'éteint
pas). Arrêter en cours : la séance compte quand même au-delà de 60 %. Écran de fin avec note
(Dur / Bien / Facile) et confettis. Le bouton retour d'Android ne ferme pas la séance, il propose
de l'arrêter.

## Le programme

Format d'une séance (10 min) : 5 s « Prêt ? », échauffement 60 s (jumping jacks 30 s + moulinets
de bras 30 s), 10 s pour s'installer, **8 exercices** séparés par une récup, retour au calme 50 s
(cobra 25 s + posture de l'enfant 25 s). Format **5 min** : jumping jacks 30 s, 4 exercices
(liste `express` de chaque séance), posture de l'enfant 30 s.

| Niveau | Effort | Récup | Durée (hors « Prêt ? ») |
|---|---|---|---|
| 1 Découverte | 30 s | 30 s | 9 min 30 |
| 2 Régulier (défaut) | 40 s | 20 s | 9 min 40 |
| 3 Solide | 45 s | 15 s | 9 min 45 |
| 4 Costaud | 50 s | 10 s | 9 min 50 |

**Rotation** (une séance par jour, chaque jour la suivante, un jour raté ne décale rien) :
`push -> pull -> core -> upper -> abs`. Ordre choisi pour ne jamais mettre deux jours de suite les
mêmes muscles du haut du corps (poussée puis tirage se suivent, c'est voulu ; les abdos reviennent
presque chaque jour, en variant).

- **Poussée & abdos** : pompes poignées, crunch, développé épaules, planche, pompes serrées,
  relevés de jambes, élévations latérales, mountain climbers.
- **Tirage & abdos** : rowing penché, crunch vélo, curl, superman, pull-over au sol, ciseaux, curl
  marteau, planche.
- **Gainage** : planche, dead bug, planche latérale D, bird dog, planche latérale G, pont fessier,
  toucher d'épaules, position creuse.
- **Haut du corps** : pompes poignées, rowing un bras D puis G, développé couché au sol, extension
  triceps, curl marteau, pompes serrées, pull-over.
- **Abdos brûlants** : mountain climbers, crunch, russian twist, crunch inversé, ciseaux, crunch
  vélo, rowing en planche, position creuse.

Matériel : poignées de pompes, haltères (1 ou 2), un tapis. Pas de banc, pas de barre.

## Les bonshommes animés (le morceau technique)

Pas d'images : chaque exercice est décrit par 2 à 8 **poses clés** dans `EX[id].frames`, et un
petit moteur dessine un bonhomme en SVG.
- Repère monde : profil, regard vers +x, **y vers le haut, sol en y = 0**. Longueurs : buste 20,
  cou 6,5, tête r 4,6, bras 11 + 10, jambe 14 + 14.
- Une pose = hanche `h`, angle du buste `t` (degrés, 0 = vers la droite, 90 = debout), angle de la
  tête `hd` (défaut = `t`), puis les **points d'appui** des mains (`hn` bras proche, `hf` bras
  lointain, défaut = `hn`) et des pieds (`fn`, `ff`). Coudes et genoux sont calculés par
  **cinématique inverse à deux os** ; `eb`/`ebf`/`kb`/`kbf` (+1 / -1) choisissent de quel côté
  plie l'articulation (+1 = côté anti-horaire de la ligne racine -> cible ; défaut coudes -1,
  genoux +1).
- Interpolation entre deux poses : un appui **identique dans les deux poses reste collé** (mains
  au sol des pompes) ; sinon on interpole les **angles** des segments (le curl tourne autour du
  coude, la jambe tendue décrit un arc). `world: true` sur un exercice interpole les points
  d'appui en ligne droite à la place (mountain climbers : sinon le pied traverse le sol).
- `tempo` = durée de chaque transition (nombre ou tableau, une valeur par pose, boucle sur la
  première). Une pose répétée = un temps de maintien (superman, pont fessier, bird dog).
- Vue de face pour jumping jacks, développé épaules, élévations latérales, russian twist : même
  moteur, `hn`/`hf` deviennent main gauche / main droite.
- Accessoires : `db` (`both`, `near`, `one` = un haltère tenu à deux mains), `handles` (poignées
  sous les mains de la première pose), `mat` (tapis, et le sol passe sous le tapis).
- Côté gauche d'un exercice unilatéral = la même figure **en miroir** (`data-m="1"`).
- Le cadrage (viewBox 4:3, sol en bas) est calculé automatiquement sur l'enveloppe des poses.
- Un **liseré** de la couleur du fond borde les membres du premier plan (à partir du milieu du
  segment, pour ne pas couper le buste) : c'est ce qui rend lisible un avant-bras devant la tête
  ou le buste (extension triceps, curl).
- Toutes les figures visibles sont animées par une seule boucle `requestAnimationFrame` ; elles se
  retirent seules quand leur élément quitte le DOM. `prefers-reduced-motion` : figures fixes.

**Vérifier une pose** : la planche de contrôle de la session de création rendait chaque exercice
à chaque pose clé via Chrome headless (script jetable, non gardé) ; le plus simple est d'ouvrir
l'onglet Exercices et la fiche de l'exercice.

## Données

`localStorage['tonus']` : `{ level, express, history: [{ at, d: 'AAAA-MM-JJ', s, lv, x, sec, feel,
partial? }], weights: { idExercice: kg }, voice, beep, vibe, theme, hintAt }`. Rien ne quitte
l'appareil. La séance du jour = la suivante de la dernière faite dans `ROT`.

## Lancer / livrer

- Local : `python -m http.server 8132` dans `tonus/` (config `tonus` dans le `.claude/launch.json`
  du dépôt parent). Ouvrir `index.html` en double-clic marche aussi (sans service worker).
- Version : `APP_VERSION` + `APP_BUILT` en tête du script ; le cache du service worker
  (`tonus-v<APP_VERSION>`) en dérive via `sw.js?v=`. **Bumper les deux à chaque livraison**, même
  pour un test (worker cache-first sur les ressources). `id` du manifeste : `/tonus/app`, à ne
  plus changer une fois installée.
- Icônes : `python tools/build_icons.py` (depuis `tonus/`, sans `-I` : PIL est dans le
  site-packages utilisateur) écrit `icons/icon.svg` et rend les PNG 192 / 512 / maskable 512 avec
  Chrome headless.

## Statut

- **v1 (2026-11-03)** : livrée en local, **pas encore en ligne ni sous git**. Testée dans le
  navigateur intégré au format téléphone : accueil, programme, exercices, fiche + charge,
  progrès, thème sombre, et une séance complète d'un bout à l'autre (16 étapes, fin, note,
  historique, état « C'est fait »), miroir du côté gauche, récup. Pas encore testé sur un vrai
  téléphone : voix, vibreur et Wake Lock dépendent du navigateur.
- Pour la mettre en ligne : dépôt public `kkjsf/tonus` + GitHub Pages (comme `ciel/`, par
  l'interface web, push SSH). Rien de personnel dans le code.

## Pièges

- Dans le panneau navigateur de Claude Code (page en arrière-plan), les animations CSS et
  `requestAnimationFrame` tournent au ralenti : une capture prise juste après un chargement montre
  la vue à moitié fondue. Ce n'est pas un bug de l'app (`document.getAnimations().forEach(a =>
  a.finish())` avant la capture).
- `navigator.vibrate` est refusé tant qu'il n'y a pas eu un vrai tap : normal si on lance une
  séance par script pour tester.
- Une variable CSS posée sur `.fig` lui-même écrase celle héritée du parent : `--fig` (couleur du
  bonhomme) a son défaut sur `:root`, et chaque carte la pose sur l'élément ou un parent.

## Idées pour la suite

- Rappel quotidien (notification) : demanderait `periodicSync` comme l'alerte gel de Ciel.
- Export / import de l'historique (fichier JSON) pour changer de téléphone.
- Une séance « mobilité » pour les lendemains de grosse sortie trail ou vélo.

---
Index de tous les projets perso et règles de travail : **`../AGENTS.md`** (lisible par
n'importe quel assistant IA). Transfert vers une autre machine / un autre compte / une autre IA :
**`../HANDOFF.md`**.
