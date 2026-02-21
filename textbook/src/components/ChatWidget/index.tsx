import React, { useState, useRef, useEffect, useCallback } from 'react';
import styles from './index.module.css';

interface ChatMessage {
  id: string;
  role: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

function getOrCreateSessionId(): string {
  if (typeof window === 'undefined') return crypto.randomUUID();
  const key = 'physical-ai-session-id';
  let sid = localStorage.getItem(key);
  if (!sid) {
    sid = crypto.randomUUID();
    localStorage.setItem(key, sid);
  }
  return sid;
}

const WELCOME_MESSAGE: ChatMessage = {
  id: 'welcome',
  role: 'bot',
  content: '👋 Hi! I\'m your Physical AI tutor. Ask me anything about the textbook — foundations, sensing, actuation, or humanoid robots!',
  timestamp: new Date(),
};

export default function ChatWidget(): React.ReactElement {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => getOrCreateSessionId());
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  const sendMessage = useCallback(async () => {
    const question = input.trim();
    if (!question || isLoading) return;

    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: question,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch('https://physical-ai-book-saba-sohail-production.up.railway.app/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, session_id: sessionId }),
      });

      let answer: string;
      if (res.ok) {
        const data = await res.json();
        answer = data.answer;
      } else if (res.status === 429) {
        answer = '⚠️ You\'re sending messages too fast. Please wait a moment and try again.';
      } else if (res.status === 503) {
        answer = '⚠️ The AI service is temporarily unavailable. Please try again in a moment.';
      } else {
        answer = '⚠️ An error occurred. Please try again.';
      }

      const botMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'bot',
        content: answer,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botMsg]);
    } catch {
      setMessages(prev => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'bot',
          content: '⚠️ Connection error. Please check your network and try again.',
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, sessionId]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* Floating toggle button */}
      <button
        className={styles.toggleButton}
        onClick={() => setIsOpen(prev => !prev)}
        aria-label={isOpen ? 'Close AI Tutor' : 'Open AI Tutor'}
        title="AI Textbook Tutor"
      >
        {isOpen ? '✕' : '🤖'}
      </button>

      {/* Chat panel */}
      {isOpen && (
        <div className={styles.panel}>
          <div className={styles.header}>
            <span className={styles.headerIcon}>🤖</span>
            <div>
              <div className={styles.headerTitle}>Physical AI Tutor</div>
              <div className={styles.headerSubtitle}>Powered by GPT-4o-mini + RAG</div>
            </div>
            <button
              className={styles.closeBtn}
              onClick={() => setIsOpen(false)}
              aria-label="Close"
            >
              ✕
            </button>
          </div>

          <div className={styles.messageList}>
            {messages.map(msg => (
              <div
                key={msg.id}
                className={`${styles.message} ${msg.role === 'user' ? styles.userMessage : styles.botMessage}`}
              >
                <div className={styles.messageContent}>{msg.content}</div>
              </div>
            ))}
            {isLoading && (
              <div className={`${styles.message} ${styles.botMessage}`}>
                <div className={styles.typingIndicator}>
                  <span /><span /><span />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.inputBar}>
            <textarea
              ref={inputRef}
              className={styles.input}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about Physical AI, sensors, actuators..."
              rows={1}
              maxLength={2000}
              disabled={isLoading}
            />
            <button
              className={styles.sendBtn}
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              aria-label="Send"
            >
              ➤
            </button>
          </div>
        </div>
      )}
    </>
  );
}
