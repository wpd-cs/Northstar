# -*- coding: utf-8 -*-
"""
William Duong
Project started: November 17, 2021
wpduong@gmail.com
Last Updated: 02/02/2021
"""

from sys import exit
from multiprocessing import Process
import datetime
import csv
import os

class Populations:
	def __init__(self):
		"""Initialize class data members"""
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

	def prepLists(self):
		"""Remove CAIR employees and assign immunizations and dates \
		   to/from the Compliant dictionary"""

		# Remove CAIR employees
		rem = []
		for key in self.CAIR_patients.keys():
			if key in self.getAllEmployees().keys() and key in self.compliant.keys():
				rem.append(key)

		[self.compliant.pop(key) for key in rem]

		# Assign immunizations and dates to patients
		for key in self.compliant.keys():
			if key in self.CAIR_patients.keys():
				self.compliant[key].chainList(self.CAIR_patients[key])
				self.compliant[key].setEmployee(self.CAIR_patients[key].getEmployee())
				self.compliant[key].setStudent(self.CAIR_patients[key].getStudent())
				self.compliant[key].setDoseCount(len(self.CAIR_patients[key].getImmunizations()))

			self.compliant[key].fillLists()

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
		# Implement when needed
		pass

	def getCompliantDetails(self):
		"""Return immunization details"""
		return self.CAIR_patients




class Patient:
	def __init__ (self, cwid, patientType = "", status = "", \
				  acadStatus = "", employee = "", student = ""):
		"""Initialize class data members"""
		self.__cwid = cwid
		self.__patientType = patientType
		self.__status = status
		self.__acadStatus = acadStatus
		self.__immunizations = []
		self.__lots = []
		self.__adminDates = []
		self.__processingDates = []
		self.__doseCount = 0
		self.__isEmployee = employee
		self.__isStudent = student

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
		return self.__immunizations

	def getLots(self):
		"""Get lot number"""
		return self.__lots

	def getAdminDates(self):
		"""Get administration date"""
		return self.__adminDates

	def getProcessingDates(self):
		"""Get processing date"""
		return self.__processingDates

	def getEmployee(self):
		"""Return whether a patient is an employee"""
		return self.__isEmployee

	def getStudent(self):
		"""Return whether a patient is a student"""
		return self.__isStudent

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
		match immunization:
			case 'COVID-19, mRNA LNP-S PF 100mcg or 50mcg':
				self.__immunizations.append('COVID-19 Moderna mRNA-LNP spike')
			case 'COVID-19, mRNA,LNP-S,PF':
				self.__immunizations.append('COVID-19 Pfizer mRNA-LNP spike')
			case 'COVID-19, vector-nr, rS-Ad26, PF':
				self.__immunizations.append('COVID-19Janssen/J&J viral vector')
			case 'COVID-19, vector-nr, rS-ChAdOx1':
				self.__immunizations.append('COVID-19 AstraZeneca viralvector')
			case _:
				self.__immunizations.append(immunization)

	def appendLot(self, lot):
		"""Set lot number"""
		self.__lots.append(lot)

	def appendAdminDate(self, adminDate):
		"""Set administration date"""
		self.__adminDates.append(adminDate)

	def appendProcessingDate(self, processingDate):
		"""Set processing date"""
		self.__processingDates.append(processingDate)

	def setDoseCount(self, count):
		"""Set dose count"""
		self.__doseCount = count

	def getDoseCount(self):
		"""Return dose count"""
		return self.__doseCount

	def chainList(self, new):
		"""Put existing lists together"""
		self.__immunizations.extend(new.getImmunizations())
		self.__lots.extend(new.getLots())
		self.__adminDates.extend(new.getAdminDates())
		self.__processingDates.extend(new.getProcessingDates())

	def fillLists(self):
		"""Pad any lists that are not of length 3"""
		N = 3
		self.__immunizations += [''] * (N - len(self.__immunizations))
		self.__lots += [''] * (N - len(self.__lots))
		self.__adminDates += [''] * (N - len(self.__adminDates))
		self.__processingDates += [''] * (N - len(self.__processingDates))

	def setEmployee(self, employee):
		"""Set employee position"""
		self.__isEmployee = employee

	def setStudent(self, student):
		"""Set student position"""
		self.__isStudent = student



def checkFiles():
	"""Check to make sure all input files are present"""
	listOfFiles = ["compliance.csv", "employee.txt", "student.txt", \
				   "nonstate.txt", "cairs.csv"]

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
	with open("compliance.csv") as f:
		csv_reader = csv.reader(f)
		next(csv_reader)

		for row in csv_reader:
			# print(row)
			patient = Patient(row[3].strip("'"), status = row[6])

			match patient.getStatus():
				case 'Compliant with Standard Requirements':
					populations.compliant[patient.getCwid()] = patient
				case 'Awaiting Review':
					populations.aReview[patient.getCwid()] = patient
				case 'Exemption: Pos COVID-19 90 Days':
					populations.cExemption[patient.getCwid()] = patient
				case 'Exemption: Extension COVID-19':
					populations.eExemption[patient.getCwid()] = patient
				case 'Exemption: Medical COVID-19':
					populations.mExemption[patient.getCwid()] = patient
				case 'Exemption: Religious COVID-19':
					populations.rExemption[patient.getCwid()] = patient
				case 'Exemption: Pregnant COVID-19':
					populations.pExemption[patient.getCwid()] = patient
				case 'Exemption: Breast Feeding COVID':
					populations.bExemption[patient.getCwid()] = patient
				case _:
					populations.notCompliant[patient.getCwid()] = patient
	print("4 finishing\n")



