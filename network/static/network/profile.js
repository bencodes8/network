document.addEventListener('DOMContentLoaded', () => {
    const followButton = document.querySelector('#header-container > button');
    const userId = document.querySelector('h3').id;

    followButton ? followButton.addEventListener('click', (event) => {
        async function handleFollow() {
            await fetch(`/api/user/${userId}`, {
                method: 'PUT',
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                document.getElementById('follower-count').innerText = data.followers_count;
                document.getElementById('following-count').innerText = data.following_count;
            });
        }

        handleFollow();

        if (event.target.id === 'unfollow-button') {
            event.target.setAttribute('id', 'follow-button');
            event.target.classList.remove('btn-secondary');
            event.target.classList.add('btn-primary');
            event.target.innerText = 'Follow';
        } else if (event.target.id === 'follow-button') {
            event.target.setAttribute('id', 'unfollow-button')
            event.target.classList.remove('btn-primary');
            event.target.classList.add('btn-secondary')
            event.target.innerText = 'Unfollow';
        }
    }) : null;

});