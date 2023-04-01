document.addEventListener('DOMContentLoaded', () => {
    const posts = document.querySelectorAll('.post-container');

    posts.forEach(post => {
        const editBtn = post.querySelector('.edit-post');
        
        const likeBtn = post.querySelector('#heart-like');
        const dislikeBtn = post.querySelector('#heart-dislike');

        const postId = post.id.substring(5);
        const editUrl = `/api/post/${postId}/edit`;
        const likeUrl = `/api/post/${postId}/like`;

        async function updateLikes(likeUrl, likesChange) {
            const likeCountEl = post.querySelector('#likes-count');
            let likes = parseInt(likeCountEl.innerText);
            likes += likesChange;
        
            await fetch(likeUrl, {
              method: 'PUT',
              body: JSON.stringify({
                likes: likes
              })
            })
            .then(response => response.json())
            .then(data => {
              console.log(data);
              likeCountEl.innerText = data.likes;
            });
          }

        // like button
        if (likeBtn) {
            likeBtn.addEventListener('click', () => {
            if (likeBtn.id === 'heart-like') {
                updateLikes(likeUrl, 1);
                likeBtn.querySelector('path:nth-child(2)').setAttribute('fill', 'red');
                likeBtn.id = 'heart-dislike';
            } else {
                updateLikes(likeUrl, -1);
                likeBtn.querySelector('path:nth-child(2)').setAttribute('fill', 'none');
                likeBtn.id = 'heart-like';
            }
            });
        }
  

        // dislike button
        if (dislikeBtn) {
            dislikeBtn.addEventListener('click', () => {
                if (dislikeBtn.id === 'heart-dislike') {
                    updateLikes(likeUrl, -1);
                    dislikeBtn.querySelector('path:nth-child(2)').setAttribute('fill', 'none');
                    dislikeBtn.id = 'heart-like';
                } else {
                    updateLikes(likeUrl, 1);
                    dislikeBtn.querySelector('path:nth-child(2)').setAttribute('fill', 'red');
                    dislikeBtn.id = 'heart-dislike';

                }
            });
        }

        // edit button
        if (editBtn) {
            editBtn.addEventListener('click', async () => {
                await fetch(editUrl)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    handleEdit(post, data);
                });
    
                function handleEdit(element, data) {
                    const bodyContainer = element.querySelector('.body-container');
                    // target p tag within the body container
                    const pElement = element.querySelector('.body-container > p');
    
                    // create textarea
                    const textArea = document.createElement('textarea');
                    textArea.setAttribute('id', 'edit-textarea');
    
                    // create cancel button
                    const cancelBtn = document.createElement('button');
                    cancelBtn.setAttribute('id', 'edit-cancel');
    
                    // create save button
                    const saveBtn = document.createElement('button');
                    saveBtn.setAttribute('id', 'edit-save');
                    saveBtn.classList = 'btn btn-primary btn-sm';
    
                    // create div and append cancel button 
                    const editDiv = document.createElement('div');
                    editDiv.classList = 'edit-div';
                    editDiv.append(saveBtn);
                    bodyContainer.append(editDiv);
    
                    
                    // replace elements
                    pElement.replaceWith(textArea);
                    editBtn.replaceWith(cancelBtn);
                    // pre-populate 
                    textArea.innerText = data.post;
                    saveBtn.innerText = "Save";
                    cancelBtn.innerText = "Cancel";
    
                    function revertChanges() {
                        textArea.replaceWith(pElement);
                        cancelBtn.replaceWith(editBtn);
                        editDiv.remove();
                    }
    
                    // handle cancel
                    cancelBtn.addEventListener('click', () => {
                        revertChanges();
                    });
    
                    // handle save 
                    saveBtn.addEventListener('click', async () => {
                        const editedPost = textArea.value;
                        await fetch(editUrl, {
                            method: 'PUT',
                            body: JSON.stringify({
                                post: editedPost
                            }),
                        })
                        .then(response => response.json())
                        .then(data => console.log(data));
    
                        revertChanges();
                        pElement.innerText = editedPost;
                    })
                }
            })
        }
    });
});
