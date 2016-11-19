from datetime import datetime
import time
import csv
import process
#import SendingMusic

class CSV_parse:
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

#format: https://github.com/acaudwell/Logstalgia/wiki/Custom-Log-Format with optional fields
    def parse(self, t):
        with open(t, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            #sm = SendingMusic("log.txt")
            cnt = 0
            p = process('log.txt')
            for row in reader:
                curt = datetime.strptime(row[1], '%d/%b/%Y:%H:%M:%S %z').minute
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
                    int(datetime.strptime(row[1], '%d/%b/%Y:%H:%M:%S %z').timestamp()),#"timestamp" :
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

t = CSV_parse()
t.parse('resutl.csv')