def readCairReport(populations):
	"""Read in CAIR Report"""
	print("5 starting\n")
	with open("cairs.csv") as f:
		csv_reader = csv.reader(f)
		next(csv_reader)

		seen = []

		for row in csv_reader:
			cwid = row[0].strip('"')

			if row[4] != '""':
				if cwid in seen:
					populations.CAIR_patients[cwid].appendImmunization(row[3])
					populations.CAIR_patients[cwid].appendLot(row[4])
					populations.CAIR_patients[cwid].appendAdminDate(row[5])
					populations.CAIR_patients[cwid].appendProcessingDate(row[6])
				else:
					populations.CAIR_patients[cwid] = Patient(cwid, employee = row[7], \
															  student = row[8])
					populations.CAIR_patients[cwid].appendImmunization(row[3])
					populations.CAIR_patients[cwid].appendLot(row[4])
					populations.CAIR_patients[cwid].appendAdminDate(row[5])
					populations.CAIR_patients[cwid].appendProcessingDate(row[6])

					seen.append(row[0])
	populations.prepLists()
	print("5 finishing\n")



def createComplianceNUMBERS(populations, path, t):
	"""Create compliance numbers file"""
	print("6 starting\n")
	# cN = os.path.join(path, "Compliance_NUMBERS({}).txt".format(t))
	# with open(cN, "w", newline='') as f:
	# 	CONTINUE HERE
	
	print("6 finishing\n")



def createComplianceCWID(populations, path, t):
	"""Create compliance CWID file"""
	print("7 starting\n")
	p = populations.getCompliant()
	cN = os.path.join(path, "Compliance CWID({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for value in p.values():
			writer.writerow([value.getCwid()])
	print("7 finishing\n")



def createExemptionList(populations, path, t):
	"""Create exemption CWID file (for Central IT)"""
	print("8 starting\n")
	p = populations.getExemptions()
	cN = os.path.join(path, "Exemption List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for value in p.values():
			writer.writerow([value.getCwid()])
	print("8 finishing\n")



def createExemptList(populations, path, t):
	"""Create exempt CWID file (for PeopleSoft)"""
	print("9 starting\n")
	p = populations.getExemptions()
	cN = os.path.join(path, "Exempt List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for value in p.values():
			writer.writerow([value.getCwid(), value.getStatus().strip('"')])
	print("9 finishing\n")


def createPNCCompliantList(populations, path, t):
	"""Create participant CWID file"""
	print("10 starting\n")
	p = populations.getParticipants()
	cN = os.path.join(path, "PNC Compliant List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for value in p.values():
			writer.writerow([value.getCwid()])
	print("10 finishing\n")



def createActiveNonCompliant(populations, path, t):
	"""Create active, but not compliant CWID file"""
	print("11 starting\n")
	# p = populations.getActiveNotCompliant()
	# cN = os.path.join(path, "Active Non-Compliant({}).csv".format(t))
	# with open(cN, "w", newline='') as f:
	# 	writer = csv.writer(f)
	# 	for key in p.keys():
	# 		writer.writerow([key])
	print("11 finishing\n")



def createCompliantDetails(populations, path, t):
	"""Create file wih immunization details"""
	print("12 starting\n")
	p = populations.getCompliant()
	cN = os.path.join(path, "Compliant Details({}).csv".format(t))

	header = ['CWID', 'Dose Count', 'I1', 'AD1', 'PD1', 'L1', \
			  'I2', 'AD2', 'PD2', 'L2', 'I3', 'AD3', 'PD3', 'L3']

	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)

		writer.writerow(header)

		for value in p.values():
			row = [value.getCwid(), value.getDoseCount(), \
				   value.getImmunizations()[0], \
				   value.getAdminDates()[0], \
				   value.getProcessingDates()[0], \
				   value.getLots()[0], \
				   value.getImmunizations()[1], \
				   value.getAdminDates()[1], \
				   value.getProcessingDates()[1], \
				   value.getLots()[1], \
				   value.getImmunizations()[2], \
				   value.getAdminDates()[2], \
				   value.getProcessingDates()[2], \
				   value.getLots()[2]]
			writer.writerow(row)
	print("12 finishing\n")



def concurrent(*functions):
	"""Function for running processes concurrently"""
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

	checkFiles()

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

	concurrent(createComplianceNUMBERS(populations, path, t), createComplianceCWID(populations, path, t), \
			   createExemptionList(populations, path, t), createExemptList(populations, path, t), \
			   createPNCCompliantList(populations, path, t), createActiveNonCompliant(populations, path, t), \
			   createCompliantDetails(populations, path, t))
