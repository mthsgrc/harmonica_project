document.addEventListener('DOMContentLoaded', function() {
    const tabContent = document.getElementById('tab-content');
    const decreaseBtn = document.getElementById('decrease-font');
    const resetBtn = document.getElementById('reset-font');
    const increaseBtn = document.getElementById('increase-font');
    
    // Default font size (matches your CSS)
    const defaultSize = 16; 
    
    // Get saved font size or use default
    let currentSize = parseInt(localStorage.getItem('tabFontSize')) || defaultSize;
    
    // Apply current font size
    applyFontSize(currentSize);
    
    // Event listeners
    decreaseBtn.addEventListener('click', () => adjustFontSize(-1));
    resetBtn.addEventListener('click', resetFontSize);
    increaseBtn.addEventListener('click', () => adjustFontSize(1));
    
    function applyFontSize(size) {
        tabContent.style.fontSize = `${size}px`;
        localStorage.setItem('tabFontSize', size.toString());
        
        // Disable buttons at limits
        decreaseBtn.disabled = size <= 12;
        increaseBtn.disabled = size >= 24;
    }
    
    function adjustFontSize(change) {
        const newSize = currentSize + change;
        
        // Set boundaries (12px min, 24px max)
        if (newSize >= 12 && newSize <= 24) {
            currentSize = newSize;
            applyFontSize(currentSize);
        }
        document.getElementById('font-size-value').textContent = size;
    }
    
    function resetFontSize() {
        currentSize = defaultSize;
        applyFontSize(currentSize);
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl + + to increase
        if (e.ctrlKey && e.key === '+') {
            e.preventDefault();
            adjustFontSize(1);
        }
        
        // Ctrl + - to decrease
        if (e.ctrlKey && e.key === '-') {
            e.preventDefault();
            adjustFontSize(-1);
        }
        
        // Ctrl + 0 to reset
        if (e.ctrlKey && e.key === '0') {
            e.preventDefault();
            resetFontSize();
        }
    });
});

document.querySelectorAll('.favorite-btn').forEach(btn => {
    btn.addEventListener('click', async function(e) {
        e.preventDefault();
        const form = this.closest('form');
        const response = await fetch(form.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        
        if (data.action === 'added') {
            this.innerHTML = '★ Unfavorite';
        } else {
            this.innerHTML = '☆ Favorite';
        }
    });
});