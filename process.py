class Proc:
    def __init__  (self, id, name, appname, create_time, time_used):
        self.name = name
        self.appname = appname
        self.create_time = create_time
        self.time_used = time_used
        self.id = id

    def getName(self):
        return self.name

    def getAppName(self):
        return self.appname

    def getCreateTime(self):
        return self.create_time

    def getTimeUsed(self):
        return self.time_used

    def getId(self):
        return self.id