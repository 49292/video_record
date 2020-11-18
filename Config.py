import json
import os
path1 = None
Cameranumber = None
Day = None
Delaytime = None
def Config():
    str = os.getcwd()
    str += "/Config1.txt"
    with open(str, 'r', encoding = 'utf-8') as f:
        global path1, Cameranumber, Day, Delaytime
        try:
            test = f.read()
            js = json.loads(test)
            path1 = js.get('path1')
            Cameranumber = js.get('Cameranumber')
            Day = js.get('Day')
            Delaytime = js.get('Delaytime')
        except Exception as e:
            print(e)