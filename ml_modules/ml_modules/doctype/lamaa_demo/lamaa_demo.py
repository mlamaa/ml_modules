# Copyright (c) 2024, White Stork and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class LamaaDemo(WebsiteGenerator):
	"""
	Lamaa Demo DocType Controller
	This is a demo doctype created for testing purposes.
	"""

	def validate(self):
		"""Validate the document before saving"""
		self.set_created_by()
		self.set_modified_by()

	def before_save(self):
		"""Called before saving the document"""
		# Add any validation or processing logic here
		pass

	def after_insert(self):
		"""Called after inserting the document"""
		# Add any post-creation logic here
		pass

	def on_update(self):
		"""Called after updating the document"""
		# Add any post-update logic here
		pass

	def on_submit(self):
		"""Called when document is submitted"""
		# Add submission logic if this is a submittable doctype
		pass

	def on_cancel(self):
		"""Called when document is cancelled"""
		# Add cancellation logic if this is a submittable doctype
		pass

	def set_created_by(self):
		"""Set the created by user field"""
		if not self.created_by_user:
			self.created_by_user = frappe.session.user

	def set_modified_by(self):
		"""Set the modified by user field"""
		self.modified_by_user = frappe.session.user

	@frappe.whitelist()
	def get_demo_info(self):
		"""
		Custom method to get demo information
		This method can be called from the frontend
		"""
		return {
			"title": self.title,
			"status": self.status,
			"priority": self.priority,
			"description": self.description,
			"demo_date": self.demo_date,
			"demo_time": self.demo_time
		}

	def get_context(self, context):
		"""
		Override get_context for web view
		This method is used when the doctype is accessed via web
		"""
		return context


@frappe.whitelist()
def get_demo_stats():
	"""
	Global method to get demo statistics
	Returns count of demos by status
	"""
	stats = frappe.db.sql("""
		SELECT status, COUNT(*) as count
		FROM `tabLamaa Demo`
		GROUP BY status
	""", as_dict=True)

	return stats


@frappe.whitelist()
def create_demo_record(title, description=None, priority="Medium"):
	"""
	Utility function to create a demo record
	"""
	doc = frappe.get_doc({
		"doctype": "Lamaa Demo",
		"title": title,
		"description": description,
		"priority": priority,
		"status": "Draft"
	})
	doc.insert()
	return doc.name
