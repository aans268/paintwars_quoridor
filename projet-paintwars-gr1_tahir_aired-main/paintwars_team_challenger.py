# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Prénom Nom: Matthias Aïred
#  Prénom Nom: Aans Tahir
import subsomption_ennemy, subsomption_suivre_mur, subsomption_alea, subsomption_patrouille
import braitenberg_loveBotEnnemy, braitenberg_loveBot, braitenberg_suivre_mur, braitenberg_alea
def get_team_name():
    return "[Robo Madrid CF]" # à compléter (comme vous voulez)

def step2(robotId, sensors):

    translation = 1 # vitesse de translation (entre -1 et +1)
    rotation = 0 # vitesse de rotation (entre -1 et +1)

    if sensors["sensor_front_left"]["distance"] < 1 or sensors["sensor_front"]["distance"] < 1:
        rotation = 0.5  # rotation vers la droite
    elif sensors["sensor_front_right"]["distance"] < 1:
        rotation = -0.5  # rotation vers la gauche

    if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False:
        enemy_detected_by_front_sensor = True # exemple de détection d'un robot de l'équipe adversaire (ne sert à rien)

    return translation, rotation

def step(robotId, sensors):
    
    if robotId in {1,2, 8 , 7}:  
        return subsomption_ennemy.step(robotId, sensors)
    elif robotId in {3, 6 } :
        return subsomption_suivre_mur.step(robotId, sensors)
    elif robotId ==  5:
        return subsomption_alea.step(robotId, sensors)
    else:
        return subsomption_patrouille.step(robotId, sensors)

