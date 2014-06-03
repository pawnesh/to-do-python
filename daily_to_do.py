#!/usr/bin/python
# a simple command line daily to do program

from time import gmtime, strftime
import xml.etree.cElementTree as ET
import sys, getopt

class Todo:
    'a class for storing to do data and reading to do data'
    count = 0

    def __init__(self):
        self.tasks = []

    def addTask(self,task):
        self.tasks.append(task)
        Todo.count = Todo.count + 1

    def removeTask(self,task_id):
        for task in self.tasks:
            if(task.id == task_id):
                self.tasks.remove(task)
                Todo.count = Todo.count - 1

    def saveTasks(self):
        global ET
        rootTask = ET.Element("tasks")
        for task in self.tasks:
            cTask = ET.SubElement(rootTask,"task")
            cTask.set("id",str(task.id))

            name = ET.SubElement(cTask,"name")
            name.text = task.getName()

            end_date = ET.SubElement(cTask,"end_date")
            end_date.text = task.getEndDate()

            start_date = ET.SubElement(cTask,"start_date")
            start_date.text = task.getStartDate()

            priority = ET.SubElement(cTask,"priority")
            priority.text = task.getPriority()

            priority = ET.SubElement(cTask,"status")
            priority.text = task.getStatus()

        #ET.dump(rootTask)
        tree = ET.ElementTree(rootTask)
        tree.write("Tasks.xml")


    def retriveTasks(self):
        try:
            rootTree = ET.parse('Tasks.xml')
            root = rootTree.getroot()
            for child in root:
                id = child.get('id')
                name = ''
                end_date = ''
                priority = ''
                status = ''
                start_date = ''
                for c in child:
                    if(c.tag in "name"):
                        name = c.text
                    if(c.tag in 'end_date'):
                        end_date = c.text
                    if(c.tag in 'start_date'):
                        start_date = c.text
                    if(c.tag in 'priority'):
                        priority = c.text
                    if(c.tag in 'status'):
                        status = c.text
                task = Task(id = id,name = name,e_date = end_date,s_date = start_date,priority = priority,status = status)
                self.addTask(task)
        except:
            print('A fresh to do list found!')

    # going to print ascii table
    def printTasks(self):
        secondTree = ET.parse('Tasks.xml')
        root = secondTree.getroot()
        header = ["id","Task name","Start date","End date","Priority","Status"]
        child_length = [len(header[0]),len(header[1]),len(header[2]),len(header[3]),len(header[4]),len(header[5])]
        # calculating the length of the maximum character for each coloumn
        for child in root:
            child_length[0] = max(len(child.get('id')),child_length[0])
            for c in child:
                if(c.tag in "name"):
                    child_length[1] = max(len(c.text),child_length[1])
                if(c.tag in 'end_date'):
                    child_length[3] = max(len(c.text),child_length[3])
                if(c.tag in 'start_date'):
                    child_length[2] = max(len(c.text),child_length[2])
                if(c.tag in 'priority'):
                    child_length[4] = max(len(c.text),child_length[4])
                if(c.tag in 'status'):
                    child_length[5] = max(len(c.text),child_length[5])

        #printing head using ljust to print extra spaces in string

        print(
        header[0].ljust(child_length[0])+" | "+ \
        header[1].ljust(child_length[1])+" | "+ \
        header[2].ljust(child_length[2])+" | "+ \
        header[3].ljust(child_length[3])+" | "+ \
        header[4].ljust(child_length[4])+" | "+ \
        header[5].ljust(child_length[5]))

        #printing line
        print(
        ('-')*(child_length[0])+" + "+ \
        ('-')*(child_length[1])+" + "+ \
        ('-')*(child_length[2])+" + "+ \
        ('-')*(child_length[3])+" + "+ \
        ('-')*(child_length[4])+" + "+ \
        ('-')*(child_length[5]))

        for child in root:
            name = ''
            s_date = ''
            e_date = ''
            priority = ''
            status = ''
            for c in child:
                if(c.tag in "name"):
                    name = c.text
                if(c.tag in 'end_date'):
                    e_date = c.text
                if(c.tag in 'start_date'):
                    s_date = c.text
                if(c.tag in 'priority'):
                    priority = c.text
                if(c.tag in 'status'):
                    status = c.text

            print(
            child.get('id').ljust(child_length[0])+" | "+ \
            name.ljust(child_length[1])+" | "+ \
            s_date.ljust(child_length[2])+" | "+ \
            e_date.ljust(child_length[3])+" | "+ \
            priority.ljust(child_length[4])+" | "+ \
            status.ljust(child_length[5])+" | "
            )

    def updateStatus(self,task_id,task_status):
        for task in self.tasks:
            if(task.id == task_id):
                task.setStatus(task_status);

class Task:
	'''
		a class for task
	'''
	def __init__(self,id = '',name = '',e_date = '',s_date = strftime("%Y-%m-%d %H:%M:%S", gmtime()),priority = '',status = 'pending'):
		self.name = name
		self.s_date = s_date
		self.e_date = e_date
		self.priority = priority
		self.status = status
		self.id = id

	def setStatus(self,status):
		self.status = status

	def getStatus(self):
		return self.status;

	def getName(self):
		return self.name
	def getStartDate(self):
		return self.s_date;
	def getEndDate(self):
		return self.e_date

	def setPriority(self,priority = '5'):
		self.priority = priority
	def getPriority(self):
		return self.priority


def help():
     print('--add <task name in comma> <end_time> <priority>')
     print('--setstatus <task_id> <status>')
     print('--view or -v for listing tasks')
     print('--remove <task_id> or -r for removing task')
     print('NOTE: status must be either pending, working or done (-_-;)')

if __name__ == "__main__":
    inputfile = ''
    outputfile = ''
    todo = Todo()
    # get old values
    todo.retriveTasks()

    argument = sys.argv[1:]
    if(argument[0] in ("--add","-a")):
        # below if statement is for checking task name
        # containg more than one word
        if(len(argument) > 4):
            difference = len(argument)-4
            taskName = ""
            tempList = []
            # joinng all text
            for i in range(1,1+difference+1):
                taskName = taskName + " " +argument[i]
                tempList.append(i)
            # removing first word index from capture list
            del tempList[0]
            # deleting every element from argument of captured
            # index
            for index in tempList:
                del argument[index]
            argument[1] = taskName
        task = Task(id = todo.count,name = argument[1],e_date = argument[2], priority = argument[3])
        todo.addTask(task)
        todo.saveTasks()
        print('Task has been saved (^o^)')

    elif(argument[0] == "--setstatus"):
        task_id = argument[1]
        task_status = argument[2]
        if(task_status in ("pending","working","done")):
            todo.updateStatus(task_id,task_status)
            todo.saveTasks()
            print('status changed successfully (~.~)')
        else:
            help()

    elif(argument[0] in ("--remove","-r")):
        todo.removeTask(argument[1])
        todo.saveTasks()
        print('Task has been removed successfully! (u_u)')

    elif(argument[0] in ("--view","-v")):
        todo.printTasks()

    else:
        help()