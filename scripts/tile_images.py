from PIL import Image
import os


def get_all_path_from_dir(dir_path):
    paths = []
    for _, _, files in os.walk(dir_path):
        for file in files:
            paths.append("{}/{}".format(dir_path, file))
    return paths


def tile_image(image_path, tile_width, tile_height):
    # Ouverture de l'image
    image = Image.open(image_path)
    image_width, image_height = image.size

    # Calcul du nombre de tuiles nécessaires
    num_tiles_x = image_width // tile_width
    num_tiles_y = image_height // tile_height

    tiles = []

    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            # Découpage de la tuile
            left = x * tile_width
            upper = y * tile_height
            right = left + tile_width
            lower = upper + tile_height
            tile = image.crop((left, upper, right, lower))
            tiles.append(tile)
    return tiles


# Paramètres de découpage des tuiles
tile_width = 100
tile_height = 100

# Répertoire de sortie des tuiles découpées
output_dir = "../dataset"

# Répertoire d'entrée contenant les images à découper
input_dir = "../images"

# Obtention de tous les chemins des fichiers dans le répertoire d'entrée
images = get_all_path_from_dir(input_dir)

# Calcul du nombre total d'images à traiter
total_images = len(images)
print("Nombre d'images à traiter : {}".format(total_images))

global_index = 0
total_tiles = 0

# Affichage du message de découpage en cours
print("Découpage des images en cours...")



# Boucle sur toutes les images
for image in images:
    # Découpage de l'image en tuiles
    tiles = tile_image(image, tile_width, tile_height)

    # Boucle sur toutes les tuiles découpées
    for i, tile in enumerate(tiles):
        # Sauvegarde de la tuile dans le répertoire de sortie
        tile.save(f"{output_dir}/tuile_{global_index}.png")

        # Mise à jour des compteurs
        total_tiles += 1
        global_index += 1



print("Découpage des images terminé !")

# Affichage du nombre total de tuiles générées
print("Nombre de tuiles générées : {}".format(total_tiles))

