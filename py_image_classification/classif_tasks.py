import logging
import os
import json
from py_image_classification.conf import INFERENCE_CONFIGS, MODELS_PATHS, MODEL_PARAMETERS
from collections import defaultdict
from transformers import pipeline
from transformers import AutoModelForImageClassification, ViTImageProcessor
import torch

logging.basicConfig(level=logging.INFO, filename='inference.log', format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger()

def infere_images(images, model_name, threshold, batch_size=512, device=0):

    assert model_name in MODELS_PATHS
    model_path = MODELS_PATHS[model_name]
    model = AutoModelForImageClassification.from_pretrained(model_path, local_files_only=True)
    feature_extractor = ViTImageProcessor.from_pretrained(model_path, local_files_only=True)

    classifier = pipeline("image-classification", model=model, feature_extractor=feature_extractor,
                          batch_size=batch_size, device=device)


    if isinstance(images, list): # Si c'est une vidéo
        outputs = classifier(images)
        outputs = [(os.path.basename(image_path), output[0]['label'], output[0]['score']) for image_path, output in
                   zip(images, outputs)]
    else: # Si c'est des images uploadées
        outputs = classifier(list(images.values()))
        outputs = [(os.path.basename(image_path), output[0]['label'], output[0]['score']) for image_path, output in
                   zip(list(images.keys()), outputs)]

    outputs = filter(lambda x: x[2] >= threshold, outputs)

    del model, feature_extractor, classifier
    return outputs

def classif_segments(classif_res, max_diff=3):

    for classe in classif_res:
        classif_res[classe].sort()

    final_res = []

    for class_name in classif_res.keys():
        class_seconds = [int(image_name.split('.')[0]) for image_name in classif_res[class_name]]
        class_seconds.sort()
        diff = [class_seconds[i + 1] - class_seconds[i] for i in range(len(class_seconds) - 1)]
        if len(diff) != sum(diff):
            m = [[class_seconds[0]]]
            for i in range(len(diff)):
                if diff[i] == 1:
                    m[-1].append(class_seconds[i + 1])
                else:
                    m.append([class_seconds[i + 1]])
        else:
            m = [class_seconds]
        for seconds in m:
            final_res.append((seconds, class_name))
        final_res.sort(key=lambda x: x[0][0])

    segments = check_maxDiff(final_res, max_diff)
    return segments


def check_maxDiff(classif_list, max_diff):

    classif_list = [x for x in classif_list if len(x[0]) >= max_diff]
    segments = {}
    for i in range(len(classif_list)):
        if classif_list[i][1] in segments:
            if classif_list[i][0][0] - segments[classif_list[i][1]][-1] < max_diff:
                segments[classif_list[i][1]][-1] = classif_list[i][0][-1]
            else:
                segments[classif_list[i][1]].append(classif_list[i][0][0])
                segments[classif_list[i][1]].append(classif_list[i][0][-1])
        else:
            segments[classif_list[i][1]] = [classif_list[i][0][0], classif_list[i][0][-1]]
    return segments


def task_classif(parameters):
    images = parameters.get('images')
    inference_config = parameters.get('inference_config')
    threshold = float(parameters.get('threshold', 0.5))
    batch_size = MODEL_PARAMETERS["BATCH_SIZE"]
    results = defaultdict(list)

    assert inference_config in INFERENCE_CONFIGS

    steps = INFERENCE_CONFIGS[inference_config]

    logger.info(f"steps {steps}, threshold {threshold}, batch_size {batch_size}")

    for step in steps:

        logger.info(f"Processing step : {step}")

        if type(step) == str:
            model_name = step

            logger.info(f"Inferring {len(images)} images")

            outputs = infere_images(images, model_name, threshold, batch_size)

            #TODO : faire plus propre?
            list([results[output[1]].append(output[0]) for output in outputs])

        elif type(step) == dict:
            for targeted_label in step:
                model_name = step[targeted_label]

                images_paths = [image_name for image_name in results[targeted_label]]
                logger.info(f"Inferring {len(images_paths)} images which were labeled {targeted_label}")

                if isinstance(images, list):  # Si c'est une vidéo
                    outputs = infere_images({key: images[int(key[:-4])] for key in images_paths}, model_name, threshold,
                                            batch_size)
                else:  # Si c'est des images uploadées
                    outputs = infere_images({key: images[key] for key in images_paths}, model_name, threshold,
                                            batch_size)

                # outputs = infere_images([images[i] for i in images_paths], model_name, threshold, batch_size)

                # TODO : faire plus propre?
                list([results[output[1]].append(output[0]) for output in outputs])
                results.pop(targeted_label)

    # TODO : refact ? Plus propre et plus d'informations autoportées à utiliser dans le worker suivant ?
    if len(images) > 2:
        results = classif_segments(results)
    return results

