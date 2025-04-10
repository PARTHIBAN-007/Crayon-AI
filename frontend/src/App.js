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
      console.log(response);

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
    const formattedContent = content
      .split('\n')
      .map((line, i) => <div key={i}>{line || '\u00A0'}</div>);
    
    return formattedContent;
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-indigo-50 to-purple-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4 shadow-sm">
        <h1 className="text-2xl font-bold text-center bg-gradient-to-r from-purple-600 to-blue-500 bg-clip-text text-transparent">
          AI Chat Assistant
        </h1>
      </div>

      {/* Messages Area */}
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.length === 0 ? (
            <div className="text-center py-8">
              <h2 className="text-lg font-medium text-gray-500">Start a conversation</h2>
              <p className="text-gray-400 mt-1">Ask me anything!</p>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg max-w-full break-words ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white ml-auto'
                    : 'bg-white border border-gray-200 shadow-sm mr-auto'
                } flex`}
              >
                <div className="mr-3 mt-1">
                  {message.role === 'user' ? (
                    <User size={20} className="text-white" />
                  ) : (
                    <Bot size={20} className="text-blue-500" />
                  )}
                </div>
                <div className={`${message.role === 'user' ? 'text-white' : 'text-gray-800'}`}>
                  {formatMessage(message.content)}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="bg-white border border-gray-200 p-4 rounded-lg shadow-sm flex max-w-lg">
              <Bot size={20} className="text-blue-500 mr-3 mt-1" />
              <div className="flex items-center text-gray-500">
                <Loader2 className="animate-spin h-4 w-4 mr-2" />
                <span>Thinking...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white p-4">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
          <div className="relative flex items-center">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 p-4 pr-12 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !inputValue.trim()}
              className={`absolute right-3 p-2 rounded-full ${
                isLoading || !inputValue.trim()
                  ? 'text-gray-400 bg-gray-100'
                  : 'text-white bg-blue-500 hover:bg-blue-600'
              }`}
            >
              <Send size={20} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}