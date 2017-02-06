import json
import requests
import xlrd
from xlrd.sheet import Sheet
from IPython.core.display import HTML

#SAXO_URL = "https://saxoliberty.mybluemix.net/rest/saxoservice/"
#SAXO_URL = "http://localhost:9080/rest/saxoservice/"
SAXO_URL = "http://cognitive-r1.devdocloud.ibmcloud.com/rest/saxoservice/"
#SAXO_URL = "http://cognitive-stable.devdocloud.ibmcloud.com/rest/saxoservice/"


class Decision:
     def __init__(self, data):
         self.data = data

     def __str__(self):
         return json.dumps(self.data)

     def to_json(self):
         return json.dumps(self.data)

     def getValue(self, property_name):
         return self.data[property_name]


class Intent:
  def __init__(self, data):
         self.data = data
  def __str__(self):
         return self.data["verbalization"]
  def to_json(self):
         print json.dumps(self.data)
         return json.dumps(self.data)

class Table:
     def __init__(self, data):
         self.data = data

     def getValues(self, col_name):
         if isinstance(self.data, Sheet):
            num_cols = self.data.ncols   # Number of columns
            num_rows = self.data.nrows # Number of rows
            for col_idx in range(0, num_cols):
                colname = self.data.cell(0, col_idx).value
                if (colname == col_name):
                    values = []
                    for row_idx in range(1, num_rows):
                        values.append(self.data.cell(row_idx, col_idx).value)
                    return values;

class ExcelDataSet:
    def __init__(self, location):
        self.location = location
        self.book = xlrd.open_workbook(location)

    def display(self):
        print "Sheets ", self.book._sheet_names

    def to_json(self):
        self.data = {'name':self.location, 'tables':{}}
        for sheet_name in self.book.sheet_names():
            table = {'name':sheet_name, 'columns':[]}
            sheet = self.book.sheet_by_name(sheet_name)
            num_cols = sheet.ncols   # Number of columns
            num_rows = sheet.nrows # Number of rows
            for col_idx in range(0, num_cols):
                column = {'name':sheet.cell(0, col_idx).value}
                table['columns'].append(column)
                values = []
                for row_idx in range(1, num_rows):
                    values.append(sheet.cell(row_idx, col_idx).value)
                column["values"] = values
            #setattr(self.data['tables'], sheet_name, table)
            self.data['tables'][sheet_name] = table
        return json.dumps(self.data)

    def getTable(self, sheet_name):
        return Table(self.book.sheet_by_name(sheet_name))

class JSONDataset:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "JSON dataset " + str(self.data["name"])

    def to_json(self):
        return json.dumps(self.data)

    def getTable(self, sheet_name):
        return self.data["tables"][sheet_name]['rows']

class Constraint:
    def __init__(self, data):
         self.data = data

    def __str__(self):
        return self.data["verbalization"]

    def to_json(self):
        print json.dumps(self.data)
        return json.dumps(self.data)

class Goal:
    def __init__(self, data):
         self.data = data

    def __str__(self):
        return self.data["verbalization"]

    def to_json(self):
        print json.dumps(self.data)
        return json.dumps(self.data)

