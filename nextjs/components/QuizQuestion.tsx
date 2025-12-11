'use client';

import { useState } from 'react';
import Image from 'next/image';
import LatexRenderer from './LatexRenderer';
import { Question } from '@/lib/types';

interface QuizQuestionProps {
    question: Question;
    onSubmit: (selectedAnswers: boolean[], isCorrect: boolean) => void;
    isSubmitted: boolean;
}

export default function QuizQuestion({ question, onSubmit, isSubmitted }: QuizQuestionProps) {
    const [selectedAnswers, setSelectedAnswers] = useState<boolean[]>(
        new Array(question.answers.length).fill(false)
    );

    const toggleAnswer = (index: number) => {
        if (isSubmitted) return;
        const newSelected = [...selectedAnswers];
        newSelected[index] = !newSelected[index];
        setSelectedAnswers(newSelected);
    };

    const getAnswerClassName = (index: number) => {
        const baseClass = 'p-4 rounded-lg cursor-pointer transition-all border-2';

        if (!isSubmitted) {
            return `${baseClass} ${selectedAnswers[index]
                    ? 'border-purple-500 bg-purple-500/10'
                    : 'border-zinc-700 bg-zinc-800/50 hover:border-zinc-600'
                }`;
        }

        const isCorrect = question.answers[index].correct;
        const isSelected = selectedAnswers[index];

        if (isCorrect) {
            return `${baseClass} border-green-500 bg-green-500/10`;
        }
        if (isSelected && !isCorrect) {
            return `${baseClass} border-red-500 bg-red-500/10`;
        }
        return `${baseClass} border-zinc-700 bg-zinc-800/30 opacity-50`;
    };

    return (
        <div className="w-full space-y-6">
            {/* Question text */}
            <div className="bg-[#1a1a2e] rounded-lg p-6">
                <LatexRenderer
                    content={question.question}
                    className="text-lg text-zinc-100 leading-relaxed"
                />

                {question.image_src && (
                    <div className="mt-6 relative w-full h-64 bg-zinc-900 rounded-lg overflow-hidden">
                        <Image
                            src={`/${question.image_src}`}
                            alt="Question image"
                            fill
                            className="object-contain"
                        />
                    </div>
                )}
            </div>

            {/* Answers */}
            <div className="space-y-3">
                {question.answers.map((answer, index) => (
                    <div
                        key={index}
                        onClick={() => toggleAnswer(index)}
                        className={getAnswerClassName(index)}
                    >
                        <div className="flex items-start gap-3">
                            <div className="flex items-center justify-center mt-1">
                                {isSubmitted ? (
                                    question.answers[index].correct ? (
                                        <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                        </svg>
                                    ) : selectedAnswers[index] ? (
                                        <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                        </svg>
                                    ) : (
                                        <div className="w-5 h-5 rounded border-2 border-zinc-600" />
                                    )
                                ) : (
                                    <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${selectedAnswers[index]
                                            ? 'border-purple-500 bg-purple-500'
                                            : 'border-zinc-600'
                                        }`}>
                                        {selectedAnswers[index] && (
                                            <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                            </svg>
                                        )}
                                    </div>
                                )}
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
