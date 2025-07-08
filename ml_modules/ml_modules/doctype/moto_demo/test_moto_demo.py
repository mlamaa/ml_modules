# Copyright (c) 2024, White Stork and contributors
# For license information, please see license.txt

import unittest
import frappe
from frappe.tests.utils import FrappeTestCase


class TestMotoDemo(FrappeTestCase):
	"""
	Test cases for Moto Demo DocType
	"""

	def setUp(self):
		"""Set up test data"""
		self.test_title = "Test Moto Demo Record"
		self.test_description = "This is a test motorcycle demo record"

	def tearDown(self):
		"""Clean up test data"""
		# Delete test records
		frappe.db.delete("Moto Demo", {"title": self.test_title})
		frappe.db.commit()

	def test_create_moto_record(self):
		"""Test creating a new motorcycle demo record"""
		doc = frappe.get_doc({
			"doctype": "Moto Demo",
			"title": self.test_title,
			"description": self.test_description,
			"priority": "High",
			"status": "Draft",
			"moto_type": "Sport",
			"engine_capacity": 600
		})
		doc.insert()

		# Test if record was created successfully
		self.assertTrue(doc.name)
		self.assertEqual(doc.title, self.test_title)
		self.assertEqual(doc.status, "Draft")
		self.assertEqual(doc.priority, "High")
		self.assertEqual(doc.moto_type, "Sport")
		self.assertEqual(doc.engine_capacity, 600)

		# Test if created_by_user is set
		self.assertTrue(doc.created_by_user)

	def test_validate_method(self):
		"""Test the validate method"""
		doc = frappe.get_doc({
			"doctype": "Moto Demo",
			"title": self.test_title + " Validate",
			"description": self.test_description,
			"status": "Active",
			"moto_type": "Cruiser",
			"engine_capacity": 1200
		})
		doc.insert()

		# Test if modified_by_user is set during validation
		self.assertTrue(doc.modified_by_user)

		# Test if created_by_user is set during validation
		self.assertTrue(doc.created_by_user)

	def test_engine_capacity_validation(self):
		"""Test engine capacity validation for different motorcycle types"""
		# Test Electric motorcycle with engine capacity (should fail)
		doc = frappe.get_doc({
			"doctype": "Moto Demo",
			"title": self.test_title + " Electric",
			"description": self.test_description,
			"moto_type": "Electric",
			"engine_capacity": 500
		})

		with self.assertRaises(frappe.ValidationError):
			doc.insert()

		# Test Scooter with high engine capacity (should fail)
		doc = frappe.get_doc({
			"doctype": "Moto Demo",
			"title": self.test_title + " Scooter",
			"description": self.test_description,
			"moto_type": "Scooter",
			"engine_capacity": 400
		})

		with self.assertRaises(frappe.ValidationError):
			doc.insert()

		# Test valid Electric motorcycle (should pass)
		doc = frappe.get_doc({
			"doctype": "Moto Demo",
			"title": self.test_title + " Electric Valid",
			"description": self.test_description,
			"moto_type": "Electric"
		})
		doc.insert()
		self.assertTrue(doc.name)

	def test_get_moto_info_method(self):
		"""Test the get_moto_info method"""
		doc = frappe.get_doc({
			"doctype": "Moto Demo",
			"title": self.test_title + " Info",
			"description": self.test_description,
			"priority": "Medium",
			"status": "Active",
			"moto_type": "Adventure",
			"engine_capacity": 1000,
			"demo_date": "2024-01-15",
			"demo_time": "10:30:00"
		})
		doc.insert()

		# Test get_moto_info method
		info = doc.get_moto_info()

		self.assertEqual(info["title"], doc.title)
		self.assertEqual(info["status"], "Active")
		self.assertEqual(info["priority"], "Medium")
		self.assertEqual(info["description"], self.test_description)
		self.assertEqual(info["moto_type"], "Adventure")
		self.assertEqual(info["engine_capacity"], 1000)
		self.assertEqual(info["demo_date"], "2024-01-15")
		self.assertEqual(info["demo_time"], "10:30:00")

	def test_status_options(self):
		"""Test that all status options work correctly"""
		status_options = ["Draft", "Active", "Inactive", "Completed"]

		for status in status_options:
			doc = frappe.get_doc({
				"doctype": "Moto Demo",
				"title": f"{self.test_title} {status}",
				"description": self.test_description,
				"status": status,
				"moto_type": "Naked"
			})
			doc.insert()

			self.assertEqual(doc.status, status)

	def test_priority_options(self):
		"""Test that all priority options work correctly"""
		priority_options = ["Low", "Medium", "High", "Urgent"]

		for priority in priority_options:
			doc = frappe.get_doc({
				"doctype": "Moto Demo",
				"title": f"{self.test_title} {priority}",
				"description": self.test_description,
				"priority": priority,
				"moto_type": "Touring"
			})
			doc.insert()

			self.assertEqual(doc.priority, priority)

	def test_moto_type_options(self):
		"""Test that all motorcycle type options work correctly"""
		moto_type_options = ["Sport", "Cruiser", "Touring", "Naked", "Adventure", "Scooter", "Electric"]

		for moto_type in moto_type_options:
			doc = frappe.get_doc({
				"doctype": "Moto Demo",
				"title": f"{self.test_title} {moto_type}",
				"description": self.test_description,
				"moto_type": moto_type
			})

			# Set appropriate engine capacity for non-electric types
			if moto_type != "Electric":
				doc.engine_capacity = 500

			doc.insert()

			self.assertEqual(doc.moto_type, moto_type)

	def test_unique_title(self):
		"""Test that title uniqueness is enforced"""
		# Create first record
		doc1 = frappe.get_doc({
			"doctype": "Moto Demo",
			"title": self.test_title + " Unique",
			"description": self.test_description,
			"moto_type": "Sport"
		})
		doc1.insert()

		# Try to create second record with same title
		doc2 = frappe.get_doc({
			"doctype": "Moto Demo",
			"title": self.test_title + " Unique",
			"description": "Different description",
			"moto_type": "Cruiser"
		})

		# This should raise an exception due to unique constraint
		with self.assertRaises(frappe.DuplicateEntryError):
			doc2.insert()

	def test_global_methods(self):
		"""Test global utility methods"""
		from ml_modules.ml_modules.doctype.moto_demo.moto_demo import get_moto_stats, create_moto_record, get_engine_capacity_range

		# Test create_moto_record utility function
		moto_name = create_moto_record(
			title=self.test_title + " Global",
			description="Created via utility function",
			priority="High",
			moto_type="Sport"
		)

		self.assertTrue(moto_name)

		# Verify the record was created
		doc = frappe.get_doc("Moto Demo", moto_name)
		self.assertEqual(doc.title, self.test_title + " Global")
		self.assertEqual(doc.priority, "High")
		self.assertEqual(doc.moto_type, "Sport")
		self.assertEqual(doc.status, "Draft")

		# Test get_moto_stats function
		stats = get_moto_stats()
		self.assertIsInstance(stats, dict)
		self.assertIn("status_stats", stats)
		self.assertIn("type_stats", stats)

		# Should have at least one record (the one we just created)
		total_status_count = sum(stat['count'] for stat in stats['status_stats'])
		self.assertGreaterEqual(total_status_count, 1)

		# Test get_engine_capacity_range function
		sport_range = get_engine_capacity_range("Sport")
		self.assertIsInstance(sport_range, dict)
		self.assertIn("min", sport_range)
		self.assertIn("max", sport_range)
		self.assertIn("typical", sport_range)

		electric_range = get_engine_capacity_range("Electric")
		self.assertEqual(electric_range["min"], 0)
		self.assertEqual(electric_range["max"], 0)

		# Test unknown type
		unknown_range = get_engine_capacity_range("Unknown")
		self.assertEqual(unknown_range["typical"], "Varies")

	def test_engine_capacity_ranges(self):
		"""Test engine capacity ranges for different motorcycle types"""
		from ml_modules.ml_modules.doctype.moto_demo.moto_demo import get_engine_capacity_range

		# Test known types
		sport_range = get_engine_capacity_range("Sport")
		self.assertEqual(sport_range["min"], 250)
		self.assertEqual(sport_range["max"], 1000)

		cruiser_range = get_engine_capacity_range("Cruiser")
		self.assertEqual(cruiser_range["min"], 500)
		self.assertEqual(cruiser_range["max"], 1800)

		scooter_range = get_engine_capacity_range("Scooter")
		self.assertEqual(scooter_range["min"], 50)
		self.assertEqual(scooter_range["max"], 300)

		electric_range = get_engine_capacity_range("Electric")
		self.assertEqual(electric_range["min"], 0)
		self.assertEqual(electric_range["max"], 0)
		self.assertIn("Electric motor", electric_range["typical"])


if __name__ == '__main__':
	unittest.main()
