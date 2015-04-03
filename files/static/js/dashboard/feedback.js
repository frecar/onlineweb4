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

            $('#feedback-add-textquestion').on('click', function (e) {
                e.preventDefault()
                $('#feedback-add-textquestion-form').slideToggle(200)
                $('#feedback-add-ratingquestion-form').hide()
                $('#feedback-add-mcquestion-form').hide()
            })

            $('#feedback-add-ratingquestion').on('click', function (e) {
                e.preventDefault()
                $('#feedback-add-ratingquestion-form').slideToggle(200)
                $('#feedback-add-textquestion-form').hide()
                $('#feedback-add-mcquestion-form').hide()
            })

            $('#feedback-add-mcquestion').on('click', function (e) {
                e.preventDefault()
                $('#feedback-add-mcquestion-form').slideToggle(200)
                $('#feedback-add-textquestion-form').hide()
                $('#feedback-add-ratingquestion-form').hide()
            })

            $('.edit-question').on('click', function (e) {
                var message = "Vær oppmærksom på at endring av spørsmålet kan endre betydningen av eksisterende svar."
                message += "\nEr du sikker på at du vil redigere spørsmålet?"
                if (confirm(message)) {
                    // STUB
                } else {
                    e.preventDefault()
                }
            })

            $('.feedback-delete').on('click', function (e) {
                var message = "Er du sikker på at du vil slette skjemaet?"
                if (confirm(message)) {
                    // STUB
                } else {
                    e.preventDefault()
                }
            })
        }

    }

})(jQuery, Dashboard.tools)

$(document).ready(function () {
    Feedback.init()
})
