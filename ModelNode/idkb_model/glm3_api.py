
"""
source:https://github.com/THUDM/ChatGLM3
des: ChatGLM3/openai_api_demo

local api format

1. get embeddings
requests:
{
    'method':'embedding',
    'texts':['text1','text2',...],
    'model':'glm3_6b_text_embeddings',
    'apikey':'',
}
response:
{
    'state':0,
    'embeddings':['text1','text2',...],
    'embedding_size':100,
    'model':'glm3_6b_text_embeddings'
    'prompt_tokens':6, 
    'total_tokens':6
}

2. get message
requests:
{
    'method':'chat',
    'apikey':'',
    messages=[
        {"role": "system","content": ""},
        {"role": "user","content": ""},
        {"role": "assistant","content": ""},
        {"role": "user","content": ""},
    ],
    model="glm3_6b",
    max_tokens=1000,
    temperature=0.8,
    top_p=0.8
}
response:
{
    'state':0,
    'content':'',
    'role':'assistant',
    'model':'glm3_6b_embeddings',
    'prompt_tokens':6, 
    'total_tokens':6
}


"""



import pathlib
from transformers import AutoModel,AutoTokenizer
from typing import List
import re
import torch
from utils import  generate_chatglm3



from flask import Flask, request, jsonify,render_template
import numpy as np
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

APIKEY=""



class Glm3Model:
    def __init__(self,model_path:str,device:str) -> int:
        self.model_path=pathlib.Path(model_path)
        if not self.model_path.exists:
            print(f"Glm3Model.__init__:{self.model_path} not exists")
            return 1
        assert device in ['cuda','cpu']
        self.device=device
        self.model=AutoModel.from_pretrained(model_path, trust_remote_code=True).to(self.device).eval()
        self.tokenizer=AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    
    def get_embeddings(self,texts:List):
        """_summary_

        Args:
            texts (List): _description_

        Returns:
            dict: {
                'embeddings': numpy.array(n,4096),
                'usage': {'prompt_tokens': 30, 'completion_tokens': 30, 'total_tokens': 60},
                'finish_reason': 'stop'}
        """
        inputs=self.tokenizer(texts, return_tensors="pt").to(self.device)
        resp = self.model.transformer(**inputs, output_hidden_states=True)
        output=torch.mean(resp.last_hidden_state, dim=0, keepdim=True).cpu().detach().numpy()
        
        prompt_tokens = 0
        for text in texts:
            prompt_tokens += len(re.split(r'\s+', text))
        
        return {
            'embeddings':output.tolist(),
            'usage':{'prompt_tokens': prompt_tokens, 'completion_tokens': 0, 'total_tokens': prompt_tokens}
        }
    
    def get_message(self,messages:List,stream=False,max_tokens=1000,temperature=0.8,top_p=0.8,repetition_penalty=1.1,functions=None):
        """_summary_

        Args:
            messages (List): _description_
            stream (bool, optional): _description_. Defaults to False.
            max_tokens (int, optional): _description_. Defaults to 1000.
            temperature (float, optional): _description_. Defaults to 0.8.
            top_p (float, optional): _description_. Defaults to 0.8.
            repetition_penalty (float, optional): _description_. Defaults to 1.1.
            functions (_type_, optional): _description_. Defaults to None.

        Returns:
            dict: {
                'text': 'msg',
                'usage': {'prompt_tokens': 30, 'completion_tokens': 30, 'total_tokens': 60},
                'finish_reason': 'stop'}
        """
        
        gen_params = dict(
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            echo=False,
            stream=stream,
            repetition_penalty=repetition_penalty,
            functions=functions,
        )
        response=generate_chatglm3(self.model,self.tokenizer, gen_params)
        if response["text"].startswith("\n"):
            response["text"] = response["text"][1:]
        response["text"] = response["text"].strip()
        return response 

# m=Glm3Model(model_path='/root/autodl-tmp/chatglm3-6b',device='cuda')
# #m.get_embeddings(['this is 1','this is 2'])
# m.get_message([
#         {"role": "system","content": "you are glm3"},
#         {"role": "user","content": "who are you"},
#         {"role": "assistant","content": "i am glm3"},
#         {"role": "user","content": "really?"},
#     ])
# #{'text': '\n yes, i am the glm model jointly trained by the KEG laboratory of Tsinghua University and Zhipu AI.', 'usage': {'prompt_tokens': 30, 'completion_tokens': 30, 'total_tokens': 60}, 'finish_reason': 'stop'}
# m.get_embeddings(['this is 1','this is 2'])
# # [[[-0.2073   0.935   -0.941   ... -0.534   -0.5957  -0.09106]  (2, 4096)
# #   [-0.1832   0.841   -0.7334  ... -0.4954  -0.7974  -0.409  ]]]









@app.route('/v1/chat/completions', methods=['POST','GET'])
def check_image():
    if request.method not in ["GET","POST"]:
        return jsonify({"error_info":f"request method '{request.method}' error"})
        
    if request.method=="GET":
        get_content={}
        return render_template('glm3_api_doc.html',get_content=get_content)
    
    if request.method=="POST":
        global glm3model
        method=request.json.get('method')
        if APIKEY!=request.json.get('apikey'):
            response=jsonify({"error_info":f"apikey error"})
            return response
        
        response={}
        if method=='chat':
            messages=request.json.get('messages')
            max_tokens=request.json.get('max_tokens')
            temperature=request.json.get('temperature')
            top_p=request.json.get('top_p')
            
            response=glm3model.get_message(messages,max_tokens=max_tokens,temperature=temperature,top_p=top_p)
            response['model']='glm3_6b'
            response=jsonify(response)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        elif method=='embedding':
            texts=request.json.get('texts')
            response=glm3model.get_embeddings(texts)
            response['model']='glm3_6b_text_embeddings'
            response=jsonify(response)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        elif method=='check':
            response['state']=0
            response['error_info']=""            
            response=jsonify(response)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

        else:
            response=jsonify({"error_info":f"error task method {method}"})
            return response

if __name__ == '__main__':
    glm3model=Glm3Model('/root/autodl-tmp/chatglm3-6b','cuda')
    app.run(host='0.0.0.0', port=8001,debug=False)