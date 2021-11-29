# -*- coding: utf-8 -*-
"""

William Duong
Project started: November 17, 2021
wpduong@gmail.com

Last Updated: 11/17/2021

"""

from sys import exit
from multiprocessing import Process
import datetime
import csv
import os

class Populations:
	def __init__(self):
		self.cStudents = []
		self.fStudents = []
		self.faculty = []
		self.staff = []
		self.asc = []
		self.asi = []
		self.nonstateStaff = []
		self.unspecified = []

		self.compliant = []
		self.aReview = []
		self.cExemption = []
		self.eExemption = []
		self.mExemption = []
		self.rExemption = []
		self.pExemption = []
		self.bExemption = []
		self.notCompliant = []

	def getAllTypes(self):
		return self.cStudents + \
			   self.fStudents + \
			   self.faculty + \
			   self.staff + \
			   self.asc + \
			   self.asi + \
			   self.nonstateStaff + \
			   self.unspecified

	def getCompliant(self):
		"""Return all compliant patients"""
		return self.compliant

	def getNotCompliant(self):
		"""Return all non-compliant patients"""
		return self.notCompliant

	def getExtensionExemptions(self):
		"""Return all extension exemptions"""
		return self.eExemption

	def getExemptions(self):
		return 	self.mExemption + \
				self.rExemption + \
				self.pExemption + \
				self.bExemption

	def getParticipants(self):
		"""Return all patients who are compliant or 
		   have attempted to comply"""
		return self.compliant + \
			   self.aReview + \
			   self.cExemption + \
			   self.eExemption + \
			   self.mExemption + \
			   self.rExemption + \
			   self.pExemption + \
			   self.bExemption

	def getActiveNotCompliant(self):
		"""Return all non-compliant active patients"""
		def dist(patient):
			return patient.getPatientType()

		active = list(filter(lambda x: dist(x) != "", self.getAllTypes()))

		st = set((p.getCwid()) for p in self.getNotCompliant())

		return ([p for p in active if (p.getCwid()) in st])



class Patient:
	def __init__ (self, cwid, patientType = "", status = "", acadStatus = ""):
		"""Initialize class data members"""
		self.__cwid = cwid
		self.__patientType = patientType
		self.__status = status
		self.__acadStatus = acadStatus

	def getCwid(self):
		"""Get CWID"""
		return self.__cwid

	def getPatientType(self):
		"""Get patient type"""
		return self.__patientType

	def getStatus(self):
		"""Get status"""
		return self.__status

	def getAcadStatus(self):
		"""Get academic status"""
		return self.__acadStatus

	def setPatientType(self, patientType):
		"""Set patient type"""
		self.__patientType = patientType

	def setStatus(self, status):
		"""Set patient PNC status"""
		self.__status = status

	def setAcadStatus(self, acadStatus):
		"""Set patient academic status"""
		self.__acadStatus = acadStatus



def checkFiles():
	"""Check to make sure all input files are present"""
	listOfFiles = ["compliance.txt", "employee.txt", "student.txt", \
				   "nonstate.txt"]

	filesNeeded = []

	for file in listOfFiles:
		if not os.path.exists(file):
			filesNeeded.append(file)

	if filesNeeded:
		exit("ERROR\nMissing files: {}".format(filesNeeded))



def readInEmployees(populations):
	"""Read in employee extract"""
	print("1 starting\n")
	with open("employee.txt", "r") as f:
		temp = f.readline()
		del temp

		for line in f:
			myLine = line.split('|')

			patient = Patient(myLine[0], myLine[21])

			if patient.getPatientType() == "Faculty":
				populations.faculty.append(patient)
			else:
				populations.staff.append(patient)
	print("1 finishing\n")



def readInStudents(populations):
	"""Read in student extract"""
	print("2 starting\n")
	with open("student.txt", "r") as f:
		temp = f.readline()
		del temp

		for line in f:
			myLine = line.split('|')

			patient = Patient(myLine[0], "Student", acadStatus = myLine[52])

			if patient.getAcadStatus() == "ACTIVE":
				populations.cStudents.append(patient)
			else:
				populations.fStudents.append(patient)
	print("2 finishing\n")



