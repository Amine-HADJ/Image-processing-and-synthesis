import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D, Transformation3D
from mesh import Mesh
import glutils


class ViewerGL:
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        
        self.vitesse = pyrr.Vector3([0.0, 0.0, 0.0])

        self.objs = [] # Liste des objets à afficher
        self.touch = {} # Dictionnaire des touches pressées
        self.mouse_pos = (0, 0) # Position initiale de la souris
        self.projectiles = []  # Liste des projectiles
        self.tps_projectiles = [] # Liste des temps de vie des projectiles
        self.affichage_texte = [] # Liste des textes à afficher
        self.rot_cam = -np.pi # Angle de la caméra
        self.rot_com_pitch = 0 # Angle de la caméra
        self.enable_mouse_movement = True

    def run(self):
        self.tframe = glfw.get_time()
        
        
        
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.dt = glfw.get_time() - self.tframe
            self.tframe = glfw.get_time()

            self.update_key() # Gestion des touches pressées
            self.objs[0].transformation.translation += self.vitesse * self.dt # Mouvement de la voiture pour la faire redesendre
            self.vitesse += pyrr.Vector3([0.0, -9.81, 0.0]) * self.dt 
            
            if self.objs[0].transformation.translation.y < 0.5734402537345886: # Si la voiture touche le sol (et descend trop bas)
                self.objs[0].transformation.translation.y = 0.5734402537345886 # La voiture est remise à la hauteur du sol
                self.vitesse.y = 0 # La vitesse est remise à 0

            for obj in self.objs: # Pour chaque objet à afficher
                GL.glUseProgram(obj.program) # Utiliser le shader de l'objet
                if isinstance(obj, Object3D): # Si l'objet est un objet 3D
                    self.update_camera(obj.program) # Mettre à jour la caméra
                obj.draw() # Afficher l'objet

            # Récupérer la position de la voiture
            car_position = self.objs[0].transformation.translation
            
            # Mouvement de rotations des pièces autour de leur centre
            for i in range(3, len(self.objs)): # Pour chaque pièce
                if i < len(self.objs): # Si la pièce existe
                    self.objs[i].transformation.rotation_euler += pyrr.Vector3([0, 0, 0.03]) # Faire tourner la pièce autour de son centre
    
                    # Récupérer la position de la pièce
                    piece_position = self.objs[i].transformation.translation

                    # Calculer la distance entre la voiture et la pièce
                    distance = np.linalg.norm(car_position - piece_position)

                    # Définir une distance seuil à partir de laquelle la pièce sera supprimée
                    seuil_de_proximite = 2.0  

                    
                    if distance < seuil_de_proximite: # Vérifier si la distance est inférieure au seuil
                        
                        self.objs.pop(i) # Supprimer la pièce de la liste des objets à afficher
                        i -= 1 # Décrémenter i pour ne pas sauter la pièce suivante (qui prend la place de la pièce supprimée)
                        
                        
           # GESTION DU MOUVEMENT RECTILIGNE DU PROJECTILE
        
            for projectile in self.projectiles: # Pour chaque projectile
                
                projectile.transformation.translation.z += 0.15 # Faire avancer le projectile
               
                GL.glUseProgram(projectile.program) # Utiliser le shader du projectile
                self.update_camera(projectile.program) # Mettre à jour la caméra
                projectile.draw() # Afficher le projectile
        
                
            # Effacer les projectiles au bout de 2 secondes
            for i in range(len(self.projectiles)): # Pour chaque projectile
                if i < len(self.projectiles): # Si le projectile existe
                    if glfw.get_time() - self.tps_projectiles[i] > 2: # Si le temps de vie du projectile est supérieur à 2 secondes
                        self.projectiles.pop(i) # Supprimer le projectile de la liste des projectiles
                        self.tps_projectiles.pop(i) # Supprimer le temps de vie du projectile de la liste des temps de vie des projectiles
                        i -= 1 # Décrémenter i pour ne pas sauter le projectile suivant (qui prend la place du projectile supprimé)
                        
            
           
            
                
            
            glfw.set_cursor_pos_callback(self.window, self.mouse_callback) # Gestion de la souris
            
            self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy()
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += self.rot_cam
            self.cam.transformation.rotation_euler[pyrr.euler.index().pitch] += self.rot_com_pitch 
            self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
            self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 5.5])

            if len(self.objs) <  4 : #Si plus de pieces (reste 3 objets qui sont la voiture, le sol, le texte)
                glfw.set_window_should_close(self.window, glfw.TRUE) #Fermer la fenetre et quitter le programme (fin du jeu)
                
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()

    def mouse_callback(self, window, xpos, ypos):
        dx = xpos - self.mouse_pos[0] # Calcul du déplacement de la souris en x
        dy = ypos - self.mouse_pos[1] # Calcul du déplacement de la souris en y
        sensibilite = 0.01 # Sensibilité de la souris
        self.rot_cam -= sensibilite * dx # Rotation de la caméra autour de la voiture
        self.rot_com_pitch -= sensibilite * dy # Rotation de la caméra autour de la voiture
        self.mouse_pos = (xpos, ypos) # Mise à jour de la position de la souris

    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)

        if key == glfw.KEY_SPACE and action == glfw.PRESS and self.objs[0].transformation.translation.y == 0.5734402537345886: # Si la voiture est sur le sol et que la touche espace est pressée
            self.vitesse = pyrr.Vector3([0.0, 6.0, 0.0]) # Faire sauter la voiture
            
        
        
            
        
        

        self.touch[key] = action 

    def add_object(self, obj):
        self.objs.append(obj)

    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):
        GL.glUseProgram(prog)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if loc == -1:
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if loc == -1:
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if loc == -1:
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)

        loc = GL.glGetUniformLocation(prog, "projection")
        if loc == -1:
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)


    def update_key(self):
        if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:
            self.objs[0].transformation.translation += pyrr.matrix33.apply_to_vector(
                pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler),
                pyrr.Vector3([0, 0, 0.1]))
        if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
            self.objs[0].transformation.translation -= pyrr.matrix33.apply_to_vector(
                pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler),
                pyrr.Vector3([0, 0, 0.05]))
        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.03
        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.03
        
            
        # Mise en place du turbo
        if glfw.KEY_T in self.touch and self.touch[glfw.KEY_T] > 0:
            self.objs[0].transformation.translation += pyrr.matrix33.apply_to_vector(
                pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler),
                pyrr.Vector3([0, 0, 0.25]))
            
        if glfw.KEY_V in self.touch and self.touch[glfw.KEY_V] > 0: # Si la touche V est pressée
            # Remise en place de la caméra à sa position de base, derrière la voiture
            self.rot_cam = -np.pi  # Remise à zéro de la rotation de la caméra
            self.rot_com_pitch = 0  # Remise à zéro de la rotation de la caméra
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] = self.rot_cam # Mise à jour de la rotation de la caméra
            self.cam.transformation.rotation_euler[pyrr.euler.index().pitch] = self.rot_com_pitch # Mise à jour de la rotation de la caméra
          
                    
        


        if glfw.KEY_LEFT_SHIFT in self.touch and self.touch[glfw.KEY_LEFT_SHIFT] > 0: # Si la touche shift est pressée
            # Création d'un projectile
            projectile_mesh = Mesh.load_obj('projectile.obj')
            projectile_mesh.normalize()
            projectile_mesh.apply_matrix(pyrr.matrix44.create_from_scale([0.5, 1.0, 0.5, 0.5]))

            projectile_transformation = Transformation3D()  

            
            projectile_transformation.translation = self.objs[0].transformation.translation.copy() # La position du projectile est celle de la voiture
       
            
           
         
            projectile_transformation.rotation_euler = pyrr.Vector3([-np.pi/2, 0, 0])  # Affectation de l'angle entre l'avant de la voiture et l'avant du projectile

            # le projectile part dans la direction de la voiture
                      

           ## Problème: le projectile ne part pas dans la bonne direction (vers lavant de la voiture)
            
            

            program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
            texture = glutils.load_texture('projectile.png')

            # Create the projectile object
            projectile_object = Object3D(
                projectile_mesh.load_to_gpu(),
                projectile_mesh.get_nb_triangles(),
                program3d_id,
                texture,
                projectile_transformation
            )
            self.projectiles.append(projectile_object)
            
            self.tps_projectiles.append(glfw.get_time())