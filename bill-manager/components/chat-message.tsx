"use client"

import { Card } from "@/components/ui/card"
import { ImageIcon, FileText } from "lucide-react"

interface ChatMessageProps {
  message: {
    content: string
    attachments?: Array<{
      id: string
      name: string
      type: string
      url: string
    }>
    timestamp: Date
  }
  isUser: boolean
}

export function ChatMessage({ message, isUser }: ChatMessageProps) {
  return (
    <div className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-orange-400 to-orange-500 flex items-center justify-center flex-shrink-0 shadow-md ring-1 ring-orange-300 dark:ring-orange-600">
          <span className="text-white text-sm font-bold">B</span>
        </div>
      )}

      <div className={`max-w-lg ${isUser ? "order-2" : "order-1"}`}>
        {/* Attachments */}
        {message.attachments && message.attachments.length > 0 && (
          <div className="mb-3 grid grid-cols-1 gap-2">
            {message.attachments.map((attachment) => (
              <Card
                key={attachment.id}
                className={`p-3 border-2 ${
                  isUser
                    ? "bg-gradient-to-r from-orange-100 to-orange-50 dark:from-slate-800 dark:to-slate-700 border-orange-200 dark:border-slate-700"
                    : "bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-700 border-slate-200 dark:border-slate-700"
                }`}
              >
                <div className="flex items-center gap-3">
                  {attachment.type.startsWith("image") ? (
                    <ImageIcon className="h-5 w-5 text-orange-600 dark:text-orange-400 flex-shrink-0" />
                  ) : (
                    <FileText className="h-5 w-5 text-orange-600 dark:text-orange-400 flex-shrink-0" />
                  )}
                  <div>
                    <p className="text-sm font-semibold text-slate-900 dark:text-white truncate">{attachment.name}</p>
                    <p className="text-xs text-slate-500 dark:text-slate-400">{attachment.type}</p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Message */}
        <Card
          className={`px-4 py-3 rounded-lg shadow-sm ${
            isUser
              ? "bg-gradient-to-r from-orange-500 to-orange-600 text-white shadow-md"
              : "bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-700"
          }`}
        >
          <p className="text-sm leading-relaxed font-medium">{message.content}</p>
        </Card>

        {/* Timestamp */}
        <p
          className={`text-xs mt-2 ${isUser ? "text-right text-slate-500 dark:text-slate-400" : "text-left text-slate-500 dark:text-slate-400"}`}
        >
          {message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </p>
      </div>

      {isUser && (
        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-slate-300 to-slate-400 dark:from-slate-700 dark:to-slate-600 flex items-center justify-center flex-shrink-0 shadow-md ring-1 ring-slate-300 dark:ring-slate-600 order-1">
          <span className="text-slate-700 dark:text-slate-300 text-sm font-bold">U</span>
        </div>
      )}
    </div>
  )
}
