import codecs
from os import walk, mkdir
import os.path
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import Term
from django.conf import settings

basePath = settings.BASE_PATH
targetPath = settings.INDEX_DIR+"/woosterapp"
ext_list = settings.EXT_LIST
filterFileType = "hpp"

def start(mypath, writer):
    for (dirpath, dirnames, filenames) in walk(mypath):
        for f in filenames:
            ext = f.split(".")[-1]
            if (ext in ext_list):
                completePath = os.path.join(dirpath, f)
                print f,dirpath
                with codecs.open(completePath, encoding='utf-8', errors='ignore') as content_file:
                    cont = content_file.read()
                    writer.add_document(path=unicode(completePath), filetype=unicode(ext),
                                        uipath=unicode(completePath[len(basePath)+1:]), content=cont)
    writer.commit()



schema = Schema(path=ID(stored=True),filetype=TEXT(stored=True), uipath=TEXT, content=TEXT)
#if not os.path.exists("indexdir"):
#    os.mkdir("indexdir")

ix = create_in(targetPath, schema)
writer = ix.writer()
start(basePath, writer)


#ix = open_dir("../whooshter_external_files/indexdir",schema=schema)
with ix.searcher() as searcher:
    #search file content
    query = QueryParser("content", ix.schema).parse(u"adobe")
    filter_q = Term("filetype", filterFileType)
    results = searcher.search(query,  limit=None)
    print results.scored_length(), len(results)
    for result in results:
        print result['filetype']
        print type(result)
        dn = result.docnum
    print results[dn]

reader = ix.reader()
#         with codecs.open(result["path"], encoding='utf-8') as fileobj:
#             filecontents = fileobj.read()
#         print(result.highlights("content", text=filecontents))
    
    #search file name
#     query1 = QueryParser("uipath", ix.schema).parse(u"ftw")
#     results1 = searcher.search(query1)
#     print len(results1)
#     print results1[0]
#     print results1[0]['path']
    # Use this for paged searching    
    #s.search_page(q, 5, pagelen=20)
    
    