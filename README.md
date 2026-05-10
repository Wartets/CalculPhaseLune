# CalculPhaseLune

Ce dépôt rassemble la reprise moderne d’un ancien projet Python consacré au calcul des phases de la Lune. L’idée de départ était déjà la bonne, mais la méthode a été entièrement retravaillée pour aller beaucoup plus loin : la théorie a été reprise proprement dans un document mathématique complet, puis la mise en œuvre numérique a été refaite dans un notebook Jupyter plus lisible, plus rigoureux et plus précis.

Le projet se découpe en deux pièces principales, étroitement liées :

- le document théorique, disponible dans [`phase_de_lune.pdf`](./phase_de_lune.pdf) et publié en ligne à l’adresse suivante : [version en ligne du PDF](https://wartets.github.io/Wartets/lib/assets/phase_de_lune.pdf)
- l’implémentation numérique, dans [`phase_lunaire_precision.ipynb`](./phase_lunaire_precision.ipynb)

## Ce que contient le projet

### Le document théorique

Le PDF rassemble toute la partie mathématique nécessaire pour construire un calcul précis de la phase lunaire. Il expose les fondations physiques du problème, la géométrie utilisée, les changements de repère, puis la définition exacte de la phase en tant qu’intersection de calottes sphériques sur la sphère lunaire.

Le cœur de l’approche repose sur une modélisation plus propre que dans la première version du projet. On y trouve notamment :

- la description du système Soleil Terre Lune dans un repère héliocentrique
- la géométrie des directions d’observation et d’illumination
- la définition topocentrique de la phase, dépendante de l’observateur
- la comparaison avec une fraction photométrique plus simple, utile pour la visualisation
- des variantes d’application, dont une version Terre observateur et une version depuis la surface de Jupiter

Le notebook reprend directement cette progression et suit la logique du PDF, notamment les équations de la partie d’application.

### Le notebook Jupyter

Le notebook [`phase_lunaire_precision.ipynb`](./phase_lunaire_precision.ipynb) est la version numérique du travail théorique. Il met en pratique les équations du document et organise le calcul de façon progressive :

- définition des constantes physiques et des paramètres orbitaux
- propagation ou reconstruction des éphémérides Terre Lune
- calcul de la position de l’observateur sur un corps en rotation
- évaluation de la phase lunaire topocentrique
- comparaison entre la phase exacte et la fraction photométrique
- affichage de courbes sur plusieurs cycles lunaires
- étude d’un cas plus exotique, avec observateur placé à la surface de Jupiter
- récupération ponctuelle de données réelles via JPL Horizons pour comparer avec des positions actuelles

Le notebook contient aussi des visualisations qui permettent de lire clairement le résultat du calcul, en particulier la visibilité locale de la Lune et l’évolution de la phase au cours du temps.

## Ancienne implémentation

Le dossier [`AncienneImplémentation`](./AncienneImplémentation) conserve le premier état du projet, celui qui servait de base avant la réécriture complète. Il s’agit de l’un de mes tout premiers projets Python, et il reste intéressant à consulter pour mesurer le chemin parcouru. Voir l'ancien [`README.md`](./AncienneImplémentation/README.md).

L’ancien README contenait aussi une visualisation GeoGebra qui reste pertinente pour interpréter le résultat visuellement : [visualisation GeoGebra](https://www.geogebra.org/m/mghvytp9).

## À propos du projet

Ce dépôt est donc une reprise complète d’un vieux projet, l’un de mes premiers essais sérieux en Python. La version initiale était déjà motivée par la même question, mais elle reposait sur une approche plus artisanale et beaucoup moins structurée. Cette nouvelle version garde l’idée de départ, tout en la réécrivant avec une base théorique solide, une organisation plus nette et une implémentation numérique beaucoup plus soignée.
