# Models-Inference-UI

Application WEB créée avec Streamlit et déployée dans un conteneur Docker, elle permet :


- La visualisation des datasets d'entraînement
- La visualisation des jeux de données à tester
- Classification et segmentation des données chargées (images ou vidéo)
- Download des frames et/ou du json segmenté

## Déploiement dans docker
docker run --gpus all -d -it -v /data_ia:/data_ia -v /home/aallal/Docker_HP/web_app:/app/py_image_classification py_huggingpics:version bash 


