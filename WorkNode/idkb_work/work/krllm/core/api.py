import openai
from openai import OpenAI
import numpy as np
from typing import List,Dict


class Message:
    def __init__(self,content,role):
        self.content=content
        self.role=role
class EmbeddingsRespone:
    def __init__(self,embeddings:List[np.array],embeddings_size,model,prompt_tokens, total_tokens):
        self.embeddings=embeddings
        self.embeddings_size=embeddings_size
        self.model=model
        self.prompt_tokens=prompt_tokens
        self.total_tokens=total_tokens
class AbstractRespone:
    def __init__(self,abstract,model,prompt_tokens, total_tokens):
        self.abstract=abstract
        self.model=model
        self.prompt_tokens=prompt_tokens
        self.total_tokens=total_tokens


class ChatResponse:
    def __init__(self,content,role,model,prompt_tokens, total_tokens):
        self.message=Message(content,role)
        self.model=model
        self.prompt_tokens=prompt_tokens
        self.total_tokens=total_tokens
class ImageResponse:
    def __init__(self,image,model,prompt_tokens, total_tokens):
        self.image=image
        self.model=model
        self.prompt_tokens=prompt_tokens
        self.total_tokens=total_tokens
class AudioResponse:
    def __init__(self,audio,model,prompt_tokens, total_tokens):
        self.audio=audio
        self.model=model
        self.prompt_tokens=prompt_tokens
        self.total_tokens=total_tokens

class OpenaiAPI:
    def __init__(self,api_key,base_url):
        self.api_key=api_key
        self.base_url=base_url
        self.update(api_key,base_url)
    def update(self,api_key,base_url):
        self.api_key=api_key
        self.base_url=base_url
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=base_url
        )
    def get_embeddings(self,texts:List[str],model,**kwargs)->EmbeddingsRespone:
        """

            CreateEmbeddingResponse(
            data=[
                Embedding(embedding=[], index=0, object='embedding'),
                Embedding(embedding=[], index=1, object='embedding')
            ],
            model='text-embedding-ada-002',
            object='list',
            usage=Usage(prompt_tokens=6, total_tokens=6, completion_tokens=None)
            )
        :return:
            EmbeddingsRespone(
            embeddings=List[numpy.array],
            embeddings_size=100,
            model='text-embedding-ada-002',
            prompt_tokens=6, total_tokens=6
            )

        """
        response=self.client.embeddings.create(
            input=texts,
            model=model,
            **kwargs
        )
        embeddings=[np.array(d.embedding) for d in response.data]
        return EmbeddingsRespone(embeddings=embeddings,model=response.model,embeddings_size=len(embeddings[0]),
                        prompt_tokens=response.usage.prompt_tokens,total_tokens=response.usage.total_tokens)

    def get_message(self,messages:List[dict],model:str,**kwargs)->ChatResponse:
        """
        sample:
            messages=[
                {"role": "system","content": ""},
                {"role": "user","content": ""},
                {"role": "assistant","content": ""},
                {"role": "user","content": ""},
            ],
            model="gpt-3.5-turbo",
            temperature=0.7
        :return:ChatCompletion(
            id='chatcmpl-8bkU48gGpTNbOwIW27wPQDQSK1L0F',
            choices=[
                Choice(
                    finish_reason='stop',
                    index=0,
                    logprobs=None,
                    message=
                    ChatCompletionMessage(
                        content='response message',
                        role='assistant',
                        function_call=None,
                        tool_calls=None),
                    delta=None)
            ],
            created=1704007512,
            model='gpt-3.5-turbo-0613',
            object='chat.completion',
            system_fingerprint=None,
            usage=CompletionUsage(completion_tokens=3, prompt_tokens=36, total_tokens=39)
        )
        """
        response=self.client.chat.completions.create(
            messages=messages,
            model=model,
            **kwargs)
        message=response.choices[0].message

        return ChatResponse(content=message.content,role=message.role,model=response.model,prompt_tokens=response.usage.prompt_tokens,total_tokens=response.usage.total_tokens)

    def get_abstract(self,content:str,model,**kwargs):
        return AbstractRespone("this is abstract",model=model,prompt_tokens=10,total_tokens=10)

class AiproxyAPI:
    def __init__(self,api_key,base_url):
        self.api_key=api_key
        self.base_url=base_url
        self.update(api_key,base_url)
    def update(self,api_key,base_url):
        self.api_key=api_key
        self.base_url=base_url
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=base_url
        )

    def get_embeddings(self, texts: List[str], model, **kwargs) -> EmbeddingsRespone:
        """

            CreateEmbeddingResponse(
            data=[
                Embedding(embedding=[], index=0, object='embedding'),
                Embedding(embedding=[], index=1, object='embedding')
            ],
            model='text-embedding-ada-002',
            object='list',
            usage=Usage(prompt_tokens=6, total_tokens=6, completion_tokens=None)
            )
        :return:
            EmbeddingsRespone(
            embeddings=List[numpy.array],
            embeddings_size=100,
            model='text-embedding-ada-002',
            prompt_tokens=6, total_tokens=6
            )

        """
        response = self.client.embeddings.create(
            input=texts,
            model=model,
            **kwargs
        )
        embeddings = [np.array(d.embedding) for d in response.data]
        return EmbeddingsRespone(embeddings=embeddings, model=response.model, embeddings_size=len(embeddings[0]),
                                 prompt_tokens=response.usage.prompt_tokens, total_tokens=response.usage.total_tokens)

    def get_message(self, messages: List[dict], model: str, **kwargs) -> ChatResponse:
        """
        sample:
            messages=[
                {"role": "system","content": ""},
                {"role": "user","content": ""},
                {"role": "assistant","content": ""},
                {"role": "user","content": ""},
            ],
            model="gpt-3.5-turbo",
            temperature=0.7
        :return:ChatCompletion(
            id='chatcmpl-8bkU48gGpTNbOwIW27wPQDQSK1L0F',
            choices=[
                Choice(
                    finish_reason='stop',
                    index=0,
                    logprobs=None,
                    message=
                    ChatCompletionMessage(
                        content='response message',
                        role='assistant',
                        function_call=None,
                        tool_calls=None),
                    delta=None)
            ],
            created=1704007512,
            model='gpt-3.5-turbo-0613',
            object='chat.completion',
            system_fingerprint=None,
            usage=CompletionUsage(completion_tokens=3, prompt_tokens=36, total_tokens=39)
        )
        """
        response = self.client.chat.completions.create(
            messages=messages,
            model=model,
            **kwargs)
        message = response.choices[0].message

        return ChatResponse(content=message.content, role=message.role, model=response.model,
                            prompt_tokens=response.usage.prompt_tokens, total_tokens=response.usage.total_tokens)

    def get_abstract(self,content:str,model,**kwargs):
        return AbstractRespone(content,model=model,prompt_tokens=10,total_tokens=10)

