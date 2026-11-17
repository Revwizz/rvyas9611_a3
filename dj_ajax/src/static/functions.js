// FILE          : functions.js
// PROJECT       : SENG2045 - Assignment 3
// PROGRAMMER    : Ritik Vyas
// FIRST VERSION : 2026-11-15
// DESCRIPTION   : Shared JavaScript helpers used on every page. Loaded from
//                 base.html before each page's own script.
// 


// FUNCTION    : handleAlerts
// DESCRIPTION : Shows a Bootstrap alert message inside the page's alert box.
//               Each page's script must define alertBox, the element with
//               id "alert-box", before this function is called.
// PARAMETERS  : type : Bootstrap alert style, e.g. 'success' or 'danger'
//               msg  : the text to show in the alert
// RETURNS     : nothing
const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `
}