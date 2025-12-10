import json
import shutil
from pathlib import Path
import random

def collect_all_questions():
    """Collect all questions from output folders."""
    output_folder = Path("./output")
    all_questions = []
    
    for folder in output_folder.iterdir():
        if folder.is_dir():
            json_file = folder / "quiz_data.json"
            if json_file.exists():
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for question in data.get('questions', []):
                        # Find the image file in this folder
                        image_files = list(folder.glob('*'))
                        image_file = next((f for f in image_files if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}), None)
                        
                        question['image'] = f"images/{folder.name}/{image_file.name}" if image_file else None
                        question['source_folder'] = folder.name
                        all_questions.append(question)
    
    return all_questions

def generate_html(questions):
    """Generate the static HTML file with all questions."""
    
    # Extract unique categories
    categories = sorted(set(q.get('category', 'Matematika') for q in questions))
    
    # Shuffle questions for random order
    shuffled_questions = questions.copy()
    random.shuffle(shuffled_questions)
    
    html = """<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matematika - Kvíz</title>
    <script>
        MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true,
                processEnvironments: true
            },
            options: {
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            }
        };
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #36393f;
            color: #dcddde;
            min-height: 100vh;
            padding: 15px;
        }
        .main-container {
            display: flex;
            gap: 15px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .sidebar {
            width: 220px;
            background: #2f3136;
            border-radius: 8px;
            padding: 16px;
            flex-shrink: 0;
            height: fit-content;
        }
        .sidebar h2 {
            font-size: 0.95em;
            margin-bottom: 14px;
            color: #5eb3d6;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 10px;
            margin-bottom: 6px;
            background: #36393f;
            border-radius: 6px;
            font-size: 0.85em;
        }
        .stat-label {
            color: #b5bac1;
        }
        .stat-value {
            font-weight: 600;
            color: #dcddde;
        }
        .category-filters {
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid #202225;
        }
        .category-filter {
            display: flex;
            align-items: center;
            padding: 8px 10px;
            margin-bottom: 6px;
            background: #36393f;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.2s;
            font-size: 0.8em;
        }
        .category-filter:hover {
            background: #40444b;
        }
        .category-filter input[type="checkbox"] {
            margin-right: 8px;
            cursor: pointer;
        }
        .category-filter label {
            cursor: pointer;
            flex: 1;
            color: #dcddde;
            line-height: 1.3;
        }
        .filter-actions {
            display: flex;
            gap: 6px;
            margin-top: 10px;
        }
        .filter-btn {
            flex: 1;
            padding: 6px;
            background: #4f545c;
            color: #dcddde;
            border: none;
            border-radius: 4px;
            font-size: 0.75em;
            cursor: pointer;
            transition: background 0.2s;
        }
        .filter-btn:hover {
            background: #5d6269;
        }
        .container {
            flex: 1;
            background: #40444b;
            border-radius: 8px;
            overflow: hidden;
        }
        .header {
            background: #2f3136;
            padding: 20px;
        }
        .header h1 {
            font-size: 1.3em;
            margin-bottom: 6px;
            color: #dcddde;
        }
        .header-subtitle {
            color: #b5bac1;
            font-size: 0.85em;
            margin-bottom: 12px;
        }
        .progress {
            background: #202225;
            height: 4px;
            border-radius: 2px;
            overflow: hidden;
        }
        .progress-bar {
            background: #5eb3d6;
            height: 100%;
            transition: width 0.3s ease;
        }
        .question-container {
            padding: 25px;
        }
        .category {
            display: inline-block;
            background: #5eb3d6;
            color: #ffffff;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            margin-bottom: 14px;
            font-weight: 500;
        }
        .toggle-image-btn {
            display: inline-block;
            margin-left: 10px;
            padding: 4px 12px;
            background: #4f545c;
            color: #dcddde;
            border: none;
            border-radius: 4px;
            font-size: 0.75em;
            cursor: pointer;
            transition: background 0.2s;
        }
        .toggle-image-btn:hover {
            background: #5d6269;
        }
        .question-image {
            width: 100%;
            max-height: 300px;
            object-fit: contain;
            margin-bottom: 20px;
            border-radius: 6px;
            display: none;
        }
        .question-image.visible {
            display: block;
        }
        .question-text {
            font-size: 1.05em;
            margin-bottom: 20px;
            line-height: 1.7;
            color: #dcddde;
        }
        .answers {
            display: grid;
            gap: 8px;
        }
        .answer-row {
            display: flex;
            align-items: center;
            padding: 10px 14px;
            background: #2f3136;
            border-radius: 6px;
            border: 2px solid transparent;
            transition: all 0.2s ease;
        }
        .answer-row:hover {
            background: #36393f;
        }
        .answer-row.correct {
            background: #2d3f2f;
            border-color: #3ba55d;
        }
        .answer-row.incorrect {
            background: #3f2d2d;
            border-color: #ed4245;
        }
        .answer-buttons {
            display: flex;
            gap: 6px;
            margin-right: 12px;
        }
        .answer-btn {
            width: 36px;
            height: 36px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.2s ease;
            background: #202225;
            color: #b5bac1;
        }
        .answer-btn:hover:not(:disabled) {
            background: #36393f;
        }
        .answer-btn.active {
            background: #5eb3d6;
            color: white;
        }
        .answer-btn:disabled {
            cursor: not-allowed;
            opacity: 0.6;
        }
        .answer-btn.btn-yes.active {
            background: #3ba55d;
        }
        .answer-btn.btn-no.active {
            background: #ed4245;
        }
        .answer-btn.btn-minus.active {
            background: #5eb3d6;
        }
        .answer-text {
            flex: 1;
            font-size: 0.95em;
            line-height: 1.5;
            color: #dcddde;
        }
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 25px;
            background: #2f3136;
            gap: 10px;
        }
        .nav-arrows {
            display: flex;
            gap: 8px;
        }
        .nav-btn {
            width: 36px;
            height: 36px;
            padding: 0;
            background: #4f545c;
            color: #dcddde;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 1.2em;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .nav-btn:hover:not(:disabled) {
            background: #5d6269;
        }
        .nav-btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        button.control-btn {
            padding: 10px 22px;
            font-size: 0.9em;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 600;
        }
        .btn-save {
            background: #4f545c;
            color: #dcddde;
        }
        .btn-save:hover {
            background: #5d6269;
        }
        .btn-evaluate {
            background: #5865f2;
            color: white;
        }
        .btn-evaluate:hover {
            background: #4752c4;
        }
        .btn-evaluate:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .feedback {
            margin-top: 16px;
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 0.95em;
            text-align: center;
            font-weight: 600;
        }
        .feedback.correct {
            background: #2d3f2f;
            color: #3ba55d;
        }
        .feedback.incorrect {
            background: #3f2d2d;
            color: #ed4245;
        }
        .hidden {
            display: none;
        }
        .no-questions {
            text-align: center;
            padding: 40px;
            color: #b5bac1;
        }
        @media (max-width: 968px) {
            .main-container {
                flex-direction: column;
            }
            .sidebar {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="sidebar">
            <h2>⚙ Stav</h2>
            <div class="stat-item">
                <span class="stat-label"># dobrých odpovědí</span>
                <span class="stat-value" id="correctCount">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">cílový počet</span>
                <span class="stat-value" id="targetCount">""" + str(len(shuffled_questions)) + """</span>
            </div>
            <div class="stat-item">
                <span class="stat-label"># zobrazených otázek</span>
                <span class="stat-value" id="answeredCount">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">série špatných odpovědí</span>
                <span class="stat-value" id="wrongStreak">0</span>
            </div>
            
            <div class="category-filters">
                <h2>📚 Kategorie</h2>
                """ + ''.join([f'''
                <div class="category-filter">
                    <input type="checkbox" id="cat_{i}" checked onchange="updateCategoryFilter()">
                    <label for="cat_{i}">{cat}</label>
                </div>
                ''' for i, cat in enumerate(categories)]) + """
                <div class="filter-actions">
                    <button class="filter-btn" onclick="selectAllCategories()">Vše</button>
                    <button class="filter-btn" onclick="deselectAllCategories()">Žádná</button>
                </div>
            </div>
        </div>
        
        <div class="container">
            <div class="header">
                <h1>Kvíz: BI-MA2</h1>
                <p class="header-subtitle" id="questionNumber">V tomto kvízu je """ + str(len(shuffled_questions)) + """ otázek. Po správném zodpovězení se vám už otázka nebude zobrazovat.</p>
                <div class="progress">
                    <div class="progress-bar" id="progressBar"></div>
                </div>
            </div>
            
            <div class="question-container" id="questionContainer">
                <!-- Question will be inserted here -->
            </div>
            
            <div class="controls">
                <div class="nav-arrows">
                    <button class="nav-btn" id="prevBtn" onclick="previousQuestion()" title="Předchozí otázka">←</button>
                    <button class="nav-btn" id="nextBtn" onclick="skipQuestion()" title="Následující otázka">→</button>
                </div>
                <button class="control-btn btn-evaluate" id="evaluateBtn" onclick="submitAnswer()">vyhodnotit</button>
            </div>
        </div>
    </div>

    <script>
        const allQuestions = """ + json.dumps(shuffled_questions, ensure_ascii=False) + """;
        const categories = """ + json.dumps(categories, ensure_ascii=False) + """;
        let filteredQuestions = [...allQuestions];
        let currentQuestion = 0;
        let userAnswers = [];
        let correctCount = 0;
        let answeredCount = 0;
        let wrongStreak = 0;
        let answeredQuestions = new Set();
        let imageVisible = false;

        function updateCategoryFilter() {
            const selectedCategories = categories.filter((_, idx) => 
                document.getElementById(`cat_${idx}`).checked
            );
            
            if (selectedCategories.length === 0) {
                filteredQuestions = [];
            } else {
                filteredQuestions = allQuestions.filter(q => 
                    selectedCategories.includes(q.category || 'Matematika')
                );
            }
            
            // Shuffle filtered questions
            filteredQuestions.sort(() => Math.random() - 0.5);
            
            // Reset state
            currentQuestion = 0;
            userAnswers = [];
            answeredQuestions.clear();
            
            // Update stats
            document.getElementById('targetCount').textContent = filteredQuestions.length;
            
            // Render first question or show message
            if (filteredQuestions.length > 0) {
                renderQuestion();
            } else {
                document.getElementById('questionContainer').innerHTML = 
                    '<div class="no-questions">Vyberte alespoň jednu kategorii pro trénování.</div>';
            }
        }

        function selectAllCategories() {
            categories.forEach((_, idx) => {
                document.getElementById(`cat_${idx}`).checked = true;
            });
            updateCategoryFilter();
        }

        function deselectAllCategories() {
            categories.forEach((_, idx) => {
                document.getElementById(`cat_${idx}`).checked = false;
            });
            updateCategoryFilter();
        }

        function renderQuestion() {
            if (filteredQuestions.length === 0) {
                document.getElementById('questionContainer').innerHTML = 
                    '<div class="no-questions">Vyberte alespoň jednu kategorii pro trénování.</div>';
                return;
            }

            const q = filteredQuestions[currentQuestion];
            const container = document.getElementById('questionContainer');
            
            let html = `<div class="category">${q.category || 'Matematika'}</div>`;
            
            if (q.image) {
                html += `<button class="toggle-image-btn" onclick="toggleImage()">Zobrazit původní otázku</button>`;
                html += `<img src="${q.image}" alt="Quiz question" class="question-image" id="questionImage">`;
            }
            
            html += `<div class="question-text">${q.question}</div>`;
            html += '<div class="answers">';
            
            q.answers.forEach((answer, idx) => {
                const userAnswer = userAnswers[currentQuestion] ? userAnswers[currentQuestion][idx] : null;
                const yesActive = userAnswer === true ? 'active btn-yes' : '';
                const minusActive = userAnswer === null ? 'active btn-minus' : '';
                const noActive = userAnswer === false ? 'active btn-no' : '';
                
                html += `
                    <div class="answer-row" id="answerRow${idx}">
                        <div class="answer-buttons">
                            <button class="answer-btn ${yesActive}" onclick="setAnswer(${idx}, true)">✓</button>
                            <button class="answer-btn ${minusActive}" onclick="setAnswer(${idx}, null)">−</button>
                            <button class="answer-btn ${noActive}" onclick="setAnswer(${idx}, false)">✕</button>
                        </div>
                        <div class="answer-text">${answer.text}</div>
                    </div>
                `;
            });
            
            html += '</div>';
            container.innerHTML = html;
            
            imageVisible = false;
            updateStats();
            updateNavigationButtons();
            
            // Render MathJax after content is inserted
            MathJax.typesetPromise([container]).catch((err) => console.log('MathJax error:', err));
        }

        function updateNavigationButtons() {
            document.getElementById('prevBtn').disabled = currentQuestion === 0;
            document.getElementById('nextBtn').disabled = currentQuestion >= filteredQuestions.length - 1;
        }

        function toggleImage() {
            const img = document.getElementById('questionImage');
            const btn = document.querySelector('.toggle-image-btn');
            if (img) {
                imageVisible = !imageVisible;
                if (imageVisible) {
                    img.classList.add('visible');
                    btn.textContent = 'Skrýt původní otázku';
                } else {
                    img.classList.remove('visible');
                    btn.textContent = 'Zobrazit původní otázku';
                }
            }
        }

        function setAnswer(idx, value) {
            if (!userAnswers[currentQuestion]) {
                userAnswers[currentQuestion] = [];
            }
            
            // Toggle if clicking the same button
            if (userAnswers[currentQuestion][idx] === value) {
                userAnswers[currentQuestion][idx] = undefined;
            } else {
                userAnswers[currentQuestion][idx] = value;
            }
            
            renderQuestion();
        }

        function updateStats() {
            document.getElementById('correctCount').textContent = correctCount;
            document.getElementById('answeredCount').textContent = answeredCount;
            document.getElementById('wrongStreak').textContent = wrongStreak;
            document.getElementById('progressBar').style.width = 
                `${filteredQuestions.length > 0 ? (correctCount / filteredQuestions.length) * 100 : 0}%`;
        }

        function submitAnswer() {
            if (filteredQuestions.length === 0) return;

            const q = filteredQuestions[currentQuestion];
            const answers = document.querySelectorAll('.answer-row');
            let allCorrect = true;
            let hasAnswered = false;
            
            q.answers.forEach((answer, idx) => {
                const userSelected = userAnswers[currentQuestion] ? userAnswers[currentQuestion][idx] : undefined;
                const shouldBeSelected = answer.correct;
                
                if (userSelected !== undefined) {
                    hasAnswered = true;
                }
                
                if (userSelected === shouldBeSelected) {
                    answers[idx].classList.add('correct');
                } else {
                    answers[idx].classList.add('incorrect');
                    allCorrect = false;
                }
                
                // Disable buttons
                answers[idx].querySelectorAll('.answer-btn').forEach(btn => {
                    btn.disabled = true;
                });
            });
            
            if (!hasAnswered) {
                alert('Prosím, zodpovězte alespoň jednu otázku.');
                answers.forEach(row => {
                    row.querySelectorAll('.answer-btn').forEach(btn => {
                        btn.disabled = false;
                    });
                    row.classList.remove('correct', 'incorrect');
                });
                return;
            }
            
            if (!answeredQuestions.has(currentQuestion)) {
                answeredCount++;
                answeredQuestions.add(currentQuestion);
            }
            
            if (allCorrect) {
                correctCount++;
                wrongStreak = 0;
            } else {
                wrongStreak++;
            }
            
            const feedback = document.createElement('div');
            feedback.className = `feedback ${allCorrect ? 'correct' : 'incorrect'}`;
            feedback.textContent = allCorrect ? '✓ Správně!' : '✗ Zkuste to znovu příště';
            document.getElementById('questionContainer').appendChild(feedback);
            
            updateStats();
            
            setTimeout(() => {
                nextQuestion();
            }, 1500);
        }

        function nextQuestion() {
            if (filteredQuestions.length === 0) return;

            if (currentQuestion < filteredQuestions.length - 1) {
                currentQuestion++;
                renderQuestion();
            } else {
                // Loop back to start
                currentQuestion = 0;
                renderQuestion();
            }
        }

        function previousQuestion() {
            if (filteredQuestions.length === 0 || currentQuestion === 0) return;
            currentQuestion--;
            renderQuestion();
        }

        function skipQuestion() {
            // Skip to next question without answering
            if (filteredQuestions.length === 0) return;
            
            if (currentQuestion < filteredQuestions.length - 1) {
                currentQuestion++;
            } else {
                currentQuestion = 0;
            }
            renderQuestion();
        }

        renderQuestion();
    </script>
</body>
</html>"""
    
    return html

def main():
    """Generate the static quiz site."""
    print("Collecting questions...")
    questions = collect_all_questions()
    print(f"Found {len(questions)} questions")
    
    # Create build folder
    build_folder = Path("./build")
    build_folder.mkdir(exist_ok=True)
    
    # Create images folder in build
    images_folder = build_folder / "images"
    if images_folder.exists():
        shutil.rmtree(images_folder)
    images_folder.mkdir()
    
    # Copy images from output to build
    output_folder = Path("./output")
    for folder in output_folder.iterdir():
        if folder.is_dir():
            dest_folder = images_folder / folder.name
            dest_folder.mkdir(exist_ok=True)
            
            # Copy only image files
            for file in folder.iterdir():
                if file.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}:
                    shutil.copy2(file, dest_folder / file.name)
    
    # Generate HTML
    print("Generating HTML...")
    html_content = generate_html(questions)
    
    # Save index.html
    with open(build_folder / "index.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Generated build/index.html with {len(questions)} questions")
    print(f"✓ Copied images to build/images/")

if __name__ == "__main__":
    main()
