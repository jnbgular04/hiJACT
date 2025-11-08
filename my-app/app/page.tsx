import { ChatInterface } from "@/components/chat-interface"

export default function Home() {
  return (
    <main className="h-screen w-full bg-gradient-to-br from-orange-50 to-amber-50 dark:from-slate-950 dark:to-slate-900">
      <ChatInterface />
    </main>
  )
}
