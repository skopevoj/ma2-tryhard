'use client';

import { useState, useRef, useEffect } from 'react';

interface CategorySelectorProps {
    categories: string[];
    selectedCategories: string[];
    onToggleCategory: (category: string) => void;
}

export default function CategorySelector({
    categories,
    selectedCategories,
    onToggleCategory,
}: CategorySelectorProps) {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const displayText = selectedCategories.length === 0
        ? 'Vyberte kategorie...'
        : selectedCategories.length === categories.length
            ? 'Všechny kategorie'
            : `${selectedCategories.length} ${selectedCategories.length === 1 ? 'kategorie' : 'kategorií'}`;

    return (
        <div className="relative flex-1 max-w-md" ref={dropdownRef}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full px-4 py-2 rounded-lg text-sm font-medium text-left
                         bg-zinc-800/50 hover:bg-zinc-700/50
                         border border-zinc-700/50 hover:border-purple-500/30
                         text-zinc-300 transition-all flex items-center justify-between gap-2"
            >
                <span className="truncate">{displayText}</span>
                <svg
                    className={`w-4 h-4 text-zinc-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
            </button>

            {isOpen && (
                <div className="absolute top-full left-0 right-0 mt-2 rounded-xl overflow-hidden
                               bg-zinc-900/95 backdrop-filter backdrop-blur-xl
                               border border-purple-500/20 shadow-2xl shadow-purple-500/10 z-[9999]
                               max-h-80 overflow-y-auto">
                    <div className="p-2">
                        {categories.map((category) => (
                            <label
                                key={category}
                                className="flex items-center gap-3 px-3 py-2.5 rounded-lg cursor-pointer
                                         hover:bg-zinc-800/50 transition-all group"
                                onClick={(e) => {
                                    e.preventDefault();
                                    onToggleCategory(category);
                                }}
                            >
                                <div className="relative flex items-center justify-center">
                                    <input
                                        type="checkbox"
                                        checked={selectedCategories.includes(category)}
                                        onChange={() => { }}
                                        className="sr-only"
                                    />
                                    <div className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-all
                                                   ${selectedCategories.includes(category)
                                            ? 'bg-purple-500 border-purple-500 shadow-lg shadow-purple-500/30'
                                            : 'border-zinc-600 group-hover:border-purple-500/50'
                                        }`}>
                                        {selectedCategories.includes(category) && (
                                            <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                            </svg>
                                        )}
                                    </div>
                                </div>
                                <span className="flex-1 text-sm text-zinc-200 group-hover:text-zinc-100">
                                    {category}
                                </span>
                            </label>
                        ))}
                    </div>

                    {categories.length > 0 && (
                        <div className="border-t border-zinc-800 p-2 flex gap-2">
                            <button
                                onClick={() => {
                                    categories.forEach(cat => {
                                        if (!selectedCategories.includes(cat)) {
                                            onToggleCategory(cat);
                                        }
                                    });
                                }}
                                className="flex-1 px-3 py-2 text-xs font-medium rounded-lg
                                         bg-zinc-800/50 hover:bg-purple-500/20 text-zinc-300 hover:text-purple-300
                                         border border-zinc-700/50 hover:border-purple-500/30 transition-all"
                            >
                                Vybrat vše
                            </button>
                            <button
                                onClick={() => {
                                    selectedCategories.forEach(cat => onToggleCategory(cat));
                                }}
                                className="flex-1 px-3 py-2 text-xs font-medium rounded-lg
                                         bg-zinc-800/50 hover:bg-red-500/20 text-zinc-300 hover:text-red-300
                                         border border-zinc-700/50 hover:border-red-500/30 transition-all"
                            >
                                Zrušit vše
                            </button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
