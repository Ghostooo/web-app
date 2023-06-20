import os
import json


def change_file_names(results, folder):
    for k in results:
        for i in range(len(results[k])):
            os.rename(os.path.join(folder, f"{results[k][i]}.jpg"), os.path.join(folder, f"{results[k][i]}_{k}.jpg"))


if __name__ == '__main__':
    folder = '/home/allal/Master2/pythonProject/git_projects/py_image_classif_renaming/data/frames/cnews_20230504'
    results = json.loads("classif_cnews_20230504.json")
    change_file_names(results, folder)