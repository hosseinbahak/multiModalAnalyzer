document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const chatHistory = document.getElementById('chat-history');
    const queryForm = document.getElementById('query-form');
    const queryText = document.getElementById('query-text');
    const submitBtn = document.getElementById('submit-btn');
    const clearBtn = document.getElementById('clear-btn');
    const imageUpload = document.getElementById('image-upload');
    const pdfUpload = document.getElementById('pdf-upload');
    const imageName = document.getElementById('image-name');
    const pdfName = document.getElementById('pdf-name');
    const previewContent = document.getElementById('preview-content');
    
    // Handle file uploads
    imageUpload.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            imageName.textContent = file.name;
            
            // Create image preview
            const reader = new FileReader();
            reader.onload = function(e) {
                previewContent.innerHTML = `<img src="${e.target.result}" alt="Image preview">`;
            };
            reader.readAsDataURL(file);
        }
    });
    
    pdfUpload.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            pdfName.textContent = file.name;
            
            // Create PDF indicator
            previewContent.innerHTML = `
                <div class="preview-pdf">
                    <i class="fas fa-file-pdf"></i>
                    <div>
                        <strong>${file.name}</strong>
                        <div>${(file.size / 1024).toFixed(2)} KB</div>
                    </div>
                </div>
            `;
        }
    });
    
    // Handle form submission
    queryForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const query = queryText.value.trim();
        if (!query) return;
        
        // Add user message to chat
        addMessage('user', query);
        
        // Add file indicators if files are attached
        let fileInfo = '';
        if (imageUpload.files && imageUpload.files[0]) {
            fileInfo += `<div class="file-indicator"><i class="fas fa-image"></i> ${imageUpload.files[0].name}</div>`;
        }
        if (pdfUpload.files && pdfUpload.files[0]) {
            fileInfo += `<div class="file-indicator"><i class="fas fa-file-pdf"></i> ${pdfUpload.files[0].name}</div>`;
        }
        
        if (fileInfo) {
            const lastMessage = chatHistory.lastElementChild;
            lastMessage.querySelector('.message-content').innerHTML += fileInfo;
        }
        
        // Show loading indicator
        addMessage('assistant', '<div class="loading"></div>', false);
        
        // Prepare form data
        const formData = new FormData(queryForm);
        
        try {
            // Send request to server
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            // Remove loading indicator
            chatHistory.removeChild(chatHistory.lastElementChild);
            
            // Add assistant response
            addMessage('assistant', data.response);
            
            // Clear input
            queryText.value = '';
            
        } catch (error) {
            console.error('Error:', error);
            
            // Remove loading indicator
            chatHistory.removeChild(chatHistory.lastElementChild);
            
            // Add error message
            addMessage('system', 'An error occurred while processing your request. Please try again.');
        }
    });
    
    // Clear conversation
    clearBtn.addEventListener('click', async function() {
        // Clear chat history
        chatHistory.innerHTML = `
            <div class="message system">
                <div class="message-content">
                    <p>Hello! I'm your Multimodal Analysis Assistant. I can help you analyze images and PDF documents. 
                       Upload a file and ask me a question to get started.</p>
                </div>
            </div>
        `;
        
        // Clear file inputs
        imageUpload.value = '';
        pdfUpload.value = '';
        imageName.textContent = '';
        pdfName.textContent = '';
        
        // Reset preview
        previewContent.innerHTML = '<p>No files uploaded</p>';
        
        // Reset session on server
        try {
            await fetch('/clear', {
                method: 'POST'
            });
        } catch (error) {
            console.error('Error clearing session:', error);
        }
    });
    
    // Helper function to add messages to the chat
    function addMessage(type, content, scroll = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = `<p>${content}</p>`;
        
        messageDiv.appendChild(messageContent);
        chatHistory.appendChild(messageDiv);
        
        if (scroll) {
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    }
    
    // Auto-resize textarea
    queryText.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});