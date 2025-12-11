export interface Answer {
    text: string;
    correct: boolean;
}

export interface Question {
    question: string;
    category: string;
    answers: Answer[];
    image_src: string;
    source_folder: string;
    quiz_id: string;
}
