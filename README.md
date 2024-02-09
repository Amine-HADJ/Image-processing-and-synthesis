------------------------------------------------------------------------

PROJET TSI

HADJ-HAMDRI MOHAMMED-AMINE
TAHIRI EL ALAOUI YOUNESS

3ETI            GRP-D
2022 -- 2023

------------------------------------------------------------------------

Notre projet est un jeu vidéo 3D réalisé principalement grâce au module OPENGL de Python.

Pour lancer le jeu, exécutez le fichier 'main.py'.
Les touches utilisables sont listées à la fin de ce fichier.

L'objet principal du jeu est une voiture qui possède les capacités suivantes :

- Se déplacer dans toutes les directions.
- Sauter à partir du sol et retomber sous l'effet de la gravité.
- Tirer des projectiles sous la forme de balles de fusil.

Sur la carte, vous trouverez également des jetons (noirs et dorés) qui sont placés aléatoirement à chaque début d'une nouvelle partie.
Ces jetons tournent sur eux-mêmes autour de leur centre.
Lorsque la voiture s'approche suffisamment d'un jeton, celui-ci disparaît (gestion des collisions).

Pour déterminer si la voiture est suffisamment proche d'un jeton, nous utilisons la méthode suivante :

1. Nous récupérons la position de la voiture.
2. Nous récupérons la position du jeton.
3. Nous calculons la distance entre les deux positions.
4. Si la distance est inférieure à un certain seuil, nous considérons que la voiture est suffisamment proche du jeton.

La caméra est initialement positionnée à l'arrière de la voiture (vue à la 3ème personne), mais elle peut être orientée tout autour de la voiture en utilisant la souris.

Liste des touches utilisables pour interagir et jouer :

- Flèches directionnelles (HAUT, DROITE, BAS, GAUCHE) : permet de déplacer la voiture.
- ESPACE : permet d'effectuer un saut avec la voiture si elle est au sol.
- T : permet d'activer le "turbo" ou "boost" (vitesse plus élevée qu'avec la touche HAUT).
- Trackpad / Souris : permet de déplacer la caméra autour de la voiture.
- V : permet de repositionner la caméra à sa position initiale (derrière la voiture).
- SHIFT (gauche) : permet de tirer des projectiles qui disparaîtront au bout de 2 secondes.

------------------------------------------------------------------------