import requests
def create_embedding_completions(url,apikey,texts,model):
    data = {
        'method': 'embedding',
        'apikey': apikey,
        'texts': texts,
        'model':model
    }
    return requests.post(url,json=data)
def create_chat_completions(url,apikey,messages,model,max_tokens=1000,temperature=0.7,top_p=0.9):
    data = {
        'method': 'chat',
        'apikey': apikey,
        'messages': messages,
        'model':model,
        'max_tokens': max_tokens,
        'temperature': temperature,
        'top_p': top_p
    }
    return requests.post(url,json=data)

class LocalModelAPI:
    def __init__(self,api_key,base_url):
        self.api_key=api_key
        self.base_url=base_url
        self.update(api_key,base_url)
    def update(self,api_key,base_url):
        self.api_key=api_key
        self.base_url=base_url
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=base_url
        )

    def get_embeddings(self, texts: List[str], model, **kwargs) -> EmbeddingsRespone:
        response=create_embedding_completions(self.base_url,self.api_key,texts,model).json()
        embeddings = [np.array(d) for d in response.get('embeddings')[0]]
        return EmbeddingsRespone(embeddings=embeddings, model=response.get('model'), embeddings_size=int(response.get('embeddings_size')),
                                 prompt_tokens=response.get('usage')['prompt_tokens'], total_tokens=response.get('usage')['total_tokens'])

    def get_message(self, messages: List[dict], model: str, **kwargs) -> ChatResponse:
        response = create_chat_completions(self.base_url,self.api_key,messages,model,**kwargs).json()
        message = response.get('content')

        return ChatResponse(content=response.get('content'), role=response.get('role'), model=response.get('model'),
                            prompt_tokens=response.get('usage')['prompt_tokens'], total_tokens=response.get('usage')['total_tokens'])

    def get_abstract(self,content:str,model,**kwargs):
        return AbstractRespone(content,model=model,prompt_tokens=10,total_tokens=10)


class TestModelAPI:
    def __init__(self,api_key='test',base_url='http://127.0.0.1'):
        self.api_key=api_key
        self.base_url=base_url
    def get_embeddings(self,texts:List[str],model,**kwargs)-> EmbeddingsRespone:
        return EmbeddingsRespone([np.random.random([10]) for i in range(len(texts))],embeddings_size=10,model=model,prompt_tokens=10,total_tokens=10)
    def get_message(self,messages:List[dict],model:str,**kwargs) -> ChatResponse:
        return ChatResponse(role='assistant',content='i am a llm',model=model,prompt_tokens=10,total_tokens=10)
    def get_abstract(self,content:str,model,**kwargs):
        return AbstractRespone(content,model=model,prompt_tokens=10,total_tokens=10)

class MultiModelAPI:
    def __init__(self,apis:Dict):
        self.apis=apis
    def get_embeddings(self,texts:List[str],api:str,model:str,**kwargs)-> EmbeddingsRespone:
        return self.apis[api].get_embeddings(texts,model,**kwargs)
    def get_message(self,messages:List[dict],api:str,model:str,**kwargs) -> ChatResponse:
        return self.apis[api].get_message(messages,model,**kwargs)
    def get_abstract(self,content:str,api:str,model:str,**kwargs):
        return self.apis[api].get_abstract(content,model,**kwargs)




# from openai import OpenAI
#
# client = OpenAI(
#     # #将这里换成你在aiproxy api keys拿到的密钥
#     api_key="sk-xVFfhXvnpu4k9VUgKiVS8FS2ODytKG8eqWxS4hBOmgK8o6Vv",
#     # 这里将官方的接口访问地址，替换成aiproxy的入口地址
#     base_url="https://api.aiproxy.io/v1"
# )
#
# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model="gpt-3.5-turbo",
# )
#
# print(chat_completion)
#
# t=AiproxyAPI(api_key='sk-xVFfhXvnpu4k9VUgKiVS8FS2ODytKG8eqWxS4hBOmgK8o6Vv',base_url="https://api.aiproxy.io/v1")
# c=t.get_message(messages=[
#                 {"role": "system","content": "you are a servent"},
#                 {"role": "user","content": "where is my clothes?"},
#                 {"role": "assistant","content": "sir,on the desk."},
#                 {"role": "user","content": "help me dress up."},
#             ],
#             model="gpt-3.5-turbo",
#             temperature=0.7)
# print(c.message.content)

