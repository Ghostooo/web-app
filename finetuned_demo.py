import os
import streamlit as st
import io
import py_image_classification.classif_tasks as ct
import renamming_frames as rf
from PIL import Image
import st_help_functions
from py_image_classification.conf import INFERENCE_CONFIGS
from mozaique_images import show_mozaique
import shutil

# os.environ['HTTP_PROXY'] = 'http://firewall.ina.fr:81'
# os.environ['HTTPS_PROXY'] = 'http://firewall.ina.fr:81'



st.set_page_config(
    page_title="Main page",
    layout="wide"
)

def check_files_type(uploaded_files):
    if all(u.type == 'video/mp4' for u in uploaded_files):
        return 'video/mp4'
    elif all(u.type == 'image/jpeg' for u in uploaded_files):
        return 'image/jpeg'
    else:
        return None



def load_files(uploaded_files, file_type):
    images = {}
    folder_path = "frames_clipped"
    with st.spinner("The images are in preparation"):
        if file_type == 'image/jpeg':
            print("image/jpeg")
            for uploaded_file in uploaded_files:
                image_data = uploaded_file.getvalue()

                images[uploaded_file.name] = Image.open(io.BytesIO(image_data))

                if os.path.exists(folder_path):
                    # Remove all files and subdirectories from the folder
                    shutil.rmtree(folder_path)

                    # Recreate an empty folder
                    os.makedirs(folder_path)

                for image_name, image in images.items():
                    # Save the image
                    image.save(f"{folder_path}/{image_name}")



        else:
            uploaded_file, video = st_help_functions.load_video(uploaded_files)
            st_help_functions.show_video(video.items())
            st_help_functions.clip_videos(uploaded_file, video)
        images = os.listdir(folder_path)
        images = [os.path.join(folder_path, im) for im in images]

    st.success("Images are ready to inference")
    return images


if __name__ == '__main__':
    results = None
    images = None
    ##### INTERFACE ######
    st.title('Pretrained model ViT - demo')
    models = os.listdir()
    option = st.selectbox(
        'Which model would you like to choose ?',
        INFERENCE_CONFIGS.keys())


    with st.form("my-form", clear_on_submit=True):
        uploaded_files = st.file_uploader(label='Pick an image or video to test', accept_multiple_files=True)
        file_type = check_files_type(uploaded_files)
        if file_type is None:
            # st.error("Upload only files of the same type")
            raise TypeError("Upload only files of the same type")
        submit = st.form_submit_button('Submit')
        if uploaded_files and submit:
            st.success('Files are uploaded')

    result = st.button('Run on uploaded files')

    if result:
        images = load_files(uploaded_files, file_type)
        show_mozaique(file_type, images)
        st.subheader('Calculating results...')
        parameters = {
            "images": images,
            "inference_config": option, "threshold": "0.5", "destination_path": "classif.json", "renamed_images":"images.zip"}

        try:
            results = ct.task_classif(parameters)
            rf.change_file_names(results, parameters['renamed_images'])
        except Exception as e:
            print(e)

        download_segmentation = st_help_functions.download_button(results, parameters['destination_path'], 'Export segmentation to json')
        st.markdown(download_segmentation, unsafe_allow_html=True)

        download_images = st_help_functions.download_button(None, parameters['renamed_images'],
                                                                'Download renamed frames', zip_it=True)
        st.markdown(download_images, unsafe_allow_html=True)


