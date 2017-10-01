# -*- coding: utf-8 -*-
# Copyright (c) 2017, DOKOS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import set_name_by_naming_series
from dateutil import relativedelta as rdelta
import datetime
from frappe.utils import getdate, now_datetime
from dateutil.relativedelta import relativedelta

class CustomContract(Document):
	def autoname(self):
		if self.contract_series=="Customer":
			series = "Con-{0}-{1}-{2}-".format(self.issue_date, "C", self.customer_name)
			self.naming_series = series

		elif self.contract_series=="Supplier":
			series = "Con-{0}-{1}-{2}-".format(self.issue_date, "S", self.supplier_name)
			self.naming_series = series

		elif self.contract_series=="Employee":
			series = "Con-{0}-{1}-{2}-".format(self.issue_date, "E", self.employee_name)
			self.naming_series = series

		elif self.contract_series=="Sales Partner":
			series = "Con-{0}-{1}-{2}-".format(self.issue_date, "SP", self.employee_name)
			self.naming_series = series

		set_name_by_naming_series(self)

	def onload(self):
		if self.docstatus==1:
			self.refresh_financials(self.taxes_included)

	def validate(self):
		self.duration_calculation()
		self.refresh_financials(self.taxes_included)

	def refresh_financials(self, taxes_included):
		if (taxes_included == "Yes"):
			total = "base_grand_total"
		else:
			total = "base_total"
		self.sales_order_total(total)
		self.sales_invoice_total(total)
		self.purchase_order_total(total)
		self.purchase_invoice_total(total)
		frappe.db.commit()

	def duration_calculation(self):
		start_date = getdate(self.contract_start_date)
		end_date = getdate(self.contract_end_date)
		rd = rdelta.relativedelta(end_date, start_date)
		self.contract_duration = "{0.years} years and {0.months} months and {0.days} days".format(rd)

	def sales_order_total(self, total):
		total = frappe.db.sql("""SELECT SUM({0}) as total FROM `tabSales Order` WHERE project in (SELECT project FROM `tabCustom Contract Projects` WHERE parent = '{1}') AND customer = '{2}' AND docstatus=1""".format(total, self.name, self.customer_name), as_dict=True)
		self.total_sales_order = total[0].total

	def sales_invoice_total(self, total):
		total = frappe.db.sql("""SELECT SUM({0}) as total FROM `tabSales Invoice` WHERE project in (SELECT project FROM `tabCustom Contract Projects` WHERE parent = '{1}') AND customer = '{2}' AND docstatus=1""".format(total, self.name, self.customer_name), as_dict=True)
		self.total_invoiced = total[0].total

	def purchase_order_total(self, total):
		total = frappe.db.sql("""SELECT SUM(base_amount) as total FROM `tabPurchase Order Item` WHERE project in (SELECT project FROM `tabCustom Contract Projects` WHERE parent = '{0}') AND parent in (SELECT name from `tabPurchase Order` WHERE supplier = '{1}') AND docstatus=1""".format(self.name, self.supplier_name), as_dict=True)
		self.total_purchase_order = total[0].total

	def purchase_invoice_total(self, total):
		total = frappe.db.sql("""SELECT SUM(base_amount) as total FROM `tabPurchase Invoice Item` WHERE project in (SELECT project FROM `tabCustom Contract Projects` WHERE parent = '{0}') AND parent in (SELECT name from `tabPurchase Invoice` WHERE supplier = '{1}') AND docstatus=1""".format(self.name, self.supplier_name), as_dict=True)
		self.total_purchased = total[0].total

@frappe.whitelist()
def change_bonds_status():
	contract_bonds = frappe.get_all("Custom Contract Bond", filters={'docstatus': 1}, fields=['name'])

	for contract_bond in contract_bonds:
		change_bond_status(contract_bond.name)
		frappe.db.set_value("Custom Contract Bond", contract_bond.name, "bond_amount", amount)

@frappe.whitelist()
def change_bond_status(bond):
	contract_bond = frappe.get_doc("Custom Contract Bond", bond)
	project_percent = frappe.get_value("Project", contract_bond.project, "percent_complete")
	custom_contract = frappe.get_doc("Custom Contract", contract_bond.custom_contract)

	if contract_bond.percentage_of_work == None:
		contract_bond.percentage_of_work = 0

	if contract_bond.from_beginning:
		sales_doc = "tabSales Order"
		purchase_doc = "tabPurchase Order Item"

	elif contract_bond.end_of_project:
		sales_doc = "tabSales Invoice"
		purchase_doc = "tabPurchase Invoice Item"

	else:
		frappe.throw("Please select a calculation mode")

	if project_percent >= contract_bond.percentage_of_work and getdate(contract_bond.collection_date) <= now_datetime().date():
		frappe.db.set_value("Custom Contract Bond", contract_bond.name, "bond_status", "Time to Collect Bond")

	if (custom_contract.contract_series=="Customer"):
		total = frappe.db.sql("""SELECT SUM(base_total) as total FROM `{0}` WHERE project = '{1}' AND customer = '{2}' AND docstatus=1""".format(sales_doc, contract_bond.project, custom_contract.customer_name), as_dict=True)
		if total[0].total == None:
			total[0].total = 0
		amount = total[0].total * float(contract_bond.percentage_of_work)/100
		return amount

	elif custom_contract.contract_series=="Supplier":
		total = frappe.db.sql("""SELECT SUM(base_amount) as total FROM `{0}` WHERE project = '{1}' AND parent in (SELECT name from `tabPurchase Invoice` WHERE supplier = '{2}') AND docstatus=1""".format(purchase_doc, contract_bond.project, custom_contract.supplier_name), as_dict=True)
		if total[0].total == None:
			total[0].total = 0
		amount = total[0].total * float(contract_bond.percentage_of_work)/100
		return amount


@frappe.whitelist()
def change_contract_status():
	contracts = frappe.get_all("Custom Contract", fields=['name', 'contract_end_date', 'alert_before_end_of_contract'])

	for contract in contracts:
		if contract.contract_status=="Open":
			renewal_date = getdate(contract.contract_end_date) - relativedelta(days=contract.alert_before_end_of_contract)
			if renewal_date <= now_datetime().date():
			 	frappe.db.set_value("Custom Contract", contract.name, "contract_status", "Renewal")
