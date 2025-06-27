// Copyright (c) 2024, White Stork and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lamaa Demo', {
	// Called when the form is refreshed
	refresh: function(frm) {
		// Add custom buttons to the form
		frm.add_custom_button(__('Get Demo Info'), function() {
			get_demo_info(frm);
		}, __('Actions'));

		frm.add_custom_button(__('Demo Statistics'), function() {
			show_demo_statistics();
		}, __('Reports'));

		// Set field properties based on status
		set_field_properties(frm);

		// Add status indicators
		add_status_indicators(frm);
	},

	// Called when the form is loaded
	onload: function(frm) {
		// Set default values
		set_default_values(frm);
	},

	// Called when status field changes
	status: function(frm) {
		set_field_properties(frm);
		add_status_indicators(frm);
	},

	// Called when priority field changes
	priority: function(frm) {
		set_priority_color(frm);
	},

	// Called when title field changes
	title: function(frm) {
		// Auto-generate description based on title if empty
		if (frm.doc.title && !frm.doc.description) {
			frm.set_value('description', 'Demo record for: ' + frm.doc.title);
		}
	},

	// Called before saving
	before_save: function(frm) {
		// Validate required fields
		validate_demo_fields(frm);
	}
});

// Function to get demo information
function get_demo_info(frm) {
	if (frm.doc.name) {
		frappe.call({
			method: 'get_demo_info',
			doc: frm.doc,
			callback: function(r) {
				if (r.message) {
					frappe.msgprint({
						title: __('Demo Information'),
						message: `
							<div class="demo-info">
								<p><strong>Title:</strong> ${r.message.title || 'Not set'}</p>
								<p><strong>Status:</strong> ${r.message.status || 'Not set'}</p>
								<p><strong>Priority:</strong> ${r.message.priority || 'Not set'}</p>
								<p><strong>Description:</strong> ${r.message.description || 'Not set'}</p>
								<p><strong>Demo Date:</strong> ${r.message.demo_date || 'Not set'}</p>
								<p><strong>Demo Time:</strong> ${r.message.demo_time || 'Not set'}</p>
							</div>
						`,
						indicator: 'blue'
					});
				}
			}
		});
	} else {
		frappe.msgprint(__('Please save the document first.'));
	}
}

// Function to show demo statistics
function show_demo_statistics() {
	frappe.call({
		method: 'ml_modules.ml_modules.doctype.lamaa_demo.lamaa_demo.get_demo_stats',
		callback: function(r) {
			if (r.message) {
				let stats_html = '<div class="demo-stats">';
				stats_html += '<h4>Demo Statistics</h4>';
				stats_html += '<table class="table table-bordered">';
				stats_html += '<thead><tr><th>Status</th><th>Count</th></tr></thead>';
				stats_html += '<tbody>';

				r.message.forEach(function(stat) {
					stats_html += `<tr><td>${stat.status}</td><td>${stat.count}</td></tr>`;
				});

				stats_html += '</tbody></table></div>';

				frappe.msgprint({
					title: __('Demo Statistics'),
					message: stats_html,
					wide: true
				});
			}
		}
	});
}

// Function to set field properties based on status
function set_field_properties(frm) {
	if (frm.doc.status === 'Completed') {
		frm.set_df_property('demo_date', 'read_only', 1);
		frm.set_df_property('demo_time', 'read_only', 1);
	} else {
		frm.set_df_property('demo_date', 'read_only', 0);
		frm.set_df_property('demo_time', 'read_only', 0);
	}

	if (frm.doc.status === 'Draft') {
		frm.set_df_property('description', 'reqd', 0);
	} else {
		frm.set_df_property('description', 'reqd', 1);
	}
}

// Function to add status indicators
function add_status_indicators(frm) {
	let color_map = {
		'Draft': 'grey',
		'Active': 'green',
		'Inactive': 'orange',
		'Completed': 'blue'
	};

	if (frm.doc.status) {
		frm.dashboard.add_indicator(__('Status: {0}', [frm.doc.status]), color_map[frm.doc.status] || 'grey');
	}
}

// Function to set priority color
function set_priority_color(frm) {
	let priority_colors = {
		'Low': 'green',
		'Medium': 'yellow',
		'High': 'orange',
		'Urgent': 'red'
	};

	if (frm.doc.priority) {
		frm.dashboard.add_indicator(__('Priority: {0}', [frm.doc.priority]), priority_colors[frm.doc.priority] || 'grey');
	}
}

// Function to set default values
function set_default_values(frm) {
	if (frm.is_new()) {
		frm.set_value('status', 'Draft');
		frm.set_value('priority', 'Medium');

		// Set default demo date to today
		frm.set_value('demo_date', frappe.datetime.get_today());
	}
}

// Function to validate demo fields
function validate_demo_fields(frm) {
	if (frm.doc.status === 'Active' && !frm.doc.demo_date) {
		frappe.validated = false;
		frappe.msgprint(__('Demo Date is required when status is Active.'));
		return false;
	}

	if (frm.doc.priority === 'Urgent' && !frm.doc.description) {
		frappe.validated = false;
		frappe.msgprint(__('Description is required for urgent priority items.'));
		return false;
	}

	return true;
}
