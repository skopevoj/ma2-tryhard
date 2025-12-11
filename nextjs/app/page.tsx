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
    <div className="min-h-screen bg-gradient-to-br from-[#0a0a0f] via-[#0f0f1a] to-[#13131f] flex flex-col items-center py-8 px-4 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-1/4 -left-20 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

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
    </div>
  );
}
