// Copyright (c) 2026, Siddarth and contributors
// For license information, please see license.txt
console.log("JobCard JS loaded")

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

    // assigned_technician(frm) {
    //     let tech = frm.doc.assigned_technician;
    //     console.log("--------------tech", tech)
    //     let device = frm.doc.device_type;
    //     console.log("---------------device", device)
    //     let db = frappe.db.get_value("Technician", tech, "specialization")
    //     console.log("-------db", db)

    // },

    refresh(frm) {

        // indicator logic : Add color-coded frm.dashboard.add_indicator based on status
        if (frm.doc.status == "Ready For Delivery") {
            frm.dashboard.add_indicator("Ready for Delivery", "yellow")
        }

        // button : Show "Mark as Delivered" button only when status=="Ready for Delivery" AND docstatus==1
        if (frm.doc.status == "Ready For Delivery" && frm.doc.docstatus == 1) {
            frm.add_custom_button("Mark as Delivered")
        }

// want to re-do this
        // let  shop = frappe.boot.user
        // // console.log("-----------shop name", shop)
        // frm.set_intro(shop)

        // h2 task 
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
            ]
        })
        d.show();    
    });
        console.log("-------Rejected")
        frm.add_custom_button("Transfer Technician", function() {
            frappe.prompt(
                [
                    {
                        label: "New Technician",
                        fieldname: "technician",
                        fieldtype: "Link",
                        options: "Technician"
                    }
                ]
            )
        });
},

    onload(frm) {
        frappe.realtime.on("job_ready", () => {
            frappe.show_alert({
                message: "Job is ready",
                indicator: "green"});
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