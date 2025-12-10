import React from 'react';
import { useChatStore } from '../store/chatStore';

interface ChatPanelProps {
  thread: any;
}

export default function ChatPanel({ thread }: ChatPanelProps) {
  const { messages } = useChatStore();
  const threadMessages = messages[thread.id] || [];

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {threadMessages.length === 0 ? (
        <div className="text-center text-gray-500">
          Nenhuma mensagem ainda. Comece descrevendo seu caso.
        </div>
      ) : (
        threadMessages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-2xl p-4 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-red-100 text-red-900'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <p className="text-sm">{msg.content}</p>
              {msg.sources && msg.sources.length > 0 && (
                <div className="mt-2 text-xs text-gray-600 border-t pt-2">
                  <p className="font-semibold">Fontes:</p>
                  {msg.sources.map((src, i) => (
                    <p key={i}>• {src}</p>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))
      )}
    </div>
  );
}
