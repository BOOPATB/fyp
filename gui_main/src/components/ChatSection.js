
import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

// Styled components
const ChatContainer = styled.div`
  background: var(--bg-card);
  display: flex;
  flex-direction: column;
  height: 100%;
`;

const ChatHeader = styled.div`
  padding: var(--spacing-6) var(--spacing-6) var(--spacing-4);
  border-bottom: 1px solid var(--border-color);
`;

const SectionTitle = styled.h2`
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-2) 0;
`;

const SectionSubtitle = styled.p`
  font-size: var(--font-size-sm);
  color: var(--text-muted);
  margin: 0;
`;

const MessagesContainer = styled.div`
  flex: 1;
  padding: var(--spacing-4) var(--spacing-6);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
  min-height: 0;
`;

const Message = styled(motion.div)`
  display: flex;
  gap: var(--spacing-3);
  align-items: flex-start;

  ${props => props.isUser && `
    flex-direction: row-reverse;
    .message-content {
      background: var(--primary-color);
      color: white;
    }
  `}
`;

const MessageAvatar = styled.div`
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: ${props => props.isUser ? 'var(--secondary-color)' : 'var(--accent-color)'};
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: var(--font-size-sm);
  color: white;
  flex-shrink: 0;
`;

const MessageContent = styled.div`
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-3) var(--spacing-4);
  max-width: 80%;
  word-wrap: break-word;

  .message-text {
    color: var(--text-primary);
    font-size: var(--font-size-sm);
    line-height: 1.5;
    margin: 0;
  }

  .message-time {
    color: var(--text-muted);
    font-size: var(--font-size-xs);
    margin-top: var(--spacing-2);
  }
`;

const TypingIndicator = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  padding: var(--spacing-2) 0;
`;

const TypingDots = styled.div`
  display: flex;
  gap: 4px;
  padding: var(--spacing-3) var(--spacing-4);
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);

  .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--text-muted);
  }
`;

const ChatInput = styled.div`
  padding: var(--spacing-4) var(--spacing-6);
  border-top: 1px solid var(--border-color);
`;

const InputContainer = styled.div`
  display: flex;
  gap: var(--spacing-3);
  align-items: flex-end;
`;

const InputField = styled.textarea`
  flex: 1;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-3) var(--spacing-4);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
  line-height: 1.5;
  resize: none;
  min-height: 44px;
  max-height: 120px;

  &:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
  }

  &::placeholder {
    color: var(--text-muted);
  }
`;

const SendButton = styled(motion.button)`
  width: 44px;
  height: 44px;
  border-radius: var(--radius-lg);
  background: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;

  &:hover {
    background: var(--primary-hover);
  }

  &:disabled {
    background: var(--bg-tertiary);
    color: var(--text-muted);
    cursor: not-allowed;
  }
`;

const ActionButtons = styled.div`
  display: flex;
  gap: var(--spacing-2);
  margin-top: var(--spacing-2);
`;

const ActionButton = styled(motion.button)`
  padding: var(--spacing-2) var(--spacing-3);
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: var(--font-size-xs);
  font-weight: 500;
  transition: all 0.2s ease;

  &:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
  }
`;

// === API CALL FUNCTION ===
const sendMessageToAgent = async (inputText) => {
  console.log('🔵 [API] Starting request to backend...', inputText);
  
  try {
    console.log('🔵 [API] Calling fetch with URL: http://localhost:5000/api/agent');
    
    const response = await fetch('http://localhost:5000/api/agent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: inputText }),
    });
    
    console.log('🔵 [API] Response status:', response.status);
    
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('✅ [API] Response data:', data);
    
    return data.response || "No response from agent.";
  } catch (err) {
    console.error('❌ [API] Error calling agent:', err);
    return `Error: Unable to communicate with AI agent. ${err.message};`
  }
};

// === MAIN COMPONENT ===
const ChatSection = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Welcome! I'm your AI meeting assistant. I can help you transcribe, summarize, and analyze your meetings.",
      isUser: false,
      time: "2:30 PM",
      sender: "AI"
    },
    {
      id: 2,
      text: "Hello! Can you help me understand the key points from today's meeting?",
      isUser: true,
      time: "2:32 PM",
      sender: "You"
    },
    {
      id: 3,
      text: "Absolutely! Based on the audio I'm processing, here are the key points I've identified:\n\n• Quarterly revenue increased by 25%\n• New product launch scheduled for Q2\n• Team expansion plans discussed\n• Budget allocation for marketing campaign\n\nWould you like me to elaborate on any of these points?",
      isUser: false,
      time: "2:32 PM",
      sender: "AI"
    }
  ]);
  
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSendMessage = async () => {
    console.log('🟢 [CHAT] handleSendMessage called');
    console.log('🟢 [CHAT] Input text:', inputText);
    
    if (!inputText.trim()) {
      console.log('⚠️ [CHAT] Empty input, not sending');
      return;
    }

    const messageToSend = inputText; // Store before clearing
    
    const newMessage = {
      id: messages.length + 1,
      text: messageToSend,
      isUser: true,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sender: "You"
    };

    console.log('🟢 [CHAT] Adding user message to chat:', newMessage);
    setMessages(prev => [...prev, newMessage]);
    setInputText('');
    setIsTyping(true);

    console.log('🟢 [CHAT] Calling backend API...');
    const aiText = await sendMessageToAgent(messageToSend);
    console.log('🟢 [CHAT] Received AI response:', aiText);
    
    const aiResponse = {
      id: newMessage.id + 1,
      text: aiText,
      isUser: false,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sender: "AI"
    };
    
    console.log('🟢 [CHAT] Adding AI response to chat:', aiResponse);
    setMessages(prev => [...prev, aiResponse]);
    setIsTyping(false);
    console.log('✅ [CHAT] Message handling complete');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      console.log('⌨️ [CHAT] Enter key pressed, triggering send');
      handleSendMessage();
    }
  };

  const quickActions = [
    "Summarize meeting",
    "Extract action items",
    "Identify speakers",
    "Generate transcript"
  ];

  return (
    <ChatContainer>
      <ChatHeader>
        <SectionTitle>AI Assistant</SectionTitle>
        <SectionSubtitle>Ask questions about your meeting or get insights</SectionSubtitle>
      </ChatHeader>

      <MessagesContainer>
        {messages.map((message) => (
          <Message
            key={message.id}
            isUser={message.isUser}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <MessageAvatar isUser={message.isUser}>
              {message.isUser ? 'U' : 'AI'}
            </MessageAvatar>
            <MessageContent className="message-content">
              <p className="message-text">{message.text}</p>
              <div className="message-time">{message.time}</div>
            </MessageContent>
          </Message>
        ))}

        {isTyping && (
          <TypingIndicator
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <MessageAvatar isUser={false}>AI</MessageAvatar>
            <TypingDots>
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  className="dot"
                  animate={{ opacity: [0.4, 1, 0.4] }}
                  transition={{
                    duration: 1.4,
                    repeat: Infinity,
                    delay: i * 0.2
                  }}
                />
              ))}
            </TypingDots>
          </TypingIndicator>
        )}
      </MessagesContainer>

      <ChatInput>
        <InputContainer>
          <InputField
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything about your meeting..."
            rows={1}
          />
          <SendButton
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isTyping}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            ➤
          </SendButton>
        </InputContainer>
        
        <ActionButtons>
          {quickActions.map((action, index) => (
            <ActionButton
              key={action}
              onClick={() => setInputText(action)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              {action}
            </ActionButton>
          ))}
        </ActionButtons>
      </ChatInput>
    </ChatContainer>
  );
};

export default ChatSection;
