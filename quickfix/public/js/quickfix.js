console.log("quickfix JS loaded")

// want to check for boot task
document.addEventListener("DOMContentLoaded", function () {
    const shopName= frappe.boot.quickfix_shop_name;
    const managerEmail = frappe.boot.quickfix_manager_email;
    
    console.log("Shop Name:", shopName);
    console.log("Manager Email:", managerEmail);

    const navbar = document.querySelector(".navbar-brand");
    if (shopName) {
        const span = document.createElement("span");
        span.style.fontWeight = "bold";
        span.id = "shop-name";
        span.innerText = shopName;

        navbar.appendChild(span);
    }
})