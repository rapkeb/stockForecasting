async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput.trim()) return;

    // Append user message to chatbox
    appendMessage('You', userInput);

    const response = await fetch('chat_service/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: userInput })
    });

    const data = await response.json();
    appendMessage('Assistant', data.response);

    // Clear the input field
    document.getElementById('user-input').value = '';
}

async function resetChat() {
    await fetch('chat_service/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    });

    document.getElementById('chatbox').innerHTML = '';
}

function detectLanguage(text) {
    // Simple check for Hebrew characters
    const hebrewPattern = /[\u0590-\u05FF]/;
    return hebrewPattern.test(text) ? 'Hebrew' : 'English';
}

function appendMessage(sender, message) {
    const chatbox = document.getElementById('chatbox');
    const messageElement = document.createElement('div');

    messageElement.setAttribute('dir', 'auto');
    
    const language = detectLanguage(message);

    if (sender === 'You') {
        sender = language === 'Hebrew' ? 'אתה' : 'You';
    } else if (sender === 'Assistant') {
        sender = language === 'Hebrew' ? 'העוזר החכם' : 'AI Assistant';
    }

    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}

async function getUserPreferencesAndSendToChat() {
    try {
        // Step 1: Fetch user preferences
        const response = await fetch('/db/preferences', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();
        const { preferences } = data;

        // Step 2: Generate the prompt from preferences
        let prompt = "Based on the following user preferences, what should they invest in?\n";
        prompt += `Sectors: ${preferences.sectors ? preferences.sectors.join(', ') : 'Not set'}\n`;
        prompt += `Risk Tolerance: ${preferences.risk_tolerance || 'Not set'}\n`;
        prompt += `Investment Horizon: ${preferences.investment_horizon || 'Not set'}\n`;
        prompt += 'please attach for each prefernces also specific shares names do it shortly in max 300 tokens';

        // Step 3: Send the prompt to the chat service
        const chatResponse = await fetch('chat_service/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: prompt })
        });

        const chatData = await chatResponse.json();
        const assistantResponse = chatData.response;

        // Step 4: Display the assistant's response
        appendMessage1(assistantResponse);

    } catch (error) {
        console.error('Error fetching preferences or sending to chat:', error);
    }
}

function appendMessage1(message) {
    const chatbox = document.getElementById('suggest');
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<strong>${message.replace(/\n/g, '<br>')}:</strong>`;
    messageElement.setAttribute('dir', 'auto');
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}

// Call the function to get preferences and send to chat
getUserPreferencesAndSendToChat();

