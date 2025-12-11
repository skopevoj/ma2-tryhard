'use client';

import { useState, useEffect } from 'react';
import CategorySelector from '@/components/CategorySelector';
import QuizQuestion from '@/components/QuizQuestion';
import { Question } from '@/lib/types';

export default function Home() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [filteredQuestions, setFilteredQuestions] = useState<Question[]>([]);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [score, setScore] = useState({ correct: 0, incorrect: 0 });
  const [showCategorySelector, setShowCategorySelector] = useState(false);
  const [showImage, setShowImage] = useState(false);
  const [showAboutModal, setShowAboutModal] = useState(false);

  useEffect(() => {
    fetch('/questions.json')
      .then((res) => res.json())
      .then((data: Question[]) => {
        setQuestions(data);
        const uniqueCategories = Array.from(new Set(data.map((q) => q.category)));
        setCategories(uniqueCategories.sort());
      });
  }, []);

  useEffect(() => {
    if (selectedCategories.length > 0) {
      const filtered = questions.filter((q) =>
        selectedCategories.includes(q.category)
      );
      setFilteredQuestions(filtered);
      if (currentQuestionIndex >= filtered.length) {
        setCurrentQuestionIndex(Math.max(0, filtered.length - 1));
      }
    } else {
      setFilteredQuestions([]);
      setCurrentQuestionIndex(0);
    }
  }, [selectedCategories, questions, currentQuestionIndex]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (showAboutModal) return; // Don't navigate when modal is open

      if (e.key === 'ArrowLeft') {
        handlePrevious();
      } else if (e.key === 'ArrowRight') {
        handleNext();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentQuestionIndex, filteredQuestions.length, showAboutModal]);

  const toggleCategory = (category: string) => {
    setSelectedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((c) => c !== category)
        : [...prev, category]
    );
    setIsSubmitted(false);
  };

  const handleSubmit = (selectedAnswers: boolean[], isCorrect: boolean) => {
    setIsSubmitted(true);
    setScore((prev) => ({
      ...prev,
      correct: prev.correct + (isCorrect ? 1 : 0),
      incorrect: prev.incorrect + (isCorrect ? 0 : 1),
    }));
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
      setIsSubmitted(false);
      setShowImage(false);
    }
  };

  const handleNext = () => {
    if (currentQuestionIndex < filteredQuestions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
      setIsSubmitted(false);
      setShowImage(false);
    }
  };

  const currentQuestion = filteredQuestions[currentQuestionIndex];

  return (
    <div className="min-h-screen bg-[#0a0a0f] flex flex-col items-center py-8 px-4 relative">

      {/* Header - Category Selector Island */}
      <div className="w-full max-w-4xl mb-6 relative z-[100]">
        <div className="glass-card p-4 rounded-3xl bg-[rgba(20,20,30,0.6)] backdrop-blur-xl border border-purple-500/10 shadow-[0_8px_32px_rgba(0,0,0,0.4),0_0_0_1px_rgba(139,92,246,0.05)_inset]">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-3 flex-1">
              <span className="text-lg font-bold text-purple-400 tracking-wider">MARNOST</span>
              <div className="h-6 w-px bg-zinc-700" />
              <CategorySelector
                categories={categories}
                selectedCategories={selectedCategories}
                onToggleCategory={toggleCategory}
              />
            </div>

            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-green-500/10 border border-green-500/20">
                <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-green-400 font-semibold text-sm">{score.correct}</span>
              </div>
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-red-500/10 border border-red-500/20">
                <svg className="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span className="text-red-400 font-semibold text-sm">{score.incorrect}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content - Question and Controls */}
      <div className="flex-1 flex items-center justify-center w-full max-w-4xl relative z-[1]">
        {filteredQuestions.length > 0 ? (
          <div className="w-full space-y-4">
            {/* Question Island */}
            <div className="rounded-3xl bg-[rgba(20,20,30,0.6)] backdrop-blur-xl border border-purple-500/10 shadow-[0_8px_32px_rgba(0,0,0,0.4),0_0_0_1px_rgba(139,92,246,0.05)_inset] p-8">
              <QuizQuestion
                question={currentQuestion}
                onSubmit={handleSubmit}
                isSubmitted={isSubmitted}
                showImage={showImage}
              />
            </div>

            {/* Controls Island */}
            <div className="rounded-3xl bg-[rgba(20,20,30,0.6)] backdrop-blur-xl border border-purple-500/10 shadow-[0_8px_32px_rgba(0,0,0,0.4),0_0_0_1px_rgba(139,92,246,0.05)_inset] p-4">
              <div className="flex items-center justify-between gap-4">
                {/* Left side - Category and ID */}
                <div className="flex items-center gap-3">
                  <span className="px-3 py-1.5 bg-purple-500/20 text-purple-300 text-xs font-semibold rounded-lg border border-purple-500/30">
                    {currentQuestion.category}
                  </span>
                  <span className="text-xs text-zinc-500">
                    ID: {currentQuestion.quiz_id}
                  </span>
                  {currentQuestion.image_src && (
                    <button
                      onClick={() => setShowImage(!showImage)}
                      className="px-3 py-1.5 text-xs font-medium rounded-lg transition-all
                               bg-zinc-800/50 hover:bg-zinc-700/50 text-zinc-400 hover:text-zinc-200
                               border border-zinc-700/50 hover:border-zinc-600/50"
                    >
                      {showImage ? '🖼️ Skrýt obrázek' : '🖼️ Zobrazit obrázek'}
                    </button>
                  )}
                </div>

                {/* Center - Navigation */}
                <div className="flex items-center gap-3">
                  <button
                    onClick={handlePrevious}
                    disabled={currentQuestionIndex === 0}
                    className="p-2 rounded-xl bg-[rgba(30,30,45,0.6)] backdrop-blur-[10px] border border-purple-500/20 text-purple-300 transition-all hover:bg-purple-500/20 hover:border-purple-500/40 hover:-translate-y-0.5 hover:shadow-[0_4px_16px_rgba(139,92,246,0.3)] disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:bg-[rgba(30,30,45,0.6)]"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                  </button>

                  <span className="text-sm text-zinc-400 font-medium min-w-[60px] text-center">
                    {currentQuestionIndex + 1} / {filteredQuestions.length}
                  </span>

                  <button
                    onClick={handleNext}
                    disabled={currentQuestionIndex === filteredQuestions.length - 1}
                    className="p-2 rounded-xl bg-[rgba(30,30,45,0.6)] backdrop-blur-[10px] border border-purple-500/20 text-purple-300 transition-all hover:bg-purple-500/20 hover:border-purple-500/40 hover:-translate-y-0.5 hover:shadow-[0_4px_16px_rgba(139,92,246,0.3)] disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:bg-[rgba(30,30,45,0.6)]"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>

                {/* Right side - Evaluate button */}
                <button
                  onClick={() => {
                    const selectedAnswers = new Array(currentQuestion.answers.length).fill(false);
                    const isCorrect = selectedAnswers.every(
                      (selected, idx) => selected === currentQuestion.answers[idx].correct
                    );
                    handleSubmit(selectedAnswers, isCorrect);
                  }}
                  disabled={isSubmitted}
                  className="px-6 py-2.5 rounded-lg font-semibold text-sm transition-all
                           bg-gradient-to-r from-purple-600 to-purple-500
                           hover:from-purple-500 hover:to-purple-400
                           text-white shadow-lg shadow-purple-500/25
                           disabled:opacity-50 disabled:cursor-not-allowed
                           border border-purple-400/20"
                >
                  Vyhodnotit
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="w-full rounded-3xl bg-[rgba(20,20,30,0.6)] backdrop-blur-xl border border-purple-500/10 shadow-[0_8px_32px_rgba(0,0,0,0.4),0_0_0_1px_rgba(139,92,246,0.05)_inset] p-12">
            <div className="text-center">
              <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-purple-500/10 border border-purple-500/20 flex items-center justify-center">
                <svg className="w-10 h-10 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <p className="text-xl text-zinc-400 mb-2">Žádné otázky k zobrazení</p>
              <p className="text-sm text-zinc-500">Vyberte kategorie z rozbalovací nabídky výše</p>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="w-full max-w-4xl mt-8 relative z-10">
        <div className="flex items-center justify-center gap-6 text-sm text-zinc-500">
          <a
            href="https://github.com/skopevoj/ma2-tryhard"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-purple-400 transition-colors flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
            </svg>
            GitHub
          </a>
          <span className="text-zinc-700">•</span>
          <span className="text-zinc-600">Discord: @darkkw</span>
          <span className="text-zinc-700">•</span>
          <button
            onClick={() => setShowAboutModal(true)}
            className="hover:text-purple-400 transition-colors"
          >
            O projektu
          </button>
        </div>
      </footer>

      {/* About Modal */}
      {showAboutModal && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[200] p-4"
          onClick={() => setShowAboutModal(false)}
        >
          <div
            className="bg-[rgba(20,20,30,0.95)] backdrop-blur-xl border border-purple-500/20 rounded-2xl p-8 max-w-3xl max-h-[80vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-purple-400">MA2 Tryhard</h2>
              <button
                onClick={() => setShowAboutModal(false)}
                className="text-zinc-400 hover:text-white transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="prose prose-invert prose-purple max-w-none">
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-purple-300 mb-3">Disclaimer</h3>
                <p className="text-zinc-300">
                  Celý repo je kromě otázek 100% vibe coded (Kuznetsov Approved) ✨
                </p>
              </div>

              <div className="mb-6">
                <h3 className="text-xl font-semibold text-purple-300 mb-3">Zdroje otázek</h3>
                <p className="text-zinc-300 mb-3">Otázky jsou převzaty z FIT Wiki:</p>
                <ul className="text-sm text-zinc-400 space-y-1">
                  <li><a href="https://fit-wiki.cz/_media/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/bi-ma2_marast_2022_1.pdf" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 - Marast 2022/1</a></li>
                  <li><a href="https://fit-wiki.cz/_media/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/bi-ma2_marast_2022_2.pdf" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 - Marast 2022/2</a></li>
                  <li><a href="https://fit-wiki.cz/_media/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/bi-ma2_marast_2022_3.pdf" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 - Marast 2022/3</a></li>
                  <li><a href="https://fit-wiki.cz/_media/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/bi-ma2_marast_2022_4.pdf" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 - Marast 2022/4</a></li>
                  <li><a href="https://fit-wiki.cz/_media/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/bi-ma2_marast_2022_5.pdf" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 - Marast 2022/5</a></li>
                  <li><a href="https://fit-wiki.cz/_media/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/bi-ma2_marast_2022_6.pdf" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 - Marast 2022/6</a></li>
                  <li><a href="https://www.figma.com/board/UTTlv8hCsMoNdnTcoCiVgN/ma2?node-id=0-1&p=f" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 Figma Board</a></li>
                  <li><a href="https://fit-wiki.cz/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/ma2_rozstrel_2025-01-22" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 Rozstřel 2025-01-22</a></li>
                  <li><a href="https://fit-wiki.cz/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/ma2_rozstrel_2025-01-29" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 Rozstřel 2025-01-29</a></li>
                  <li><a href="https://fit-wiki.cz/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/ma2_rozstrel_2024-01-25" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 Rozstřel 2024-01-25</a></li>
                  <li><a href="https://fit-wiki.cz/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/ma2_rozstrel_2024-2-1" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 Rozstřel 2024-02-01</a></li>
                  <li><a href="https://fit-wiki.cz/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/ma2_rozstrel_2024-2-8" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 Rozstřel 2024-02-08</a></li>
                  <li><a href="https://fit-wiki.cz/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/ma2_rozstrel_2023-01-04" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 Rozstřel 2023-01-04</a></li>
                  <li><a href="https://fit-wiki.cz/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/ma2_rozstrel_2023-01-25" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 Rozstřel 2023-01-25</a></li>
                  <li><a href="https://fit-wiki.cz/%C5%A1kola/p%C5%99edm%C4%9Bty/bi-ma2.21/ma2_rozstrel_2023-02-01" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300">MA2 Rozstřel 2023-02-01</a></li>
                </ul>
              </div>

              <div className="mb-6">
                <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
                  <p className="text-yellow-200 text-sm">
                    ⚠️ <strong>Upozornění:</strong> Je možné, že se v otázkách vyskytuje chyba přepisu. Pokud nějakou najdete, vytvořte prosím{' '}
                    <a href="https://github.com/skopevoj/ma2-tryhard/issues" target="_blank" rel="noopener noreferrer" className="text-yellow-300 hover:text-yellow-200 underline">issue</a>.
                  </p>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-purple-300 mb-3">Pipeline</h3>
                <ol className="text-zinc-300 space-y-2 list-decimal list-inside">
                  <li><strong>Scraping</strong> - Stažení otázek z FIT Wiki</li>
                  <li><strong>Konverze</strong> - Gemini API převádí screenshoty na JSON formát</li>
                  <li><strong>Build</strong> - Script generuje statický HTML web</li>
                </ol>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
