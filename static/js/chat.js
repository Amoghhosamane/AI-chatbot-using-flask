document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = userInput.scrollHeight + 'px';

        if (userInput.value.trim() !== "") {
            sendBtn.classList.add('active');
        } else {
            sendBtn.classList.remove('active');
        }
    });

    const addMessage = (message, isUser = false) => {
        const wrapper = document.createElement('div');
        wrapper.className = `message-wrapper ${isUser ? 'user' : 'bot'}`;

        const content = document.createElement('div');
        content.className = 'message-content';

        const avatar = document.createElement('div');
        avatar.className = `avatar ${isUser ? 'user-avatar' : 'bot-avatar'}`;
        avatar.innerHTML = isUser ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';

        const textWrapper = document.createElement('div');
        textWrapper.className = 'text';
        textWrapper.innerText = message;

        content.appendChild(avatar);
        content.appendChild(textWrapper);
        wrapper.appendChild(content);
        chatHistory.appendChild(wrapper);

        // Scroll to bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;
    };

    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        // Clear input
        userInput.value = '';
        userInput.style.height = 'auto';
        sendBtn.classList.remove('active');

        // Add user message to UI
        addMessage(message, true);

        // Show typing indicator (simulated)
        const typingWrapper = document.createElement('div');
        typingWrapper.className = 'message-wrapper bot';
        typingWrapper.id = 'typing-indicator';
        typingWrapper.innerHTML = `
            <div class="message-content">
                <div class="avatar bot-avatar">
                    <i class="fa-solid fa-robot"></i>
                </div>
                <div class="text">
                    <span class="typing"></span>
                    <span class="typing" style="animation-delay: 0.2s"></span>
                    <span class="typing" style="animation-delay: 0.4s"></span>
                </div>
            </div>
        `;
        chatHistory.appendChild(typingWrapper);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        try {
            const response = await fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // Remove typing indicator
            document.getElementById('typing-indicator').remove();

            // Add bot message to UI
            addMessage(data.response, false);
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('typing-indicator').remove();
            addMessage("Lo siento, hubo un error al procesar tu solicitud.", false);
        }
    };

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});
