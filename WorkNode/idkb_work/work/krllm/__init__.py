

import pathlib
from typing import List

from .config import API
from .core.file_loader import FileLoader
from .core.text_spliter import CharacterTextSplitter
from .core.vdb import MilvusDB,MilvusCollection,get_FileBlock_fields,get_FileAbstract_fields
from .core.api import TestModelAPI
from .settings import base_loader,base_api,base_db,base_splitter


def file_to_name_type(file_name):
    x=file_name.split('.')
    return ''.join(x[:-1]),x[-1]

def text_merge(texts:List[str],min_length=10):
    l=len(texts)
    if l<2:
        return texts
    lens=[len(text) for text in texts]
    s=0
    i=0
    j=0
    mtexts=[]
    while j<l:
        if s>=min_length:
            mtexts.append(" ".join(texts[i:j]))
            i=j
            s=0
        s+=lens[j]
        j+=1

    return mtexts



def file_vdb_upload(username:str,file_name:str,file_type:str,file_path:pathlib.Path,base_api,api:str,model:str,db:MilvusDB,loader:FileLoader,splitter:CharacterTextSplitter):
    process=False
    try:
        embeddings_size=API[api]["embeddings_size"][model]
        name=username+"_"+file_name+"_"+file_type
        doc=loader.load(str(file_path.absolute()), file_type, username)[0].page_content
        texts=splitter.split_text(doc)
        # abstract=base_api.get_abstract(content="".join(texts),api=api,model=model).abstract
        abstract=base_api.get_abstract(content=texts[0],api=api,model=model).abstract
        abstract_embeddings=base_api.get_embeddings(texts=[abstract],api=api,model=model).embeddings[0]
        file_collection=MilvusCollection(db.get_collection(f"FileAbstract_{embeddings_size}"),"FileAbstract",f"{embeddings_size}")
        file_collection.insert([
            [name],
            [abstract],
            [abstract_embeddings],
        ])
        block_embeddings=base_api.get_embeddings(texts=texts,api=api,model=model).embeddings
        block_ids=[str(i) for i in range(len(texts))]

        db.create_collection(f"FileBlock_{name}",get_FileBlock_fields(embeddings_size))
        fb_collection=MilvusCollection(db.get_collection(f"FileBlock_{name}"),f"FileBlock",name)
        fb_collection.update_index('embeddings')

        fb_collection.insert([
            block_ids,
            texts,
            block_embeddings
        ])

        process = True
    except Exception as e:
        with open('../idkb_module.error', mode='at+') as f:
            f.write(str(e)+'\n')
            f.write(str(type(e).__name__)+'\n')
            f.write(str(e.__traceback__.tb_lineno)+'\n\n')
        pass
    return process


# file_vdb_delete will delete entity of FileAbstract twice with only do delete operation once.
# it maybe the problem of mlivus and django, this problem does not impact the efficiency
def file_vdb_delete(username:str,file_name:str,file_type:str,embeddings_size:int,vdb):
    process=False
    try:
        name=username+"_"+file_name+"_"+file_type
        MilvusCollection(vdb.get_collection(f"FileAbstract_{embeddings_size}"),"FileAbstract",f"{embeddings_size}").delete_by_expr(f'file_name in [ "{name}" ]')
        vdb.drop_collection(f"FileBlock_{name}")
        process=True
    except Exception as e:
        with open('../idkb_module.error', mode='at+') as f:
            f.write(str(e)+'\n')
            f.write(str(type(e).__name__)+'\n')
            f.write(str(e.__traceback__.tb_lineno)+'\n\n')
        pass
    return process

def kb_vdb_create(username:str,kbname:str,base_api,api:str,embedding_model:str,embeddings_size:int,db:MilvusDB):
    process=False
    try:
      db.create_collection(f"FileAbstract_{username}_{kbname}",get_FileAbstract_fields(embeddings_size))
      MilvusCollection(db.get_collection(f"FileAbstract_{username}_{kbname}"),"FileAbstract",f"{username}_{kbname}").update_index("embeddings")
      process=True
    except:
      pass
    return process
