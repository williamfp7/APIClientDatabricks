import json
import requests
import os

class Job():
    @property
    def secretScope(self):
        return self.__secretScope

    @secretScope.setter
    def secretScope(self,secretScope):
        self.__secretScope=secretScope

    @property
    def URI(self):
        return self.__URI

    @URI.setter
    def URI(self,URI):
        self.__URI=URI

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self,token):
        self.__token=token

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self,header):
        self.__header=header

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name=name

    @property
    def notebook(self):
        return self.__notebook

    @notebook.setter
    def notebook(self,notebook):
        self.__notebook=notebook

    @property
    def jobId(self):
        return self.__jobId

    @jobId.setter
    def jobId(self,id):
        self.__jobId=id
    
    @property
    def runId(self):
        return self.__runId

    @runId.setter
    def runId(self,id):
        self.__runId=id

    def __init__(self,name,notebook):
        self.URI=os.getenv('SICRM_API')
        self.token=os.getenv('SICRM_Token')
        self.secretScope=os.getenv('SICRM_Secret_Scope')
        self.header={"Authorization": "Bearer "+self.token}
        self.notebook=notebook
        self.name=name
        if self.jobExists()==False:
            self.jobCreate()


    def jobExists(self):
        r=requests.get(self.URI+"/api/2.0/jobs/list",headers=self.header)
        jobList=json.loads(r.text)
        if len(jobList)!=0:
            for x in jobList["jobs"]:
                if x["settings"]["name"]==self.name:
                    self.jobId=x["job_id"]
                    return True
        return False

    def jobCreate(self):
        conf={
            "name": self.name,
            "new_cluster": {
                "cluster_name": "",
                "spark_version": "8.3.x-scala2.12",
                "spark_conf": {
                    "spark.blobcontainer": "{{secrets/"+self.secretScope+"/blobcontainer}}",
                    "spark.storagewrite": "{{secrets/"+self.secretScope+"/storagewrite}}",
                    "spark.storageread": "{{secrets/"+self.secretScope+"/storageread}}",
                    "spark.mountpoint": "{{secrets/"+self.secretScope+"/mountpoint}}",
                    "spark.SQLServerIPCI": "{{secrets/"+self.secretScope+"/SQLServerIPCI}}",
                    "spark.SQLServerPortCI": "{{secrets/"+self.secretScope+"/SQLServerPortCI}}",
                    "spark.SQLServerIPRTDM": "{{secrets/"+self.secretScope+"/SQLServerIPRTDM}}",
                    "spark.SQLServerPassword": "{{secrets/"+self.secretScope+"/SQLServerPassword}}",
                    "spark.SQLServerPortRTDM": "{{secrets/"+self.secretScope+"/SQLServerPortRTDM}}",
                    "spark.SQLServerUser": "{{secrets/"+self.secretScope+"/SQLServerUser}}",
                    "spark.storageaccount": "{{secrets/"+self.secretScope+"/storageaccount}}"
                },
                "node_type_id": "Standard_DS3_v2",
                "spark_env_vars": {
                    "PYSPARK_PYTHON": "/databricks/python3/bin/python3"
                },
                "enable_elastic_disk": True,
                "azure_attributes": {
                    "first_on_demand": 1,
                    "availability": "SPOT_WITH_FALLBACK_AZURE",
                    "spot_bid_max_price": -1
                },
                "autoscale": {
                    "min_workers": 1,
                    "max_workers": 8
                }
            },
            "email_notifications": {
                "no_alert_for_skipped_runs": False
            },
            "timeout_seconds": 0,
            "notebook_task": {
                "notebook_path": self.notebook
            },
            "max_concurrent_runs": 1
        }
        r=requests.post(self.URI+"/api/2.0/jobs/create",headers=self.header,data=json.dumps(conf))
        tmp=json.loads(r.text)
        self.jobId=tmp["job_id"]

    def jobExecute(self):
        data=json.dumps({"job_id":self.jobId})
        r=requests.post(self.URI+"/api/2.0/jobs/run-now",headers=self.header,data=data)
        execution=json.loads(r.text)
        self.runId=execution["run_id"]

    def jobVerify(self):
        goodStatus=["PENDING","RUNNING","TERMINATING"]
        lifeCycleStateError={
            "SKIPPED":TypeError("This run was aborted because a previous run of the same job was already active."),
            "INTERNAL_ERROR":TypeError("Databricks job service error.")
        }
        terminatedError={
            "FAILED":TypeError("The task completed with an error."),
            "TIMEDOUT":TypeError("The run was stopped after reaching the timeout."),
            "CANCELED":TypeError("The run was canceled at user request.")
        }
        params={"run_id":self.runId}
        r=requests.get(self.URI+"/api/2.0/jobs/runs/get",headers=self.header,params=params)
        verification=json.loads(r.text)
        if verification["state"]["life_cycle_state"]=="TERMINATED":
            if verification["state"]["result_state"]!="SUCCESS":
                raise terminatedError[verification["state"]["result_state"]]
            return False
        if verification["state"]["life_cycle_state"] in set(goodStatus):
            return True
        else:
            raise lifeCycleStateError[verification["state"]["life_cycle_state"]]
