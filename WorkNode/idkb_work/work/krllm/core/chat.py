from typing import List
# message s =[
#     {"role": "system" ,"content": ""},
#     {"role": "user" ,"content": ""},
#     {"role": "assistant" ,"content": ""},
#     {"role": "user" ,"content": ""},
# ]
class Message:
    # support_types=['img','text','audio','video','doc']
    # support_roles=['assistant','setting','system','user']
    def __init__(self,role,type,content):
        self.content=content
        self.role=role
        self.type = type
    def to_dict(self):
        return {'role':self.role,'content':self.content,'type':self.type}

# reply the question by using the knowledge provided(If it does not exist, answer that no relevant content was found)
class Chat:
    def __init__(self,max_context,chat_template,question_template):
        self.message=[]
        self.system=Message('system',"text",chat_template)
        self.max_context=max_context
        self.question_template=question_template
    def update(self,msg:Message):
        self.message.append(msg)
    def get_all_message(self):
        d=[self.system]
        d.extend(self.message)
        return d
    def get_context_message(self):
        d=[self.system]
        d.extend(self.message[-self.max_context:])
        return d
    def msg2dict(self,msglist):
        d=[]
        for msg in msglist:
            d.append({"role":msg.role,"type":msg.type,"content":msg.content})
        return d
    def dict2msg(self,dlist:List[dict]):
        m=[]
        for d in dlist:
            m.append(Message(d['role'],d['type'],d['content']))
        return m
    def load(self,history):
        self.message=history
    def msg2_api_dict(self,msglist):
        """
        api dict exclude type
        """
        d=[]
        for msg in msglist:
            d.append({"role":msg.role,"content":msg.content})
        return d



def get_query_format(question:str,kns:List[dict],question_template):
    r=f"{question_template}:\n question:{question} \n\n knowledges:\n"
    for kn in kns:
        r+=f"{kn['text']}\n"
    return r














