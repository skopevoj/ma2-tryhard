'use client';

interface CategorySelectorProps {
    categories: string[];
    selectedCategories: string[];
    onToggleCategory: (category: string) => void;
    compact?: boolean;
}

export default function CategorySelector({
    categories,
    selectedCategories,
    onToggleCategory,
    compact = false,
}: CategorySelectorProps) {
    if (compact) {
        return (
            <div className="flex flex-wrap gap-2">
                {categories.map((category) => (
                    <button
                        key={category}
                        onClick={() => onToggleCategory(category)}
                        className={`px-3 py-1.5 rounded-md text-sm transition-all ${selectedCategories.includes(category)
                                ? 'bg-purple-600 text-white'
                                : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700'
                            }`}
                    >
                        {category}
                    </button>
                ))}
            </div>
        );
    }

    return (
        <div className="w-full max-w-4xl mx-auto space-y-6">
            <div className="bg-[#1a1a2e] rounded-lg p-6">
                <h2 className="text-2xl font-bold mb-6 text-zinc-100">
                    Vyberte kategorie
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {categories.map((category) => (
                        <div
                            key={category}
                            onClick={() => onToggleCategory(category)}
                            className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${selectedCategories.includes(category)
                                    ? 'border-purple-500 bg-purple-500/10'
                                    : 'border-zinc-700 bg-zinc-800/50 hover:border-zinc-600'
                                }`}
                        >
                            <div className="flex items-center gap-3">
                                <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${selectedCategories.includes(category)
                                        ? 'border-purple-500 bg-purple-500'
                                        : 'border-zinc-600'
                                    }`}>
                                    {selectedCategories.includes(category) && (
                                        <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                        </svg>
                                    )}
                                </div>
                                <span className="text-zinc-200">{category}</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
