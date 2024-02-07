from controller import Robot, Motor
from math import sin


class AtlasController(Robot):
    def __init__(self):
        super().__init__()

        # Récupérer les moteurs des jambes du robot Atlas
        self.left_leg_hy = self.getDevice('LLegLhy')
        self.right_leg_hy = self.getDevice('RLegLhy')
        self.back_ubx = self.getDevice('BackUbx')
        self.back_mby = self.getDevice('BackMby')

        # Initialiser le temps d'échantillonnage
        self.timestep = int(self.getBasicTimeStep())
        self.t = 0

    def dance(self):
        # Déplacer les jambes de manière périodique
        leg_position = sin(self.t)
        self.left_leg_hy.setPosition(leg_position)
        self.right_leg_hy.setPosition(-leg_position)

        # Faire bouger le torse
        torso_position = sin(self.t) * 0.5
        self.back_ubx.setPosition(torso_position)
        self.back_mby.setPosition(torso_position)

        # Mettre à jour le temps pour le mouvement périodique
        self.t += self.timestep / 2000.0


# Créer une instance du contrôleur Atlas
atlas_controller = AtlasController()

# Boucle principale
while atlas_controller.step(atlas_controller.timestep) != -1:
    # Appeler la fonction de danse pour effectuer les mouvements
    atlas_controller.dance()
