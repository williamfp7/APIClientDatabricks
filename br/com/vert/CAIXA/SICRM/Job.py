import json
class Job():
    
    @property
    def secretScope(self):
        return self.__secretScope

    @secretScope.setter
    def secretScope(self,secretScope):
        self.__secretScope=secretScope

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

    @property
    def API(self):
        return self.__API

    @API.setter
    def API(self,API):
        self.__API=API

    def __init__(self,API,name=None,notebook=None,secretScope=None):
        self.API=API
        self.secretScope=secretScope
        self.notebook=notebook
        self.name=name

    def delete(self):
        if self.exists():
            data={"job_id":self.jobId}
            self.API.post("/api/2.0/jobs/delete",data)
        else:
            print("o job não existe")

    def createIfNotExists(self):
        if self.exists()==False:
            self.create()

    def exists(self):
        jobList=self.API.get("/api/2.0/jobs/list")
        if len(jobList)!=0:
            for x in jobList["jobs"]:
                if x["settings"]["name"]==self.name:
                    self.jobId=x["job_id"]
                    return True
        return False

    def create(self):#rever o json para o cluster
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
        tmp=self.API.post("/api/2.0/jobs/create",conf)
        print(tmp)
        self.jobId=tmp["job_id"]

    def execute(self):
        if self.exists()==False:
            raise TypeError("O job não existe")
        data={"job_id":self.jobId}
        execution=self.API.post("/api/2.0/jobs/run-now",data)
        self.runId=execution["run_id"]

    def verify(self):
        goodStatus=["PENDING","RUNNING","TERMINATING"]
        lifeCycleStateError={
            "SKIPPED":"This run was aborted because a previous run of the same job was already active.",
            "INTERNAL_ERROR":"Databricks job service error."
        }
        terminatedError={
            "FAILED":"The task completed with an error.",
            "TIMEDOUT":"The run was stopped after reaching the timeout.",
            "CANCELED":"The run was canceled at user request."
        }
        params={"run_id":self.runId}
        verification=self.API.get("/api/2.0/jobs/runs/get",params=params)            

        if verification["state"]["life_cycle_state"]=="TERMINATED":
            if verification["state"]["result_state"]!="SUCCESS":
                error=terminatedError[verification["state"]["result_state"]]
                raise TypeError(error)
            return False
        if verification["state"]["life_cycle_state"] in set(goodStatus):
            return True
        else:
            error=lifeCycleStateError[verification["state"]["life_cycle_state"]]
            raise TypeError(error)

    def removeAll(self):
        jobList=self.API.get("/api/2.0/jobs/list")
        if len(jobList)!=0:
            for x in jobList["jobs"]:
                data={"job_id":x["job_id"]}
                self.API.post("/api/2.0/jobs/delete",data)