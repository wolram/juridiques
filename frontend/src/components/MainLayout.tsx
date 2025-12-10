import React, { useState, useRef, useEffect } from 'react';
import { Send, Upload, Settings, Menu } from 'lucide-react';
import ChatPanel from './ChatPanel';
import ThreadSidebar from './ThreadSidebar';
import { useChatStore } from '../store/chatStore';

export default function MainLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentThread, setCurrentThread] = useState(null);
  const [input, setInput] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);
  const { addMessage, threads } = useChatStore();

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Criar thread se não existir
    if (!currentThread) {
      setCurrentThread({ id: Date.now(), title: input.substring(0, 50) });
    }

    // Adicionar mensagem do usuário
    addMessage(currentThread?.id, {
      role: 'user',
      content: input,
      sources: [],
    });

    // TODO: Chamar backend agent
    setInput('');
    setSelectedFile(null);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <ThreadSidebar open={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

      {/* Main area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-gray-100 rounded-lg"
          >
            <Menu size={20} />
          </button>
          <h1 className="text-2xl font-bold text-red-600">Juridiques</h1>
          <button className="p-2 hover:bg-gray-100 rounded-lg">
            <Settings size={20} />
          </button>
        </div>

        {/* Chat area */}
        {currentThread ? (
          <ChatPanel thread={currentThread} />
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-gray-800 mb-2">Juridiques</h2>
              <p className="text-gray-500">Selecione uma thread ou comece uma nova</p>
            </div>
          </div>
        )}

        {/* Input area */}
        <div className="bg-white border-t border-gray-200 p-4">
          <form onSubmit={handleSendMessage} className="space-y-3">
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <Upload size={20} />
              </button>
              <input
                ref={fileInputRef}
                type="file"
                multiple
                className="hidden"
                onChange={(e) => setSelectedFile(e.target.files?.[0])}
              />
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Descreva seu caso ou consulta jurídica..."
                className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
              />
              <button
                type="submit"
                className="bg-red-600 text-white p-3 rounded-lg hover:bg-red-700"
              >
                <Send size={20} />
              </button>
            </div>
            {selectedFile && (
              <div className="text-sm text-gray-600">
                📎 {selectedFile.name}
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}
