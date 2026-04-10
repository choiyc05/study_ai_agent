document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('explore-btn');
    const grid = document.querySelector('.futuristic-grid');

    // Mouse following effect for the grid
    window.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        grid.style.transform = `translate(${x * 10}px, ${y * 10}px)`;
    });

    btn.addEventListener('click', () => {
        btn.innerText = 'Synchronizing...';
        setTimeout(() => {
            alert('Neural Link Established. Welcome to the future.');
            btn.innerText = 'Connected';
        }, 1500);
    });

    // Simple scroll reveal observer
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.glass-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        card.style.transition = 'all 0.8s ease-out';
        observer.observe(card);
    });
});
