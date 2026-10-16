# Insertion professionnelle des diplômés MIAGE en France

Étudiant en L3 MIAGE (Réseau MIAGE) à l'Université Toulouse III Paul Sabatier,
je me suis demandé si mon choix de filière et de ville était pertinent en
termes de débouchés professionnels. Ce projet répond à trois questions à
partir des données officielles du ministère de l'Enseignement supérieur.

## Questions posées

1. Les diplômés MIAGE de Toulouse s'insèrent-ils aussi bien qu'ailleurs
   (Paris, Lyon, Bordeaux) ?
2. Comment l'Informatique se positionne-t-elle parmi les autres secteurs
   disciplinaires en France ?
3. Au sein même de l'Informatique, la MIAGE est-elle un bon choix par
   rapport aux autres diplômes ?

## Source des données

[Insertion professionnelle des diplômés](https://data.esr.gouv.fr) —
data.esr.gouv.fr (jeu `fr-esr-insersup`). ~1 million de lignes, données
2019-2024.

**Toutes les analyses portent sur des diplômés de niveau Master.** L'enquête
ne couvre pas la licence : les taux d'emploi et les salaires présentés ici
décrivent donc le débouché de la filière à son terme, pas celui d'un L3. C'est
précisément ce qui m'intéressait, puisque la question était de savoir où mène
la MIAGE.

## Méthodologie

- Filtrage sur les diplômés uniquement (exclusion des sortants non diplômés)
- Agrégation par ville/promotion (plusieurs universités par ville dans
  certains cas)
- Nettoyage des valeurs "nd" (secret statistique sur petits effectifs)
- Comparaison sur trois horizons (6, 12, 30 mois après le diplôme) pour
  distinguer vitesse d'insertion et insertion durable

## Résultats

### 1. MIAGE : Toulouse vs autres villes

![Taux d'emploi par ville](images/taux_emploi_miage_villes.png)
![Salaire par ville](images/salaire_miage_villes.png)

Toulouse se situe dans la moyenne sur le taux d'emploi. Sur le salaire en
revanche, l'écart avec Paris est net (environ 400-500€/mois), plus
probablement lié au coût de la vie et à la concentration d'entreprises en
Île-de-France qu'à une différence de qualité de formation.

### 2. L'Informatique parmi les secteurs disciplinaires

![Classement des secteurs](images/classement_secteurs.png)

L'Informatique se classe dans le top 25% des secteurs pour le taux d'emploi,
et se distingue par un très bon salaire médian.

### 3. La MIAGE au sein de l'Informatique

![Classement des diplômes informatique](images/classement_diplomes_info.png)

La MIAGE se classe parmi les meilleurs diplômes du secteur informatique,
devant le diplôme générique "Informatique".

## Limites

- Les moyennes ne sont pas pondérées par l'effectif réel de chaque diplôme
- Certaines villes (Lyon) reposent sur de petits échantillons, à
  interpréter avec prudence
- Données jusqu'à 30 mois post-diplôme uniquement pour les promotions
  2019-2023

## Conclusion

Choisir la MIAGE, c'est choisir une filière du secteur informatique déjà
favorisé en France qui performe mieux que la moyenne des diplômes
d'informatique eux-mêmes. Le choix de la ville influe surtout sur le
salaire, moins sur les chances d'obtenir un emploi.

## Utilisation

```bash
pip install -r requirements.txt
python exploration.py
```

Le fichier de données (`fr-esr-insersup.csv`) n'est pas versionné : il pèse
trop lourd pour le dépôt. Il faut le télécharger puis le placer à la racine
du projet.

1. Ouvrir la page du jeu de données :
   [fr-esr-insersup sur data.esr.gouv.fr](https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-insersup/)
2. Onglet **Export**, puis **CSV** — ou directement
   [ce lien de téléchargement](https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-insersup/download/?format=csv&use_labels_for_header=true).
3. Renommer le fichier en `fr-esr-insersup.csv` et le déposer à la racine.

Le jeu est mis à jour deux fois par an : les chiffres obtenus peuvent donc
différer légèrement de ceux commentés ci-dessus.
