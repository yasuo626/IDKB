
from .log_utils import LoggingObject

import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
from typing import List




class MilvusDB(LoggingObject):
    def __init__(self,host:str="localhost",port:str="19530"):
        super().__init__("db.MilvusDB")
        self.connect(host=host,port=port)
    def connect(self,host:str,port:str):
        try:
            connections.connect("default", host=host, port=port)
            self.log(f"connect to milvus",'info')
        except Exception as e:
            self.log(f"{e}",'critical')
    def disconnect(self):
        try:
            connections.disconnect()
            self.log(f"disconnect from milvus",'info')
        except Exception as e:
            self.log(f"{e}",'error')
    def has_collection(self,collection_name:str) -> bool:
        return utility.has_collection(collection_name)

    def create_collection(self,name,fields,desc='',consistency_level="Strong")->bool:
        if self.has_collection(name):
            print(f"collection {name} exists!")
            self.log(f"collection {name} exists!",'warning')
            return False
        schema = CollectionSchema(fields,desc)
        col=Collection(name, schema, consistency_level=consistency_level)
        self.log(f"create collection {name}",'info')
        return True
    def get_collection(self,name):
        if self.has_collection(name):
            return Collection(name)
        else:
            return None
    def drop_collection(self,name):
        if self.has_collection(name):
            utility.drop_collection(name)
            self.log(f"drop collection {name}", 'info')
            return True
        self.log(f"{name} does not exists!", 'warning')
        return False

class MilvusCollection(LoggingObject):
    def __init__(self,collection:Collection,class_name:str,obj_name:str) -> object:
        super().__init__("db.MilvusCollection_"+class_name)
        self.obj_name=obj_name
        self.collection=collection
    def insert(self,entities)->bool:
        self.collection.insert(entities)
        # self.log(f"{self.obj_name}: entities {entities[0]} insert","info")
    def delete_by_expr(self,expr=""):
        if expr=="":
            expr=f'{self.pk_field} not in ["-1"]'
        self.collection.delete(expr)
        # self.log(f'{self.obj_name}: delete {expr}','info')
    def modify(self,pk:str,value:str,entity:list):
        """
        :param pk:
        :param value:
        :param entity: only accept one entity in list
        :return:
        """
        self.delete_by_expr(f"{pk} in [{value}]")
        self.insert(entity)
    def query(self,expr,output_fields=["*"],limit = 10):
        """
        :param expr:
            "book_id in [0,1]"
            "book_name != Unknown"
            "book_id > 5 && word_count <= 9999"
        :param output_fields:  ["book_id", "book_intro"] ["count(*)"]
        :return:
        """
        self.load()
        if output_fields[0]=="count(*)":
            limit=None
        return self.collection.query(expr=expr, output_fields = output_fields,limit=limit)
    def search(self,anns_field,vectors:List[List],limit=2,expr=None,search_params=None,output_fields=["*"]):
        self.load()
        if search_params is None:
            search_params = {
                "metric_type": "COSINE",
                "offset": 0,
                "ignore_growing": False,
                "params": {"nprobe": 10}
            }
        return self.collection.search(data=vectors,anns_field=anns_field,param=search_params,limit=limit,expr=expr,output_fields=output_fields)
    def update_index(self,vector_field,index=None):
        if index is None:
            index = {
                "index_type": "IVF_SQ8",
                "metric_type": "COSINE",
                "params": {"nlist": 128},
            }
        if self.collection.has_index():
            self.collection.release()
            self.collection.drop_index()
        self.collection.create_index(vector_field, index)
    def load(self):
        self.collection.load()
    def release(self):
        self.collection.release()


class File:
    def __init__(self,file_name,user_name,size,file_path,abstract,embeddings,create_time="",update_time=""):
        self.name=f"{user_name}_{file_name}"
        self.user=user_name
        self.size=size
        self.path=file_path
        self.abstract=abstract
        self.embeddings=embeddings
        self.create_time=create_time
        self.update_time=update_time

class FileAbstract:
    def __init__(self,file_name,abstract_text,embeddings):
        self.file=file_name
        self.abstract=abstract_text
        self.embeddings=embeddings

