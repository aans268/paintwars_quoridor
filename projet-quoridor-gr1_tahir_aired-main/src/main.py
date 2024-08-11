# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random 
import numpy as np
import sys
from itertools import chain


import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme







# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'mini-quoridorMap'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 15  # frames per second
    game.mainiteration()
    player = game.player
    

def main():
    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    #print ("Iterations: ")
    #print (iterations)
    init()
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    
    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize
    assert nbLignes == nbCols # a priori on souhaite un plateau carre
    lMin=2  # les limites du plateau de jeu (2 premieres lignes utilisees pour stocker les murs)
    lMax=nbLignes-2 
    cMin=2
    cMax=nbCols-2
   
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
           
    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in players]
    ligneObjectif = (initStates[1][0],initStates[0][0]) # chaque joueur cherche a atteindre la ligne ou est place l'autre 
    #print(ligneObjectif)
    
    # on localise tous les murs
    # sur le layer ramassable    
    walls = [[],[]]
    walls[0] = [o for o in game.layers['ramassable'] if (o.get_rowcol()[0] == 0 or o.get_rowcol()[0] == 1)]  
    walls[1] = [o for o in game.layers['ramassable'] if (o.get_rowcol()[0] == nbLignes-2 or o.get_rowcol()[0] == nbLignes-1)]  
    allWalls = walls[0]+walls[1]
    nbWalls = len(walls[0])
    assert len(walls[0])==len(walls[1]) # les 2 joueurs doivent avoir le mm nombre de murs
    
    #-------------------------------
    # Fonctions permettant de récupérer les listes des coordonnées
    # d'un ensemble d'objets murs ou joueurs
    #-------------------------------
    
    def wallStates(walls): 
        # donne la liste des coordonnees des murs
        return [w.get_rowcol() for w in walls]
    
    def playerStates(players):
        # donne la liste des coordonnees des joueurs
        return [p.get_rowcol() for p in players]
    
   
    #-------------------------------
    # Rapport de ce qui est trouve sut la carte
    #-------------------------------
    #print("lecture carte")
    #print("-------------------------------------------")
    #print("lignes", nbLignes)
    #print("colonnes", nbCols)
    #print("Trouvé ", nbPlayers, " joueurs avec ", int(nbWalls/2), " murs chacun" )
    #print ("Init states:", initStates)
    #print("-------------------------------------------")

    #-------------------------------
    # Carte demo 
    # 2 joueurs 
    # Joueur 0: place au hasard
    # Joueur 1: A*
    #-------------------------------
    
        
    #-------------------------------
    # On choisit une case objectif au hasard pour chaque joueur
    #-------------------------------
    
    allObjectifs = ([(ligneObjectif[0],i) for i in range(cMin,cMax)],[(ligneObjectif[1],i) for i in range(cMin,cMax)])
    #print("Tous les objectifs joueur 0", allObjectifs[0])
    #print("Tous les objectifs joueur 1", allObjectifs[1])
    objectifs =  (allObjectifs[0][random.randint(cMin,cMax-3)], allObjectifs[1][random.randint(cMin,cMax-3)])
    print("Objectif joueur 0 choisi au hasard", objectifs[0])
    print("Objectif joueur 1 choisi au hasard", objectifs[1])

    #-------------------------------
    # Fonctions definissant les positions legales et placement de mur aléatoire
    #-------------------------------
    


    #A REGLER PROBLEME
    def legal_wall_position(pos,joueur,terrain):
        row,col = pos
        #print(f"pos:{pos}")
        # une position legale est dans la carte et pas sur un mur deja pose ni sur un joueur
        # attention: pas de test ici qu'il reste un chemin vers l'objectif
        simulation=terrain
        simulation.append(pos)
        path=calcul_path(terrain,joueur)
        #print(f"path:{path},\nobjectif jouer : {objectifs[joueur]}")
        if(objectifs[joueur] not in path):
            return False
        joueur=(joueur+1)%2        
        path=calcul_path(terrain,joueur)
        #print(f"path:{path},\nobjectif jouer : {objectifs[joueur]}")
        if(objectifs[joueur] not in path):
            return False
        return ((pos not in wallStates(allWalls)) and (pos not in playerStates(players)) and row>lMin and row<lMax-1 and col>=cMin and col<cMax)
    
    def draw_random_wall_location(joueur):
        # tire au hasard un couple de position permettant de placer un mur
        while True:
            random_loc = (random.randint(lMin,lMax),random.randint(cMin,cMax))
            terrain=wallStates(allWalls)
            if legal_wall_position(random_loc,joueur,terrain):  
                inc_pos =[(0,1),(0,-1),(1,0),(-1,0)]
                terrain.append(random_loc)
                random.shuffle(inc_pos)
                for w in inc_pos:
                    random_loc_bis = (random_loc[0] + w[0],random_loc[1]+w[1])
                    if legal_wall_position(random_loc_bis,joueur,terrain):
                        return(random_loc,random_loc_bis)

    #-------------------------------
    # Le joueur 0 place tous les murs au hasard
    #-------------------------------
                    
    """                 
    for i in range(0,len(walls[0]),2): 
        ((x1,y1),(x2,y2)) = draw_random_wall_location()
        walls[0][i].set_rowcol(x1,y1)
        walls[0][i+1].set_rowcol(x2,y2)
        game.mainiteration()
    """
   
    
    #-------------------------------
    # calcul A* pour le joueur 
    #-------------------------------
    
    def calcul_path(WallStates,joueur):
        g =np.ones((nbLignes,nbCols),dtype=bool)  # une matrice remplie par defaut a True  
        for w in WallStates:            # on met False quand murs
            g[w]=False
        for i in range(nbLignes):                 # on exclut aussi les bordures du plateau
            g[0][i]=False
            g[1][i]=False
            g[nbLignes-1][i]=False
            g[nbLignes-2][i]=False
            g[i][0]=False
            g[i][1]=False
            g[i][nbLignes-1]=False
            g[i][nbLignes-2]=False
        p = ProblemeGrid2D(initStates[joueur],objectifs[joueur],g,'manhattan')
        path = probleme.astar(p,verbose=False)
        #print ("Chemin trouvé:", path)
        return path
    
    
    
    #---------------------------------------------
    #------------------PROJET---------------------
    #---------------------------------------------
    posPlayers = initStates
    list_coups=[[],[]]
    cpt_walls=[0,0]             #compte le nombre de murs placés par les joueurs
    
    def draw_random_wall_location_long(joueur,old_path_adv,old_path_me):
        # tire au hasard un couple de position permettant de placer un mur
        a=0
        while True:
            a+=1
            random_loc = (random.randint(lMin,lMax),random.randint(cMin,cMax))
            terrain=wallStates(allWalls)
            if legal_wall_position(random_loc,joueur,terrain):  
                inc_pos =[(0,1),(0,-1),(1,0),(-1,0)]
                terrain.append(random_loc)
                random.shuffle(inc_pos)
                for w in inc_pos:
                    random_loc_bis = (random_loc[0] + w[0],random_loc[1]+w[1])
                    if legal_wall_position(random_loc_bis,joueur,terrain):
                        terrain.append(random_loc_bis)
                        path_adversaire=calcul_path(terrain,(joueur+1)%2)
                        path_me = calcul_path(terrain,joueur)
                        if len(path_adversaire)>len(old_path_adv) and len(path_me)<=len(old_path_me):
                            return(random_loc,random_loc_bis)
                        if a>100:
                            return ((-2,-2),(-2,-2))   

    def aleatoire(choix,joueur):
            #choix aléatoire entre poser un mur ou avancer d'une case
            #print("choix : ",choix)
            if choix==0 and cpt_walls[joueur]<(len(walls[joueur])):      #pose un mur si il reste un mur à placer
                # print(f"last_coup : {list_coups[(joueur+1)%2]}")
                ((x1,y1),(x2,y2)) = draw_random_wall_location(joueur)
                walls[joueur][cpt_walls[joueur]].set_rowcol(x1,y1)
                walls[joueur][cpt_walls[joueur]+1].set_rowcol(x2,y2)
                cpt_walls[joueur]= cpt_walls[joueur]+2
                list_coups[joueur].append((choix,((x1,y1),(x2,y2))))
                game.mainiteration()
            else:
                #-------------------------------
                # calcul A* pour le joueur qui a la main
                #-------------------------------
                # print(f"last_coup : {list_coups[(joueur+1)%2]}")
                path=calcul_path(wallStates(allWalls),joueur)

                # on fait bouger le joueur 1 jusqu'à son but
                # en suivant le chemin trouve avec A* 
                row,col = path[1]
                posPlayers[joueur]=(row,col)
                players[joueur].set_rowcol(row,col)
                #print ("pos joueur ",joueur,":", row,col)
                list_coups[joueur].append((choix,(row,col)))
                posPlayers[joueur]=(row,col)
                
                return (row,col)
                
                # mise à jour du plateau de jeu
    
    def strat1(joueur):
        #le joueur ne fait qu'avancer
        path=calcul_path(wallStates(allWalls),joueur)
        row,col = path[1]
        posPlayers[joueur]=(row,col)
        players[joueur].set_rowcol(row,col)
        #print ("pos joueur ",joueur,":", row,col)
        list_coups[joueur].append((1,(row,col)))
        posPlayers[joueur]=(row,col)
        game.mainiteration()

    def strat2(joueur,old_path,old_path_me):      
        choix= random.randint(0,1)     #choix aléatoire entre poser un mur ou avancer d'une case
        #print("choix : ",choix)
        # print(f"last_coup : {list_coups[(joueur+1)%2]}")
        ((x1,y1),(x2,y2)) = draw_random_wall_location_long(joueur,old_path,old_path_me)
        
        if ((x1,y1),(x2,y2)) != ((-2,-2),(-2,-2)) and (len(calcul_path(wallStates(allWalls),joueur))>len(calcul_path(wallStates(allWalls),(joueur+1)%2))) and cpt_walls[joueur]<(len(walls[joueur])):
            walls[joueur][cpt_walls[joueur]].set_rowcol(x1,y1)
            walls[joueur][cpt_walls[joueur]+1].set_rowcol(x2,y2)
            cpt_walls[joueur]= cpt_walls[joueur]+2
            list_coups[joueur].append((choix,((x1,y1),(x2,y2))))
                # mise à jour du plateau de jeu
            game.mainiteration()
        else:
            path=calcul_path(wallStates(allWalls),joueur)
            # on fait bouger le joueur 1 jusqu'à son but
            # en suivant le chemin trouve avec A* 
            row,col = path[1]
            posPlayers[joueur]=(row,col)
            players[joueur].set_rowcol(row,col)
            #print ("pos joueur ",joueur,":", row,col)
            list_coups[joueur].append((choix,(row,col)))
            posPlayers[joueur]=(row,col)
            game.mainiteration()

    def strat3(joueur):
        centre=(5,5)
        walls= wallStates(allWalls)
        if legal_wall_position(centre,joueur,walls):
            if legal_wall_position((centre[0],centre[1]+1),joueur,walls):
                place_mur(joueur,centre,(centre[0],centre[1]+1))
            elif legal_wall_position((centre[0],centre[1]-1),joueur,walls):
                place_mur(joueur,centre,(centre[0],centre[1]-1))
            else:
                strat2(joueur,calcul_path(wallStates(allWalls),(joueur+1)%2),calcul_path(wallStates(allWalls),joueur))
        else:
            x,y=posPlayers[(joueur+1)%2]
            if y<5:
                for i in range(0,4):
                    if legal_wall_position((5,5-i), joueur, walls) and legal_wall_position((5,5-(i+1)), joueur, walls) and chemin_non_handicapant(joueur,(5,5-i),(5,5-(i+1))):
                        place_mur(joueur, (5,5-i), (5,5-(i+1)))
                        return
                strat2(joueur,calcul_path(wallStates(allWalls),(joueur+1)%2),calcul_path(wallStates(allWalls),joueur))
            elif y>5:
                for i in range(5,8):
                    if legal_wall_position((5,i), joueur, walls) and legal_wall_position((5,i+1), joueur, walls) and chemin_non_handicapant(joueur,(5,i),(5,i+1)):
                        place_mur(joueur, (5,i), (5,i+1))
                        return
                strat2(joueur,calcul_path(wallStates(allWalls),(joueur+1)%2),calcul_path(wallStates(allWalls),joueur))
            else:
                strat2(joueur,calcul_path(wallStates(allWalls),(joueur+1)%2),calcul_path(wallStates(allWalls),joueur))
     
    def place_mur(joueur, pos1, pos2):
        ((x1,y1),(x2,y2)) = (pos1,pos2)
        walls[joueur][cpt_walls[joueur]].set_rowcol(x1,y1)
        walls[joueur][cpt_walls[joueur]+1].set_rowcol(x2,y2)
        cpt_walls[joueur]= cpt_walls[joueur]+2
        list_coups[joueur].append((0,((x1,y1),(x2,y2))))
        game.mainiteration()

    def chemin_non_handicapant(joueur,pos1,pos2):
        path=calcul_path(wallStates(allWalls),joueur)
        murs= wallStates(allWalls)
        murs.append((pos1,pos2))
        if len(calcul_path(murs,joueur))>len(path):
            return False
        return True




