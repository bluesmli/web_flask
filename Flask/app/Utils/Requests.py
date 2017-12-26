#coding:utf-8
import requests
import traceback
import sys

reload(sys)
sys.setdefaultencoding('utf8')



def getReq(path,bool_redict,headers={},cookies={}):
    try:
       req=requests.get(path,
                         cookies=cookies,
                         headers=headers,
                         allow_redirects=bool_redict,
                         # verify=False
                         )
       print req.content
       #解决编码
       print req.encoding
       if req.encoding is not None:
           if str(req.encoding.lower()).find('iso-8859-1')!=-1:
                return str(req.content),req.headers,req
           elif str(req.encoding.lower()).find('gbk')!=-1 or str(req.encoding.lower()).find('gb2312')!=-1 \
                   or str(req.encoding.lower()).find('gb')!=-1:
                return req.text,req.headers,req
           else:
               return req.content,req.headers,req

       else:
            return req.content,req.headers,req
    except Exception as e:
		print traceback.format_exc()
		print e.message


def postReq(path,data,bool_redict,headers={},cookies={},):
    try:
       req=requests.post(path,
       					 data,
                         cookies=cookies,
                         headers=headers,
                         allow_redirects=bool_redict,
                         verify=False
                         )
       #解决编码
       if req.encoding is not None:
           if str(req.encoding.lower()).find('iso-8859-1')!=-1:
                return str(req.content),req.headers,req
           elif str(req.encoding.lower()).find('gbk')!=-1 or str(req.encoding.lower()).find('gb2312')!=-1\
                                                          or str(req.encoding.lower()).find('gb')!=-1:
                return req.text,req.headers,req
           else:
               return req.content,req.headers,req
       else:
            return req.content,req.headers,req
    except Exception as e:
		print traceback.format_exc()
		print e.message


