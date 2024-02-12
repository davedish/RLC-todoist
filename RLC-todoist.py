from todoist_api_python.api import TodoistAPI
from pprint import pprint
import re
from datetime import datetime, timedelta

api = TodoistAPI("8a7230b7cfc53216033ddc8bba1e40ae1a8f3438")

# try:
#     tasks = api.get_tasks()
#     #pprint(projects)
#     for item in tasks:
#         #print (item.name + ': ' + item.id)
#         #if item.id == 2215349894:
#         if item.due is not None:
#             pprint (item)
# except Exception as error:
#     print(error)


reCm  = re.compile("^.*administer a Recurrent line check to (?P<pos>\w+) (?P<name>\w+) on")                              # QU BWIASB6
reDate = re.compile("^.*on (?P<weekday>\w+), (?P<month>\w+) (?P<date>\d+), (?P<year>\d+)")
reFlight = re.compile("^.*Flight (?P<flt>\d+) (?P<orig>\w+) to (?P<dest>\w+)[ |\.]")

infile = open("RLC-email.txt","r")
fileContents = infile.readline()
fileContents = infile.readline()
fileContents = infile.readline()
#print(fileContents)

m1 = reCm.match(fileContents)
pprint(m1.groupdict())

m2 = reDate.match(fileContents)
print(m2)
pprint(m2.groupdict())

m3 = reFlight.match(fileContents)
pprint(m3.groupdict())


# Pilot / IE = 2215349894

dateStr = m2['month'] + ' '
if len(m2['date']) < 2: 
    dateStr = dateStr + '0'
dateStr = dateStr + m2['date'] + ' ' +  m2['year']

RlcDate = datetime.strptime(dateStr,"%B %d %Y")

try:
    task = api.add_task(content="Conduct RLC " 
                        + m1['pos'] + ' ' + m1['name']
                        + ' JBU' + m3['flt']
                        + ' ' + m3['orig'] + '-' + m3['dest'],
                        project_id="2215349894", 
                        labels=["Urgent","Important"],
                        due_date=datetime.strftime(RlcDate,'%Y-%m-%d'),
                        priority=1)
    pprint(task)

    task = api.add_task(content="Crew Check " 
                        + m1['pos'] + ' ' + m1['name']
                        + ' JBU' + m3['flt']
                        + ' ' + m3['orig'] + '-' + m3['dest'],
                        project_id="2215349894", 
                        labels=["Urgent","Important"],
                        due_date=datetime.strftime(RlcDate - timedelta(days=1),'%Y-%m-%d'),
                        priority=1)
    pprint(task)
    task = api.add_task(content="Grade RLC " 
                        + m1['pos'] + ' ' + m1['name']
                        + ' JBU' + m3['flt']
                        + ' ' + m3['orig'] + '-' + m3['dest'],
                        project_id="2215349894", 
                        labels=["Urgent","Important"],
                        due_date=datetime.strftime(RlcDate + timedelta(days=1),'%Y-%m-%d'),
                        priority=1)
    pprint(task)
except Exception as error:
    print(error)




# Fetch tasks synchronously
def get_tasks_sync():
    try:
        tasks = api.get_tasks()
        print(tasks)
    except Exception as error:
        print(error)