def kb_vdb_delete(username:str,kbname:str,db:MilvusDB):
    process=False
    try:
        db.drop_collection(f"FileAbstract_{username}_{kbname}")
        process = True
    except:
      pass
    return process
def kb_vdb_add_files(username,kbname,file_names,embeddings_size,vdb):
    process=False
    try:
        names=[]
        for file_name in file_names:
            name,ftype=file_to_name_type(file_name)
            names.append(f'{username}_{name}_{ftype}')

        col_f=MilvusCollection(vdb.get_collection(f"FileAbstract_{embeddings_size}"),f"FileAbstract",f"{embeddings_size}")
        col_b=MilvusCollection(vdb.get_collection(f"FileAbstract_{username}_{kbname}"),f"FileAbstract",f"{username}_{kbname}")
        file_entities=col_f.query("file_name in  "+str(names))
        filenames=[]
        abstracts=[]
        embeddings=[]
        for entity in file_entities:
            filenames.append(entity["file_name"])
            abstracts.append(entity["abstract"])
            embeddings.append(entity["embeddings"])
        col_b.insert([
            filenames,
            abstracts,
            embeddings
            ])
        process=True
    except Exception as e:
        with open('../idkb_module.error', mode='at+') as f:
            f.write(str(e)+'\n')
            f.write(str(type(e).__name__)+'\n')
            f.write(str(e.__traceback__.tb_lineno)+'\n\n')
        pass
    return process
def kb_vdb_get_files(username,kbname,vdb): #be sure username,file_name,filetype no allow _
    col_b = MilvusCollection(vdb.get_collection(f"FileAbstract_{username}_{kbname}"), f"FileAbstract", f"{username}_{kbname}")
    entities=col_b.query("")
    files=[]
    for entity in entities:
        username,name,type=entity["file_name"].split("_")
        files.append(name+"."+type)
    return files

def kb_vdb_drop_files(username,kbname,file_names,vdb):
    process = False
    try:
        names = []
        for file_name in file_names:
            name, ftype = file_to_name_type(file_name)
            names.append(f'{username}_{name}_{ftype}')

        col_b = MilvusCollection(vdb.get_collection(f"FileAbstract_{username}_{kbname}"), f"FileAbstract", f"{username}_{kbname}")
        col_b.delete_by_expr("file_name in  " + str(names))
        process = True
    except Exception as e:
        with open('../idkb_module.error', mode='at+') as f:
            f.write(str(e)+'\n')
            f.write(str(type(e).__name__)+'\n')
            f.write(str(e.__traceback__.tb_lineno)+'\n\n')
        pass
    return process




def search_knowledges(username:str,kbname:str,vector:List,db:MilvusDB,vector_field='embeddings',max_files=3,max_blocks=5,max_knowledges=5,min_file_cosine=0.5,min_block_cosine=0.3):

    fa=MilvusCollection(db.get_collection(f"FileAbstract_{username}_{kbname}"),"FileAbstract",f"{username}_{kbname}")
    hits=fa.search(anns_field=vector_field,vectors=[vector],limit=max_files)[0]
    files=[]
    for hit in hits:
        if hit.distance > min_file_cosine:
            files.append(hit.file_name)

    fbs=[ MilvusCollection(db.get_collection(f"FileBlock_{file}"),"FileBlock",f"{file}") for file in files]
    knowledges=[]
    for i in range(len(fbs)):
        blocks=fbs[i].search(anns_field=vector_field,vectors=[vector],limit=max_blocks)[0]
        for block in blocks:
            if block.distance > min_block_cosine:
                username,name,type=files[i].split("_")
                knowledges.append({'text':block.text,'file':f"{name}.{type}",'distance':block.distance})
    sorted_knowledges = sorted(knowledges, key=lambda x: -x['distance'])[:max_knowledges]
    return sorted_knowledges

def text2embeddings(text,base_api,api:str,embedding_model:str):
    return base_api.get_embeddings(texts=[text], api=api, model=embedding_model).embeddings[0]

def get_msg(messages,base_api,api,llm):
    return base_api.get_message(messages,api,llm).message.content
