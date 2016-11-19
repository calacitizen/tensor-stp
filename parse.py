from datetime import datetime
import time
import csv
from process import Process
#import SendingMusic
import xml.etree.ElementTree as etree

class CSV_parse:
    def __init__(self):
        self.data = []
        self.format = '%H:%M:%S'
        self.cur_time = 0
        self.count = 10000
        self.timedel = - 1
        self.begin_time = datetime.strptime("01/Jan/1970:00:00:00 +0300", '%d/%b/%Y:%H:%M:%S %z')
        self.start_time = datetime.strptime("01/Jan/1970:00:00:00 +0300", '%d/%b/%Y:%H:%M:%S %z')
        self.end_time = datetime.strptime("01/Jan/2030:00:00:00 +0300", '%d/%b/%Y:%H:%M:%S %z')
        self.stop_time = datetime.strptime("01/Jan/2030:00:00:00 +0300", '%d/%b/%Y:%H:%M:%S %z')

    def get_data(self):
        return self.data

    def to_time(self, t):
        tt = t[t.find(':') + 1:t.find('+')-1]
        return datetime.strptime(tt, self.format)

    def set_time(self, stime, etime):
        self.begin_time = datetime.strptime(stime, '%d/%b/%Y:%H:%M:%S %z')
        self.end_time = datetime.strptime(stime, '%d/%b/%Y:%H:%M:%S %z')

    def is_success(self, t):
        if t == "200":
            return 1
        else:
            return 0

    def timezone_reformat(self, t):
        tt = t.split(' ')
        if len(tt[1]) != 5:
            return tt[0] + " " + tt[1][0] + "0" + tt[1][1:]
        else:
            return t

    def is_interest(self, t):
        if t[2] == 'Основной сервис inside' or t[2] == 'Аутентификация':
            return True
        else:
            return False


#format: https://github.com/acaudwell/Logstalgia/wiki/Custom-Log-Format with optional fields
    def parse(self, t):
        with open(t, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            #sm = SendingMusic("log.txt")
            cnt = 0
            p = Process('log.txt')
            for row in reader:
                tr = self.timezone_reformat(row[1])
                curt = datetime.strptime(tr, '%d/%b/%Y:%H:%M:%S %z').second

                if datetime.strptime(tr, '%d/%b/%Y:%H:%M:%S %z') < self.begin_time :
                    continue
                if datetime.strptime(tr, '%d/%b/%Y:%H:%M:%S %z') > self.end_time :
                    if self.data != []:
                        with open('log.txt', 'w', encoding='utf-8') as f1:
                            writer = csv.writer(f1, delimiter='|')
                            writer.writerows(self.data)
                        self.data = []
                    return
                if curt != self.cur_time:
                    if cnt % 10 == 0 and self.data != []:
                        with open('log.txt', 'w', encoding='utf-8') as f1:
                            writer = csv.writer(f1, delimiter='|')
                            writer.writerows(self.data)
                        self.data = []
                        #p.start()
                    self.cur_time = curt
                    cnt += 1
                if self.is_interest(row):
                    self.data.append([
                        int(datetime.strptime(tr, '%d/%b/%Y:%H:%M:%S %z').timestamp()),#"timestamp" :
                        row[0], #"hostname" :
                        "/" + row[2]+"/"+row[3],#"path" :
                        row[4],#"resp_code" :
                        row[5],#"resp_size" :
                        self.is_success(row[4]),#"success" :
                        "-",#"resp_color" :
                        "-",#"ref_url" :
                        row[6].split(' ')[0],#"user_agent" :
                        row[2],#"virt_host" :
                        "-",#"pid" :
                    ])


class Access_parse:
    def __init__(self):
        self.data = []
        self.format = '%H:%M:%S'
        self.cur_time = 0
        self.count = 10000

    def get_data(self):
        return self.data

    def to_time(self, t):
        tt = t[t.find(':') + 1:t.find('+')-1]
        return datetime.strptime(tt, self.format)

    def is_success(self, t):
        if t == "200":
            return 1
        else:
            return 0

    def parse(self, t):
        with open(t, 'r', encoding='utf-8') as f:
            #sm = SendingMusic("log.txt")
            cnt = 0
            p = Process('log.txt')
            for row in f:
                nrow = row.split("] [")

                nrow[0] = nrow[0].strip('[]\n')
                nrow[len(nrow) - 1] = nrow[len(nrow) - 1].strip('[]\n')

                curt = datetime.strptime(nrow[4], '%d/%b/%Y:%H:%M:%S %z').minute
                if curt != self.cur_time:
                    if cnt % 10 == 0 and self.data != []:
                        with open('log.txt', 'w', encoding='utf-8') as f1:
                            writer = csv.writer(f1, delimiter='|')
                            writer.writerows(self.data)
                        self.data = []
                        p.start()
                    self.cur_time = curt
                    cnt += 1
                self.data.append([
                    int(datetime.strptime(nrow[4], '%d/%b/%Y:%H:%M:%S %z').timestamp()),#"timestamp" :
                    nrow[2], #"hostname" :
                    nrow[6].split(' ')[1],#"path" :
                    nrow[9],#"resp_code" :
                    nrow[11],#"resp_size" :
                    self.is_success(nrow[9]),#"success" :
                    "-",#"resp_color" :
                    nrow[22],#"ref_url" :
                    nrow[23].split(' ')[0],#"user_agent" :
                    "-",#"virt_host" :
                    "-",#"pid" :
                ])

class XML_parse:
    def __init__(self):
        self.data = []
        self.format = '%H:%M:%S'
        self.cur_time = 0
        self.count = 10000

    def get_data(self):
        return self.data

    def to_time(self, t):
        tt = t[t.find(':') + 1:t.find('+')-1]
        return datetime.strptime(tt, self.format)

    def is_success(self, t):
        if t == "200":
            return 1
        else:
            return 0

    def parse(self, t):
        """
        with open(t, 'r', encoding='utf-8') as f:
            #sm = SendingMusic("log.txt")
            cnt = 0
            p = Process('log.txt')
            tree = etree.parse(self.)
            root = tree.getroot()
        """

        p = Process('log.txt')
        tree = etree.parse(t)
        root = tree.getroot()
        self.data = []
        for user in root[1]:
            for item in user[0]:
                self.data.append([
                    int(datetime.strptime(item[0].text, '%Y-%m-%d %H:%M:%S').timestamp()),#"timestamp" : 2016-11-15 05:00:07
                    item[2].text, #"hostname" :
                    item[4].text,#"path" :
                    item[1].text,#"resp_code" :
                    item[1].text,#"resp_size" :
                    "1",#"success" :
                    "-",#"resp_color" :
                    item[3].text,#"ref_url" :
                    "-",#"user_agent" :
                    item[4].text + "/" + item[2].text ,#"virt_host" :
                    "-",#"pid" :
                ])
        self.data.sort(key=lambda x: x[0])
        with open('log.txt', 'w', encoding='utf-8') as f1:
            writer = csv.writer(f1, delimiter='|')
            writer.writerows(self.data)
        self.data = []
        p.start()



t = CSV_parse()
t.set_time("15/Nov/2016:09:10:00 +0300", "15/Nov/2016:09:15:00 +0300")
t.parse('result.csv')

#tt = Access_parse()
#tt.parse('fix-inside.tensor.ru.80.access.log')

#ttt = XML_parse()
#ttt.parse('freeformatter-out.xml')
