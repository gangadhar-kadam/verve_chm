# Copyright (c) 2015, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe import throw, _, msgprint
import frappe.share
from frappe.utils import cstr,now,add_days,nowdate,cint

class AttendanceRecord(Document):
	def validate(self):
		pass

	def autoname(self):
		from frappe.model.naming import make_autoname
		if self.attendance_type=='Event Attendance':
			sub=self.meeting_sub[:3].upper()
			self.name = make_autoname('EVATT' + '.####')
		else:
			if self.meeting_category=='Cell Meeting':
				self.name = make_autoname(self.cell + '/' + 'CELL' + 'ATT' + '.####')
			else :
				sub=self.meeting_sub[:3].upper()
				self.name = make_autoname(self.cell + '/' + sub + 'ATT' + '.####')			
	
	def load_participents(self):
		self.set('invitation_member_details', [])
		member_ftv=''
		if self.cell:
			member_ftv = frappe.db.sql("select name,ftv_name,email_id from `tabFirst Timer` where cell='%s' and approved=0 union select name,member_name,email_id from `tabMember` where cell='%s' "%(self.cell,self.cell))
		elif self.church:
			member_ftv = frappe.db.sql("select name,ftv_name,email_id from `tabFirst Timer` where church='%s' and approved=0 union select name,member_name,email_id from `tabMember` where church='%s'"%(self.church,self.church))	
		for d in member_ftv:
			child = self.append('invitation_member_details', {})
			child.member = d[0]
			child.member_name = d[1]
			child.email_id = d[2]

	# def set_higher_values(self):
	# 	if self.region:
	# 		value = frappe.db.sql("select zone,church_group,church,pcf,senior_cell,name from `tabCells` where region='%s'"%(self.region),as_list=1)
	# 		ret={}
	# 		if value:
	# 			ret={
	# 				"zone": value[0][0],
	# 				"church_group": value[0][1],
	# 				"church" : value[0][2],
	# 				"pcf" : value[0][3],
	# 				"senior_cell" : value[0][4],
	# 				"cell" : value[0][5]
	# 			}
	# 		return ret
	# 	elif self.zone:
	# 		value = frappe.db.sql("select region,church_group,church,pcf,senior_cell,name from `tabCells` where zone='%s'"%(self.zone),as_list=1)
	# 		ret={}
	# 		if value:
	# 			ret={
	# 				"region": value[0][0],
	# 				"church_group": value[0][1],
	# 				"church" : value[0][2],
	# 				"pcf" : value[0][3],
	# 				"senior_cell" : value[0][4],
	# 				"cell" : value[0][5]
	# 			}
	# 		return ret
	# 	elif self.church_group:
	# 		value = frappe.db.sql("select region,zone,church,pcf,senior_cell,name from `tabCells` where church_group='%s'"%(self.church_group),as_list=1)
	# 		ret={}
	# 		if value:
	# 			ret={
	# 				"region": value[0][0],
	# 				"zone": value[0][1],
	# 				"church" : value[0][2],
	# 				"pcf" : value[0][3],
	# 				"senior_cell" : value[0][4],
	# 				"cell" : value[0][5]
	# 			}
	# 		return ret
	# 	elif self.church:
	# 		value = frappe.db.sql("select region,zone,church_group,pcf,senior_cell,name from `tabCells` where church='%s'"%(self.church),as_list=1)
	# 		ret={}
	# 		if value:
	# 			ret={
	# 				"region": value[0][0],
	# 				"zone": value[0][1],
	# 				"church_group" : value[0][2],
	# 				"pcf" : value[0][3],
	# 				"senior_cell" : value[0][4],
	# 				"cell" : value[0][5]
	# 			}
	# 		return ret
	# 	elif self.pcf:
	# 		value = frappe.db.sql("select region,zone,church_group,church,senior_cell,name from `tabCells` where pcf='%s'"%(self.pcf),as_list=1)
	# 		ret={}
	# 		if value:
	# 			ret={
	# 				"region": value[0][0],
	# 				"zone": value[0][1],
	# 				"church_group" : value[0][2],
	# 				"church" : value[0][3],
	# 				"senior_cell" : value[0][4],
	# 				"cell" : value[0][5]
	# 			}
	# 		return ret
	# 	elif self.senior_cell:
	# 		value = frappe.db.sql("select region,zone,church_group,church,pcf,name from `tabCells` where senior_cell='%s'"%(self.senior_cell),as_list=1)
	# 		ret={}
	# 		if value:
	# 			ret={
	# 				"region": value[0][0],
	# 				"zone": value[0][1],
	# 				"church_group" : value[0][2],
	# 				"church" : value[0][3],
	# 				"pcf" : value[0][4],
	# 				"cell" : value[0][5]
	# 			}
	# 		return ret
	# 	elif self.cell:
	# 		value = frappe.db.sql("select region,zone,church_group,church,pcf,senior_cell from `tabCells` where name='%s'"%(self.cell),as_list=1)
	# 		ret={}
	# 		if value:
	# 			ret={
	# 				"region": value[0][0],
	# 				"zone": value[0][1],
	# 				"church_group" : value[0][2],
	# 				"church" : value[0][3],
	# 				"pcf" : value[0][4],
	# 				"senior_cell" : value[0][5]
	# 			}
	# 		return ret

def validate_duplicate(doc,method):
	frappe.errprint("hello gangadhar")
	frappe.errprint(doc.data_17)
	if doc.get("__islocal"):
		if not doc.invitation_member_details:
			doc.load_participents()
		fdate=doc.from_date.split(" ")
		f_date=fdate[0]
		tdate=doc.to_date.split(" ")
		t_date=tdate[0]
		res=frappe.db.sql("select name from `tabAttendance Record` where (cell='%s' or church='%s') and from_date like '%s%%' and to_date like '%s%%'"%(doc.cell,doc.church,f_date,t_date))
		#frappe.errprint(res)
		if res:
			frappe.throw(_("Attendance Record '{0}' is already created for same details on same date '{1}'").format(res[0][0],f_date))

		if doc.from_date and doc.to_date:
			if doc.from_date >= doc.to_date:
				frappe.throw(_("To Date should be greater than From Date..!"))

		if len(doc.invitation_member_details)<1:
			pass
			#rappe.throw(_("Attendance Member table is empty.There should be at least 1 member in attendance list. Please load members in table."))

		if doc.data_17 and cint(doc.data_17) <= 0 :
				frappe.throw(_("Total Attendance cannot be negative..!"))
		if doc.number_of_first_timers and cint(doc.number_of_first_timers) <= 0 :
				frappe.throw(_("Number of First Timers cannot be negative..!"))
		if doc.data_19 and cint(doc.data_19) <= 0 :
				frappe.throw(_("Number of New Converts cannot be negative..!"))
		if doc.data_20 and cint(doc.data_20) <= 0 :
				frappe.throw(_("Total Cell Offering cannot be negative..!"))
