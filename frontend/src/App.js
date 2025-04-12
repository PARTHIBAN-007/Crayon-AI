import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Loader2, User, Bot } from 'lucide-react';

export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = { role: 'user', content: inputValue };
    setMessages([...messages, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/chat', {
        message: userMessage.content
      });

      setMessages(prevMessages => [
        ...prevMessages,
        { role: 'assistant', content: response.data.response['output'] }
      ]);
    } catch (error) {
      console.error('Error fetching response:', error);
      setMessages(prevMessages => [
        ...prevMessages,
        { 
          role: 'assistant', 
          content: 'Sorry, I encountered an error. Please try again.' 
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatMessage = (content) => {
    return content
      .split('\n')
      .map((line, i) => <div key={i}>{line || '\u00A0'}</div>);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 text-sm font-normal">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-3 shadow-sm">
        <h1 className="text-base font-semibold text-center text-gray-700">
          Indian Tax System AI Assistant
        </h1>
      </div>

      {/* Messages Area */}
      <div className="flex-1 p-3 overflow-y-auto">
        <div className="max-w-2xl mx-auto space-y-3">
          {messages.length === 0 ? (
            <div className="text-center py-6">
              <h2 className="text-sm font-medium text-gray-500">Start a conversation</h2>
              <p className="text-xs text-gray-400 mt-1">Ask me anything about Indian Tax System.</p>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className={`p-3 rounded-md max-w-full break-words text-sm flex ${
                  message.role === 'user'
                    ? 'bg-blue-100 text-blue-900 ml-auto'
                    : 'bg-white border border-gray-200 text-gray-800 mr-auto'
                }`}
              >
                <div className="mr-2 mt-0.5">
                  {message.role === 'user' ? (
                    <User size={16} className="text-blue-700" />
                  ) : (
                    <Bot size={16} className="text-gray-500" />
                  )}
                </div>
                <div>
                  {formatMessage(message.content)}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="bg-white border border-gray-200 p-3 rounded-md flex max-w-md">
              <Bot size={16} className="text-gray-500 mr-2 mt-0.5" />
              <div className="flex items-center text-gray-500 text-sm">
                <Loader2 className="animate-spin h-4 w-4 mr-2" />
                <span>Thinking...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white p-3">
        <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
          <div className="relative flex items-center">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type a message..."
              className="flex-1 px-4 py-2 text-sm border border-gray-300 rounded-full focus:outline-none focus:ring-1 focus:ring-blue-400 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !inputValue.trim()}
              className={`absolute right-2 p-2 rounded-full ${
                isLoading || !inputValue.trim()
                  ? 'text-gray-400 bg-gray-100'
                  : 'text-white bg-blue-500 hover:bg-blue-600'
              }`}
            >
              <Send size={16} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
