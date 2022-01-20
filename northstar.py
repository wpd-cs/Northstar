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
		self.cStudents = {}
		self.fStudents = {}
		self.faculty = {}
		self.staff = {}
		self.asc = {}
		self.asi = {}
		self.nonstateStaff = {}
		self.unspecified = {}

		self.compliant = {}
		self.aReview = {}
		self.cExemption = {}
		self.eExemption = {}
		self.mExemption = {}
		self.rExemption = {}
		self.pExemption = {}
		self.bExemption = {}
		self.notCompliant = {}

		self.CAIR_patients = {}

	def getAllTypes(self):
		"""Return all types of patients"""
		temp = {}
		for d in [self.cStudents, self.fStudents, self.faculty, self.staff, \
				  self.asc, self.asi, self.nonstateStaff, self.unspecified]:
			temp.update(d)
		return temp

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
		"""Return exemptions"""
		temp = {}
		for d in [self.mExemption, self.rExemption, self.pExemption, /
				  self.bExemption]:
			temp.update(d)
		return temp

	def getParticipants(self):
		"""Return all patients who are compliant or 
		   have attempted to comply"""
		temp = {}
		for d in [self.compliant, self.aReview, self.cExemption, \
				  self.eExemption, self.mExemption, self.rExemption, \
				  self.pExemption, self.bExemption]:
			temp.update(d)
		return temp

	def getActiveNotCompliant(self):
		"""Return all non-compliant active patients"""
		# REDO
		pass



class Patient:
	def __init__ (self, cwid, patientType = "", status = "", acadStatus = "", immunizations = [], adminDates = []):
		"""Initialize class data members"""
		self.__cwid = cwid
		self.__patientType = patientType
		self.__status = status
		self.__acadStatus = acadStatus
		self.__immunizations = immunizations
		self.__adminDates = adminDates

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

	def getImmunization(self):
		"""Get immunization type"""
		return self.__immunization

	def getAdminDate(self):
		"""Get administration date"""
		return self.__adminDate

	def setPatientType(self, patientType):
		"""Set patient type"""
		self.__patientType = patientType

	def setStatus(self, status):
		"""Set patient PNC status"""
		self.__status = status

	def setAcadStatus(self, acadStatus):
		"""Set patient academic status"""
		self.__acadStatus = acadStatus

	def appendImmunization(self, immunization):
		"""Set immunization type"""
		self.__immunizations = immunization

	def appendAdminDate(self, adminDate):
		"""Set administration date"""
		self.__adminDates.append(adminDate)



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

			patient = Patient(myLine[0].strip('"'), myLine[21])

			if patient.getPatientType() == "Faculty":
				populations.faculty[patient.getCwid()] = patient
			else:
				populations.staff[patient.getCwid()] = patient
	print("1 finishing\n")



def readInStudents(populations):
	"""Read in student extract"""
	print("2 starting\n")
	with open("student.txt", "r") as f:
		temp = f.readline()
		del temp

		for line in f:
			myLine = line.split('|')

			patient = Patient(myLine[0].strip('"'), "Student", acadStatus = myLine[52])

			if patient.getAcadStatus() == "ACTIVE":
				populations.cStudents[patient.getCwid()] = patient
			else:
				populations.fStudents[patient.getCwid()] = patient
	print("2 finishing\n")



def readInNonState(populations):
	"""Read in non-state extract"""
	print("3 starting\n")
	with open("nonstate.txt", "r") as f:
		temp = f.readline()
		del temp

		for line in f:
			myLine = line.split('|')

			patient = Patient(myLine[0].strip('"'), myLine[9])

			if patient.getPatientType() == "ASC":
				populations.asc[patient.getCwid()] = patient
			elif patient.getPatientType() == "ASI":
				populations.asi[patient.getCwid()] = patient
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

			patient = Patient(myLine[3].strip('"'), status = myLine[7])

			match patient.getStatus():
				case '"Compliant with Standard Requirements"':
					populations.compliant[patient.getCwid()] = patient
				case '"Awaiting Review"':
					populations.aReview[patient.getCwid()] = patient
				case '"Exemption: Pos COVID-19 90 Days"':
					populations.cExemption[patient.getCwid()] = patient
				case '"Exemption: Extension COVID-19"':
					populations.eExemption[patient.getCwid()] = patient
				case '"Exemption: Medical COVID-19"':
					populations.mExemption[patient.getCwid()] = patient
				case '"Exemption: Religious COVID-19"':
					populations.rExemption[patient.getCwid()] = patient
				case '"Exemption: Pregnant COVID-19"':
					populations.pExemption[patient.getCwid()] = patient
				case '"Exemption: Breast Feeding COVID"':
					populations.bExemption[patient.getCwid()] = patient
				case _:
					populations.notCompliant[patient.getCwid()] = patient
	print("4 finishing\n")



def readCairReport(populations):
	"""Read in CAIR Report"""
	with open("sample.txt", "r") as f:
		temp = f.readline()
		del temp

		seen = []

		for line in f:
			myLine = line.split(',')
			if myLine[0] in seen:
				populations.CAIR_patients[myLine[0]]["immunizations"].append(myLine[3])
				populations.CAIR_patients[myLine[0]]["adminDates"].append(myLine[5])
			else:
				populations.CAIR_patients[myLine[0]]["immunizations"] = []
				populations.CAIR_patients[myLine[0]]["adminDates"] = []
				seen.append(myLine[0])




def createComplianceNUMBERS(populations, path, t):
	"""Create compliance numbers file"""
	cN = os.path.join(path, "Compliance_NUMBERS({}).txt".format(t))
	with open(cN, "w", newline='') as f:
		pass
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
			   readInNonState(populations), readInCompliance(populations), \
			   readCairReport(populations))
	
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