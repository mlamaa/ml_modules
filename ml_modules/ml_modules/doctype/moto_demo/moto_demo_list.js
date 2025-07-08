// Copyright (c) 2024, White Stork and contributors
// For license information, please see license.txt

frappe.listview_settings['Moto Demo'] = {
	// Add indicator colors based on status
	add_fields: ["status", "priority", "moto_type", "engine_capacity"],

	get_indicator: function(doc) {
		let status_color = {
			"Draft": ["Draft", "grey", "status,=,Draft"],
			"Active": ["Active", "green", "status,=,Active"],
			"Inactive": ["Inactive", "orange", "status,=,Inactive"],
			"Completed": ["Completed", "blue", "status,=,Completed"]
		};

		return status_color[doc.status] || ["Unknown", "grey", ""];
	},

	// Custom button in list view
	button: {
		show: function(doc) {
			return doc.status !== "Completed";
		},
		get_label: function() {
			return __('Mark as Active');
		},
		get_description: function(doc) {
			return __('Mark {0} as Active', [doc.title]);
		},
		action: function(doc) {
			frappe.db.set_value(doc.doctype, doc.name, "status", "Active")
				.then(() => {
					frappe.show_alert({
						message: __('Status updated to Active'),
						indicator: 'green'
					});
					cur_list.refresh();
				});
		}
	},

	// Format list view columns
	formatters: {
		title: function(value, field, doc) {
			let priority_icon = "";
			let type_icon = "";

			// Priority icons
			if (doc.priority === "Urgent") {
				priority_icon = ' <i class="fa fa-exclamation-triangle text-danger" title="Urgent"></i>';
			} else if (doc.priority === "High") {
				priority_icon = ' <i class="fa fa-arrow-up text-warning" title="High Priority"></i>';
			}

			// Motorcycle type icons
			if (doc.moto_type === "Sport") {
				type_icon = ' <i class="fa fa-fighter-jet text-primary" title="Sport"></i>';
			} else if (doc.moto_type === "Cruiser") {
				type_icon = ' <i class="fa fa-road text-info" title="Cruiser"></i>';
			} else if (doc.moto_type === "Electric") {
				type_icon = ' <i class="fa fa-bolt text-success" title="Electric"></i>';
			} else if (doc.moto_type === "Scooter") {
				type_icon = ' <i class="fa fa-motorcycle text-muted" title="Scooter"></i>';
			}

			return value + priority_icon + type_icon;
		},

		engine_capacity: function(value, field, doc) {
			if (doc.moto_type === "Electric") {
				return '<span class="text-success">Electric</span>';
			}
			return value ? value + ' cc' : '';
		}
	},

	// Refresh list view every 30 seconds for active demos
	refresh: function(me) {
		// Custom refresh logic
		if (me.filter_area && me.filter_area.get().find(f => f[2] === "Active")) {
			setTimeout(() => {
				me.refresh();
			}, 30000);
		}
	},

	// Custom filters
	filters: [
		["status", "in", ["Draft", "Active", "Inactive", "Completed"]]
	],

	// Enable bulk operations
	bulk_operations: [
		{
			label: __("Set Priority to High"),
			action: function(docs) {
				frappe.call({
					method: "frappe.desk.bulk_update.bulk_update",
					args: {
						doctype: "Moto Demo",
						docs: docs,
						update: {priority: "High"}
					},
					callback: function(r) {
						if (!r.exc) {
							frappe.show_alert({
								message: __("Priority updated for {0} records", [docs.length]),
								indicator: "green"
							});
							cur_list.refresh();
						}
					}
				});
			}
		},
		{
			label: __("Mark as Completed"),
			action: function(docs) {
				frappe.call({
					method: "frappe.desk.bulk_update.bulk_update",
					args: {
						doctype: "Moto Demo",
						docs: docs,
						update: {status: "Completed"}
					},
					callback: function(r) {
						if (!r.exc) {
							frappe.show_alert({
								message: __("Status updated for {0} records", [docs.length]),
								indicator: "blue"
							});
							cur_list.refresh();
						}
					}
				});
			}
		},
		{
			label: __("Set Type to Sport"),
			action: function(docs) {
				frappe.call({
					method: "frappe.desk.bulk_update.bulk_update",
					args: {
						doctype: "Moto Demo",
						docs: docs,
						update: {moto_type: "Sport"}
					},
					callback: function(r) {
						if (!r.exc) {
							frappe.show_alert({
								message: __("Motorcycle type updated for {0} records", [docs.length]),
								indicator: "blue"
							});
							cur_list.refresh();
						}
					}
				});
			}
		}
	],

	// Group by options
	group_by: "moto_type",

	// Custom onload
	onload: function(listview) {
		// Add custom filter for motorcycle types
		listview.page.add_menu_item(__("Show Sport Bikes Only"), function() {
			listview.filter_area.add([[listview.doctype, "moto_type", "=", "Sport"]]);
		});

		listview.page.add_menu_item(__("Show Electric Only"), function() {
			listview.filter_area.add([[listview.doctype, "moto_type", "=", "Electric"]]);
		});

		listview.page.add_menu_item(__("Show High Capacity (>500cc)"), function() {
			listview.filter_area.add([[listview.doctype, "engine_capacity", ">", 500]]);
		});
	}
};
