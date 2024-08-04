from dotenv import load_dotenv
import requests
from x_openai import ask_openai
from chat_result import Chat_Result
import streamlit as st
import io
from PIL import Image
from pathlib import Path
import pdf2image
import x_image



load_dotenv(".env")

_icon = "\U0001F987"

def streamlit_interface():
    st.set_page_config(
        layout="wide",
        page_title="Ask ChatGPT",
        page_icon="\U0001F47E"
    )
    st.title('Ask ChatGPT')
    left, right = st.columns(2)
    with left:
        # test picture from https://picsum.photos/images
        # https://fastly.picsum.photos/id/26/4209/2769.jpg?hmac=vcInmowFvPCyKGtV7Vfh7zWcA_Z0kStrPDW3ppP0iGI
        # https://fastly.picsum.photos/id/36/4179/2790.jpg?hmac=OCuYYm0PkDCMwxWhrtoSefG5UDir4O0XCcR2x-aSPjs
        url_input = st.text_input("Enter an URL or upload an image")
        uploaded_file = st.file_uploader(label='Upload image',
                                         type=['.png','.jpg','.jpeg','.pdf'],
                                         accept_multiple_files=False)
        text_input = st.text_area("Prompt:")
        int_value = st.slider("Max token:", min_value=200, max_value=2000, value=500, step=50)   
        li, re = st.columns(2)   

        if text_input:
            if uploaded_file:
                suffix = Path(uploaded_file.name).suffix
                if suffix == '.pdf':
                    image = pdf2image.convert(uploaded_file)
                    source = io.BytesIO()
                    image.save(source, format='PNG')                 
                else:
                    image = Image.open(uploaded_file)
                    source = uploaded_file                    
                st.image(image, use_column_width=True)
    
            elif url_input:
                source = url_input
            else:
                source = None  
            if url_input:
                # with re:
                #     if st.checkbox("Show image"):
                #         # response = requests.get(url=url_input)
                #         # image = Image.open(io.BytesIO(response.content))
                image = x_image.load_img(image_url=url_input)
                with left:
                    st.image(image,use_column_width=True)
            with li:
                if st.button("start"):
                    with st.spinner():
                        answer = ask_openai(prompt=text_input,source=source,system='',max=int_value)
                        result = Chat_Result.from_completion(completion=answer)
                        with right:
                            st.subheader(f"{result.token} ------------- Result -------------------")
                            st.write(result.content)
                            uploaded_file = None
                            url_input = ''



if __name__ == "__main__":
    streamlit_interface()
 