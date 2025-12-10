import React from 'react';
import { MessageCircle, Plus, Archive, Share2 } from 'lucide-react';
import { useChatStore } from '../store/chatStore';

interface ThreadSidebarProps {
  open: boolean;
  onToggle: () => void;
}

export default function ThreadSidebar({ open, onToggle }: ThreadSidebarProps) {
  const { threads } = useChatStore();

  if (!open) return null;

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* User profile */}
      <div className="p-4 border-b border-gray-200">
        <div className="w-10 h-10 bg-red-200 rounded-full cursor-pointer flex items-center justify-center">
          <span className="text-red-600 font-bold">U</span>
        </div>
      </div>

      {/* Threads list */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        <h3 className="text-xs uppercase text-gray-500 font-bold mb-3">Threads</h3>
        {threads.map((thread) => (
          <div
            key={thread.id}
            className="p-3 hover:bg-gray-100 rounded-lg cursor-pointer group"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1 flex gap-2">
                <MessageCircle size={16} className="mt-1 flex-shrink-0" />
                <div className="min-w-0">
                  <p className="font-medium text-sm truncate">{thread.title}</p>
                  <p className="text-xs text-gray-500">CNJ: {thread.cnj || 'N/A'}</p>
                </div>
              </div>
              <div className="opacity-0 group-hover:opacity-100 flex gap-1">
                <button className="p-1 hover:bg-gray-200 rounded">
                  <Share2 size={14} />
                </button>
                <button className="p-1 hover:bg-gray-200 rounded">
                  <Archive size={14} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* New thread button */}
      <div className="p-4 border-t border-gray-200">
        <button className="w-full flex items-center gap-2 bg-red-600 text-white p-2 rounded-lg hover:bg-red-700">
          <Plus size={18} />
          <span>Nova thread</span>
        </button>
      </div>
    </div>
  );
}
