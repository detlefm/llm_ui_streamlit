import base64
from dataclasses import dataclass
import mimetypes
from x_image import base64_mimetype
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from io import BytesIO


_model = "gpt-4o-mini"
_temperatur = 1
_top_p = 1
_frequency_penalty = 0
_presence_penalty = 0


_client = None

def init()-> OpenAI:
    global _client
    if not _client:
        _client = OpenAI()
    return _client


class Role:

    def __init__(self, role:str, prompt:str):
        assert (role in ['user','system'])
        assert (prompt)
        self.dict = dict()
        self.dict['role']=role
        self.dict['content']=[{"type": "text", "text": f"{prompt}"}]


    def add_image(self,imgbase64:str):
        mtype = base64_mimetype(imgbase64)
        self.dict['content'].append( {"type": "image_url", "image_url": {"url": f"data:{mtype};base64,{imgbase64}"}})



    def add_url(self, url:str):
        self.dict['content'].append({"type": "image_url", "image_url": {"url": url}})



    def add_source(self,source:str|BytesIO|list):
        def add(img:str|BytesIO):
            if isinstance(img, BytesIO):
                base64_image = base64.b64encode(img.getvalue()).decode('utf-8')
                self.add_image(base64_image)
            else:
                self.add_url(img)
        if isinstance(source,list):
            for img in source:
                add(img=img)
        else:
            add(img=source)




def ask_openai(prompt:str,
               source:str|BytesIO|list,
               system:str='',
               max:int=2000):
    messages = []
    user = Role('user',prompt=prompt)
    if source:
        user.add_source(source)
    messages.append(user.dict)
    if system:
        sysusr = Role('system',prompt=prompt)
        messages.append(sysusr.dict)


    client = init()
    response:ChatCompletion = client.chat.completions.create(
            model=_model,
            messages=messages,
            max_tokens=max,
            temperature=_temperatur,
            top_p=_top_p,
            frequency_penalty= _frequency_penalty,
            presence_penalty= _presence_penalty
        )  
    return response          

ANSW_CONTENT = "content"
ANSW_FINISH = "finish_reason" 

@dataclass
class ChatResult:
    completion:ChatCompletion

    def total_token(self) -> int:
        return self.completion.usage.total_tokens

    def count_choices(self) -> int:
        return len(self.completion.choices)

    def choice(self,index:int=0) -> dict:
        if index >= len(self.completion.choices):
            return None
        return {
            ANSW_CONTENT: self.completion.choices[index].message.content,
            ANSW_FINISH: self.completion.choices[index].finish_reason
        }

