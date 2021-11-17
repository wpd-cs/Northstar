# -*- coding: utf-8 -*-
"""

William Duong
Project started: November 17, 2021
wpduong@gmail.com

Last Updated: 11/17/2021

"""


class Populations(self):
	self.cStudents = []
	self.fStudents = []
	self.faculty = []
	self.staff = []
	self.asc = []
	self.asi = []
	self.nonstateStaff
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

	def getCompliant(self):
		"""Return all compliant patients"""
		return self.compliant

	def getExemptions(self):
		return 	self.eExemption + \
				self.mExemption + \
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
		"""copy this: https://blog.finxter.com/how-to-get-specific-elements-from-a-list/#Get_Elements_from_List_using_filter"""
		pass



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



def readInEmployees(populations):
	"""Read in employee extract"""
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



def readInStudents(populations):
	"""Read in student extract"""
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



def readInNonState(populations):
	"""Read in non-state extract"""
	with open("nonstate.txt", "r") as f:
		temp = f.readline()
		del temp

		for line in f:
			myLine = line.split('|')

			patient = Patient(myLine[0], myLine[9])

			if patient.getPatientType() == "ASC":
				populations.asc.append(patient)
			else if patient.getPatientType() == "ASI":
				populations.asi.append(patient)
			else:
				populations.nonstateStaff.append(patient)



def readInCompliance(populations):
	"""Read in PNC Data"""
	with open("compliance.txt", "r") as f:
		temp = f.readline()
		del temp

		for line in f:
			myLine = line.split(',')

			cwid = myLine[3].strip('"')
			pstatus = myLine[7]

			patient = Patient(cwid, status = pstatus)

			if patient.getStatus() == '"Compliant with Standard Requirements"':
				populations.compliant.append(patient)
			if patient.getStatus() == '"Awaiting Review"':
				populations.aReview.append(patient)
			if patient.getStatus() == '"Exemption: Pos COVID-19 90 Days"':
				populations.cExemption.append(patient)
			if patient.getStatus() == '"Exemption: Extension COVID-19"':
				populations.eExemption.append(patient)
			if patient.getStatus() == '"Exemption: Medical COVID-19"':
				populations.mExemption.append(patient)
			if patient.getStatus() == '"Exemption: Religious COVID-19"':
				populations.rExemption.append(patient)
			if patient.getStatus() == '"Exemption: Pregnant COVID-19"':
				populations.pExemption.append(patient)
			if patient.getStatus() == '"Exemption: Breast Feeding COVID"':
				populations.bExemption.append(patient)
			else:
				populations.notCompliant.append(patient)






def main():
	"""Main function"""

	# Initialize variables

	populations = Populations()



main()