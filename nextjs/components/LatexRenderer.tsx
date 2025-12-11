'use client';

import { useEffect, useRef } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

interface LatexRendererProps {
    content: string;
    className?: string;
}

export default function LatexRenderer({ content, className = '' }: LatexRendererProps) {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!containerRef.current) return;

        const processLatex = (text: string) => {
            // Replace display math $$ ... $$
            let processed = text.replace(/\$\$([\s\S]*?)\$\$/g, (_, math) => {
                try {
                    return katex.renderToString(math, { displayMode: true, throwOnError: false });
                } catch (e) {
                    return `$$${math}$$`;
                }
            });

            // Replace inline math $ ... $
            processed = processed.replace(/\$(.*?)\$/g, (_, math) => {
                try {
                    return katex.renderToString(math, { displayMode: false, throwOnError: false });
                } catch (e) {
                    return `$${math}$`;
                }
            });

            return processed;
        };

        containerRef.current.innerHTML = processLatex(content);
    }, [content]);

    return <div ref={containerRef} className={className} />;
}
