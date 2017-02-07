import requests
import json
from co.Decision import Decision
from IPython.core.display import HTML


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

