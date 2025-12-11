'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import LatexRenderer from './LatexRenderer';
import { Question } from '@/lib/types';

interface QuizQuestionProps {
    question: Question;
    onSubmit: (selectedAnswers: (boolean | null)[], isCorrect: boolean) => void;
    onEvaluate: () => void;
    isSubmitted: boolean;
    showImage: boolean;
}

export default function QuizQuestion({ question, onSubmit, onEvaluate, isSubmitted, showImage }: QuizQuestionProps) {
    // Answer state: null = nevím, true = ano, false = ne
    const [selectedAnswers, setSelectedAnswers] = useState<(boolean | null)[]>(
        new Array(question.answers.length).fill(null)
    );

    // Reset answers and image state when question changes
    useEffect(() => {
        setSelectedAnswers(new Array(question.answers.length).fill(null));
    }, [question]);

    // Expose handleEvaluate to parent through onEvaluate callback
    useEffect(() => {
        const handleEvaluate = () => {
            const isCorrect = question.answers.every((answer, idx) => {
                const userAnswer = selectedAnswers[idx];
                if (answer.correct) {
                    return userAnswer === true;
                } else {
                    return userAnswer === false;
                }
            });
            onSubmit(selectedAnswers, isCorrect);
        };

        // Store the function reference so parent can call it
        (window as any).__quizEvaluate = handleEvaluate;
    }, [question, selectedAnswers, onSubmit]);

    const toggleAnswer = (index: number, newState: boolean | null) => {
        if (isSubmitted) return;
        const newSelected = [...selectedAnswers];
        newSelected[index] = newState;
        setSelectedAnswers(newSelected);
    };

    const getAnswerClassName = (index: number) => {
        const baseClass = 'p-4 rounded-xl transition-all border';

        if (!isSubmitted) {
            return `${baseClass} bg-zinc-800/30 border-zinc-700/50 hover:border-zinc-600/50 hover:bg-zinc-800/50`;
        }

        const isCorrect = question.answers[index].correct;
        const userAnswer = selectedAnswers[index];

        // Zelená pokud uživatel odpověděl správně (ano na správnou odpověď, ne na špatnou)
        if ((userAnswer === true && isCorrect) || (userAnswer === false && !isCorrect)) {
            return `${baseClass} bg-green-500/10 border-green-500/40 shadow-lg shadow-green-500/20`;
        }
        // Červená pokud uživatel odpověděl špatně (ano na špatnou, ne na správnou, nebo nevím)
        return `${baseClass} bg-red-500/10 border-red-500/40 shadow-lg shadow-red-500/20`;
    };

    return (
        <div className="w-full space-y-6">
            {/* Question text */}
            <div className="mb-8">
                <LatexRenderer
                    content={question.question}
                    className="text-lg text-zinc-100 leading-relaxed"
                />
            </div>

            {/* Image - conditionally rendered based on showImage prop */}
            {showImage && question.image_src && (
                <div className="mb-6 rounded-xl overflow-hidden border border-purple-500/20 shadow-2xl shadow-purple-500/10">
                    <div className="relative w-full h-96 bg-zinc-900/50">
                        <Image
                            src={`/${question.image_src}`}
                            alt="Question image"
                            fill
                            className="object-contain"
                        />
                    </div>
                </div>
            )}

            {/* Answers */}
            <div className="space-y-3">
                {question.answers.map((answer, index) => (
                    <div
                        key={index}
                        className={getAnswerClassName(index)}
                    >
                        <div className="flex items-start gap-3">
                            {/* User's answer toggle - always visible */}
                            <div className="flex items-center justify-center mt-1 flex-shrink-0">
                                <div className="flex items-center gap-0.5 bg-zinc-800/50 rounded-lg p-0.5 border border-zinc-700/50">
                                    <button
                                        onClick={() => toggleAnswer(index, true)}
                                        disabled={isSubmitted}
                                        className={`p-1.5 rounded transition-all ${selectedAnswers[index] === true
                                            ? 'bg-zinc-600 text-white'
                                            : 'text-zinc-500 hover:text-zinc-300'
                                            } ${isSubmitted ? 'cursor-not-allowed opacity-70' : ''}`}
                                        title="Ano"
                                    >
                                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                                        </svg>
                                    </button>
                                    <button
                                        onClick={() => toggleAnswer(index, null)}
                                        disabled={isSubmitted}
                                        className={`p-1.5 rounded transition-all ${selectedAnswers[index] === null
                                            ? 'bg-zinc-600 text-white'
                                            : 'text-zinc-500 hover:text-zinc-300'
                                            } ${isSubmitted ? 'cursor-not-allowed opacity-70' : ''}`}
                                        title="Nevím"
                                    >
                                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M20 12H4" />
                                        </svg>
                                    </button>
                                    <button
                                        onClick={() => toggleAnswer(index, false)}
                                        disabled={isSubmitted}
                                        className={`p-1.5 rounded transition-all ${selectedAnswers[index] === false
                                            ? 'bg-zinc-600 text-white'
                                            : 'text-zinc-500 hover:text-zinc-300'
                                            } ${isSubmitted ? 'cursor-not-allowed opacity-70' : ''}`}
                                        title="Ne"
                                    >
                                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
                                        </svg>
                                    </button>
                                </div>
                            </div>

                            <LatexRenderer
                                content={answer.text}
                                className="flex-1 text-zinc-200 leading-relaxed"
                            />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
