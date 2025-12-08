import React, { useState, useEffect, useRef, useImperativeHandle, forwardRef } from 'react';
import './ChatWidget.css';



const ChatWidget = forwardRef((props, ref) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useImperativeHandle(ref, () => ({
    sendMessageFromOutside: async (messageText) => {
      setIsOpen(true); // Open chat if not already open
      await handleSendMessage(messageText);
    },
    setIsOpen,
  }));

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = async (messageText) => {
    if (messageText.trim() === '' || isLoading) return;

    const userMessage = { text: messageText, sender: 'user' };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputMessage(''); // Clear input only if it's from the input field
    setIsLoading(true);

    try {
      const response = await fetch("https://chatbot-backend-for-book.up.railway.app/ask", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: messageText }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: data.reply, sender: 'bot', sources: data.sources },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: `Error: ${error.message}. Please try again.`, sender: 'bot', isError: true },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setInputMessage(e.target.value);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage(inputMessage);
    }
  };

  return (
    <div className="chat-widget">
      <button className="chat-button" onClick={() => setIsOpen(!isOpen)}>
        💬
      </button>

      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <h3>AI Tutor</h3>
            <button className="close-button" onClick={() => setIsOpen(false)}>
              &times;
            </button>
          </div>
          <div className="chat-messages">
            {messages.length === 0 && !isLoading && (
                <div className="chat-welcome">
                    Welcome! Ask me anything about the Physical AI Textbook.
                </div>
            )}
            {messages.map((msg, index) => (
              <div key={index} className={`chat-msg ${msg.sender}`}>
                <p>{msg.text}</p>
                {msg.sources && msg.sources.length > 0 && (
                  <div className="chat-sources">
                    <strong>Sources:</strong> {msg.sources.join(', ')}
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="chat-msg bot loading">
                <p>...</p>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={inputMessage}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question..."
              disabled={isLoading}
            />
            <button onClick={() => handleSendMessage(inputMessage)} disabled={isLoading}>
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
});

export default ChatWidget;
