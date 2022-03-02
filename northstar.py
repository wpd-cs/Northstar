# -*- coding: utf-8 -*-
"""
William Duong
Project started: November 17, 2021
wpduong@gmail.com
Last Updated: 03/02/2021
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

		self.cair_EMP = {}
		self.cair_STU = {}

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

	def getAllStudents(self):
		"""Return all types of students"""
		temp = {}
		for d in [self.cStudents, self.fStudents]:
			temp.update(d)
		return temp

	def getAllCAIRS(self):
		"""Return all CAIRS data"""
		temp = {}
		for d in [self.cair_EMP, self.cair_STU]:
			temp.update(d)
		return temp

	def prepLists(self):
		"""Assign immunizations and dates to/from the Compliant dictionary"""

		for key in self.cair_EMP.keys():
			self.cair_EMP[key].fillLists()
		for key in self.cair_STU.keys():
			self.cair_STU[key].fillLists()

		p = populations.getAllCAIRS()
		for key in p.keys():
			if p[key].checkCompliance():
				self.compliant[key] = p[key]
			else:
				continue

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
		self.__PScodes = []
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

	def getPScodes(self):
		"""Get PS code"""
		return self.__PScodes

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
			case ('COVID-19, mRNA LNP-S PF 100mcg or 50mcg' | 'COVID-19 Moderna mRNA-LNP spike' | 'COVID19 Moderna mRNA-LNP spike'):
				self.__immunizations.append('COVID19 Moderna mRNA-LNP spike')
			case 'Pfizer mRNA LNP-S PF 12yrs and older':
				self.__immunizations.append('COVID19 Pfizer mRNA-LNP Spk 12yr')
			case ('COVID-19, mRNA,LNP-S,PF' | 'COVID-19 Pfizer mRNA-LNP spike' | 'COVID19 Pfizer mRNA-LNP spike'):
				self.__immunizations.append('COVID19 Pfizer mRNA-LNP spike')
			case ('COVID-19, vector-nr, rS-Ad26, PF' | 'COVID19 Janssen/J&J viral vector' | 'COVID-19Janssen/J&J viral vector'):
				self.__immunizations.append('COVID19 Janssen/J&J viral vector')
			case ('COVID-19, vector-nr, rS-ChAdOx1' | 'COVID-19 AstraZeneca viralvector' | 'COVID19 AstraZeneca viralvector'):
				self.__immunizations.append('COVID19 AstraZeneca viralvector')
			case _:
				self.__immunizations.append(immunization)
		self.__doseCount += 1

	def appendPScode(self, immunization):
		"""Set PS code"""
		match immunization:
			case ('COVID-19, mRNA LNP-S PF 100mcg or 50mcg' | 'COVID19 Moderna 50mcg booster' | 'COVID19 Moderna mRNA-LNP spike' | 'COVID-19 Moderna mRNA-LNP spike'):
				self.__PScodes.append('MOD')
			case ('COVID-19, mRNA,LNP-S,PF' | 'COVID19 Pfizer mRNA-LNP spike' | 'Pfizer mRNA LNP-S PF 12yrs and older' | 'COVID-19 Pfizer mRNA-LNP spike' | 'COVID19 Pfizer mRNA-LNP Spk 12yr'):
				self.__PScodes.append('PFZ')
			case ('COVID-19, vector-nr, rS-Ad26, PF' | 'COVID19 Janssen/J&J viral vector' | 'COVID-19Janssen/J&J viral vector'):
				self.__PScodes.append('J&J')
			case _:
				self.__PScodes.append('NL2')

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
		self.__PScodes.extend(new.getPScodes())
		self.__lots.extend(new.getLots())
		self.__adminDates.extend(new.getAdminDates())
		self.__processingDates.extend(new.getProcessingDates())

	def fillLists(self):
		"""Pad any lists that are not of length 3"""
		N = 3
		self.__immunizations += ['N/A'] * (N - len(self.__immunizations))
		self.__PScodes += ['N/A'] * (N - len(self.__PScodes))
		self.__lots += ['N/A'] * (N - len(self.__lots))
		self.__adminDates += ['N/A'] * (N - len(self.__adminDates))
		self.__processingDates += ['N/A'] * (N - len(self.__processingDates))

	def checkCompliance(self):
		"""Check vaccination compliance of patient"""
		if (self.__PScodes.count('MOD') >= 2) or (self.__PScodes.count('PFZ') >= 2) \
			or (self.__PScodes.count('J&J') >= 1) or (self.__PScodes.count('NL2') >= 2):
			return True
		elif ((self.__immunizations.count('COVID19 Moderna mRNA-LNP spike') >= 1) \
			or (self.__immunizations.count('COVID19 Pfizer mRNA-LNP Spk 12yr') >= 1) \
			or (self.__immunizations.count('COVID19 Pfizer mRNA-LNP spike') >= 1)) and \
			(self.__PScodes.count('NL2') >= 1):
			return True
		else:
			return False

	def setEmployee(self, employee):
		"""Set employee position"""
		self.__isEmployee = employee

	def setStudent(self, student):
		"""Set student position"""
		self.__isStudent = student



def checkFiles():
	"""Check to make sure all input files are present"""
	listOfFiles = ["compliance.csv", "employee.txt", "student.txt", \
				   "nonstate.txt", "c19emp.csv", "c19stu.csv"]

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
					# populations.compliant[patient.getCwid()] = patient
					continue
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



def readC19Emp(populations):
	"""Read in C19 employee report excluding CAIRs data"""
	print("5 starting\n")
	with open("c19emp.csv") as f:
		csv_reader = csv.reader(f)
		next(csv_reader)

		seen = []

		for row in csv_reader:
			cwid = row[0].strip('"')

			if cwid in seen:
				populations.cair_EMP[cwid].appendImmunization(row[1])
				populations.cair_EMP[cwid].appendPScode(row[1])
				populations.cair_EMP[cwid].appendLot(row[2])
				populations.cair_EMP[cwid].appendAdminDate(row[3])
				populations.cair_EMP[cwid].appendProcessingDate(row[6])
			else:
				populations.cair_EMP[cwid] = Patient(cwid, employee = row[5], \
														  student = row[6])
				populations.cair_EMP[cwid].appendImmunization(row[1])
				populations.cair_EMP[cwid].appendPScode(row[1])
				populations.cair_EMP[cwid].appendLot(row[2])
				populations.cair_EMP[cwid].appendAdminDate(row[3])
				populations.cair_EMP[cwid].appendProcessingDate(row[4])

				seen.append(row[0])
	print("5 finishing\n")



def readC19Stu(populations):
	"""Read in C19 student report including CAIRs data"""
	print("6 starting\n")
	with open("c19stu.csv") as f:
		csv_reader = csv.reader(f)
		next(csv_reader)

		seen = []

		for row in csv_reader:
			cwid = row[0].strip('"')

			if cwid in seen:
				populations.cair_STU[cwid].appendImmunization(row[1])
				populations.cair_STU[cwid].appendPScode(row[1])
				populations.cair_STU[cwid].appendLot(row[2])
				populations.cair_STU[cwid].appendAdminDate(row[3])
				populations.cair_STU[cwid].appendProcessingDate(row[4])
			else:
				populations.cair_STU[cwid] = Patient(cwid, employee = row[5], \
														  student = row[6])
				populations.cair_STU[cwid].appendImmunization(row[1])
				populations.cair_STU[cwid].appendPScode(row[1])
				populations.cair_STU[cwid].appendLot(row[2])
				populations.cair_STU[cwid].appendAdminDate(row[3])
				populations.cair_STU[cwid].appendProcessingDate(row[4])

				seen.append(row[0])
	print("6 finishing\n")



def createComplianceNUMBERS(populations, path, t):
	"""Create compliance numbers file"""
	print("7 starting\n")
	# cN = os.path.join(path, "Compliance_NUMBERS({}).txt".format(t))
	# with open(cN, "w", newline='') as f:
	# 	CONTINUE HERE
	
	print("7 finishing\n")



def createComplianceCWID(populations, path, t):
	"""Create compliance CWID file"""
	print("8 starting\n")
	p = populations.getCompliant()
	cN = os.path.join(path, "Primary Compliance CWID({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for value in p.values():
			writer.writerow([value.getCwid()])
	print("8 finishing\n")



def createExemptionList(populations, path, t):
	"""Create exemption CWID file (for Central IT)"""
	print("9 starting\n")
	p = populations.getExemptions()
	cN = os.path.join(path, "Exemption List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for value in p.values():
			writer.writerow([value.getCwid()])
	print("9 finishing\n")



def createExemptList(populations, path, t):
	"""Create exempt CWID file (for PeopleSoft)"""
	print("10 starting\n")
	p = populations.getExemptions()
	cN = os.path.join(path, "Exempt List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for value in p.values():
			writer.writerow([value.getCwid(), value.getStatus().strip('"')])
	print("10 finishing\n")



def createPNCCompliantList(populations, path, t):
	"""Create participant CWID file"""
	print("11 starting\n")
	p = populations.getParticipants()
	cN = os.path.join(path, "PNC Compliant List({}).csv".format(t))
	with open(cN, "w", newline='') as f:
		writer = csv.writer(f)
		for value in p.values():
			writer.writerow([value.getCwid()])
	print("11 finishing\n")



def createActiveNonCompliant(populations, path, t):
	"""Create active, but not compliant CWID file"""
	print("12 starting\n")
	# p = populations.getActiveNotCompliant()
	# cN = os.path.join(path, "Active Non-Compliant({}).csv".format(t))
	# with open(cN, "w", newline='') as f:
	# 	writer = csv.writer(f)
	# 	for key in p.keys():
	# 		writer.writerow([key])
	print("12 finishing\n")



def createCompliantDetails(populations, path, t):
	"""Create file with immunization details"""
	print("13 starting\n")
	p = populations.getAllCAIRS()
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
	print("13 finishing\n")



def createPSCodeReportsEMP(populations, path, t):
	"""Create a file with PS codes"""
	print("14 starting\n")
	p = populations.cair_EMP

	cE = os.path.join(path, "C19 EMP({}).csv".format(t))

	header = ['CWID', 'Administered Date', 'PS Code', 'Immunization']

	with open(cE, "w", newline='') as f:
		writer = csv.writer(f)

		writer.writerow(header)

		for value in p.values():
			rows = [
					[value.getCwid(), value.getAdminDates()[0], value.getPScodes()[0], value.getImmunizations()[0]],
					[value.getCwid(), value.getAdminDates()[1], value.getPScodes()[1], value.getImmunizations()[1]],
					[value.getCwid(), value.getAdminDates()[2], value.getPScodes()[2], value.getImmunizations()[2]],
				   ]

			writer.writerows(rows)
	print("14 finishing\n")



def createPSCodeReportsSTU(populations, path, t):
	"""Create a file with PS codes"""
	print("15 starting\n")
	p = populations.cair_STU

	cS = os.path.join(path, "C19 STU({}).csv".format(t))

	header = ['CWID', 'Administered Date', 'PS Code', 'Immunization']

	with open(cS, "w", newline='') as f:
		writer = csv.writer(f)

		writer.writerow(header)

		for value in p.values():

			rows = [
					[value.getCwid(), value.getAdminDates()[0], value.getPScodes()[0], value.getImmunizations()[0]],
					[value.getCwid(), value.getAdminDates()[1], value.getPScodes()[1], value.getImmunizations()[1]],
					[value.getCwid(), value.getAdminDates()[2], value.getPScodes()[2], value.getImmunizations()[2]],
				   ]

			writer.writerows(rows)
	print("15 finishing\n")



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
			   readC19Emp(populations), readC19Stu(populations))

	populations.prepLists()

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
			   createCompliantDetails(populations, path, t), createPSCodeReportsEMP(populations, path, t), \
			   createPSCodeReportsSTU(populations, path, t))
