// FILE          : main.js
// PROJECT       : SENG2045 - Assignment 3
// PROGRAMMER    : Ritik Vyas
// FIRST VERSION : 2026-11-14
// DESCRIPTION   : Handles the main posts page. Loads posts with Ajax (three at a
//                 time), handles liking and unliking posts, creating new posts
//                 from the modal form, uploading photos with Dropzone, and
//                 showing an alert after a post is deleted.


// page elements
const postsBox = document.getElementById('posts-box')
const spinnerBox = document.getElementById('spinner-box')
const loadBtn = document.getElementById('load-btn')
const endBox = document.getElementById('end-box')

// create post form with inputs
const postForm = document.getElementById('post-form')
const title = document.getElementById('id_title')
const body = document.getElementById('id_body')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const url = window.location.href    // current page address

const alertBox = document.getElementById('alert-box')

// dropzone and modal buttons
const dropzone = document.getElementById('my-dropzone')
const addBtn = document.getElementById('add-btn')
const closeBtns = [...document.getElementsByClassName('add-modal-close')]

// FUNCTION    : getCookie
// DESCRIPTION : Reads the value of a cookie by its name. Used to get Django's
//               CSRF token for the Ajax POST requests.
// PARAMETERS  : name : the name of the cookie to find
// RETURNS     : the cookie's value, or null if it is not found
// SOURCE      : Django documentation (CSRF with Ajax)

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const deleted = localStorage.getItem('title')
if(deleted){
    handleAlerts('danger', `deleted "${deleted}"`)
    localStorage.clear()
}

// FUNCTION    : likeUnlikePosts
// DESCRIPTION : Adds a submit listener to every like/unlike form on the page.
//               On submit, sends the post id to the server with Ajax and
//               updates the button text and like count without reloading.
// PARAMETERS  : none
// RETURNS     : nothing

const likeUnlikePosts = () =>{
    const likeUnlikeForms = [...document.getElementsByClassName('like-unlike-forms')]
    likeUnlikeForms.forEach(form => form.addEventListener('submit', e=>{
        e.preventDefault()
        const clickedId = e.target.getAttribute('data-form-id')
        const clickedBtn = document.getElementById(`like-unlike-${clickedId}`)

        $.ajax({
            type: 'POST',
            url: "/like-unlike/",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'pk': clickedId,
            },
            success: function(response){
                console.log(response)
                clickedBtn.textContent = response.liked ? `Unlike (${response.count})` : `Like (${response.count})`
            },
            error: function(error){
                console.log(error)
            }
        })
    }))
}

let visible = 3

// FUNCTION    : getData
// DESCRIPTION : Requests the next group of posts from the server with Ajax,
//               adds each post to the page as a Bootstrap card, connects the
//               like buttons, and hides the Load more button when there are
//               no more posts.
// PARAMETERS  : none
// RETURNS     : nothing

const getData = () => {
    $.ajax({
    type: 'GET',
    url: `/data/${visible}/`,
    success: function(response){
        console.log(response)
        const data = response.data
        setTimeout (() =>{
        spinnerBox.classList.add('not-visible')
        console.log(data)
        data.forEach(el => {
            postsBox.innerHTML += `
                <div class="card mb-2">
                    <div class="card-body">
                        <h5 class="card-title">${el.title}</h5>
                        <p class="card-text">${el.body}</p>
                    </div>
                    <div class = "card-footer">
                        <div class = "row">
                            <div class = "col-2">
                                <a href="${url}${el.id}" class="btn btn-primary">Details</a>
                            </div>
                            <div class = "col-2">
                                <form class = "like-unlike-forms" data-form-id = "${el.id}">
                                    <button class="btn btn-primary" id = "like-unlike-${el.id}">${el.liked ? `Unlike (${el.count})` : `Like (${el.count})`}</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            `
        });
        likeUnlikePosts()
        }, 100)
        console.log(response.size)
        if (response.size === 0){
            endBox.textContent = "No post added"
        }
        else if (response.size <= visible){
            loadBtn.classList.add('not-visible')
            endBox.textContent = 'No more posts to load'
        }
    },
    error: function(error){
        console.log(error)
    }
})
}

// EVENT       : Load more button click
// DESCRIPTION : Shows the spinner and requests three more posts.

loadBtn.addEventListener('click', () =>{
    spinnerBox.classList.remove('not-visible')
    visible += 3
    getData()
})

let newPostId = null

// EVENT       : Create post form submit
// DESCRIPTION : Sends the new post's title and body to the server with Ajax.
//               On success, adds the new post to the top of the list,
//               connects its like button, and shows a success alert.

postForm.addEventListener('submit', e=>{
    e.preventDefault()

    $.ajax({
        type: 'POST',
        url: '',
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'title': title.value,
            'body': body.value
        },
        success: function(response){
            console.log(response)
            newPostId = response.id
            postsBox.insertAdjacentHTML('afterbegin', `
                <div class="card mb-2">
                        <div class="card-body">
                            <h5 class="card-title">${response.title}</h5>
                            <p class="card-text">${response.body}</p>
                        </div>
                    <div class = "card-footer">
                        <div class = "row">
                            <div class = "col-2">
                                <a href="${url}${response.id}" class="btn btn-primary">Details</a>
                            </div>
                            <div class = "col-2">
                                <form class = "like-unlike-forms" data-form-id = "${response.id}">
                                    <button class="btn btn-primary" id = "like-unlike-${response.id}">Like (0)</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
                `)
                likeUnlikePosts()
                //$('#addPostModal').modal('hide')
                handleAlerts('success', 'New post added!')
                //postForm.reset()
        },
        error: function(error){
            console.log(error)
            handleAlerts('danger', 'Oops, something went wrong')
        }
    })
})

// EVENT       : Add button click
// DESCRIPTION : Shows the Dropzone area so photos can be added to the new post.

addBtn.addEventListener('click', ()=> {
    dropzone.classList.remove('not-visible')
})

// EVENT       : Modal close buttons click
// DESCRIPTION : Resets the create post form, hides the Dropzone area again,
//               and removes any files that were added to Dropzone.

closeBtns.forEach(btn => btn.addEventListener('click', ()=> {
    postForm.reset()
    if(!dropzone.classList.contains('not-visible')) {
        dropzone.classList.add('not-visible')
    }
    const myDropzone = Dropzone.forElement("#my-dropzone")
    myDropzone.removeAllFiles(true)
}))

Dropzone.autoDiscover = false
const myDropzone = new Dropzone('#my-dropzone', {
    url: "upload/",
    init: function() {
        this.on('sending', function(file, xhr, formData){
            formData.append('csrfmiddlewaretoken', csrftoken)
            formData.append('new_post_id', newPostId)
        })
    },
    maxFiles: 3,
    maxFilessize: 4,
    acceptedFiles: '.png, .jpg, .jpeg'
})

getData()