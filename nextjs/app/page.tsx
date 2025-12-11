'use client';

import { useState, useEffect } from 'react';
import CategorySelector from '@/components/CategorySelector';
import QuizQuestion from '@/components/QuizQuestion';
import LatexRenderer from '@/components/LatexRenderer';
import { Question } from '@/lib/types';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

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
  const [showStatsModal, setShowStatsModal] = useState(false);
  const [questionStats, setQuestionStats] = useState<Record<string, {
    correct: number;
    incorrect: number;
    answerStats?: Record<number, { selected: number; correct: boolean }>;
  }>>({});
  const [statsEnabled, setStatsEnabled] = useState(true);
  const [expandedQuestions, setExpandedQuestions] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetch('/questions.json')
      .then((res) => res.json())
      .then((data: Question[]) => {
        setQuestions(data);
        const uniqueCategories = Array.from(new Set(data.map((q) => q.category)));
        setCategories(uniqueCategories.sort());
      });

    // Load stats from localStorage
    const savedStats = localStorage.getItem('questionStats');
    if (savedStats) {
      setQuestionStats(JSON.parse(savedStats));
    }

    // Load stats enabled setting
    const statsEnabledSetting = localStorage.getItem('statsEnabled');
    if (statsEnabledSetting !== null) {
      setStatsEnabled(statsEnabledSetting === 'true');
    }
  }, []); useEffect(() => {
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
      if (showAboutModal || showStatsModal) return; // Don't navigate when modal is open

      if (e.key === 'ArrowLeft') {
        handlePrevious();
      } else if (e.key === 'ArrowRight') {
        handleNext();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentQuestionIndex, filteredQuestions.length, showAboutModal, showStatsModal]);

  const toggleCategory = (category: string) => {
    setSelectedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((c) => c !== category)
        : [...prev, category]
    );
    setIsSubmitted(false);
  };

  const handleSubmit = (selectedAnswers: (boolean | null)[], isCorrect: boolean) => {
    setIsSubmitted(true);
    setScore((prev) => ({
      ...prev,
      correct: prev.correct + (isCorrect ? 1 : 0),
      incorrect: prev.incorrect + (isCorrect ? 0 : 1),
    }));

    // Save stats to localStorage only if enabled
    if (statsEnabled) {
      const quizId = currentQuestion.quiz_id;
      const newStats = { ...questionStats };
      if (!newStats[quizId]) {
        newStats[quizId] = { correct: 0, incorrect: 0, answerStats: {} };
      }
      if (isCorrect) {
        newStats[quizId].correct++;
      } else {
        newStats[quizId].incorrect++;
      }

      // Track per-answer statistics
      if (!newStats[quizId].answerStats) {
        newStats[quizId].answerStats = {};
      }
      selectedAnswers.forEach((selected, idx) => {
        if (selected === true) {
          const answerCorrect = currentQuestion.answers[idx].correct;
          if (!newStats[quizId].answerStats![idx]) {
            newStats[quizId].answerStats![idx] = { selected: 0, correct: answerCorrect };
          }
          newStats[quizId].answerStats![idx].selected++;
        }
      });

      setQuestionStats(newStats);
      localStorage.setItem('questionStats', JSON.stringify(newStats));
    }
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

  const jumpToQuestion = (quizId: string) => {
    const index = filteredQuestions.findIndex(q => q.quiz_id === quizId);
    if (index !== -1) {
      setCurrentQuestionIndex(index);
      setIsSubmitted(false);
      setShowImage(false);
      setShowStatsModal(false);
    }
  };

  const resetStats = () => {
    if (confirm('Opravdu chcete resetovat všechny statistiky?')) {
      setQuestionStats({});
      localStorage.removeItem('questionStats');
    }
  };

  const toggleStatsEnabled = (enabled: boolean) => {
    setStatsEnabled(enabled);
    localStorage.setItem('statsEnabled', enabled.toString());
    if (!enabled) {
      setQuestionStats({});
      localStorage.removeItem('questionStats');
    }
  };

  const toggleQuestionExpanded = (quizId: string) => {
    const newExpanded = new Set(expandedQuestions);
    if (newExpanded.has(quizId)) {
      newExpanded.delete(quizId);
    } else {
      newExpanded.add(quizId);
    }
    setExpandedQuestions(newExpanded);
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
              <button
                onClick={() => setShowStatsModal(true)}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-purple-500/10 border border-purple-500/20 hover:bg-purple-500/20 transition-colors"
              >
                <svg className="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span className="text-purple-400 font-semibold text-sm">Statistiky</span>
              </button>
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

                {/* Right side - Empty space for balance */}
                <div className="w-[120px]"></div>
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

      {/* Statistics Modal */}
      {showStatsModal && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[200] p-4"
          onClick={() => setShowStatsModal(false)}
        >
          <div
            className="bg-[rgba(20,20,30,0.95)] backdrop-blur-xl border border-purple-500/20 rounded-2xl p-8 max-w-4xl max-h-[80vh] overflow-y-auto w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-purple-400">Statistiky</h2>
              <button
                onClick={() => setShowStatsModal(false)}
                className="text-zinc-400 hover:text-white transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Disclaimer and Settings */}
            <div className="mb-6 space-y-3">
              <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
                <p className="text-blue-200 text-sm">
                  ℹ️ <strong>Upozornění:</strong> Statistiky jsou uloženy pouze lokálně ve vašem prohlížeči. Pokud smažete data prohlížeče, statistiky budou ztraceny.
                </p>
              </div>

              <div className="flex items-center justify-between gap-4 bg-zinc-800/30 border border-zinc-700/50 rounded-lg p-4">
                <div className="flex-1">
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={statsEnabled}
                      onChange={(e) => toggleStatsEnabled(e.target.checked)}
                      className="w-5 h-5 rounded border-2 border-purple-500 bg-zinc-900 checked:bg-purple-500 checked:border-purple-500 transition-colors"
                    />
                    <div>
                      <span className="text-zinc-200 font-medium">Povolit statistiky</span>
                      <p className="text-xs text-zinc-500">Ukládání odpovědí pro analýzu pokroku</p>
                    </div>
                  </label>
                </div>
                <button
                  onClick={resetStats}
                  disabled={Object.keys(questionStats).length === 0}
                  className="px-4 py-2 text-sm font-medium rounded-lg transition-all
                           bg-red-500/10 hover:bg-red-500/20 text-red-400 hover:text-red-300
                           border border-red-500/30 hover:border-red-500/50
                           disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Resetovat statistiky
                </button>
              </div>
            </div>

            {Object.keys(questionStats).length === 0 ? (
              <div className="text-center py-12">
                <p className="text-zinc-400 text-lg">Zatím nejsou žádné statistiky</p>
                <p className="text-zinc-500 text-sm mt-2">Začněte odpovídat na otázky</p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Questions Table */}
                <div>
                  <h3 className="text-xl font-semibold text-purple-300 mb-4">Všechny otázky</h3>
                  <div className="border border-zinc-700/30 rounded-xl overflow-hidden bg-zinc-900/30">
                    <Table>
                      <TableHeader>
                        <TableRow className="border-zinc-700/50 hover:bg-transparent">
                          <TableHead className="text-purple-300 font-semibold">Kategorie</TableHead>
                          <TableHead className="text-purple-300 font-semibold">Otázka</TableHead>
                          <TableHead className="text-purple-300 font-semibold text-center">Správně</TableHead>
                          <TableHead className="text-purple-300 font-semibold text-center">Špatně</TableHead>
                          <TableHead className="text-purple-300 font-semibold text-center">Úspěšnost</TableHead>
                          <TableHead className="text-purple-300 font-semibold text-center w-[60px]"></TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {(() => {
                          const questionsWithStats = questions
                            .map(q => {
                              const stats = questionStats[q.quiz_id];
                              if (!stats || (stats.correct + stats.incorrect === 0)) return null;

                              const total = stats.correct + stats.incorrect;
                              const successRate = (stats.correct / total) * 100;

                              return {
                                question: q,
                                stats,
                                successRate,
                                total
                              };
                            })
                            .filter(Boolean)
                            .sort((a, b) => {
                              if (!a || !b) return 0;
                              return a.successRate - b.successRate;
                            });

                          if (questionsWithStats.length === 0) {
                            return (
                              <TableRow>
                                <TableCell colSpan={6} className="text-center py-8 text-zinc-500">
                                  Žádná data
                                </TableCell>
                              </TableRow>
                            );
                          }

                          return questionsWithStats.map((item) => {
                            if (!item) return null;
                            const { question, stats, successRate } = item;
                            const isExpanded = expandedQuestions.has(question.quiz_id);

                            return (
                              <>
                                <TableRow
                                  key={question.quiz_id}
                                  className="border-zinc-700/30 hover:bg-zinc-800/30 cursor-pointer transition-colors"
                                  onClick={() => toggleQuestionExpanded(question.quiz_id)}
                                >
                                  <TableCell>
                                    <span className="text-xs px-2 py-1 bg-purple-500/20 text-purple-300 rounded font-medium inline-block">
                                      {question.category}
                                    </span>
                                  </TableCell>
                                  <TableCell className="max-w-md">
                                    <div className="text-zinc-300 text-sm line-clamp-2">
                                      <LatexRenderer content={question.question} className="inline" />
                                    </div>
                                  </TableCell>
                                  <TableCell className="text-center">
                                    <span className="text-green-400 font-semibold">{stats.correct}</span>
                                  </TableCell>
                                  <TableCell className="text-center">
                                    <span className="text-red-400 font-semibold">{stats.incorrect}</span>
                                  </TableCell>
                                  <TableCell className="text-center">
                                    <div className="flex items-center justify-center gap-2">
                                      <span className={`font-semibold ${successRate >= 50 ? 'text-green-400' : 'text-red-400'}`}>
                                        {successRate.toFixed(0)}%
                                      </span>
                                      <div className="w-12 h-1.5 bg-zinc-700/50 rounded-full overflow-hidden">
                                        <div
                                          className={`h-full transition-all ${successRate >= 50 ? 'bg-green-500' : 'bg-red-500'}`}
                                          style={{ width: `${successRate}%` }}
                                        />
                                      </div>
                                    </div>
                                  </TableCell>
                                  <TableCell className="text-center">
                                    <button
                                      onClick={(e) => {
                                        e.stopPropagation();
                                        jumpToQuestion(question.quiz_id);
                                      }}
                                      className="p-1.5 rounded-lg bg-purple-500/10 hover:bg-purple-500/20 text-purple-400 transition-colors"
                                      title="Přejít na otázku"
                                    >
                                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                                      </svg>
                                    </button>
                                  </TableCell>
                                </TableRow>
                                {isExpanded && (
                                  <TableRow className="border-zinc-700/30 bg-zinc-900/50 hover:bg-zinc-900/50">
                                    <TableCell colSpan={6} className="p-0">
                                      <div className="p-6 space-y-4">
                                        {/* Full Question */}
                                        <div>
                                          <h4 className="text-sm font-semibold text-purple-300 mb-2">Zadání:</h4>
                                          <LatexRenderer
                                            content={question.question}
                                            className="text-zinc-200 leading-relaxed"
                                          />
                                        </div>

                                        {/* Answers with Stats */}
                                        <div>
                                          <h4 className="text-sm font-semibold text-purple-300 mb-3">Odpovědi a statistiky:</h4>
                                          <div className="border border-zinc-700/30 rounded-lg overflow-hidden bg-zinc-900/20">
                                            <Table>
                                              <TableHeader>
                                                <TableRow className="border-zinc-700/50 hover:bg-transparent">
                                                  <TableHead className="text-purple-300 font-semibold text-xs w-[40px]"></TableHead>
                                                  <TableHead className="text-purple-300 font-semibold text-xs">Odpověď</TableHead>
                                                  <TableHead className="text-purple-300 font-semibold text-xs text-center">Vybráno</TableHead>
                                                  <TableHead className="text-purple-300 font-semibold text-xs text-center">% výběru</TableHead>
                                                  <TableHead className="text-purple-300 font-semibold text-xs text-center">% správnosti</TableHead>
                                                </TableRow>
                                              </TableHeader>
                                              <TableBody>
                                                {question.answers.map((answer, idx) => {
                                                  const answerStat = stats.answerStats?.[idx];
                                                  const totalAttempts = stats.correct + stats.incorrect;
                                                  const selectionRate = answerStat ? (answerStat.selected / totalAttempts) * 100 : 0;

                                                  // Calculate correctness percentage for this specific answer
                                                  // For correct answers: how many times was it correctly selected
                                                  // For incorrect answers: how many times was it correctly NOT selected (or marked as No)
                                                  let correctnessRate = 0;
                                                  if (answer.correct) {
                                                    // Correct answer: percentage of times it was selected (Yes)
                                                    correctnessRate = answerStat ? selectionRate : 0;
                                                  } else {
                                                    // Incorrect answer: percentage of times it was NOT selected
                                                    // (100% - selection rate would be if we tracked "not selected", but we only track selections)
                                                    // So for incorrect answers, lower selection rate = higher correctness
                                                    correctnessRate = answerStat ? 100 - selectionRate : 100;
                                                  }

                                                  return (
                                                    <TableRow
                                                      key={idx}
                                                      className={`border-zinc-700/30 hover:bg-zinc-800/20 ${answer.correct ? 'bg-green-500/5' : ''
                                                        }`}
                                                    >
                                                      <TableCell className="text-center">
                                                        <span className={`text-lg font-semibold ${answer.correct ? 'text-green-400' : 'text-zinc-500'}`}>
                                                          {answer.correct ? '✓' : '○'}
                                                        </span>
                                                      </TableCell>
                                                      <TableCell>
                                                        <LatexRenderer
                                                          content={answer.text}
                                                          className="text-zinc-300 text-sm leading-relaxed"
                                                        />
                                                      </TableCell>
                                                      <TableCell className="text-center whitespace-nowrap">
                                                        <span className="text-zinc-300 font-semibold">
                                                          {answerStat ? `${answerStat.selected}×` : '0×'}
                                                        </span>
                                                      </TableCell>
                                                      <TableCell className="text-center whitespace-nowrap">
                                                        <div className="flex items-center justify-center gap-2">
                                                          <span className="text-purple-300 font-semibold text-sm">
                                                            {selectionRate.toFixed(0)}%
                                                          </span>
                                                          <div className="w-12 h-1.5 bg-zinc-700/50 rounded-full overflow-hidden">
                                                            <div
                                                              className="h-full bg-purple-500 transition-all"
                                                              style={{ width: `${selectionRate}%` }}
                                                            />
                                                          </div>
                                                        </div>
                                                      </TableCell>
                                                      <TableCell className="text-center whitespace-nowrap">
                                                        <div className="flex items-center justify-center gap-2">
                                                          <span className={`font-semibold text-sm ${correctnessRate >= 50 ? 'text-green-400' : 'text-red-400'
                                                            }`}>
                                                            {correctnessRate.toFixed(0)}%
                                                          </span>
                                                          <div className="w-12 h-1.5 bg-zinc-700/50 rounded-full overflow-hidden">
                                                            <div
                                                              className={`h-full transition-all ${correctnessRate >= 50 ? 'bg-green-500' : 'bg-red-500'
                                                                }`}
                                                              style={{ width: `${correctnessRate}%` }}
                                                            />
                                                          </div>
                                                        </div>
                                                      </TableCell>
                                                    </TableRow>
                                                  );
                                                })}
                                              </TableBody>
                                            </Table>
                                          </div>
                                        </div>
                                      </div>
                                    </TableCell>
                                  </TableRow>
                                )}
                              </>
                            );
                          });
                        })()}
                      </TableBody>
                    </Table>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}      {/* About Modal */}
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
