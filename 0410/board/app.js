document.addEventListener('DOMContentLoaded', () => {
    const postsList = document.getElementById('posts-list');
    const searchInput = document.getElementById('search-input');
    const writeBtn = document.getElementById('write-btn');
    const postModal = document.getElementById('post-modal');
    const modalBody = document.getElementById('modal-body');
    const closeModal = document.querySelector('.close-btn');

    // Mock Data
    const posts = [
        {
            id: 1,
            title: "Exploring the Neural Link Protocol v4.2",
            author: "Dr. Aris Vane",
            avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Aris",
            date: "2 hours ago",
            type: "Technical",
            content: "The latest update to the neural link protocol introduces quantum entanglement for zero-latency data transfer between biological and digital substrates. We've seen a 40% increase in synchronization stability...",
            likes: 124,
            comments: 42,
            views: "1.2k"
        },
        {
            id: 2,
            title: "Neo-Capitalism in the Orbital Habitats",
            author: "Luna Echo",
            avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Luna",
            date: "5 hours ago",
            type: "Sociology",
            content: "As we move further into the Kuiper belt, the traditional economic models are failing. Credits are being replaced by computation power as the primary currency within the habitat clusters...",
            likes: 89,
            comments: 15,
            views: "850"
        },
        {
            id: 3,
            title: "Cybernetic Enhancement vs. Pure Biology",
            author: "Kaelen 01",
            avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Kaelen",
            date: "Yesterday",
            type: "Philosophy",
            content: "Where do we draw the line? At what point does a human become a machine, and does it even matter in a world where consciousness can be backed up to the cloud? This debate has reached a boiling point in sector 7...",
            likes: 256,
            comments: 110,
            views: "3.4k"
        },
        {
            id: 4,
            title: "VOID: New Stealth Infiltration Tech",
            author: "Cipher Black",
            avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Cipher",
            date: "1 day ago",
            type: "Security",
            content: "The VOID coating allows light to pass through the object by warping the local gravitational field. Initial tests show complete invisibility to all current sensor arrays including thermal and LiDAR...",
            likes: 512,
            comments: 88,
            views: "5.8k"
        }
    ];

    // Render Posts
    function renderPosts(filteredPosts) {
        postsList.innerHTML = '';
        if (filteredPosts.length === 0) {
            postsList.innerHTML = '<div class="glass-card" style="text-align:center; padding: 40px;">No transmissions found in this sector.</div>';
            return;
        }

        filteredPosts.forEach(post => {
            const card = document.createElement('div');
            card.className = 'post-card';
            card.innerHTML = `
                <div class="post-header">
                    <div class="post-user">
                        <img src="${post.avatar}" alt="${post.author}">
                        <div>
                            <p class="name">${post.author}</p>
                            <p class="date">${post.date}</p>
                        </div>
                    </div>
                    <span class="post-type">${post.type}</span>
                </div>
                <div class="post-content">
                    <h3>${post.title}</h3>
                    <p>${post.content}</p>
                </div>
                <div class="post-footer">
                    <div class="stat"><i class="fa-regular fa-heart"></i> ${post.likes}</div>
                    <div class="stat"><i class="fa-regular fa-comment"></i> ${post.comments}</div>
                    <div class="stat"><i class="fa-regular fa-eye"></i> ${post.views}</div>
                </div>
            `;
            card.addEventListener('click', () => openPost(post));
            postsList.appendChild(card);
        });
    }

    // Modal Interaction
    function openPost(post) {
        modalBody.innerHTML = `
            <div class="post-header">
                <div class="post-user">
                    <img src="${post.avatar}" alt="${post.author}" style="width: 60px; height: 60px;">
                    <div>
                        <h2 style="margin-bottom: 0;">${post.author}</h2>
                        <p class="date">${post.date} • ${post.type}</p>
                    </div>
                </div>
            </div>
            <div class="post-detail-content" style="margin-top: 30px;">
                <h1 style="font-size: 2.5rem; line-height: 1.2; margin-bottom: 20px;">${post.title}</h1>
                <p style="font-size: 1.1rem; color: #ccc; line-height: 1.8;">${post.content}${post.content}${post.content}</p>
                <div style="margin-top: 40px; display: flex; gap: 15px;">
                    <button class="btn-primary"><i class="fa-solid fa-heart"></i> Endorse</button>
                    <button class="btn-icon"><i class="fa-solid fa-share-nodes"></i></button>
                </div>
            </div>
        `;
        postModal.style.display = 'flex';
    }

    // Search Logic
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = posts.filter(p => 
            p.title.toLowerCase().includes(term) || 
            p.content.toLowerCase().includes(term) ||
            p.author.toLowerCase().includes(term)
        );
        renderPosts(filtered);
    });

    // Close Modal
    closeModal.addEventListener('click', () => {
        postModal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === postModal) postModal.style.display = 'none';
    });

    // Write Button Action
    writeBtn.addEventListener('click', () => {
        alert("Initializing Neural Transmitter... (Form feature coming in next expansion)");
    });

    // Initial Render with extra delay for "wow" effect of skeleton
    setTimeout(() => {
        renderPosts(posts);
    }, 1200);
});