class KnowledgeBase:
    def __init__(self,kb_name,user_name):
        self.kb=kb_name
        self.user=user_name
        self.embeddings=np.zeros([1],dtype=float)


class BlockoFile:
    def __init__(self,block_name,block_text,embeddings):
        self.block=block_name
        self.text=block_text
        self.embeddings=embeddings


def get_FileAbstract_fields(embeddings_size):
    return [
        FieldSchema(name="file_name", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=200),
        FieldSchema(name="abstract",dtype=DataType.VARCHAR,max_length=3000),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=embeddings_size)
    ]
def get_FileBlock_fields(embeddings_size):
    return [
        FieldSchema(name="block", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
        FieldSchema(name="text",dtype=DataType.VARCHAR,max_length=3000),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=embeddings_size)
    ]







# db=MilvusDB()
# # BLockoFile,FileAbstract
# FileAbstract_fields = [
#     # FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
#     # FieldSchema(name="kb", dtype=DataType.VARCHAR, max_length=100),
#     FieldSchema(name="file", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
#     FieldSchema(name="abstract",dtype=DataType.VARCHAR,max_length=1000),
#     FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=4)
# ]
#
# BlockoFile_fields = [
#     # FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
#     # FieldSchema(name="kb", dtype=DataType.VARCHAR, max_length=100),
#     FieldSchema(name="block", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
#     FieldSchema(name="text",dtype=DataType.VARCHAR,max_length=1000),
#     FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=4)
# ]


# fa_ent=[
#     ["BLockoFile_f1",'BLockoFile_f2','BLockoFile_f3','BLockoFile_f4','BLockoFile_f5'],
#     ["f1 abstract","f2 abstract","f3 abstract","f4 abstract","f5 abstract"],
#     np.random.random([5,4])
# ]
#
# bf_ent=[
#     ["b1",'b2','b3','b4','b5'],
#     ["b1 block","b2 block","b3 block","b4 block","b5 block"],
#     np.random.random([5,4])
# ]

# db.create_collection('FileAbstract_testkb',FileAbstract_fields)
# db.create_collection('BLockoFile_f1',BLockoFile_fields)
# db.create_collection('BLockoFile_f2',BLockoFile_fields)
# db.create_collection('BLockoFile_f3',BLockoFile_fields)
# db.create_collection('BLockoFile_f4',BLockoFile_fields)
# db.create_collection('BLockoFile_f5',BLockoFile_fields)

# fa=MilvusCollection(db.get_collection('FileAbstract_testkb'))
# bf1=MilvusCollection(db.get_collection('BLockoFile_f1'))
# bf2=MilvusCollection(db.get_collection('BLockoFile_f2'))
# bf3=MilvusCollection(db.get_collection('BLockoFile_f3'))
# bf4=MilvusCollection(db.get_collection('BLockoFile_f4'))
# bf5=MilvusCollection(db.get_collection('BLockoFile_f5'))
# fa.update_index('embeddings')
# bf1.update_index('embeddings')
# bf2.update_index('embeddings')
# bf3.update_index('embeddings')
# bf4.update_index('embeddings')
# bf5.update_index('embeddings')

# fa.insert(fa_ent)
# bf1.insert(bf_ent)
# bf2.insert(bf_ent)
# bf3.insert(bf_ent)
# bf4.insert(bf_ent)
# bf5.insert(bf_ent)


# o=search_knowledge([[0.1,0.2,0.3,0.4]],'testkb',db,max_file_distance=0.9,max_block_distance=0.3)
# print(o)
# print(fa.query('file in ',["count(*)"]))
# print(bf1.query('',["count(*)"]))
# print(bf2.query('',["count(*)"]))
# print(bf3.query('',["count(*)"]))
# print(bf4.query('',["count(*)"]))
# print(bf5.query('',["count(*)"]))


# db.drop_collection('FileAbstract_testkb')
# db.drop_collection('BLockoFile_f1')
# db.drop_collection('BLockoFile_f2')
# db.drop_collection('BLockoFile_f3')
# db.drop_collection('BLockoFile_f4')
# db.drop_collection('BLockoFile_f5')