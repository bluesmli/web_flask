import json

class res(object):

    def __init__(self,code,message,data=None):
        self.code=code
        self.message=message
        self.data=data


    def getcode(self):
        return  self.code





def  jsonSerialization(jsonobsj):
    '''
    json序列化对象
    :param jsonobsj:
    :return:
    '''
    return (json.dumps(jsonobsj, default=lambda obj: obj.__dict__,sort_keys=True,indent=4))