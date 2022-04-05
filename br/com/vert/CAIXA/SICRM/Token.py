import datetime

class Token():

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self,value):
        self.__value=value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self,id):
        self.__id=id

    @property
    def expiration(self):
        return self.__expiration

    @expiration.setter
    def expiration(self,expiration):
        self.__expiration=expiration

    def __init__(self,API,metadata):
        self.API=API
        self.value=metadata["value"]
        self.API.header={"Authorization": "Bearer "+self.value}
        self.list()
        if ("id" in metadata)==False:
            self.update()
        elif metadata["expiration"]-(datetime.datetime.now().timestamp()*1000)<=25920000: #Troca o Token se estiver perto do vencimento
            self.update()
            self.delete(metadata["id"])
        else:
            self.id=metadata["id"]
            self.expiration=metadata["expiration"]
        self.API.header={"Authorization": "Bearer "+self.value}
                

            
    def update(self):
        newToken=self.create()
        self.value=newToken["token_value"]
        self.id=newToken["token_info"]["token_id"]
        self.expiration=newToken["token_info"]["expiry_time"]        

    def list(self):
        endpoint="/api/2.0/token/list"
        return self.API.get(endpoint)

    def create(self):
        conf={ 
                "comment": "API SICRM", 
                "lifetime_seconds": 7776000
            }
        endpoint="/api/2.0/token/create"
        return self.API.post(endpoint,conf)

    def delete(self,id):
        conf={
                "token_id": id
            }
        endpoint="/api/2.0/token/delete"
        return self.API.post(endpoint,conf)