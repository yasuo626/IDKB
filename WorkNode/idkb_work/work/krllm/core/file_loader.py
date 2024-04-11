
from langchain.document_loaders import UnstructuredFileLoader,PDFMinerLoader,UnstructuredMarkdownLoader,\
    UnstructuredExcelLoader,\
    UnstructuredURLLoader,UnstructuredWordDocumentLoader,UnstructuredHTMLLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.docstore.document import Document


import pathlib
from typing import Dict, List, Optional
from .log_utils import LoggingObject

class RapidOCRLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        def img2text(filepath):
            from rapidocr_onnxruntime import RapidOCR
            resp = ""
            ocr = RapidOCR()
            result, _ = ocr(filepath)
            if result:
                ocr_result = [line[1] for line in result]
                resp += "\n".join(ocr_result)
            return resp

        text = img2text(self.file_path)
        from unstructured.partition.text import partition_text
        return partition_text(text=text, **self.unstructured_kwargs)


FILE_LOADERS={
    'txt':UnstructuredMarkdownLoader,
    'md':UnstructuredMarkdownLoader,
    'pdf':PDFMinerLoader,
    'docx':UnstructuredWordDocumentLoader,
    'png':RapidOCRLoader,
    'jpg': RapidOCRLoader,
    'jpeg': RapidOCRLoader,
    'csv': CSVLoader,
    'xlsx': UnstructuredExcelLoader,
    'url': UnstructuredURLLoader,
    'html':UnstructuredHTMLLoader,
}



class KnowledgeBaseFile:
    """
    file class for kb
    """
    def __init__(self,file_path:pathlib.Path,user_id,size,file_type):
        self.file_path=file_path
        self.user_id=user_id
        self.size=size
        self.file_type=file_type
        self.state=0
    @property
    def exists(self):
        return self.file_path.exists()
    @property
    def str_path(self):
        return str(self.file_path.absolute())


class FileLoader(LoggingObject):
    """
    from file to document

    c=FileLoader(FILE_LOADERS,SUPPORT_FILE_TYPES)
    print(c.load(file_path=f.str_path,file_type=f.file_type))
    """
    def __init__(self,file_loaders:Dict,support_file_types:List[str]):
        super().__init__('file_preprocess.FileLoader')
        self.support_loaders={}
        for ft in support_file_types:
            if ft in file_loaders.keys():
                self.support_loaders[ft]=file_loaders[ft]
    def load(self,file_path:str,file_type:str,user="<USER>")->List[Document]:
        try:
            if file_type in self.support_loaders.keys():
                content=self.support_loaders[file_type](file_path).load()
                self.log(f"{user} load file:{file_path}",level='info')
                return content
            else:
                raise Exception(f"{user} load {file_path}:{file_type} is not supported by loaders({self.support_loaders.keys()})")
        except Exception as e:
            self.log(e,level='error')

# 获取文件信息

# 文件加载



# 文本分割
# from text_spliter import ChineseTextSplitter
# from config import TEST_DOCS_DIR
# c=CharacterTextSplitter() #无法切割
# c=ChineseTextSplitter() # 每行切割 快速
# c=BertTextSplitter() # 每行切割 慢

# pdf,docx,img,md,csv,txt,html,excel
# python-docx exceptions #下载nltk_data 包放在环境下 openpyxl  pdf2image unstructured pdfminer.six(some problem in pdfminer ) cv2 unstructured_inference pikepdf pypdf unstructured_pytesseract
# o=PDFMinerLoader(str((TEST_DOCS_DIR/'t.pdf').absolute()))
# print(o.load())
# o=UnstructuredWordDocumentLoader(str((TEST_DOCS_DIR/'t.docx').absolute()))
# print(o.load())
# o=RapidOCRLoader(str((TEST_DOCS_DIR/'t.png').absolute())) #
# print(o.load())
# o=CSVLoader(str((TEST_DOCS_DIR/'t.csv').absolute())) #
# print(o.load())
# o=UnstructuredMarkdownLoader(str((TEST_DOCS_DIR/'t.md').absolute())) # markdown
# print(o.load())
# print(UnstructuredMarkdownLoader(str((TEST_DOCS_DIR/'t.txt').absolute())).load())
# o=ChineseTextSplitter().split_text(UnstructuredMarkdownLoader(str((TEST_DOCS_DIR/'t.txt').absolute())).load()[0].page_content) #
# print(o)
# o=UnstructuredFileLoader(str((TEST_DOCS_DIR/'t.html').absolute())) #
# print(o.load())
# o=UnstructuredExcelLoader(str((TEST_DOCS_DIR/'t.xlsx').absolute())) # openpyxl
# print(o.load())
# o=UnstructuredURLLoader(["http://blog.aidroid.top/"]) # 会存在网页反爬问题
# print(o.load())



















