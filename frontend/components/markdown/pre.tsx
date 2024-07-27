"use client";

import { Copy, DoneAll } from '@icon-park/react';
import { useTheme } from 'next-themes';
import { DetailedHTMLProps, HTMLAttributes, useRef, useState } from 'react';

const Pre: React.ComponentType<DetailedHTMLProps<HTMLAttributes<HTMLPreElement>, HTMLPreElement>> = ({ children, ...props }) => {
  const textInput = useRef<HTMLDivElement>(null)
  const [hovered, setHovered] = useState(false)
  const [copied, setCopied] = useState(false)
  const { theme, setTheme } = useTheme();

  const onEnter = () => {
    setHovered(true)
  }
  const onExit = () => {
    setHovered(false)
    setCopied(false)
  }
  const onCopy = () => {
    setCopied(true)
    navigator.clipboard.writeText(textInput.current?.textContent || '')
    setTimeout(() => {
      setCopied(false)
    }, 2000)
  }

  return (
    <div ref={textInput} onMouseEnter={onEnter} onMouseLeave={onExit} className="relative">
      {hovered && (
        <div
          className="absolute right-2 top-2 h-6 w-6 rounded border-2 bg-gray-200 p-1 dark:bg-gray-900 dark:border-gray-900 cursor-pointer flex items-center justify-center"
          onClick={onCopy}
        >
            {copied ? (<DoneAll theme="filled" size="24" fill="#10B981"/>) : (<Copy theme="outline" size="24" fill={theme=='light'? "#333": "#F9FAFB"}/>)}
        </div>
      )}

      <pre {...props}>{children}</pre>
    </div>
  )
}

export default Pre