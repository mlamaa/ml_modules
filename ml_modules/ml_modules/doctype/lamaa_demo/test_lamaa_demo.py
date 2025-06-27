# Copyright (c) 2024, White Stork and contributors
# For license information, please see license.txt

import unittest
import frappe
from frappe.tests.utils import FrappeTestCase


class TestLamaaDemo(FrappeTestCase):
	"""
	Test cases for Lamaa Demo DocType
	"""

	def setUp(self):
		"""Set up test data"""
		self.test_title = "Test Demo Record"
		self.test_description = "This is a test demo record"

	def tearDown(self):
		"""Clean up test data"""
		# Delete test records
		frappe.db.delete("Lamaa Demo", {"title": self.test_title})
		frappe.db.commit()

	def test_create_demo_record(self):
		"""Test creating a new demo record"""
		doc = frappe.get_doc({
			"doctype": "Lamaa Demo",
			"title": self.test_title,
			"description": self.test_description,
			"priority": "High",
			"status": "Draft"
		})
		doc.insert()

		# Test if record was created successfully
		self.assertTrue(doc.name)
		self.assertEqual(doc.title, self.test_title)
		self.assertEqual(doc.status, "Draft")
		self.assertEqual(doc.priority, "High")

		# Test if created_by_user is set
		self.assertTrue(doc.created_by_user)

	def test_validate_method(self):
		"""Test the validate method"""
		doc = frappe.get_doc({
			"doctype": "Lamaa Demo",
			"title": self.test_title + " Validate",
			"description": self.test_description,
			"status": "Active"
		})
		doc.insert()

		# Test if modified_by_user is set during validation
		self.assertTrue(doc.modified_by_user)

		# Test if created_by_user is set during validation
		self.assertTrue(doc.created_by_user)

	def test_get_demo_info_method(self):
		"""Test the get_demo_info method"""
		doc = frappe.get_doc({
			"doctype": "Lamaa Demo",
			"title": self.test_title + " Info",
			"description": self.test_description,
			"priority": "Medium",
			"status": "Active",
			"demo_date": "2024-01-15",
			"demo_time": "10:30:00"
		})
		doc.insert()

		# Test get_demo_info method
		info = doc.get_demo_info()

		self.assertEqual(info["title"], doc.title)
		self.assertEqual(info["status"], "Active")
		self.assertEqual(info["priority"], "Medium")
		self.assertEqual(info["description"], self.test_description)
		self.assertEqual(info["demo_date"], "2024-01-15")
		self.assertEqual(info["demo_time"], "10:30:00")

	def test_status_options(self):
		"""Test that all status options work correctly"""
		status_options = ["Draft", "Active", "Inactive", "Completed"]

		for status in status_options:
			doc = frappe.get_doc({
				"doctype": "Lamaa Demo",
				"title": f"{self.test_title} {status}",
				"description": self.test_description,
				"status": status
			})
			doc.insert()

			self.assertEqual(doc.status, status)

	def test_priority_options(self):
		"""Test that all priority options work correctly"""
		priority_options = ["Low", "Medium", "High", "Urgent"]

		for priority in priority_options:
			doc = frappe.get_doc({
				"doctype": "Lamaa Demo",
				"title": f"{self.test_title} {priority}",
				"description": self.test_description,
				"priority": priority
			})
			doc.insert()

			self.assertEqual(doc.priority, priority)

	def test_unique_title(self):
		"""Test that title uniqueness is enforced"""
		# Create first record
		doc1 = frappe.get_doc({
			"doctype": "Lamaa Demo",
			"title": self.test_title + " Unique",
			"description": self.test_description
		})
		doc1.insert()

		# Try to create second record with same title
		doc2 = frappe.get_doc({
			"doctype": "Lamaa Demo",
			"title": self.test_title + " Unique",
			"description": "Different description"
		})

		# This should raise an exception due to unique constraint
		with self.assertRaises(frappe.DuplicateEntryError):
			doc2.insert()

	def test_global_methods(self):
		"""Test global utility methods"""
		from ml_modules.ml_modules.doctype.lamaa_demo.lamaa_demo import get_demo_stats, create_demo_record

		# Test create_demo_record utility function
		demo_name = create_demo_record(
			title=self.test_title + " Global",
			description="Created via utility function",
			priority="High"
		)

		self.assertTrue(demo_name)

		# Verify the record was created
		doc = frappe.get_doc("Lamaa Demo", demo_name)
		self.assertEqual(doc.title, self.test_title + " Global")
		self.assertEqual(doc.priority, "High")
		self.assertEqual(doc.status, "Draft")

		# Test get_demo_stats function
		stats = get_demo_stats()
		self.assertIsInstance(stats, list)

		# Should have at least one record (the one we just created)
		total_count = sum(stat['count'] for stat in stats)
		self.assertGreaterEqual(total_count, 1)


if __name__ == '__main__':
	unittest.main()
