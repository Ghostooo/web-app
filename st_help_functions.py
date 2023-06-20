import shutil
import tempfile
import cv2
import os
import streamlit as st
import io
import pandas as pd
import base64
import json
import pickle
import uuid
import re
import renamming_frames as rf

def download_button(object_to_download, download_filename, button_text, pickle_it=False, zip_it=False):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
    """
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if zip_it:
            try:
                with open(download_filename, 'rb') as file_data:
                    object_to_download = file_data.read()
            except IOError as e:
                st.write(e)
                return None

        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(header = True, index = False)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

    return dl_link

def clip_videos(uploaded_file, video_name):

    # Vider le dossier frames_clipped
    folder = 'frames_clipped/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    for uploaded_file, vid in zip(uploaded_file, video_name):
        pathOut = f'frames_clipped/'
        if not os.path.exists(pathOut):
            os.system(f'mkdir "{pathOut}"')
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())

        cap = cv2.VideoCapture(tfile.name)

        count = 0
        success = True
        while success:
            cap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
            try:
                success, image = cap.read()
            except Exception as e:
                print(e.stackTrace())
            if success:
                cv2.imwrite(pathOut + f'/{count}.jpg', image)
                count += 1


@st.cache_data
def show_video(videos):
    for video in videos:
        st.markdown(f"## {video[0]}")
        st.video(video[1])

def load_video(uploaded_files):
    videos = {}
    for uploaded_file in uploaded_files:
        video_data = uploaded_file.getvalue()

        videos[uploaded_file.name] = io.BytesIO(video_data)

    return uploaded_files, videos