#--------------------------------------------------------------------------------------------------------------------------------------------------
#----------------ESSAI POUR MINMAX -------------------------------------------------------------------
    def evaluation(terrain, joueur):

        # Critère 1 : Distance entre les joueurs et leurs objectifs
        joueur0_dist = len(calcul_path(wallStates(allWalls),0))
        joueur1_dist = len(calcul_path(wallStates(allWalls),1))

        # Critère 2 : Nombre de murs restants
        joueur0_walls_left = len(walls)-cpt_walls[0]
        joueur1_walls_left = len(walls)-cpt_walls[1]

        # Critère 3 : Nombre de murs qui bloquent le chemin le plus court vers l'objectif adverse
        joueur0_blockage = 0
        joueur1_blockage = 0

        for wall in wallStates(allWalls):
            if wall in walls[1]:
                # Le mur est posé par le joueur 1 : on vérifie s'il bloque le chemin du joueur 0
                if calcul_path(wallStates(allWalls),0) == -1:                
                    joueur1_blockage += 2
            else:
                # Le mur est posé par le joueur 0 : on vérifie s'il bloque le chemin du joueur 1
                if calcul_path(wallStates(allWalls),1) == -1:
                    joueur0_blockage += 2

        # Calcul du score final
        joueur0_score = joueur0_dist + joueur0_walls_left + joueur1_blockage
        joueur1_score = joueur1_dist + joueur1_walls_left + joueur0_blockage

        return joueur0_score - joueur1_score

    def minmax(profondeur, maximizing_player, joueur, terrain):
        if profondeur == 0 or posPlayers[0] == objectifs[0] or posPlayers[1] == objectifs[1]:
            return None, evaluation(terrain, joueur)
        if maximizing_player:
            best_value= -1000
            best_move= None
            best_move_type= None
            move_type= None

            path= calcul_path(terrain[0],joueur)[1]
            coup=[path[0],path[1]]
            new_terrain= simulate_move(coup,joueur,terrain)
            value= evaluation(new_terrain, joueur)
            value_bis=-100
            for wall in get_possible_walls(terrain[0]):
                new_terrain_bis=simulate_wall(terrain,wall)
                move,value_bis= minmax(profondeur-1, False, (joueur+1)%2, new_terrain_bis)
            if value_bis>value:
                value= value_bis
                move_type= 0

            else: 
                path=calcul_path(wallStates(allWalls),joueur)[1]
                move=[path[0],path[1]]
                move_type= 1
            if best_value<value:
                best_value=value
                best_move= move
                best_move_type=move_type
        else:
            best_value= -1000
            best_move= None
            best_move_type= None
            move_type= None
            
            path= calcul_path(terrain[0],joueur)[1]
            coup=[path[0],path[1]]
            new_terrain= simulate_move(coup,joueur,terrain)
            value= evaluation(new_terrain, joueur)
            value_bis=-100
            for wall in get_possible_walls(terrain[0]):
                new_terrain_bis=simulate_wall(terrain,wall)
                move,value_bis= minmax(profondeur-1, False, (joueur+1)%2, new_terrain_bis)
            if value_bis>value:
                move_type=1
            else: 
                path=calcul_path(wallStates(allWalls),joueur)[1]
                move=[path[0],path[1]]
                move_type=0
            if best_value>value:
                best_value=value
                best_move= move
                best_move_type= move_type
        return best_move, best_move_type
            
    def get_possible_walls(walls):
        legal = []
        for i in range(2, 10, 2):
            for j in range(2, 10, 2):
                if (i, j) not in walls:
                    # Vérifier qu'il n'y a pas de murs adjacents horizontaux
                    if (i - 2, j) not in walls and (i + 2, j) not in walls:
                        # Vérifier qu'il n'y a pas de murs adjacents verticaux
                        if (i, j - 2) not in walls and (i, j + 2) not in walls:
                            legal.append((i, j))
        return legal

    def simulate_move(move,joueur,terrain):
        if joueur%2==0:
            new_terrain= [terrain[0],(move,terrain[1][1]) ]
        else:
            new_terrain= [terrain[0],(terrain[1][0],move) ]
        return new_terrain

    def simulate_wall(terrain,wall):
        simulation = terrain
        simulation[0].append(wall)
        return simulation

    def strat_minmax(joueur, horizon):
        move,move_type=minmax(horizon, True, joueur, [wallStates(allWalls),playerStates(players)])
        if move_type==0:
            ((x1,y1),(x2,y2)) = move
            walls[joueur][cpt_walls[joueur]].set_rowcol(x1,y1)
            walls[joueur][cpt_walls[joueur]+1].set_rowcol(x2,y2)
            cpt_walls[joueur]= cpt_walls[joueur]+2
            list_coups[joueur].append((move_type,((x1,y1),(x2,y2))))
            game.mainiteration()
        else:
            row,col = move
            posPlayers[joueur]=(row,col)
            players[joueur].set_rowcol(row,col)
            #print ("pos joueur ",joueur,":", row,col)
            list_coups[joueur].append((move_type,(row,col)))
            posPlayers[joueur]=(row,col)
