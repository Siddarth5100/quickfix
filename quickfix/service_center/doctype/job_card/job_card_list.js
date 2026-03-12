

frappe.listview_settings["Job Card"] = {

    has_indicator_for_draft : true,

    add_fields: ["final_amount", "priority"],

    formatters: {
        final_amount(value) {
            // console.log(value)
            // console.log(doc.status)
            return "₹ " + value;
        }
    },

    get_indicator(doc) {

        if (doc.status === "Draft") {
            return ["Draft", "grey"]
        }

        if (doc.status == "Pending") {
            return ["Pending", "orange"]
        }

        if (doc.status == "Awaiting Customer Approval") {
            return ["waiting Customer Approval", "yellow"]
        }

        if (doc.status == "In Repair") {
            return ["In Repair", "purple"]
        } 

        if (doc.status == "Ready For Delivery") {
            console.log("Indicator running", doc.status, "blue---")
            return ["Ready For Delivery", "blue"]
        }   
        
        if (doc.status == "Delivered") {
            cons.log("--------------Delivered", doc.status)
            return ["Delivered", "green"] 
        }

        if (doc.status == "Cancelled") {
            console.log("Indicator running", doc.status)
            return ["Cancelled", "yellow"]
        }
         
    },

    

    button: {
        show(doc) {
            // console.log("doc.repair", doc.repair)
            return doc.status == "In Repair"
        },
        
        get_label(doc) {
            return 'Complete Repair';
        },
        
        action(doc) {
            console.log("clicked for:", doc.name)
        },

        get_description(doc) {
            return "Mark repair as completed"
        }
       
    },
}