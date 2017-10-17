from datetime import datetime

class LogEntry:
    def __init__(self, entry):
        self.Project = ''
        self.Module = ''
        self.Method = ''
        self.Step = ''
        self.LogType = 'Info'
        self.Entry = entry
        self.Tag = ''
        pass

    def __str__(self):
#        template = '{\'@timestamp\': \'%s\', \'severity\' : \'%s\', \'_type\': \'%s\', \'project_name\': \'%s\', \'method_name\': \'%s\', \'message\': \'%s\', \'tags\': \'%s\'}' \
#                   % datetime.utcnow() % self.LogType % self.Module % self.Project % self.Method % str(self.Entry) % self.Tag
        template = '{\'_timestamp\': \'%s\'}' \
                   % datetime.utcnow() #% self.LogType % self.Module % self.Project % self.Method % str(self.Entry) % self.Tag
        return template
    
