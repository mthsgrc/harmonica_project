document.addEventListener('DOMContentLoaded', function() {
    // Select all checkbox
    const selectAllBtn = document.createElement('button');
    selectAllBtn.textContent = 'Select All';
    selectAllBtn.className = 'btn btn-sm btn-outline-secondary';
    selectAllBtn.type = 'button';
    
    document.querySelector('.bulk-actions').prepend(selectAllBtn);
    
    selectAllBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.favorite-checkbox');
        const allChecked = Array.from(checkboxes).every(cb => cb.checked);
        
        checkboxes.forEach(cb => {
            cb.checked = !allChecked;
        });
        
        this.textContent = allChecked ? 'Select All' : 'Deselect All';
    });
});