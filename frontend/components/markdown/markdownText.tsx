import '@/styles/github-hljs.css';
import '@/styles/github-markdown.css';
import 'katex/dist/katex.min.css';
import Markdown from "react-markdown";
import rehypeHighlight from 'rehype-highlight';
import rehypeKatex from 'rehype-katex';
import rehypePrism from 'rehype-prism';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import Pre from './pre';


const icon = `<?xml version="1.0" encoding="UTF-8"?><svg width="24" height="24" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M26.2401 16.373L17.1001 7.23303C14.4388 4.57168 10.0653 4.6303 7.33158 7.36397C4.59791 10.0976 4.53929 14.4712 7.20064 17.1325L15.1359 25.0678" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M32.9027 23.0031L40.838 30.9384C43.4994 33.5998 43.4407 37.9733 40.7071 40.707C37.9734 43.4407 33.5999 43.4993 30.9385 40.8379L21.7985 31.6979" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M26.1093 26.1416C28.843 23.4079 28.9016 19.0344 26.2403 16.373" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M21.7989 21.7984C19.0652 24.5321 19.0066 28.9056 21.6679 31.5669" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>`



export function MarkdownText({ text }: { text: string }) {
  return (
    <div>
        <Markdown
            className="markdown"
            remarkPlugins={[
                remarkGfm,
                remarkMath
            ]}
            rehypePlugins={[
                rehypeKatex,
                rehypePrism,
                rehypeHighlight
            ]}
            components={{
                pre({ children, ...props }) {
                    return <Pre {...props}>{children}</Pre>
                }
            }}
        >
            {text}
        </Markdown>
    </div>
    );
}