#------------------------------------------------------------------------------------------------------------------------------------------------
      
    def partie():
        for i in range(iterations): 
            joueur= i%2        
            choix= random.randint(0,1) 
            #if len(calcul_path(wallStates(allWalls),joueur))>len(calcul_path(wallStates(allWalls),(joueur+1)%2)):
            #    strat2(joueur)
            #else:
            #    aleatoire(choix,joueur)
            if joueur%2==0:
                #aleatoire(choix,joueur)
                #strat1(joueur)
                #strat2(joueur,calcul_path(wallStates(allWalls),(joueur+1)%2),calcul_path(wallStates(allWalls),joueur))
                strat3(joueur)
                #strat_minmax(joueur,2)
            else:
                #strat1(joueur)
                #strat2(joueur,calcul_path(wallStates(allWalls),(joueur+1)%2),calcul_path(wallStates(allWalls),joueur))
                #strat3(joueur)
                aleatoire(choix,joueur)
            if posPlayers[joueur] == objectifs[joueur]:
                game.mainiteration()
                print("____________________________________\nLe joueur ",joueur," a atteint son but!\n____________________________________\n")
                vainqueur = joueur
                break
        
        pygame.quit()
        return vainqueur
    
    return partie()
    
    
    
    
    #-------------------------------
    
def n_parties(n):
    score=[0,0]
    for i in range(n):
        score[main()]+=1
    print("SCORE FINAL AU BOUT DE ",n," PARTIES :",score)
    
    
n_parties(10)

    


