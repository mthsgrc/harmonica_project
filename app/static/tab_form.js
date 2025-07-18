document.addEventListener('DOMContentLoaded', function() {
    const youtubeField = document.getElementById('youtube_link');
    
    if (youtubeField) {
        youtubeField.addEventListener('blur', function() {
            let url = this.value.trim();
            
            if (!url) return;
            
            // Convert youtu.be links to youtube.com format
            if (url.includes('youtu.be')) {
                const videoId = url.split('/').pop();
                this.value = `https://www.youtube.com/watch?v=${videoId}`;
                return;
            }
            
            // Ensure it's a full URL
            if (!url.startsWith('http')) {
                this.value = `https://${url}`;
            }
        });
    }
});

// Markdown preview
const contentField = document.getElementById('content');
const contentPreview = document.getElementById('content-preview');

if (contentField && contentPreview) {
    contentField.addEventListener('input', function() {
        // Simple conversion for demonstration
        // In production, use a proper markdown parser
        const text = this.value;
        
        // Basic conversions
        let html = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>')             // italic
            .replace(/`(.*?)`/g, '<code>$1</code>')           // inline code
            .replace(/^# (.*$)/gm, '<h3>$1</h3>')             // h1
            .replace(/^## (.*$)/gm, '<h4>$1</h4>')            // h2
            .replace(/\n/g, '<br>');                          // line breaks
        
        contentPreview.innerHTML = html;
    });
}