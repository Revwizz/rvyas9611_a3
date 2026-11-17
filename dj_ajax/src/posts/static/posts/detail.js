// FILE          : detail.js
// PROJECT       : SENG2045 - Assignment 3
// PROGRAMMER    : Ritik Vyas
// FIRST VERSION : 2026-11-15
// DESCRIPTION   : Handles the post detail page. Loads the post data with Ajax,
//                 shows the Update and Delete buttons to the post's author,
//                 and updates or deletes the post with Ajax requests.
// 

// Page elements
const postBox = document.getElementById('post-box')
const alertBox = document.getElementById('alert-box')
const backBtn = document.getElementById('back-btn')
const updateBtn = document.getElementById('update-btn')
const deleteBtn = document.getElementById('delete-btn')

// URL for Ajax request
const url = window.location.href + "data/"
const updateUrl = window.location.href + "update/"
const deleteUrl = window.location.href + "delete/"

// update and delete modals
const updateForm = document.getElementById('update-form')
const deleteForm = document.getElementById('delete-form')

// spinner box 
const spinnerBox = document.getElementById('spinner-box')

// Inputs of update form
const titleInput = document.getElementById('id_title')
const bodyInput = document.getElementById('id_body')

// CSRF token 
const csrf = document.getElementsByName('csrfmiddlewaretoken')

// REQUEST     : Load post data (GET)
// DESCRIPTION : Gets the post's title, body and author from the server,
//               shows them on the page, fills the update form, and shows the
//               Update and Delete buttons only if the logged-in user is the author.

$.ajax({
    type: 'GET',
    url: url,
    success: function(response){
        console.log(response)
        const data = response.data

        if (data.logged_in !== data.author){
            console.log('different')
        } else {
            console.log('same')
            updateBtn.classList.remove('not-visible')
            deleteBtn.classList.remove('not-visible')
        }

        const titleEl = document.createElement('h3')
        titleEl.setAttribute('class', 'mt-3')
        titleEl.setAttribute('id', 'title')


        const bodyEl = document.createElement('p')
        bodyEl.setAttribute('class', 'mt-1')
        bodyEl.setAttribute('id', 'body')

        titleEl.textContent = data.title
        bodyEl.textContent = data.body

        postBox.appendChild(titleEl)
        postBox.appendChild(bodyEl)

        titleInput.value = data.title
        bodyInput.value = data.body

        spinnerBox.classList.add('not-visible')
    },
    error: function(error){
        console.log(error)
    }
})

// EVENT       : Update form submit
// DESCRIPTION : Sends the new title and body to the server with Ajax,
//               then updates the post on the page without reloading
//               and shows a success alert.

updateForm.addEventListener('submit', e=>{
    e.preventDefault()

    const title = document.getElementById('title')
    const body = document.getElementById('body')

    $.ajax({
        type: 'POST',
        url: updateUrl,
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'title': titleInput.value,
            'body': bodyInput.value,
        },
        success: function(response){
            console.log(response)
            handleAlerts('success', 'post is updated')
            title.textContent = response.title
            body.textContent = response.body
        },
        error: function(error){
            console.log(error)
        }
    })
})

// EVENT       : Delete form submit
// DESCRIPTION : Asks the server to delete the post with Ajax. On success,
//               saves the deleted post's title in local storage (so the main
//               page can show an alert) and goes back to the main page.

deleteForm.addEventListener('submit', e=>{
    e.preventDefault()

    $.ajax({
        type: 'POST',
        url: deleteUrl,
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
        },
        success: function(response){
            window.location.href = window.location.origin
            localStorage.setItem('title', titleInput.value)
        },
        error: function(error){
            console.log(error)
        }
    })
})