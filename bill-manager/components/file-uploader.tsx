"use client"

import type React from "react"

import { useRef } from "react"
import { Upload } from "lucide-react"
import { Button } from "@/components/ui/button"

interface FileUploaderProps {
  onFilesSelect: (files: Array<{ id: string; name: string; type: string; url: string }>) => void
}

export function FileUploader({ onFilesSelect }: FileUploaderProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (!files) return

    const uploadedFiles = Array.from(files).map((file) => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      type: file.type,
      url: URL.createObjectURL(file),
    }))

    onFilesSelect(uploadedFiles)

    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  return (
    <>
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept="image/*,.pdf"
        onChange={handleFileSelect}
        className="hidden"
        aria-label="Upload bill or receipt"
      />
      <Button
        type="button"
        onClick={() => fileInputRef.current?.click()}
        variant="outline"
        size="icon"
        className="border-orange-200 dark:border-slate-700 text-orange-600 dark:text-orange-400 hover:bg-orange-50 dark:hover:bg-slate-800 rounded-lg transition-all hover:border-orange-300 dark:hover:border-slate-600"
        title="Upload image or PDF"
      >
        <Upload className="h-4 w-4" />
      </Button>
    </>
  )
}
