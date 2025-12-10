// Store de estado global (Zustand)

import { create } from 'zustand';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
}

interface Thread {
  id: number;
  title: string;
  cnj?: string;
}

interface ChatStore {
  threads: Thread[];
  messages: Record<number, Message[]>;
  addThread: (thread: Thread) => void;
  addMessage: (threadId: number, message: Message) => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  threads: [],
  messages: {},
  
  addThread: (thread) =>
    set((state) => ({
      threads: [...state.threads, thread],
    })),
  
  addMessage: (threadId, message) =>
    set((state) => ({
      messages: {
        ...state.messages,
        [threadId]: [...(state.messages[threadId] || []), message],
      },
    })),
}));
