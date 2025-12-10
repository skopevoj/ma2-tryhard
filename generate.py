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
    <title>MARAST - BI-MA2 Kvíz</title>
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
        :root {
            --bg-primary: #36393f;
            --bg-secondary: #2f3136;
            --bg-tertiary: #40444b;
            --bg-input: #202225;
            --text-primary: #dcddde;
            --text-secondary: #b5bac1;
            --accent: #5eb3d6;
            --accent-hover: #4a9bb8;
            --success: #3ba55d;
            --error: #ed4245;
            --border: #202225;
        }
        
        [data-theme="light"] {
            --bg-primary: #ffffff;
            --bg-secondary: #f2f3f5;
            --bg-tertiary: #e3e5e8;
            --bg-input: #ebedef;
            --text-primary: #2e3338;
            --text-secondary: #4e5058;
            --accent: #5865f2;
            --accent-hover: #4752c4;
            --success: #3ba55d;
            --error: #ed4245;
            --border: #d1d5db;
        }
        
        [data-theme="orange"] {
            --bg-primary: #2c2520;
            --bg-secondary: #3a302a;
            --bg-tertiary: #4a3d35;
            --bg-input: #1f1a17;
            --text-primary: #f5e6d3;
            --text-secondary: #d4c4b0;
            --accent: #ff6b35;
            --accent-hover: #e55a2b;
            --success: #4caf50;
            --error: #f44336;
            --border: #1f1a17;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 15px;
            transition: background 0.3s, color 0.3s;
        }
        
        .welcome-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            padding: 20px;
        }
        
        .welcome-overlay.hidden {
            display: none;
        }
        
        .welcome-modal {
            background: var(--bg-secondary);
            border-radius: 12px;
            max-width: 600px;
            width: 100%;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        
        .welcome-modal h1 {
            font-size: 2em;
            margin-bottom: 10px;
            color: var(--accent);
        }
        
        .welcome-modal h2 {
            font-size: 1.5em;
            margin-bottom: 20px;
            color: var(--text-primary);
        }
        
        .welcome-modal p {
            line-height: 1.6;
            color: var(--text-secondary);
            margin-bottom: 15px;
        }
        
        .welcome-modal ul {
            margin: 20px 0;
            padding-left: 20px;
        }
        
        .welcome-modal li {
            margin-bottom: 10px;
            color: var(--text-secondary);
            line-height: 1.5;
        }
        
        .welcome-btn {
            width: 100%;
            padding: 14px;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
            transition: background 0.2s;
        }
        
        .welcome-btn:hover {
            background: var(--accent-hover);
        }
        
        .logo {
            font-size: 1.8em;
            font-weight: 700;
            color: var(--accent);
            letter-spacing: 2px;
            margin-bottom: 20px;
        }
        
        .main-container {
            display: flex;
            gap: 15px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .sidebar {
            width: 220px;
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 16px;
            flex-shrink: 0;
            height: fit-content;
        }
        .sidebar h2 {
            font-size: 0.95em;
            margin-bottom: 14px;
            color: var(--accent);
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 10px;
            margin-bottom: 6px;
            background: var(--bg-primary);
            border-radius: 6px;
            font-size: 0.85em;
        }
        .stat-label {
            color: var(--text-secondary);
        }
        .stat-value {
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .progress-display {
            margin-top: 10px;
            padding: 10px;
            background: var(--bg-primary);
            border-radius: 6px;
            font-size: 0.85em;
        }
        
        .progress-display .progress-fraction {
            text-align: center;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--accent);
        }
        
        .progress-display .progress {
            background: var(--bg-input);
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-display .progress-bar {
            background: var(--accent);
            height: 100%;
            transition: width 0.3s ease;
        }
        
        .theme-switcher {
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
        }
        
        .theme-buttons {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            margin-top: 10px;
        }
        
        .theme-btn {
            padding: 8px;
            border: 2px solid transparent;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.75em;
            background: var(--bg-primary);
            color: var(--text-primary);
        }
        
        .theme-btn.active {
            border-color: var(--accent);
            background: var(--accent);
            color: white;
        }
        
        .theme-btn:hover {
            background: var(--bg-tertiary);
        }
        
        .category-filters {
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
        }
        .category-filter {
            display: flex;
            align-items: center;
            padding: 8px 10px;
            margin-bottom: 6px;
            background: var(--bg-primary);
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.2s;
            font-size: 0.8em;
        }
        .category-filter:hover {
            background: var(--bg-tertiary);
        }
        .category-filter input[type="checkbox"] {
            margin-right: 8px;
            cursor: pointer;
        }
        .category-filter label {
            cursor: pointer;
            flex: 1;
            color: var(--text-primary);
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
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border: none;
            border-radius: 4px;
            font-size: 0.75em;
            cursor: pointer;
            transition: background 0.2s;
        }
        .filter-btn:hover {
            opacity: 0.8;
        }
        
        .shuffle-btn {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 0.85em;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        
        .shuffle-btn:hover {
            background: var(--accent-hover);
        }
        
        .container {
            flex: 1;
            background: var(--bg-tertiary);
            border-radius: 8px;
            overflow: hidden;
        }
        .header {
            background: var(--bg-secondary);
            padding: 20px;
        }
        
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .header h1 {
            font-size: 1.3em;
            color: var(--text-primary);
        }
        
        .header-subtitle {
            color: var(--text-secondary);
            font-size: 0.85em;
            margin-bottom: 12px;
        }
        .progress {
            background: var(--bg-input);
            height: 4px;
            border-radius: 2px;
            overflow: hidden;
        }
        .progress-bar {
            background: var(--accent);
            height: 100%;
            transition: width 0.3s ease;
        }
        .question-container {
            padding: 25px;
        }
        .category {
            display: inline-block;
            background: var(--accent);
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
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: none;
            border-radius: 4px;
            font-size: 0.75em;
            cursor: pointer;
            transition: background 0.2s;
        }
        .toggle-image-btn:hover {
            background: var(--bg-tertiary);
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
            color: var(--text-primary);
        }
        .answers {
            display: grid;
            gap: 8px;
        }
        .answer-row {
            display: flex;
            align-items: center;
            padding: 10px 14px;
            background: var(--bg-secondary);
            border-radius: 6px;
            border: 2px solid transparent;
            transition: all 0.2s ease;
        }
        .answer-row:hover {
            background: var(--bg-primary);
        }
        .answer-row.correct {
            background: rgba(59, 165, 93, 0.15);
            border-color: var(--success);
        }
        .answer-row.incorrect {
            background: rgba(237, 66, 69, 0.15);
            border-color: var(--error);
        }
        
        .answer-buttons {
            display: flex;
            gap: 6px;
            margin-right: 12px;
            flex-shrink: 0;
        }
        
        .answer-btn {
            width: 40px;
            height: 32px;
            border: 2px solid var(--border);
            border-radius: 4px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.2s ease;
            background: var(--bg-input);
            color: var(--text-secondary);
        }
        
        .answer-btn:hover:not(:disabled) {
            border-color: var(--accent);
            background: var(--bg-tertiary);
        }
        
        .answer-btn.active {
            border-color: var(--accent);
            background: var(--accent);
            color: white;
        }
        
        .answer-btn:disabled {
            cursor: not-allowed;
            opacity: 0.6;
        }
        
        .answer-btn.btn-yes.active {
            border-color: var(--success);
            background: var(--success);
        }
        
        .answer-btn.btn-no.active {
            border-color: var(--error);
            background: var(--error);
        }
        
        .answer-text {
            flex: 1;
            font-size: 0.95em;
            line-height: 1.5;
            color: var(--text-primary);
        }
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 25px;
            background: var(--bg-secondary);
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
            background: var(--bg-tertiary);
            color: var(--text-primary);
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
            background: var(--bg-primary);
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
        .btn-evaluate {
            background: var(--accent);
            color: white;
        }
        .btn-evaluate:hover {
            background: var(--accent-hover);
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
            background: rgba(59, 165, 93, 0.15);
            color: var(--success);
        }
        .feedback.incorrect {
            background: rgba(237, 66, 69, 0.15);
            color: var(--error);
        }
        .hidden {
            display: none;
        }
        .no-questions {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
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
<body data-theme="dark">
    <div class="welcome-overlay" id="welcomeOverlay">
        <div class="welcome-modal">
            <div class="logo">MARAST</div>
            <h2>BI-MA2 Kvíz</h2>
            <p>Vítejte v interaktivním kvízu pro přípravu na zkoušku z matematiky 2!</p>
            <ul>
                <li><strong>Označte správné odpovědi</strong> pomocí tlačítek ✓ (správně), − (nevím), ✕ (špatně)</li>
                <li><strong>Vyberte kategorie</strong>, které chcete procvičovat</li>
                <li><strong>Sledujte svůj pokrok</strong> v levém panelu</li>
                <li><strong>Přepínejte motivy</strong> podle svých preferencí</li>
                <li><strong>Používejte šipky</strong> pro navigaci mezi otázkami</li>
            </ul>
            <p>Po správném zodpovězení se vám otázka už nebude zobrazovat. Držíme palce! 🎓</p>
            <button class="welcome-btn" onclick="closeWelcome()">Rozumím, začít kvíz</button>
        </div>
    </div>

    <div class="main-container">
        <div class="sidebar">
            <div class="logo">MARAST</div>
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
            
            <div class="progress-display">
                <div class="progress-fraction" id="progressFraction">0 / """ + str(len(shuffled_questions)) + """</div>
                <div class="progress">
                    <div class="progress-bar" id="sidebarProgressBar"></div>
                </div>
            </div>
            
            <button class="shuffle-btn" onclick="shuffleQuestions()">🔀 Zamíchat otázky</button>
            
            <div class="theme-switcher">
                <h2>🎨 Motiv</h2>
                <div class="theme-buttons">
                    <button class="theme-btn active" onclick="setTheme('dark')">Tmavý</button>
                    <button class="theme-btn" onclick="setTheme('light')">Světlý</button>
                    <button class="theme-btn" onclick="setTheme('orange')">Oranžový</button>
                </div>
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
                <div class="header-top">
                    <h1>Kvíz: BI-MA2</h1>
                </div>
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
        
        function closeWelcome() {
            document.getElementById('welcomeOverlay').classList.add('hidden');
            localStorage.setItem('welcomeShown', 'true');
        }
        
        function setTheme(theme) {
            document.body.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            
            document.querySelectorAll('.theme-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
        }
        
        function shuffleQuestions() {
            filteredQuestions.sort(() => Math.random() - 0.5);
            currentQuestion = 0;
            userAnswers = [];
            renderQuestion();
        }

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
            
            filteredQuestions.sort(() => Math.random() - 0.5);
            currentQuestion = 0;
            userAnswers = [];
            answeredQuestions.clear();
            
            document.getElementById('targetCount').textContent = filteredQuestions.length;
            
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
            
            const progressPercent = filteredQuestions.length > 0 ? (correctCount / filteredQuestions.length) * 100 : 0;
            document.getElementById('progressBar').style.width = `${progressPercent}%`;
            document.getElementById('sidebarProgressBar').style.width = `${progressPercent}%`;
            document.getElementById('progressFraction').textContent = `${correctCount} / ${filteredQuestions.length}`;
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
            if (filteredQuestions.length === 0) return;
            
            if (currentQuestion < filteredQuestions.length - 1) {
                currentQuestion++;
            } else {
                currentQuestion = 0;
            }
            renderQuestion();
        }
        
        // Load saved theme and welcome state
        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            document.body.setAttribute('data-theme', savedTheme);
            
            const welcomeShown = localStorage.getItem('welcomeShown');
            if (welcomeShown) {
                document.getElementById('welcomeOverlay').classList.add('hidden');
            }
            
            document.querySelectorAll('.theme-btn').forEach(btn => {
                if (btn.textContent.toLowerCase().includes(savedTheme === 'dark' ? 'tmavý' : savedTheme === 'light' ? 'světlý' : 'oranžový')) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
            
            renderQuestion();
        });
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
