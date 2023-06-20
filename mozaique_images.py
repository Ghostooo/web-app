import streamlit as st
from PIL import Image
import os
import random
import shutil

# Vider le dossier frames_clipped
# def clean_folder():
#     folder = 'frames_clipped/'
#     for filename in os.listdir(folder):
#         file_path = os.path.join(folder, filename)
#         try:
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#         except Exception as e:
#             print('Failed to delete %s. Reason: %s' % (file_path, e))


def show_mozaique(file_type, images):
    # if file_type == "image/jpeg":
    #     clean_folder()
    #     n = min(9, len(list(images)))
    #     rand_keys = random.sample(list(images), n)
    #     for i, r in enumerate(rand_keys):
    #         images[r].save(f"frames_clipped/{i}.jpg")

    images = os.listdir("frames_clipped/")
    n = min(9, len(images))
    p = "./frames_clipped/"
    images = list(map(lambda x: p+x, images))

    images = random.sample(images, n)

    # Définissez le nombre d'images par ligne
    images_per_row = 3

    # Calculez le nombre total de lignes nécessaires
    num_rows = len(images) // images_per_row
    if len(images) % images_per_row != 0:
        num_rows += 1

    # Parcourez les images et affichez-les dans la mosaïque
    for i in range(num_rows):
        # Créez une nouvelle ligne pour chaque itération
        row = st.columns(images_per_row)

        # Parcourez les colonnes de la ligne actuelle
        for j in range(images_per_row):
            # Calculez l'indice de l'image correspondante
            index = i * images_per_row + j

            # Vérifiez si l'indice dépasse le nombre d'images disponibles
            if index < len(images):
                # Chargez l'image et affichez-la dans la colonne correspondante
                image = Image.open(images[index])
                row[j].image(image, caption=f"Image {index+1}", use_column_width=True)
