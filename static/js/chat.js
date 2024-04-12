document.getElementById('chat-button').addEventListener('click', function() {
    const userId = this.getAttribute('data-user-id');
    const chatSocket = new WebSocket(`ws://your_server/chat/${userId}/`);
    
    chatSocket.onopen = function() {
        console.log('WebSocket connection established.');
        // You can show a chat window or perform other actions here.
    };
    
    chatSocket.onmessage = function(event) {
        const messageData = JSON.parse(event.data);
        // Handle incoming chat messages and display them in the chat window.
    };
    
    chatSocket.onclose = function(event) {
        console.log('WebSocket connection closed.');
    };
    
    // You can send messages using chatSocket.send() as needed.
});