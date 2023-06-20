import os
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Dataset Visualisation",
    layout="wide"
)

def show_mozaique_training(train_dir):
    # Récupérez la liste des classes (nom des sous-répertoires)
    classes = os.listdir(train_dir)

    # Widget pour choisir le nombre d'images par classe à afficher
    num_images = st.sidebar.number_input("Nombre d'images par classe", min_value=1, max_value=15, value=8)

    # Parcourez chaque classe et affichez un aperçu des images correspondantes
    for class_name in classes:
        st.subheader(class_name)

        # Chemin du répertoire de la classe
        class_dir = os.path.join(train_dir, class_name)

        # Récupérez la liste des fichiers d'images dans la classe
        image_files = os.listdir(class_dir)

        # Limitez le nombre d'images à afficher par classe
        image_files = image_files[:num_images]

        # Créez une ligne pour afficher les images de la classe
        row = st.columns(len(image_files))

        # Parcourez les images et affichez-les dans Streamlit
        for i, image_file in enumerate(image_files):
            # Chemin de l'image
            image_path = os.path.join(class_dir, image_file)

            # Chargez l'image à l'aide de Pillow
            image = Image.open(image_path)

            # Affichez l'image dans Streamlit avec une largeur spécifiée pour alignement horizontal
            row[i].image(image, caption=image_file, use_column_width=True)

if __name__ == '__main__':
    DATASET_PATHS = {
        "saap": "dataset_example/SAAP",
        "saad_cnews": "dataset_example/SAAD_CNEWS",
        "saad_gen_cnews": "dataset_example/SAAD_GEN_CNEWS"
    }

    option = st.selectbox(
        'Which Dataset would you like to visualise ?',
        DATASET_PATHS.keys())

    show_mozaique_training(DATASET_PATHS[option])