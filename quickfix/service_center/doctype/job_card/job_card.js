// Copyright (c) 2026, Siddarth and contributors
// For license information, please see license.txt
console.log("JobCard JS loaded")

// H1 Setup handler:
frappe.ui.form.on("Job Card", {
    setup(frm) {
        frm.set_query("assigned_technician", function () {
            return {
                filters: {
                    status: "Active",
                    specialization: frm.doc.device_type
                }
            }
        })
	},

    assigned_technician: function(frm) {
        let tech = frm.doc.assigned_technician;
        // console.log("--------------tech", tech)
        let device = frm.doc.device_type;
        // console.log("---------------device", device)
        frappe.db.get_value("Technician", tech, "specialization")
        // console.log("-------db", db)
            .then(r => {
                let specialization = r.message.specialization;
                // console.log("specialization:", specialization);

                if (specialization != device) {
                    frappe.msgprint("There is no technician, in this specialization")
                }
            });
    },

    refresh(frm) {

        // to test shipped JS
        frappe.msgprint("From Backend")

        // 
        if (!frappe.user.has_role("Manager")) {
            frm.set_df_property("customer_phone", "hidden", 1);
        }

        // indicator logic : Add color-coded frm.dashboard.add_indicator based on status
        if (frm.doc.status == "Ready For Delivery") {
            frm.dashboard.add_indicator("Ready for Delivery", "green")
        }

        if (frm.doc.status == "Cancelled") {
            frm.dashboard.add_indicator("Cancelled", "red")
        }

        // button : Show "Mark as Delivered" button only when status=="Ready for Delivery" AND docstatus==1
        if (frm.doc.status == "Ready For Delivery" && frm.doc.docstatus == 1) {
            frm.add_custom_button("Mark as Delivered")
        }

        // Read frappe.boot.quickfix_shop_name and display it in the form heade
        let shop = frappe.boot.quickfix_shop_name
        frm.set_intro(shop)

        // h2 Dialog, Prompt, Confirm
        frm.add_custom_button("Reject Job", function() {
            let d = new frappe.ui.Dialog({
            title: "Reject Job",
            fields: [
                {
                    label: "Rejection Reason",
                    fieldname: "reason",
                    fieldtype: "Small Text",
                    reqd: 1
                }
            ],
            
            primary_action_label: "Submit",
            primary_action(values) {

                frappe.confirm("Are you sure you want to reject?",
                    function() {
                        frm.set_value("status", "Cancelled");
                        frm.set_value("rejection_reason", values.reason);
                        frm.save();
                        d.hide();
                    }
                );
            }
        });    
        d.show();    
    });
    
        frm.add_custom_button("Transfer Technician", function() {
            frappe.prompt(
                [
                    {
                        label: "New Technician",
                        fieldname: "technician",
                        fieldtype: "Link",
                        options: "Technician",
                        reqd: 1
                    }
                ],

                // function(values) {
                //     frappe.confirm(
                //         'Are you sure want to transfer?',
                //         function() {
                            
                //             frappe.call({
                //                 method: "quickfix.service_center.doctype.job_card.assigned_technician",
                //                 args: {
                //                     technician: values.technician,
                //                     docname: frm.doc.name
                //                 },
                //             callback: function(r) {
                //                 console.log(r.message)
                //             }
                //         })
                //             console.log("Clicked Yes")
                //             frm.set_value("assigned_technician", values.technician);
                //             frm.save();
                //             frm.trigger("assigned_technician");
                //         },
                //         function() {
                //             console.log("ITss No")
                //         }
                //     )
                // }
            )
        });
    },

    // Realtime: Listen for "job_ready" event in onload (not refresh) and show frappe.show_alert
    onload(frm) {
        frappe.realtime.on("job_ready", () => {
            if (frm.doc.status == "Ready For Delivery") {

            frappe.show_alert({
                message: "Job is ready",
                indicator: "red"});
            }
        });
    }
});


// frappe.ui.form.on("Part Usage Entry", {
//     qty(frm, cdt, cdn) {
//         let row = locals[cdt][cdn];
//         console.log("-------row", row)
//         let total = row.qty * row.unit_price;
//         console.log("-----------", total)
//         frappe.model.set_value(cdt, cdn, "total_price", total)
//     }
// });