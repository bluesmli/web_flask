import json
import requests
import traceback
import logging
def getreq(url,params,headers):
    '''
    get 请求
    :param url:
    :param params:
    :param headers:
    :return:
    '''
    try:
        r=requests.get(url=url,params = params,headers = headers,)
        status_code = r.status_code
        logging.info("获取返回的状态码:%d" % status_code)
        response_json = r.json()
        logging.info("响应内容：%s" % response_json)
        return status_code, response_json
    except:
        traceback.format_exc()


def postform(url, data=None, headers=None):
    '''
    post form 请求
    :param url:
    :param data:
    :param headers:
    :return:
    '''
    try:
        r =requests.post(url,data,headers)
        logging.info("请求的内容：%s" % data)
        status_code = r.status_code  # 获取返回的状态码
        logging.info("获取返回的状态码:%d" % status_code)
        response_json = r.json()  # 响应内容，json类型转化成python数据类型
        logging.info("响应内容：%s" % response_json)
        return status_code, response_json  # 返回响应码，响应内容
    except BaseException as e:
        logging.error("请求失败！", exc_info=1)


def post_json(url, data, header):
    '''
    post json 请求
    :param self:
    :param url:
    :param data:
    :param headers:
    :return:
    '''
    try:
        print (url,data,header)
        r = requests.post(url,data=json.dumps(data),headers=header)
        logging.info("请求的内容：%s" % data)
        status_code = r.status_code
        print (status_code)
        logging.info("获取返回的状态码:%d" % status_code)
        response = r.json()
        logging.info("响应内容：%s" % response)
        runInfo='''
                "请求接口的url:{}
                "请求的内容:"{}
                "响应内容:"{}
        '''.format(url,data,response)
        return status_code, response,runInfo
    except BaseException as e:
        logging.error("请求失败！", exc_info=1)
        logging.error(traceback.format_exc())


def typetransfer(dicstypes=[]):
    dicslist,typeobj = [],{}
    list_str=[]
    import json
    for i in dicstypes:
        if(i['type']=="string"):
            typeobj[i['key']]=str(i['value'])
        elif (i['type']=="int"):
            typeobj[i['key']] = int(i['value'])
        elif (i['type']=="float"):
            typeobj[i['key']] = float(i['value'])
        elif (i['type']=="JSON"):
            typeobj[i['key']] = json.dumps(i['value'])
        elif (i['type']=="Boolean"):
            typeobj[i['key']] = True if i['value'].lower() == 'true' else False
        elif (i['type']=="list"):
            typeobj[i['key']] = list_str.extend(i['value'])

    return typeobj


def loadtype(value):
    if type(value)==str:
        return "string"
    if type(value)==int:
        return "int"
    if type(value)==float:
        return "float"
    if type(value)==bool:
        return "Boolean"

if __name__ == '__main__':
    # s=[{"value":"true","key":"sfdsf","type":"Boolean"}]
    # print (typetransfer(s))
    # print(loadtype("s"))

    code,res=post_json("http://11.0.0.63:5000/getSteps",{'id':1},{"Content-Type": "application/json"})
    print (code,res)