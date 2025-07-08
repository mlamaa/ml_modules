# Copyright (c) 2024, White Stork and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class MotoDemo(WebsiteGenerator):
	"""
	Moto Demo DocType Controller
	This is a demo doctype for motorcycle demonstrations.
	"""

	def validate(self):
		"""Validate the document before saving"""
		self.set_created_by()
		self.set_modified_by()
		self.validate_engine_capacity()

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

	def validate_engine_capacity(self):
		"""Validate engine capacity based on motorcycle type"""
		if self.moto_type == "Electric" and self.engine_capacity:
			frappe.throw("Electric motorcycles should not have engine capacity specified")

		if self.moto_type == "Scooter" and self.engine_capacity and self.engine_capacity > 300:
			frappe.throw("Scooters typically have engine capacity under 300cc")

	@frappe.whitelist()
	def get_moto_info(self):
		"""
		Custom method to get motorcycle demo information
		This method can be called from the frontend
		"""
		return {
			"title": self.title,
			"status": self.status,
			"priority": self.priority,
			"description": self.description,
			"demo_date": self.demo_date,
			"demo_time": self.demo_time,
			"moto_type": self.moto_type,
			"engine_capacity": self.engine_capacity
		}

	def get_context(self, context):
		"""
		Override get_context for web view
		This method is used when the doctype is accessed via web
		"""
		return context


@frappe.whitelist()
def get_moto_stats():
	"""
	Global method to get motorcycle demo statistics
	Returns count of demos by status and type
	"""
	stats = frappe.db.sql("""
		SELECT status, COUNT(*) as count
		FROM `tabMoto Demo`
		GROUP BY status
	""", as_dict=True)

	type_stats = frappe.db.sql("""
		SELECT moto_type, COUNT(*) as count
		FROM `tabMoto Demo`
		WHERE moto_type IS NOT NULL
		GROUP BY moto_type
	""", as_dict=True)

	return {
		"status_stats": stats,
		"type_stats": type_stats
	}


@frappe.whitelist()
def create_moto_record(title, description=None, priority="Medium", moto_type=None):
	"""
	Utility function to create a motorcycle demo record
	"""
	doc = frappe.get_doc({
		"doctype": "Moto Demo",
		"title": title,
		"description": description,
		"priority": priority,
		"moto_type": moto_type,
		"status": "Draft"
	})
	doc.insert()
	return doc.name


@frappe.whitelist()
def get_engine_capacity_range(moto_type):
	"""
	Get typical engine capacity range for a motorcycle type
	"""
	capacity_ranges = {
		"Sport": {"min": 250, "max": 1000, "typical": "600-1000cc"},
		"Cruiser": {"min": 500, "max": 1800, "typical": "800-1600cc"},
		"Touring": {"min": 800, "max": 1800, "typical": "1000-1600cc"},
		"Naked": {"min": 250, "max": 1000, "typical": "400-800cc"},
		"Adventure": {"min": 650, "max": 1250, "typical": "800-1200cc"},
		"Scooter": {"min": 50, "max": 300, "typical": "125-250cc"},
		"Electric": {"min": 0, "max": 0, "typical": "N/A - Electric motor"}
	}

	return capacity_ranges.get(moto_type, {"min": 0, "max": 2000, "typical": "Varies"})
