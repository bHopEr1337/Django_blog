document.querySelectorAll('.filter-buttons button').forEach(button => {
    button.addEventListener('click', () => {
        // Remove 'active' class from all buttons
        document.querySelectorAll('.filter-buttons button').forEach(btn => {
            btn.classList.remove('active');
        });
        // Add 'active' class to the clicked button
        button.classList.add('active');

        const category = button.dataset.category;
        fetchPosts(category);
    });
});




    document.querySelectorAll('.filter-buttons button').forEach(button => {
    button.addEventListener('click', () => {
        const category = button.dataset.category;
        fetchPosts(category);
    });
});

    function fetchPosts(category) {
    fetch(`/blog/filter/?category=${category}`)
        .then(response => response.json())
        .then(data => {
            const postListElement = document.querySelector('.post-list');
            postListElement.innerHTML = '';

            data.posts.forEach(post => {
                const words = post.body.split(' ');
                const truncatedBody = words.slice(0, 30).join(' ') + '...';
                const postElement = document.createElement('div');
                postElement.classList.add('post');
                postElement.innerHTML = `
                      <h2><a href="${post.url}">${post.title}</a></h2>
                      <p class="date">
                    Published ${post.publish} by ${post.author}
                      </p>
                      <div class="body">${truncatedBody}</div>
                      <p>Category: ${post.category}</p>
                    `;
                postListElement.appendChild(postElement);
            });
        })
        .catch(error => console.error(error));
}

    // Trigger the 'click' event on the 'all' button when the page loads
    document.querySelector('.filter-buttons button[data-category=""]').click();