import os
import shutil

def compress(zip_name):
    folder = 'frames_clipped'
    shutil.make_archive(zip_name[:-4], 'zip', '.', folder)


def change_file_names(results, zip_name):
    # if file_type == 'image/jpeg':
    #     # new_images = {}
    #     # for i, k in enumerate(images.keys()):
    #     #     label = df[df['frame'] == k].iloc[0]['label1']
    #     #     new_images[f"{df[df['frame'] == k].iloc[0]['frame'][:-4]}_{label}.{k.rsplit('.')[1]}"] = images[k]
    #     # return new_images
    #     pass
    # else:
    folder = 'frames_clipped'
    if len(os.listdir(folder)) >= 3:
        # Parcours des fichiers du dossier
        for k in results:
            for i in range(0, len(results[k]), 2):
                for j in range(results[k][i], results[k][i+1]+1):
                    os.rename(os.path.join(folder, f"{j}.jpg"), os.path.join(folder, f"{j}_{k}.jpg"))
    else:
        for k in results:
            for i in range(len(results[k])):
                os.rename(os.path.join(folder, f"{results[k][i]}.jpg"), os.path.join(folder, f"{results[k][i]}_{k}.jpg"))

    compress(zip_name)


