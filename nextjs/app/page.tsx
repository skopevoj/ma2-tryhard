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
  const [score, setScore] = useState({ correct: 0, incorrect: 0, skipped: 0 });
  const [showCategorySelector, setShowCategorySelector] = useState(false);

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
    // Filter questions based on selected categories
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
    }
  };

  const handleNext = () => {
    if (currentQuestionIndex < filteredQuestions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
      setIsSubmitted(false);
    }
  };

  const currentQuestion = filteredQuestions[currentQuestionIndex];

  return (
    <div className="min-h-screen bg-[#0f0f1a] flex flex-col">
      {/* Header with title, settings, and score */}
      <div className="w-full border-b border-zinc-800 py-4 px-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-2xl font-bold text-purple-400 tracking-wide">
              MARNOST
            </h1>
            <button
              onClick={() => setShowCategorySelector(!showCategorySelector)}
              className="p-2 hover:bg-zinc-800 rounded-lg transition-colors"
            >
              <svg className="w-5 h-5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>

          <div className="flex items-center gap-6 text-sm">
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              <span className="text-zinc-300">{score.correct}</span>
            </div>
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" />
              </svg>
              <span className="text-zinc-300">{score.incorrect}</span>
            </div>
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              <span className="text-zinc-300">{score.skipped}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Category selector dropdown */}
      {showCategorySelector && (
        <div className="w-full border-b border-zinc-800 bg-[#13131f] py-4 px-6">
          <div className="max-w-7xl mx-auto">
            <CategorySelector
              categories={categories}
              selectedCategories={selectedCategories}
              onToggleCategory={toggleCategory}
              compact={true}
            />
          </div>
        </div>
      )}

      {/* Main content - centered */}
      <div className="flex-1 flex items-center justify-center px-6 py-8">
        {filteredQuestions.length > 0 ? (
          <div className="w-full max-w-4xl">
            <QuizQuestion
              question={currentQuestion}
              onSubmit={handleSubmit}
              isSubmitted={isSubmitted}
            />
          </div>
        ) : (
          <div className="text-center text-zinc-500">
            <p className="text-xl mb-4">Vyberte kategorie pro zobrazení otázek</p>
            <button
              onClick={() => setShowCategorySelector(true)}
              className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
            >
              Vybrat kategorie
            </button>
          </div>
        )}
      </div>

      {/* Footer with navigation and info */}
      {filteredQuestions.length > 0 && (
        <div className="w-full border-t border-zinc-800 py-4 px-6">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span className="px-3 py-1 bg-purple-600 text-white text-sm rounded-full">
                {currentQuestion.category}
              </span>
              <span className="text-zinc-500 text-sm">
                ID: {currentQuestion.quiz_id}
              </span>
            </div>

            <div className="flex items-center gap-4">
              <button
                onClick={handlePrevious}
                disabled={currentQuestionIndex === 0}
                className="p-2 hover:bg-zinc-800 rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              >
                <svg className="w-5 h-5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>

              <span className="text-zinc-400 text-sm">
                {currentQuestionIndex + 1} / {filteredQuestions.length}
              </span>

              <button
                onClick={handleNext}
                disabled={currentQuestionIndex === filteredQuestions.length - 1}
                className="p-2 hover:bg-zinc-800 rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              >
                <svg className="w-5 h-5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            <button className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium">
              Vyhodnotit
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
