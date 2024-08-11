# Rapport de projet

## Groupe
* AIRED Matthias
* TAHIR Aans 28710067

## Description des choix importants d'implémentation

Blablabla

## Description des stratégies proposées

Nous avons en tout 4 stratégies :

-La stratégie aleatoire() qui n'est pas vraiment une stratégie car le joueur choisit d'abord au hasard 
si il va placer un mur ou avancer. S'il décide de placer un mur, il choisit une position un emplacement au hasard. 

-La 1ère vraie stratégie strat1() consiste à toujours avancer et ne jamais poser de murs.

-La 2ème stratégie consiste à placer un mur bloquant le chemin de l'adversaire si l'adversaire a un chemin plus court que le notre jusqu'à son objectif. On place un mur que s'il ne rallonge pas notre distance à 
notre objectif, s'il n'est pas handicapant pour nous. 

-La 3ème stratégie est une ouverture, on place dès que possible un mur au centre du plateau puis en placer un autre collé (si possible) du côté vers lequel l'adversaire va. Par exemple si l'adversaire se décale vers la gauche pour éviter le premier mur, on place un autre mur collé au premier du côté du joueur pour allonger son chemin et l'obliger à changer de direction. Le reste du temps le joueur adopte la 2ème stratégie (dans la 1ère version de cette 3ème stratégie, le joueur jouait le reste du temps comme le joueur de la stratégie 1).

-La dernière stratégie est basé sur l'algorithme minmax mais nous n'avons malheureusement pas réussi à l'implémenter correctement et elle n'est pas fonctionnelle. Cependant nous pouvons expliquer son fonctionnement. Il explore l'arbre de toutes les coups possibles en alternant entre le joueur Max et le joueur Min, attribuant une valeur à chaque feuille de l'arbre. La valeur de chaque nœud Max est le maximum de ses enfants, tandis que la valeur de chaque nœud Min est le minimum de ses enfants. La valeur de chaque feuille est obtenue par une fonction d'évaluation qui à partir de critères d'évaluation de l'état de la partie retourne si le coup est rentable ou pas(plus la valeur est élevée, plus le coup est meilleur). 

## Description des résultats
La strat1 est la pire évidemment, cependant lors de la première version de la 3ème stratégie où le joueur ne faisait qu'avancer après avoir poser ses 2 murs, la 3ème stratégie était la pire et perdait dès fois 10 fois sur 10 contre la stratégie 1. 
La stratégie 2 gagne dans 100% des cas contre la stratégie 1 et l'ancienne stratégie 3. 
