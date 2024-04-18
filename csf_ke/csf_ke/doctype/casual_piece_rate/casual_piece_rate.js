// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Casual Piece Rate', {
    refresh: function(frm) {
        // Add a custom button to the form
        frm.add_custom_button(__('Get Employees'), function() {
            // Handle button click event
            var attendanceDate = frm.doc.attendance_date;
            var shiftType = frm.doc.shift_type;
            var company = frm.doc.company;
            fetchEmployees(frm, attendanceDate, shiftType, company);
        });

        frm.add_custom_button(__('Calculate Payout'), function() {
                calculatePayout(frm);
    }
    );
    },

    shift_type: function(frm) {
            var shift_type=frm.doc.shift_type;
            frappe.call({
                method: 'csf_ke.csf_ke.doctype.casual_piece_rate.casual_piece_rate.get_salary_structure_and_component',
                args: {
                    "shift_type":shift_type
                },
                callback: function(response) {
                    if (response.message) {
                        frm.set_value('salary_structure', response.message.salary_structure);
                        frm.set_value('casual_salary_component', response.message.salary_component);
                    }
                }
            });
            }
    
});


//
frappe.ui.form.on('Activity Calculator', {
    quantity: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn]; // Get the child table row object
        var total_quantity=0
		var total_amount=0
        frappe.call({
            method: 'csf_ke.csf_ke.doctype.casual_piece_rate.casual_piece_rate.get_rate',
            args: {
                activity: child.activity_type,
                item: child.item,
            },
            callback: function(response) {
                if (response && response.message) {
                    var rate = response.message;
                    var amount = rate * child.quantity;

                    frappe.model.set_value(cdt, cdn, 'rate', rate);
                    frappe.model.set_value(cdt, cdn, 'amount', amount);

                    frm.refresh_field('activity_calculator_tab');

                    frm.doc.activity_calculator_tab.forEach(function(row) {
						total_quantity += row.quantity || 0;
						total_amount += row.amount || 0;
					});
					frm.set_value('total_quantity', total_quantity);
					frm.set_value('total_amount', total_amount);
					frm.refresh_field('total_quantity');
					frm.refresh_field('total_amount');
                }
            }
        });
    }
});


// Function to fetch employees based on predefined filters
function fetchEmployees(frm, attendanceDate, shiftType, company) {
    frappe.call({
        method: 'csf_ke.csf_ke.doctype.casual_piece_rate.casual_piece_rate.fetch_employees',
        args: {
            "attendance_date": attendanceDate,
            "shift_type": shiftType,
            "company": company,
            "total_amount": frm.doc.total_amount,
            "salary_structure": frm.doc.salary_structure,

        },
        callback: function(response) {
            if (response && response.message) {
                var employees = response.message;

                response.message.forEach(function(casual) {
                    frappe.model.clear_table(frm.doc, 'casual_employees');
                    var new_casual_employee = frm.add_child('casual_employees');
                    

                    new_casual_employee.employee = casual.employee;
                    new_casual_employee.employee_name = casual.employee_name;
                    new_casual_employee.shift_type = casual.shift_type;
                    new_casual_employee.attendance = casual.attendance;
                    new_casual_employee.prev_salary_structure=casual.prev_salary_structure;
                    new_casual_employee.amount = casual.amount;

                });

                frm.refresh();

            }
        }
    });
}
// Function to calculate payout based on total amount and number of employees
function calculatePayout(frm) {
    var totalAmount = frm.doc.total_amount || 0;
    var numberOfEmployees = frm.doc.casual_employees.length;

    if (numberOfEmployees > 0) {
        var payoutPerEmployee = totalAmount / numberOfEmployees;
        
        frm.doc.casual_employees.forEach(function(employee) {
            frappe.model.set_value(employee.doctype, employee.name, 'amount', payoutPerEmployee);
        });

        frm.refresh_field('casual_employees');

    } else {
        frappe.msgprint("No employees found. Unable to calculate payout.");
    }
}
