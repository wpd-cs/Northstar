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

	def getAllEmployees(self):
		"""Return all types of employees"""
		temp = {}
		for d in [self.faculty, self.staff, self.asc, self.asi, \
				  self.nonstateStaff]:
			temp.update(d)
		return temp

	def getCompliant(self):
		"""Return all compliant patients"""
		rem = []

		for key in self.CAIR_patients.keys():
			if key in self.getAllEmployees().keys():
				rem.append(key)

		# # Cannot include employees with CAIRS data
		# for key in self.compliant.keys():
		# 	if key in self.CAIR_patients.keys() && key in self.getAllEmployees().keys():
		# 		if self.CAIR_patients[key].getLots():
		# 			rem.append(key)

		[self.compliant.pop(key) for key in rem]
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
		for d in [self.mExemption, self.rExemption, self.pExemption, \
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
	def __init__ (self, cwid, patientType = "", status = "", acadStatus = ""):
		"""Initialize class data members"""
		self.__cwid = cwid
		self.__patientType = patientType
		self.__status = status
		self.__acadStatus = acadStatus
		self.__immunizations = []
		self.__adminDates = []
		self.__lots = []

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

	def getImmunizations(self):
		"""Get immunization type"""
		return self.__immunization

	def getAdminDates(self):
		"""Get administration date"""
		return self.__adminDate

	def getLots(self):
		"""Get lot number"""
		return self.__lots

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
		self.__immunizations.append(immunization)

	def appendAdminDate(self, adminDate):
		"""Set administration date"""
		self.__adminDates.append(adminDate)

	def appendLot(self, lot):
		"""Set lot number"""
		self.__lots.append(lot)



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
				populations.nonstateStaff[patient.getCwid()] = patient
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
	print("5 starting\n")
	with open("cairs.txt", "r") as f:
		temp = f.readline()
		del temp

		seen = []

		for line in f:
			myLine = line.split(',')

			cwid = myLine[0].strip('"')

			if myLine[4] != '""':
				if cwid in seen:
					populations.CAIR_patients[cwid].appendImmunization(myLine[3])
					populations.CAIR_patients[cwid].appendAdminDate(myLine[5])
					populations.CAIR_patients[cwid].appendLot(myLine[4])
				else:
					populations.CAIR_patients[cwid] = Patient(cwid)
					populations.CAIR_patients[cwid].appendImmunization(myLine[3])
					populations.CAIR_patients[cwid].appendAdminDate(myLine[5])
					populations.CAIR_patients[cwid].appendLot(myLine[4])

					seen.append(myLine[0])
	print("5 finishing\n")



def createComplianceNUMBERS(populations, path, t):
	"""Create compliance numbers file"""
	print("6 starting\n")
	# cN = os.path.join(path, "Compliance_NUMBERS({}).txt".format(t))
	# with open(cN, "w", newline='') as f:
	# 	pass
	# 	CONTINUE HERE
	print("6 finishing\n")



def createComplianceCWID(populations, path, t):
	"""Create compliance CWID file"""
	print("7 starting\n")
	p = populations.getCompliant()
	cN = os.path.join(path, "Compliance CWID({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for key in p.keys():
			writer.writerow([key])
	print("7 finishing\n")



def createExemptionList(populations, path, t):
	"""Create exemption CWID file (for Central IT)"""
	print("8 starting\n")
	p = populations.getExemptions()
	cN = os.path.join(path, "Exemption List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for key, value in p.items():
			writer.writerow([key])
	print("8 finishing\n")



def createExemptList(populations, path, t):
	"""Create exempt CWID file (for PeopleSoft)"""
	print("9 starting\n")
	p = populations.getExemptions()
	cN = os.path.join(path, "Exempt List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for key, value in p.items():
			writer.writerow([key, value.getStatus().strip('"')])
	print("9 finishing\n")


def createPNCCompliantList(populations, path, t):
	"""Create participant CWID file"""
	print("10 starting\n")
	p = populations.getParticipants()
	cN = os.path.join(path, "PNC Compliant List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for key in p.keys():
			writer.writerow([key])
	print("10 finishing\n")



# def createActiveNonCompliant(populations, path, t):
# 	"""Create active, but not compliant CWID file"""
# 	p = populations.getActiveNotCompliant()
# 	cN = os.path.join(path, "Active Non-Compliant({}).csv".format(t))
# 	with open(cN, "w", newline='') as f:
# 		writer = csv.writer(f)
# 		for key in p.keys():
# 			writer.writerow([key])



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

	concurrent(createComplianceCWID(populations, path, t), createExemptionList(populations, path, t), \
			   createExemptList(populations, path, t), createPNCCompliantList(populations, path, t))