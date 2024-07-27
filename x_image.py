import base64
from io import BytesIO
import re
from PIL import Image, ImageFile
import requests


base64_mime_type = {
    '/9j/':'image/jpeg',
    'iVBORw0KGgoAAA':'image/png',
    'R0lGOD':'image/gif',
    'PHN2Zy':'image/svg+xml',
    'JVBERi0xLj':'application/pdf',
    # 'data:text/plain;base64,':'text/plain',
    # 'data:text/html;base64,':'text/html',
    # 'data:application/json;base64,':'application/json',
    # 'data:application/xml;base64,':'application/xml',
    'UEsDBBQ':'application/zip',
}


# Todo: Only tested with jpg and png

def base64_mimetype(text:str): 
    prefix = text[:min(50,len(text))]
    if prefix.startswith('data:'):
        match = re.search(r"data:(.*);", text)
        if match:
            return match.group(1)
    elif (found := [key for key in base64_mime_type.keys() 
                        if prefix.startswith(key)]):
        return base64_mime_type[found[0]]
    raise LookupError(f'Unknown mime type {text[:min(50,len(text))]}...')


def load_img(image_url:str) ->ImageFile:
    # URL des externen Bildes
    #image_url = "https://example.com/path/to/image.jpg"

    # Bild von der URL herunterladen
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    return image

# def image2base64(img_file:Image) -> str:
#     buffered = BytesIO()
#     img_file.save(buffered,format = "PNG")
#     return base64.b64encode(buffered.getvalue()).decode('utf-8')
