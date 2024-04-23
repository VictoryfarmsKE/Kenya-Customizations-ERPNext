# Copyright (c) 2024, Navari Limited and contributors
# For license information, please see license.txt
from datetime import datetime

import frappe
from frappe.model.document import Document

class CasualPayrollPayout(Document):
	def validate(self):
		if not self.attendance_date:
			frappe.throw("Attendance Date is mandatory field")
		if not self.shift_type:
			frappe.throw("Shift Type is mandatory field")
   
	# def on_submit(self):
	# 	employees=self.casual_payrol_payout_employee
	# 	for employee in employees:
	# 		additional_salary=frappe.new_doc("Additional Salary")
	# 		additional_salary.employee=employee.employee
	# 		additional_salary.employee_name=employee.employee_name
	# 		additional_salary.salary_structure=employee.prev_salary_structure
	# 		additional_salary.salary_component=self.casual_salary_component
	# 		additional_salary.amount=self.total_amount/len(employees)
	# 		additional_salary.company=self.company
	# 		additional_salary.payroll_date=self.attendance_date
	# 		additional_salary.ref_doctype="Casual Payroll Payout"
	# 		additional_salary.ref_docname=self.name
	# 		additional_salary.docstatus=1

	# 		additional_salary.save()
	# 		frappe.db.commit()
  
  

@frappe.whitelist(allow_guest=True)
def get_rate():
	activity=frappe.form_dict.get("activity")
	item=frappe.form_dict.get("item")
	#frappe.msgprint("Activity: "+activity+" Item: "+item)
	costing=frappe.get_all("Casual Activity Item", filters={"activity_type":activity, "item":item}, fields=["costing_rate"])
	if costing:
		rate=costing[0].costing_rate
		frappe.response['message']=rate
	else:
		frappe.throw("Create Costing for this Activity in Casual Activity Item doctype")
  

@frappe.whitelist(allow_guest=True)
def fetch_employees():
	total_amount=frappe.form_dict.get("total_amount")
	shift_type=frappe.form_dict.get("shift_type")
	attendance_date=frappe.form_dict.get("attendance_date")
	company=frappe.form_dict.get("company")
	salary_structure=frappe.form_dict.get("salary_structure")
	employees_attendance = frappe.get_all("Attendance", filters={"attendance_date": attendance_date, "shift": shift_type, "company":company}, fields=["employee", "employee_name", "shift", "status","name"])
	employee_details=[]
	for employee_attendance in employees_attendance:
		employees_with_additional_salary=filter_employees_with_additional_salary_on_attendance_date(attendance_date)
		if employee_attendance.employee in employees_with_additional_salary:
			continue
		prev_salary_structure=frappe.get_all("Salary Slip", filters={"employee":employee_attendance.name}, fields=["salary_structure"])
		if prev_salary_structure:
			previous_salary_structure=prev_salary_structure[0].name
		else:
			previous_salary_structure=salary_structure
   
		employee_checkin=frappe.get_all("Employee Checkin", filters={"attendance": employee_attendance.name, "employee":employee_attendance.employee, "log_type":"IN"}, fields=["time"])
		employee_checkout=frappe.get_all("Employee Checkin", filters={"attendance": employee_attendance.name, "employee":employee_attendance.employee, "log_type":"OUT"}, fields=["time"])

		
		employee_detail={
			"employee":employee_attendance.employee,
			"employee_name":employee_attendance.employee_name,
			"shift_type":employee_attendance.shift,
			"attendance":employee_attendance.name,
			# "prev_salary_structure":previous_salary_structure,
   			"prev_salary_structure":previous_salary_structure,
			"checkin":employee_checkin[0].time if employee_checkin else "00:00:00",
			"checkout":employee_checkout[0].time if employee_checkout else "00:00:00",

		}
		
		employee_details.append(employee_detail)
	frappe.response['message']=employee_details
 
def filter_employees_with_additional_salary_on_attendance_date(attendance_date):
	employees=[]
	additional_salaries=frappe.get_all("Additional Salary", filters={"payroll_date":attendance_date}, fields=["employee"])
	if additional_salaries:
		for additional_salary in additional_salaries:
			employees.append(additional_salary.employee)
	return employees
 
 
def create_new_salary_structure_assignment(employee, attendance_date, shift_type, company, salary_structure):
	if check_nssf_deducted(employee, attendance_date):
		new_salary_structure=frappe.new_doc("Salary Structure Assignment")
		new_salary_structure.employee=employee
		new_salary_structure.start_date=attendance_date
		new_salary_structure.company=company
		new_salary_structure.salary_structure=salary_structure
 
def check_nssf_deducted(employee, attendance_date):
	# Parse attendance_date string to datetime object
	attendance_datetime = datetime.strptime(attendance_date, '%d-%m-%Y')
	start_date = attendance_datetime.replace(day=1)

	# Retrieve salary slip for the employee and attendance date
	salary_slip = frappe.get_all("Salary Slip", filters={"employee": employee, "start_date": start_date}, fields=["*"])
 
	# Initialize nssf_deduction flag
	nssf_deduction = False

	if salary_slip:
		salary_slip_name = salary_slip[0].name
		salary_slip_doc = frappe.get_doc("Salary Slip", salary_slip_name)
		deductions = salary_slip_doc.get("deductions")

		# Check if Employer NSSF or Employee NSSF deduction exists
		for deduction in deductions:
			if deduction.salary_component == "Employer NSSF" or deduction.salary_component == "Employee NSSF":
				nssf_deduction = True
				break
	else:
		nssf_deduction = False

	return nssf_deduction
	
	
	
@frappe.whitelist(allow_guest=True)
def get_salary_structure_and_component():
	shift = frappe.form_dict.get("shift_type")
	shift_type=frappe.get_doc("Shift Type", shift)
	salary_structure=shift_type.custom_salary_structure
	salary_component=shift_type.custom_casual_salary_component
	
	frappe.response['message'] = {"salary_structure":salary_structure, "salary_component":salary_component}
	
	
 
#get activity items related to activity type
@frappe.whitelist(allow_guest=True)
def get_activity_items():
	activity_type = frappe.form_dict.get("activity_type")
	items = frappe.get_all("Casual Activity Item", filters={"activity_type": activity_type}, fields=["item"])

	item_names = [item["item"] for item in items]
	frappe.response['message'] = item_names

   
@frappe.whitelist(allow_guest=True)
def open_monthly_nssf_deduction():
	salary_components=frappe.get_all("Salary Component", filters={"name": ["like", "%NSSF%"]}, fields=["name"])
	for salary_component in salary_components:
		if salary_component.monthly==1:
			salary_component_doc=frappe.get_doc("Salary Component", salary_component.name)
			salary_component_doc.monthly=0
			salary_component_doc.save()
			frappe.db.commit()
	frappe.msgprint(str(salary_component))
	
	

