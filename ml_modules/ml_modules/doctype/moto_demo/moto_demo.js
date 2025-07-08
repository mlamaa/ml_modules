// Copyright (c) 2024, White Stork and contributors
// For license information, please see license.txt

frappe.ui.form.on('Moto Demo', {
	// Called when the form is refreshed
	refresh: function(frm) {
		// Add custom buttons to the form
		frm.add_custom_button(__('Get Moto Info'), function() {
			get_moto_info(frm);
		}, __('Actions'));

		frm.add_custom_button(__('Moto Statistics'), function() {
			show_moto_statistics();
		}, __('Reports'));

		frm.add_custom_button(__('Engine Capacity Guide'), function() {
			show_engine_capacity_guide(frm);
		}, __('Help'));

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

	// Called when moto_type field changes
	moto_type: function(frm) {
		update_engine_capacity_help(frm);
		validate_engine_capacity_for_type(frm);
	},

	// Called when engine_capacity field changes
	engine_capacity: function(frm) {
		validate_engine_capacity_for_type(frm);
	},

	// Called when title field changes
	title: function(frm) {
		// Auto-generate description based on title if empty
		if (frm.doc.title && !frm.doc.description) {
			frm.set_value('description', 'Motorcycle demo for: ' + frm.doc.title);
		}
	},

	// Called before saving
	before_save: function(frm) {
		// Validate required fields
		validate_moto_fields(frm);
	}
});

// Function to get motorcycle demo information
function get_moto_info(frm) {
	if (frm.doc.name) {
		frappe.call({
			method: 'get_moto_info',
			doc: frm.doc,
			callback: function(r) {
				if (r.message) {
					frappe.msgprint({
						title: __('Motorcycle Demo Information'),
						message: `
							<div class="moto-info">
								<p><strong>Title:</strong> ${r.message.title || 'Not set'}</p>
								<p><strong>Status:</strong> ${r.message.status || 'Not set'}</p>
								<p><strong>Priority:</strong> ${r.message.priority || 'Not set'}</p>
								<p><strong>Motorcycle Type:</strong> ${r.message.moto_type || 'Not set'}</p>
								<p><strong>Engine Capacity:</strong> ${r.message.engine_capacity ? r.message.engine_capacity + ' cc' : 'Not set'}</p>
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

// Function to show motorcycle demo statistics
function show_moto_statistics() {
	frappe.call({
		method: 'ml_modules.ml_modules.doctype.moto_demo.moto_demo.get_moto_stats',
		callback: function(r) {
			if (r.message) {
				let stats_html = '<div class="moto-stats">';
				stats_html += '<h4>Motorcycle Demo Statistics</h4>';

				// Status statistics
				stats_html += '<h5>By Status</h5>';
				stats_html += '<table class="table table-bordered">';
				stats_html += '<thead><tr><th>Status</th><th>Count</th></tr></thead>';
				stats_html += '<tbody>';

				r.message.status_stats.forEach(function(stat) {
					stats_html += `<tr><td>${stat.status}</td><td>${stat.count}</td></tr>`;
				});

				stats_html += '</tbody></table>';

				// Type statistics
				if (r.message.type_stats && r.message.type_stats.length > 0) {
					stats_html += '<h5>By Motorcycle Type</h5>';
					stats_html += '<table class="table table-bordered">';
					stats_html += '<thead><tr><th>Type</th><th>Count</th></tr></thead>';
					stats_html += '<tbody>';

					r.message.type_stats.forEach(function(stat) {
						stats_html += `<tr><td>${stat.moto_type}</td><td>${stat.count}</td></tr>`;
					});

					stats_html += '</tbody></table>';
				}

				stats_html += '</div>';

				frappe.msgprint({
					title: __('Motorcycle Demo Statistics'),
					message: stats_html,
					wide: true
				});
			}
		}
	});
}

// Function to show engine capacity guide
function show_engine_capacity_guide(frm) {
	let moto_type = frm.doc.moto_type;

	if (moto_type) {
		frappe.call({
			method: 'ml_modules.ml_modules.doctype.moto_demo.moto_demo.get_engine_capacity_range',
			args: { moto_type: moto_type },
			callback: function(r) {
				if (r.message) {
					frappe.msgprint({
						title: __('Engine Capacity Guide for {0}', [moto_type]),
						message: `
							<div class="capacity-guide">
								<p><strong>Typical Range:</strong> ${r.message.typical}</p>
								<p><strong>Minimum:</strong> ${r.message.min} cc</p>
								<p><strong>Maximum:</strong> ${r.message.max} cc</p>
							</div>
						`,
						indicator: 'green'
					});
				}
			}
		});
	} else {
		frappe.msgprint(__('Please select a motorcycle type first.'));
	}
}

// Function to set field properties based on status
function set_field_properties(frm) {
	if (frm.doc.status === 'Completed') {
		frm.set_df_property('demo_date', 'read_only', 1);
		frm.set_df_property('demo_time', 'read_only', 1);
		frm.set_df_property('moto_type', 'read_only', 1);
		frm.set_df_property('engine_capacity', 'read_only', 1);
	} else {
		frm.set_df_property('demo_date', 'read_only', 0);
		frm.set_df_property('demo_time', 'read_only', 0);
		frm.set_df_property('moto_type', 'read_only', 0);
		frm.set_df_property('engine_capacity', 'read_only', 0);
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

	frm.dashboard.clear_headline();

	if (frm.doc.status) {
		frm.dashboard.add_indicator(__('Status: {0}', [frm.doc.status]), color_map[frm.doc.status] || 'grey');
	}

	if (frm.doc.moto_type) {
		frm.dashboard.add_indicator(__('Type: {0}', [frm.doc.moto_type]), 'blue');
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

// Function to update engine capacity help text
function update_engine_capacity_help(frm) {
	if (frm.doc.moto_type) {
		frappe.call({
			method: 'ml_modules.ml_modules.doctype.moto_demo.moto_demo.get_engine_capacity_range',
			args: { moto_type: frm.doc.moto_type },
			callback: function(r) {
				if (r.message) {
					frm.set_df_property('engine_capacity', 'description',
						`Typical range for ${frm.doc.moto_type}: ${r.message.typical}`);
				}
			}
		});
	}
}

// Function to validate engine capacity for motorcycle type
function validate_engine_capacity_for_type(frm) {
	if (frm.doc.moto_type === 'Electric' && frm.doc.engine_capacity) {
		frappe.msgprint({
			title: __('Warning'),
			message: __('Electric motorcycles should not have engine capacity specified.'),
			indicator: 'orange'
		});
	}

	if (frm.doc.moto_type === 'Scooter' && frm.doc.engine_capacity && frm.doc.engine_capacity > 300) {
		frappe.msgprint({
			title: __('Warning'),
			message: __('Scooters typically have engine capacity under 300cc.'),
			indicator: 'orange'
		});
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

// Function to validate motorcycle demo fields
function validate_moto_fields(frm) {
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

	if (frm.doc.moto_type === 'Electric' && frm.doc.engine_capacity) {
		frappe.validated = false;
		frappe.msgprint(__('Electric motorcycles should not have engine capacity specified.'));
		return false;
	}

	return true;
}
