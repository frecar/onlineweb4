/*
    The Company module exposes functionality needed in the company section
    of the dashboard.
*/

var Feedback = (function ($, tools) {

    // Perform self check, display error if missing deps
    var performSelfCheck = function () {
        var errors = false
        if ($ == undefined) {
            console.error('jQuery missing!')
            errors = true
        }
        if (tools == undefined) {
            console.error('Dashboard tools missing!')
            errors = true
        }
        if (errors) return false
        return true
    }

    return {

        // Bind them buttons and other initial functionality here
        init: function () {

            if (!performSelfCheck()) return

            // $('#inventory-delete-item').on('click', function (e) {
            //     e.preventDefault()
            //     if (confirm('Er du sikker på at du vil slette denne varen?')) {
            //         window.location = this.href
            //     }
            // })

            $('#feedback-add-textquestion').on('click', function (e) {
                e.preventDefault()
                console.log("Pressed");
                $('#feedback-add-textquestion-form').slideToggle(200)
            })

            // $('.deletebatch').on('click', function (e) {
            //     if (confirm('Er du sikker på at du vil slette denne batchen?')) {
            //         // STUB
            //     } else {
            //         e.preventDefault()
            //     }
            // })
        }

    }

})(jQuery, Dashboard.tools)

$(document).ready(function () {
    Feedback.init()
})
