// FILE          : main.js
// PROJECT       : SENG2045 - Assignment 3
// PROGRAMMER    : Ritik Vyas
// FIRST VERSION : 2026-11-16
// DESCRIPTION   : Handles the My Profile page. Sends the updated bio and avatar
//                 image to the server with Ajax, then shows the new avatar and
//                 bio on the page without reloading.
//

console.log('my profile')

// page elements
const avatarBox = document.getElementById('avatar-box')
const alertBox = document.getElementById('alert-box')
const profileForm = document.getElementById('profile-form')

// CSRF tokens fir POST request
const csrf = document.getElementsByName('csrfmiddlewaretoken')

// Profile form inputs
const bioInput = document.getElementById('id_bio')
const avatarInput = document.getElementById('id_avatar')

// EVENT       : Profile form submit
// DESCRIPTION : Builds a FormData object with the CSRF token, bio and avatar
//               file, and sends it to the server with Ajax. On success, shows
//               the new avatar and bio, and a success alert.

profileForm.addEventListener('submit', e=> {
    e.preventDefault()

    const formData = new FormData()
    formData.append('csrfmiddlewaretoken', csrf[0].value)
    formData.append('bio', bioInput.value)
    formData.append('avatar', avatarInput.files[0])

    $.ajax({
        type: 'POST',
        url: '',
        enctype: 'multipart/form-data',
        data: formData,
        success: function(response){
            console.log(response)
            avatarBox.innerHTML = `
                <img src = "${response.avatar}" class = "rounded" height = "200px" width = "auto" alt = "${response.user}">
            `
            bioInput.value = response.bio
            handleAlerts('success', 'Profile Updated')
        },
        error: function(error){
            console.log(error)
        },
        processData: false,
        contentType: false,
        cache: false,
    })
})