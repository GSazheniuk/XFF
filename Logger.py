from datetime import datetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen


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
    

class Logger:
    def __init__(self, project, module):
        self.Entry = LogEntry('')
        self.Entry.Project = project
        self.Entry.Module = module
        pass

    def serialize_entry(self):
        pass

    def save_msg(self, msg):
        self.Entry = LogEntry(msg)
        self.save_log()
        pass
    
    def save_log(self):
        url = 'http://logsene-receiver.sematext.com/1ffc688a-f9a3-470b-bc66-a536e0b13024/%s/'
        url = url % 'Test' #self.Entry.Module
        request = Request(url, str(self.Entry).encode())
        print(str(self.Entry))
        res = urlopen(request).read().decode()
        print(res)
        pass