def readInNonState(populations):
	"""Read in non-state extract"""
	print("3 starting\n")
	with open("nonstate.txt", "r") as f:
		temp = f.readline()
		del temp

		for line in f:
			myLine = line.split('|')

			patient = Patient(myLine[0], myLine[9])

			if patient.getPatientType() == "ASC":
				populations.asc.append(patient)
			elif patient.getPatientType() == "ASI":
				populations.asi.append(patient)
			else:
				populations.nonstateStaff.append(patient)
	print("3 finishing\n")



def readInCompliance(populations):
	"""Read in PNC Data"""
	print("4 starting\n")
	with open("compliance.txt", "r") as f:
		temp = f.readline()
		del temp

		for line in f:
			myLine = line.split(',')

			cwid = myLine[3].strip('"')
			pstatus = myLine[7]

			patient = Patient(cwid, status = pstatus)

			match patient.getStatus():
				case '"Compliant with Standard Requirements"':
					populations.compliant.append(patient)
				case '"Awaiting Review"':
					populations.aReview.append(patient)
				case '"Exemption: Pos COVID-19 90 Days"':
					populations.cExemption.append(patient)
				case '"Exemption: Extension COVID-19"':
					populations.eExemption.append(patient)
				case '"Exemption: Medical COVID-19"':
					populations.mExemption.append(patient)
				case '"Exemption: Religious COVID-19"':
					populations.rExemption.append(patient)
				case '"Exemption: Pregnant COVID-19"':
					populations.pExemption.append(patient)
				case '"Exemption: Breast Feeding COVID"':
					populations.bExemption.append(patient)
				case _:
					populations.notCompliant.append(patient)
	print("4 finishing\n")



def createComplianceNUMBERS(populations, path, t):
	"""Create compliance numbers file"""
	cN = os.path.join(path, "Compliance_NUMBERS({}).txt".format(t))
	with open(cN, "w", newline='') as f:
		# CONTINUE HERE



def createComplianceCWID(populations, path, t):
	"""Create compliance CWID file"""
	p = populations.getCompliant()
	a = [[item.getCwid()] for item in p]
	cN = os.path.join(path, "Compliance CWID({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		with f:
			write = csv.writer(f)
			write.writerows(a)



def createExemptionList(populations, path, t):
	"""Create exemption CWID file (for Central IT)"""
	p = populations.getExemptions()
	a = [[item.getCwid()] for item in p]
	cN = os.path.join(path, "Exemption List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		with f:
			write = csv.writer(f)
			write.writerows(a)



def createExemptList(populations, path, t):
	"""Create exempt CWID file (for PeopleSoft)"""
	a = [[item.getCwid(), item.getStatus().strip('"')] for item in p]
	cN = os.path.join(path, "Exempt List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		with f:
			write = csv.writer(f)
			write.writerows(a)



def createPNCCompliantList(populations, path, t):
	"""Create participant CWID file"""
	p = populations.getParticipants()
	a = [[item.getCwid()] for item in p]
	cN = os.path.join(path, "PNC Compliant List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		with f:
			write = csv.writer(f)
			write.writerows(a)



def createActiveNonCompliant(populations, path, t):
	"""Create active, but not compliant CWID file"""
	p = populations.getActiveNotCompliant()
	a = [[item.getCwid()] for item in p]
	cN = os.path.join(path, "Active Non-Compliant({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		with f:
			write = csv.writer(f)
			write.writerows(a)



def concurrent(*functions):
	proc = []
	for fn in functions:
		p = Process(target=fn)
		p.start()
		proc.append(p)
	for p in proc:
		p.join()



populations = Populations()



if __name__ == "__main__":
	"""Main function"""

	# Initialize variables

	# populations = Populations()

	concurrent(readInEmployees(populations), readInStudents(populations), \
			   readInNonState(populations), readInCompliance(populations))
	
	# Get current time
	d = datetime.datetime.now()
	e = d.strftime("%m-%d-%y %H%M%S %p")

	# Get today's date
	t = d.strftime("%b-%d-%Y")

	# Create folder
	parent_dir = os.getcwd()
	path = os.path.join(parent_dir, e)
	os.mkdir(path)

	concurrent()