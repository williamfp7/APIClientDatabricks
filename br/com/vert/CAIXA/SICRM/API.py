import json
import requests
from .Token import Token

class API():

    @property
    def cifra(self):
        return self.__cifra
    
    @cifra.setter
    def cifra(self,cifra):
        self.__cifra=cifra

    @property
    def URI(self):
        return self.__URI

    @URI.setter
    def URI(self,URI):
        if URI.endswith("/"):
            URI=URI[0:len(URI)-1]
        self.__URI=URI

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self,token):
        self.__token=token

    @property
    def info(self):
        return self.__info
    
    @info.setter
    def info(self,info):
        self.__info=info

    def __init__(self,cifra,info):
        self.cifra=cifra
        self.info=info
        metadata=self.__getInfo()
        self.URI=metadata["URI"]
        self.token=Token(self,metadata["Token"])
        self.__updateInfo()


    def __getInfo(self):
        try:
            f=open(self.info,"r")
            info=self.cifra.decrypt(f.read())
            f.close()
            return json.loads(info)
        except Exception as e:
            raise TypeError(e)        

    def __updateInfo(self):
        try:
            f=open("sicrm.ini","w")
            f.write(self.cifra.encrypt(self.toJson()))
            f.close()
        except Exception as e:
            raise TypeError(e)        

    def toJson(self):
        return "{\
            \t\"URI\":\""+self.URI+"\",\
            \t\"Token\":{\
                \t\t\"value\":\""+self.token.value+"\",\
                \t\t\"id\":\""+self.token.id+"\",\
                \t\t\"expiration\":"+str(self.token.expiration)+"\
            \t}\
        }"

    def post(self,endpoint,conf):
        try:
            r=requests.post(self.URI+endpoint,headers=self.header,data=json.dumps(conf))
        except Exception as e:
            raise TypeError(e)
        return self.__json2dict(r.text)

    def get(self,endpoint,params=None):
        try:
            r=requests.get(self.URI+endpoint,headers=self.header,params=params)
        except Exception as e:
            raise TypeError(e)
        return self.__json2dict(r.text)
        
    def __json2dict(self,txt):
        try:
            return json.loads(txt)
        except Exception as e:
            raise TypeError(e)
