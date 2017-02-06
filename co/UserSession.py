import requests
import json


#SAXO_URL = "https://saxoliberty.mybluemix.net/rest/saxoservice/"
#SAXO_URL = "http://localhost:9080/rest/saxoservice/"
SAXO_URL = "http://cognitive-r1.devdocloud.ibmcloud.com/rest/saxoservice/"
#SAXO_URL = "http://cognitive-stable.devdocloud.ibmcloud.com/rest/saxoservice/"




class UserSession:
    baseUrl = SAXO_URL

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.url = self.baseUrl + "login?user=python&password=python"
        response = requests.get(self.url)
        if(response.ok):
            # Loading the response data into a dict variable
            # json.loads takes in only binary or string variables so using content to fetch binary content
            # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
            print "UserSession login SUCCESS"
            #    jData = json.loads(response.content)
        else:
            # If response code is not ok (200), print the resulting http error code with description
            print "UserSession login FAILED"
            #response.raise_for_status()



    def uploadDataset(self, datasetname, dataset):
        if (isinstance(dataset, ExcelDataSet) or isinstance(dataset, JSONDataset)):
            self.url = self.baseUrl + self.user + "/uploadJson?dataset="+datasetname
            json = dataset.to_json()
            response = requests.post(self.url, data = json)
            if (response.ok):
                 print "UserSession uploadDataset SUCCESS"
            else:
                print "UserSession uploadDataset FAIL"
        else:
            print "UserSession unknown dataset type"

    def suggestIntents(self, datasetname, query):
        self.url = self.baseUrl + self.user + "/suggestIntents?dataset=" + datasetname + "&&query=" + query
        response = requests.get(self.url)
        if (response.ok):
            print "UserSession suggestIntents SUCCESS"
            tintents = json.loads(response.content)["intents"]
            intents = []
            for tintent in tintents:
                intents.append(Intent(tintent))
            return intents

    def createSession(self, sessionname, datasetname, intent):
        self.url = self.baseUrl + self.user + "/createDesignSession?dataset=" + datasetname + "&&sessionName=" + sessionname
        jsonvalue = intent.data
        #to_json()
        response =  requests.post(self.url, json = jsonvalue)
        if (response.ok):
            print "UserSession createSession SUCCESS"
            return DesignSession(self, json.loads(response.content))
        else:
            print "UserSession createSession FAILED"

    def loadSession(self, sessionname, datasetname, intent):
        self.url = self.baseUrl + self.user + "/createDesignSession?dataset=" + datasetname + "&&sessionName=" + sessionname +"&includeSolution=true"
        #to_json()
        jsonvalue = {}
        response =  requests.post(self.url, json = jsonvalue)
        if (response.ok):
            print "UserSession loadSession SUCCESS"
            return DesignSession(self, json.loads(response.content))
        else:
            print "UserSession loadSession FAILED"

    def inputDataURL(self, datasetId):
        return 'https://cognitive-r1.devdocloud.ibmcloud.com/input-data.html?user='+self.user+'&&dataset='+datasetId

    def inputDataFrame(self, datasetId):
        return '<iframe height="500px" src="'+ self.inputDataURL(datasetId) +'" width="100%"></iframe>'

    def getDataset(self, datasetname):
        self.url = self.baseUrl + self.user + "/dataset/" + datasetname
        response = requests.get(self.url)
        if (response.ok):
            print "UserSession getDataset SUCCESS"
            return JSONDataset(json.loads(response.content)["datasetContent"])
            
            