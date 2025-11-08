"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { FileUploader } from "./file-uploader"
import { ChatMessage } from "./chat-message"
import { Send, Plus, Zap } from "lucide-react"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  attachments?: Array<{
    id: string
    name: string
    type: string
    url: string
  }>
  timestamp: Date
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content:
        "Hi! I'm your AI bill assistant. Upload receipts, invoices, or bill documents and I'll instantly extract key details, calculate totals, and help you track expenses.",
      timestamp: new Date(Date.now() - 60000),
    },
  ])
  const [input, setInput] = useState("")
  const [attachments, setAttachments] = useState<Array<{ id: string; name: string; type: string; url: string }>>([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleAttachments = (files: Array<{ id: string; name: string; type: string; url: string }>) => {
    setAttachments((prev) => [...prev, ...files])
  }

  const removeAttachment = (id: string) => {
    setAttachments((prev) => prev.filter((att) => att.id !== id))
  }

  const handleSend = async () => {
    if (!input.trim() && attachments.length === 0) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      attachments: attachments.length > 0 ? attachments : undefined,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setAttachments([])
    setIsLoading(true)

    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          attachments.length > 0
            ? `Got it! I've processed ${attachments.length} document(s). Analyzing bill details including vendor, amount, and dates. Here's what I found: Amount due: $156.99 | Vendor: Acme Corp | Due date: March 15, 2025`
            : "I'm here to help! You can ask me about bill details, request expense summaries, or upload new documents.",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
      setIsLoading(false)
    }, 1200)
  }

  return (
    <div className="flex h-full flex-col bg-gradient-to-br from-orange-50 via-white to-orange-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
      <div className="border-b border-orange-100 dark:border-slate-800 bg-gradient-to-r from-orange-500 to-orange-600 dark:from-orange-600 dark:to-orange-700 px-6 py-5 text-white shadow-md">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-lg bg-white/20 backdrop-blur-sm flex items-center justify-center">
                <Zap className="h-6 w-6" />
              </div>
              <h1 className="text-2xl font-bold tracking-tight">Bill Assistant</h1>
            </div>
            <p className="text-orange-100 text-sm">AI-powered bill analysis & expense tracking</p>
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="text-white hover:bg-white/20 hover:text-white rounded-lg transition-all"
          >
            <Plus className="h-5 w-5" />
          </Button>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto space-y-4 p-6">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} isUser={message.role === "user"} />
        ))}
        {isLoading && (
          <div className="flex gap-3 items-start">
            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-orange-400 to-orange-500 flex items-center justify-center flex-shrink-0 shadow-md">
              <div className="w-5 h-5 rounded-full border-2 border-white/30 border-t-white animate-spin" />
            </div>
            <div className="text-sm text-slate-600 dark:text-slate-300 font-medium mt-2.5">Analyzing your bill...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t border-orange-100 dark:border-slate-800 bg-gradient-to-b from-white to-orange-50 dark:from-slate-900 dark:to-slate-950 p-6">
        <Card className="border border-orange-100 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-lg backdrop-blur-sm">
          {/* Attachments Preview */}
          {attachments.length > 0 && (
            <div className="border-b border-orange-100 dark:border-slate-800 p-4">
              <p className="text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide mb-3">
                Attached Files ({attachments.length})
              </p>
              <div className="flex gap-2 flex-wrap">
                {attachments.map((attachment) => (
                  <div
                    key={attachment.id}
                    className="bg-gradient-to-r from-orange-50 to-orange-100 dark:from-slate-800 dark:to-slate-700 border border-orange-200 dark:border-slate-700 rounded-lg px-3 py-2 flex items-center gap-2 text-sm group hover:shadow-sm transition-all"
                  >
                    <span className="text-orange-700 dark:text-orange-300 font-medium truncate max-w-[150px]">
                      {attachment.name}
                    </span>
                    <button
                      onClick={() => removeAttachment(attachment.id)}
                      className="text-orange-400 hover:text-orange-600 dark:text-orange-500 dark:hover:text-orange-400 ml-1 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Input and File Upload */}
          <div className="flex gap-3 p-4">
            <FileUploader onFilesSelect={handleAttachments} />
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault()
                  handleSend()
                }
              }}
              placeholder="Ask about bills, request a summary, or describe what you need..."
              className="flex-1 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-4 py-3 text-sm placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-200 dark:focus:ring-orange-900/40 transition-all font-medium"
            />
            <Button
              onClick={handleSend}
              disabled={isLoading || (!input.trim() && attachments.length === 0)}
              className="bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white rounded-lg px-4 py-3 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </Card>
      </div>
    </div>
  )
}