class DesignSession:
    def __init__(self, userSession, data):
        self.baseUrl = userSession.baseUrl
        self.designSession = data["designSession"]
        if 'solutionJson' in data:
            self.solutionJson = data['solutionJson']

    def copy(self, newSessionId, newDataSetId):
        self.url = self.baseUrl + self.designSession["user"] + "/copySession?newSessionId="+newSessionId+"&&newDatasetId="+newDataSetId
        jsonvalue = self.designSession
        #to_json()
        response =  requests.post(self.url, json = jsonvalue)
        if (response.ok):
            print "DesignSession copy SUCCESS"
            self.designSession = json.loads(response.content)["designSession"]
            #self.solutionJson = json.loads(response.content)["solutionJson"]
        else:
            print "DesignSession copy FAILED"
        return response.ok

    def solve(self):
        self.url = self.baseUrl + self.designSession["user"] + "/refineDesignSession?solve=true&&onCloud=true"
        # data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
        jsonvalue = self.designSession
        #to_json()
        response =  requests.post(self.url, json = jsonvalue)
        if (response.ok):
            self.designSession = json.loads(response.content)["designSession"]
            self.solutionJson = json.loads(response.content)["solutionJson"]
        else:
            print "DesignSession Solve FAILED"
        return response.ok

    def refine(self):
        self.url = self.baseUrl + self.designSession["user"] + "/refineDesignSession?solve=false"
        # data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
        jsonvalue = self.designSession
        #to_json()
        response =  requests.post(self.url, json = jsonvalue)
        if (response.ok):
            self.designSession = json.loads(response.content)["designSession"]
            self.solutionJson = None
        else:
            print "DesignSession Solve FAILED"
        return response.ok

    def suggestConstraints(self, query):
        self.designSession["constraintQuery"] = query;
        if (self.refine()):
            print "UserSession suggestConstraints SUCCESS"
            tconstraints = self.designSession["suggestedConstraints"]
            constraints = []
            for tconstraint in tconstraints:
                constraints.append(Constraint(tconstraint))
            return constraints
        else:
            print "UserSession suggestConstraints FAILED"

    def addConstraint(self, constraint):
        self.designSession["constraints"] = [constraint.data]

    def suggestGoals(self, query):
        self.designSession["goalQuery"] = query;
        if (self.refine()):
            print "UserSession suggestGoals SUCCESS"
            tgoals = self.designSession["suggestedGoals"]
            goals = []
            for tgoal in tgoals:
                goals.append(Goal(tgoal))
            return goals
        else:
            print "UserSession suggestGoals FAILED"

    def addGoal(self, goal):
        self.designSession["goals"] = [goal.data]


    def hasSolution(self):
        if (not hasattr(self, 'solutionJson')):
            return False
        if self.solutionJson is None:
            return False
        return not hasattr(self.solutionJson, 'noSolution')

    def getDecisions(self, name):
        tdecisions = self.solutionJson["decisions"][name]
        decisions = [];
        for tdecision in tdecisions:
            decisions.append(Decision(tdecision))
        return decisions

    def getGoalObjective(self, i):
        return self.solutionJson["goalObjectives"][i]

    def designURL(self):
        return 'https://cognitive-r1.devdocloud.ibmcloud.com/design-model.html?user='+self.designSession["user"]+'&dataset='+self.designSession["datasetId"]+'&session='+self.designSession["sessionName"]+'&solveButton=true&embedded=true'
        #return 'https://cognitive-stable.devdocloud.ibmcloud.com/design-model.html?user='+self.designSession["user"]+'&dataset='+self.designSession["datasetId"]+'&session='+self.designSession["sessionName"]+'&solveButton=true&embedded=true'

    def designFrame(self):
        return '<iframe height="500px" src="'+ self.designURL() +'" width="100%"></iframe>'

    def ganttChartURL(self):
        return 'https://cognitive-r1.devdocloud.ibmcloud.com/docloud-gantt.html?user='+self.designSession["user"]+'&&dataset='+self.designSession["datasetId"]+'&&session='+self.designSession["sessionName"]+'&&solveButton=true'

    def ganttChartFrame(self):
        return '<iframe height="500px" src="'+ self.ganttChartURL() +'" width="100%"></iframe>'


class UserSession:
    baseUrl = SAXO_URL

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.url = self.baseUrl + "login?user=python&password=python"
        #data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
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
        # data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
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
        # data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
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
        # data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
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
        # data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
        response = requests.get(self.url)
        if (response.ok):
            print "UserSession getDataset SUCCESS"
            return JSONDataset(json.loads(response.content)["datasetContent"])
            