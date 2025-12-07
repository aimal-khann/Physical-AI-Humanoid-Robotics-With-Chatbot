import React, { useState, useEffect, useRef } from 'react';
import ChatWidget from '../components/ChatWidget';

function Root({ children }) {
  const chatWidgetRef = useRef(null);
  const [showAskAIButton, setShowAskAIButton] = useState(false);
  const [askAIButtonPosition, setAskAIButtonPosition] = useState({ top: 0, left: 0 });
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    const handleMouseUp = (e) => {
      const selection = window.getSelection();
      const text = selection.toString().trim();

      if (text.length > 0 && e.target.closest('.chat-widget') === null) { // Prevent showing button over chat widget
        setSelectedText(text);
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        
        // Position the button slightly above and to the right of the selection
        setAskAIButtonPosition({
          top: window.scrollY + rect.top - 40, // 40px above selection
          left: window.scrollX + rect.right - 50, // 50px to the left of the right edge
        });
        setShowAskAIButton(true);
      } else {
        setShowAskAIButton(false);
      }
    };

    const handleClickOutside = (e) => {
      if (!e.target.closest('.ask-ai-button')) { // If click is not on the button itself
        setShowAskAIButton(false);
      }
    };

    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('mousedown', handleClickOutside); // Use mousedown to hide earlier

    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleAskAI = () => {
    if (chatWidgetRef.current && selectedText) {
      chatWidgetRef.current.sendMessageFromOutside(selectedText);
      chatWidgetRef.current.setIsOpen(true); // Ensure chat window is open
    }
    setShowAskAIButton(false); // Hide button after sending
  };

  return (
    <>
      {children}
      {showAskAIButton && (
        <button
          className="ask-ai-button"
          style={{ position: 'absolute', top: askAIButtonPosition.top, left: askAIButtonPosition.left }}
          onClick={handleAskAI}
        >
          Ask AI
        </button>
      )}
      <ChatWidget ref={chatWidgetRef} />
    </>
  );
}

export default Root;