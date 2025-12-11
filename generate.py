import json
import shutil
from pathlib import Path
import random

def collect_all_questions():
    """Collect all questions from output folders."""
    output_folder = Path("./questions")
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
    <title>MARNOST</title>
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
            --bg-primary: #0a0a0f;
            --bg-secondary: rgba(20, 20, 30, 0.4);
            --bg-tertiary: rgba(30, 30, 45, 0.6);
            --bg-input: rgba(15, 15, 25, 0.5);
            --bg-card: rgba(20, 20, 30, 0.5);
            --text-primary: #f0f2f5;
            --text-secondary: #b8bdc8;
            --accent: #8b5cf6;
            --accent-hover: #7c3aed;
            --accent-glow: rgba(139, 92, 246, 0.4);
            --success: #10b981;
            --error: #ef4444;
            --border: rgba(139, 92, 246, 0.1);
            --text-size: 1;
        }
        
        [data-theme="light"] {
            --bg-primary: #f5f5f7;
            --bg-secondary: rgba(255, 255, 255, 0.7);
            --bg-tertiary: rgba(240, 240, 245, 0.8);
            --bg-input: rgba(235, 235, 240, 0.6);
            --bg-card: rgba(255, 255, 255, 0.6);
            --text-primary: #1a1a1f;
            --text-secondary: #4e5058;
            --accent: #8b5cf6;
            --accent-hover: #7c3aed;
            --accent-glow: rgba(139, 92, 246, 0.3);
            --success: #10b981;
            --error: #ef4444;
            --border: rgba(139, 92, 246, 0.15);
        }
        
        [data-theme="orange"] {
            --bg-primary: #0f0a0a;
            --bg-secondary: rgba(30, 20, 20, 0.4);
            --bg-tertiary: rgba(45, 30, 30, 0.6);
            --bg-input: rgba(25, 15, 15, 0.5);
            --bg-card: rgba(30, 20, 20, 0.5);
            --text-primary: #f5e6d3;
            --text-secondary: #d4c4b0;
            --accent: #ff6b35;
            --accent-hover: #e55a2b;
            --accent-glow: rgba(255, 107, 53, 0.4);
            --success: #10b981;
            --error: #ef4444;
            --border: rgba(255, 107, 53, 0.1);
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
            transition: background 0.3s, color 0.3s;
            font-size: calc(16px * var(--text-size));
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 30% 50%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
                        radial-gradient(circle at 70% 80%, rgba(167, 139, 250, 0.06) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }
        
        .glass-card {
            position: relative;
            overflow: visible;
            border-radius: 24px;
            padding: 1.5rem;
            background: var(--bg-card);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: none;
            transition: all 0.3s ease;
            transform-style: preserve-3d;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .glass-card::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 24px;
            padding: 2px;
            background: linear-gradient(180deg, rgba(139, 92, 246, 0.4) 0%, rgba(139, 92, 246, 0.05) 100%);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
            opacity: 0.5;
        }
        
        .card-blob {
            display: none;
        }
        
        .welcome-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(10px);
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
            background: var(--bg-card);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-radius: 24px;
            max-width: 600px;
            width: 100%;
            padding: 40px;
            box-shadow: 0 12px 48px var(--accent-glow);
            border: 2px solid var(--border);
            position: relative;
        }
        
        .welcome-modal::before {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 24px;
            z-index: -1;
        }
        
        .welcome-modal h1 {
            font-size: 2em;
            margin-bottom: 10px;
            color: var(--accent);
            text-shadow: 0 0 20px var(--accent-glow);
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
            border-radius: 12px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px var(--accent-glow);
        }
        
        .welcome-btn:hover {
            background: var(--accent-hover);
            transform: translateY(-2px);
            box-shadow: 0 8px 32px var(--accent-glow);
        }
        
        .settings-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(10px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            padding: 20px;
        }
        
        .settings-modal.visible {
            display: flex;
        }
        
        .settings-content {
            background: var(--bg-card);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-radius: 24px;
            max-width: 500px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 12px 48px var(--accent-glow);
            border: 2px solid var(--border);
        }
        
        .settings-header {
            padding: 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .settings-header h2 {
            font-size: 1.3em;
            color: var(--text-primary);
        }
        
        .close-settings {
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 1.5em;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 8px;
            transition: all 0.2s;
        }
        
        .close-settings:hover {
            background: var(--bg-tertiary);
            color: var(--accent);
        }
        
        .settings-body {
            padding: 24px;
        }
        
        .settings-section {
            margin-bottom: 28px;
        }
        
        .settings-section:last-child {
            margin-bottom: 0;
        }
        
        .settings-section h3 {
            font-size: 0.95em;
            color: var(--accent);
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            text-shadow: 0 0 10px var(--accent-glow);
        }
        
        .theme-buttons {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }
        
        .theme-btn {
            padding: 10px;
            border: 2px solid var(--border);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9em;
            background: var(--bg-input);
            backdrop-filter: blur(10px);
            color: var(--text-primary);
        }
        
        .theme-btn.active {
            border-color: var(--accent);
            background: var(--accent);
            color: white;
            box-shadow: 0 4px 16px var(--accent-glow);
        }
        
        .theme-btn:hover {
            background: var(--bg-tertiary);
            transform: translateY(-2px);
        }
        
        .text-size-control {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .text-size-slider {
            flex: 1;
            height: 6px;
            -webkit-appearance: none;
            appearance: none;
            background: var(--bg-input);
            border-radius: 3px;
            outline: none;
        }
        
        .text-size-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 18px;
            height: 18px;
            background: var(--accent);
            cursor: pointer;
            border-radius: 50%;
            box-shadow: 0 2px 8px var(--accent-glow);
        }
        
        .text-size-slider::-moz-range-thumb {
            width: 18px;
            height: 18px;
            background: var(--accent);
            cursor: pointer;
            border-radius: 50%;
            border: none;
            box-shadow: 0 2px 8px var(--accent-glow);
        }
        
        .text-size-label {
            min-width: 80px;
            text-align: center;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .category-filter {
            display: flex;
            align-items: center;
            padding: 10px 12px;
            margin-bottom: 8px;
            background: var(--bg-input);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid transparent;
        }
        
        .category-filter:hover {
            background: var(--bg-tertiary);
            border-color: var(--border);
            transform: translateX(4px);
        }
        
        .category-filter input[type="checkbox"] {
            margin-right: 10px;
            cursor: pointer;
            width: 18px;
            height: 18px;
            accent-color: var(--accent);
        }
        
        .category-filter label {
            cursor: pointer;
            flex: 1;
            color: var(--text-primary);
        }
        
        .filter-actions {
            display: flex;
            gap: 8px;
            margin-top: 12px;
        }
        
        .filter-btn, .shuffle-btn {
            flex: 1;
            padding: 10px;
            background: var(--bg-tertiary);
            backdrop-filter: blur(10px);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: 12px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
        }
        
        .filter-btn:hover, .shuffle-btn:hover {
            background: var(--accent);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 16px var(--accent-glow);
        }
        
        .main-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            position: relative;
            z-index: 1;
        }
        
        .page-wrapper {
            max-width: 800px;
            width: 100%;
        }
        
        .stats-bar {
            width: 100%;
            background: var(--bg-card);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-radius: 24px;
            padding: 16px 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            border: 2px solid var(--border);
            position: relative;
        }
        
        .stats-bar::before {
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 50%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            opacity: 0.5;
        }
        
        .stats-left {
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .logo {
            font-size: 1.5em;
            font-weight: 700;
            color: var(--accent);
            letter-spacing: 2px;
            text-shadow: 0 0 20px var(--accent-glow);
        }
        
        .settings-btn {
            background: var(--bg-input);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            color: var(--text-primary);
            font-size: 1.2em;
            cursor: pointer;
            padding: 8px 12px;
            border-radius: 12px;
            transition: all 0.2s;
        }
        
        .settings-btn:hover {
            background: var(--accent);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 16px var(--accent-glow);
        }
        
        .stats-right {
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .stat-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 14px;
            background: var(--bg-input);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            border: 1px solid var(--border);
            transition: all 0.2s;
        }
        
        .stat-item:hover {
            transform: translateY(-2px);
            border-color: var(--accent);
            box-shadow: 0 4px 16px var(--accent-glow);
        }
        
        .stat-icon {
            font-size: 1.2em;
        }
        
        .stat-value {
            font-weight: 700;
            color: var(--text-primary);
            font-size: 1em;
        }
        
        .progress-bar-container {
            width: 100%;
            margin-top: 12px;
            padding: 12px;
            background: var(--bg-input);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            border: 1px solid var(--border);
        }
        
        .progress-fraction {
            text-align: center;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--accent);
            font-size: 1em;
            text-shadow: 0 0 10px var(--accent-glow);
        }
        
        .progress {
            background: rgba(0, 0, 0, 0.3);
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-bar {
            background: linear-gradient(90deg, var(--accent-hover), var(--accent));
            height: 100%;
            transition: width 0.3s ease;
            box-shadow: 0 0 10px var(--accent-glow);
        }
        
        .content-wrapper {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .container {
            width: 100%;
            position: relative;
        }
        
        .question-container {
            min-height: 400px;
        }
        
        .question-image {
            width: 100%;
            max-height: 400px;
            object-fit: contain;
            margin-bottom: 20px;
            border-radius: 16px;
            display: none;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .question-image.visible {
            display: block;
        }
        
        .question-text {
            font-size: 1.1em;
            margin-bottom: 24px;
            line-height: 1.7;
            color: var(--text-primary);
        }
        
        .answers {
            display: grid;
            gap: 10px;
        }
        
        .answer-row {
            display: flex;
            align-items: center;
            padding: 12px 16px;
            background: var(--bg-input);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 2px solid var(--border);
            transition: all 0.2s ease;
        }
        
        .answer-row:hover {
            background: var(--bg-tertiary);
            //transform: translateX(4px);
            border-color: var(--accent);
        }
        
        .answer-row.correct {
            background: rgba(16, 185, 129, 0.15);
            border-color: var(--success);
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
        }
        
        .answer-row.incorrect {
            background: rgba(239, 68, 68, 0.15);
            border-color: var(--error);
            box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);
        }
        
        .answer-buttons {
            display: flex;
            gap: 6px;
            margin-right: 14px;
            flex-shrink: 0;
        }
        
        .answer-btn {
            width: 42px;
            height: 34px;
            border: 2px solid var(--border);
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.2s ease;
            background: var(--bg-input);
            backdrop-filter: blur(10px);
            color: var(--text-secondary);
        }
        
        .answer-btn:hover:not(:disabled) {
            border-color: var(--accent);
            background: var(--bg-tertiary);
            transform: scale(1.05);
        }
        
        .answer-btn.active {
            border-color: var(--accent);
            background: var(--accent);
            color: white;
            box-shadow: 0 4px 16px var(--accent-glow);
        }
        
        .answer-btn:disabled {
            cursor: not-allowed;
            opacity: 0.6;
        }
        
        .answer-btn.btn-yes.active {
            border-color: var(--success);
            background: var(--success);
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4);
        }
        
        .answer-btn.btn-no.active {
            border-color: var(--error);
            background: var(--error);
            box-shadow: 0 4px 16px rgba(239, 68, 68, 0.4);
        }
        
        .answer-text {
            flex: 1;
            font-size: 1em;
            line-height: 1.6;
            color: var(--text-primary);
        }
        
        .controls {
            width: 100%;
            position: relative;
            overflow: visible;
        }
        
        .controls-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 28px;
            border-bottom: 1px solid var(--border);
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .category {
            display: inline-block;
            background: var(--accent);
            color: #ffffff;
            padding: 6px 14px;
            border-radius: 16px;
            font-size: 0.85em;
            font-weight: 600;
            box-shadow: 0 4px 16px var(--accent-glow);
        }
        
        .toggle-image-btn {
            padding: 6px 14px;
            background: var(--bg-tertiary);
            backdrop-filter: blur(10px);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: 10px;
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .toggle-image-btn:hover {
            background: var(--accent);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 16px var(--accent-glow);
        }
        
        .controls-bottom {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 28px;
            gap: 10px;
        }
        
        .nav-arrows {
            display: flex;
            gap: 8px;
        }
        
        .nav-btn {
            width: 40px;
            height: 40px;
            padding: 0;
            background: var(--bg-tertiary);
            backdrop-filter: blur(10px);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 1.3em;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .nav-btn:hover:not(:disabled) {
            background: var(--accent);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 16px var(--accent-glow);
        }
        
        .nav-btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        
        button.control-btn {
            padding: 12px 26px;
            font-size: 0.95em;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 600;
        }
        
        .btn-evaluate {
            background: var(--accent);
            color: white;
            box-shadow: 0 4px 16px var(--accent-glow);
        }
        
        .btn-evaluate:hover {
            background: var(--accent-hover);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px var(--accent-glow);
        }
        
        .btn-evaluate:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .feedback {
            margin-top: 20px;
            padding: 14px 18px;
            border-radius: 12px;
            font-size: 1em;
            text-align: center;
            font-weight: 600;
        }
        
        .feedback.correct {
            background: rgba(16, 185, 129, 0.15);
            color: var(--success);
            border: 2px solid var(--success);
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
        }
        
        .feedback.incorrect {
            background: rgba(239, 68, 68, 0.15);
            color: var(--error);
            border: 2px solid var(--error);
            box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);
        }
        
        .hidden {
            display: none;
        }
        
        .no-questions {
            text-align: center;
            padding: 60px 20px;
            color: var(--text-secondary);
            font-size: 1.1em;
        }
        
        .footer {
            width: 100%;
            padding: 16px 24px;
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.85em;
            margin-top: 40px;
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 8px;
            flex-wrap: wrap;
        }
        
        .footer-link {
            color: var(--accent);
            text-decoration: none;
            transition: all 0.2s;
        }
        
        .footer-link:hover {
            color: var(--accent-hover);
            text-decoration: underline;
            text-shadow: 0 0 10px var(--accent-glow);
        }
        
        .footer p {
            margin: 0;
        }
        
        @media (max-width: 968px) {
            body {
                font-size: calc(15px * var(--text-size));
            }
            
            .main-container {
                padding: 20px 10px;
            }
            
            .stats-bar {
                padding: 12px 16px;
            }
            
            .logo {
                font-size: 1.2em;
            }
            
            .stats-left,
            .stats-right {
                width: 100%;
                justify-content: space-between;
            }
            
            .stat-item {
                padding: 6px 10px;
            }
            
            .glass-card {
                padding: 24px 20px;
            }
            
            .controls-top {
                padding: 12px 16px;
                flex-direction: column;
                align-items: flex-start;
            }
            
            .controls-bottom {
                padding: 16px;
                flex-direction: column;
            }
            
            .nav-arrows {
                width: 100%;
                justify-content: center;
            }
            
            .btn-evaluate {
                width: 100%;
            }
            
            .answer-row {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
            
            .answer-buttons {
                margin-right: 0;
                width: 100%;
                justify-content: center;
            }
            
            .answer-text {
                width: 100%;
                text-align: center;
            }
            
            .footer {
                padding: 12px 16px;
                margin-top: 20px;
                font-size: 0.8em;
            }
            
            .footer-links {
                flex-direction: column;
                gap: 8px;
                margin-bottom: 6px;
            }
        }
    </style>
</head>
<body data-theme="dark">
    <div class="welcome-overlay" id="welcomeOverlay">
        <div class="welcome-modal">
            <div class="logo">MARNOST</div>
            <h2>BI-MA2 Kvíz</h2>
            <ul>
                <li><strong>Vyberte kategorii k procvičování</strong> v nastavení</li>
                <li>
  <strong>Na případné chyby v přepisu prosím vytvořte issue</strong>
  <a href="https://github.com/skopevoj/ma2-tryhard/issues">https://github.com/skopevoj/ma2-tryhard/issues</a>
</li>
                <li><strong>Používejte šipky</strong> (← →) pro navigaci mezi otázkami</li>
            </ul>
            <button class="welcome-btn" onclick="closeWelcome()">Rozumím, začít kvíz</button>
        </div>
    </div>

    <div class="settings-modal" id="settingsModal">
        <div class="settings-content">
            <div class="settings-header">
                <h2>Nastavení</h2>
                <button class="close-settings" onclick="closeSettings()">×</button>
            </div>
            <div class="settings-body">
                <div class="settings-section">
                    <h3>Motiv</h3>
                    <div class="theme-buttons">
                        <button class="theme-btn active" onclick="setTheme('dark')">Tmavý</button>
                        <button class="theme-btn" onclick="setTheme('light')">Světlý</button>
                        
                    </div>
                </div>
                
                <div class="settings-section">
                    <h3>Velikost textu</h3>
                    <div class="text-size-control">
                        <span class="text-size-label" id="textSizeLabel">Normální</span>
                        <input type="range" min="0.8" max="1.4" step="0.1" value="1" class="text-size-slider" id="textSizeSlider" oninput="changeTextSize(this.value)">
                    </div>
                </div>
                
                <div class="settings-section">
                    <h3>Kategorie</h3>
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
        </div>
    </div>

    <div class="main-container">
        <div class="page-wrapper">
            <div class="stats-bar">
                <div class="stats-left">
                    <div class="logo">MARNOST</div>
                    <button class="settings-btn" onclick="openSettings()" title="Nastavení">⚙️</button>
                </div>
                <div class="stats-right">
                    <div class="stat-item" title="Správně zodpovězené otázky">
                        <span class="stat-icon">✓</span>
                        <span class="stat-value" id="correctCount">0</span>
                    </div>
                    <div class="stat-item" title="Zobrazené otázky">
                        <span class="stat-icon">👁</span>
                        <span class="stat-value" id="answeredCount">0</span>
                    </div>
                    <div class="stat-item" title="Série chyb">
                        <span class="stat-icon">✗</span>
                        <span class="stat-value" id="wrongStreak">0</span>
                    </div>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-fraction" id="progressFraction">0 / """ + str(len(shuffled_questions)) + """</div>
                    <div class="progress">
                        <div class="progress-bar" id="sidebarProgressBar"></div>
                    </div>
                </div>
            </div>
            
            <div class="content-wrapper">
                <div class="container glass-card">
                    <div class="card-blob"></div>
                    <div class="question-container" id="questionContainer">
                        <!-- Question will be inserted here -->
                    </div>
                </div>
                
                <div class="controls glass-card">
                    <div class="card-blob"></div>
                    <div class="controls-top" id="controlsTop">
                        <!-- Category and image toggle will be inserted here -->
                    </div>
                    <div class="controls-bottom">
                        <div class="nav-arrows">
                            <button class="nav-btn" id="prevBtn" onclick="previousQuestion()" title="Předchozí otázka (←)">←</button>
                            <button class="nav-btn" id="nextBtn" onclick="skipQuestion()" title="Následující otázka (→)">→</button>
                        </div>
                        <button class="control-btn btn-evaluate" id="evaluateBtn" onclick="submitAnswer()">Vyhodnotit</button>
                    </div>
                </div>
                
                <div class="footer">
                    <div class="footer-links">
                        <a href="https://github.com/skopevoj/ma2-tryhard" class="footer-link" target="_blank">GitHub</a>
                        <a  class="footer-link">Discord: @darkkw</a>
                    </div>
                </div>
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
            sessionStorage.setItem('welcomeClosed', 'true');
        }
        
        function openSettings() {
            document.getElementById('settingsModal').classList.add('visible');
        }
        
        function closeSettings() {
            document.getElementById('settingsModal').classList.remove('visible');
        }
        
        function setTheme(theme) {
            document.body.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            
            document.querySelectorAll('.theme-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
        }
        
        function changeTextSize(value) {
            document.documentElement.style.setProperty('--text-size', value);
            localStorage.setItem('textSize', value);
            
            const labels = ['Velmi malý', 'Malý', 'Normální', 'Velký', 'Velmi velký', 'Extra velký', 'Maximální'];
            const index = Math.round((value - 0.8) / 0.1);
            document.getElementById('textSizeLabel').textContent = labels[index] || 'Normální';
            
            if (window.MathJax) {
                MathJax.typesetClear();
                MathJax.typesetPromise().catch((err) => console.log('MathJax error:', err));
            }
        }
        
        function shuffleQuestions() {
            filteredQuestions.sort(() => Math.random() - 0.5);
            currentQuestion = 0;
            userAnswers = [];
            renderQuestion();
            closeSettings();
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
            correctCount = 0;
            answeredCount = 0;
            wrongStreak = 0;
            
            updateProgressFraction();
            
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
        
        function updateProgressFraction() {
            document.getElementById('progressFraction').textContent = `${correctCount} / ${filteredQuestions.length}`;
        }

        function renderQuestion() {
            if (filteredQuestions.length === 0) {
                document.getElementById('questionContainer').innerHTML = 
                    '<div class="no-questions">Vyberte alespoň jednu kategorii pro trénování.</div>';
                document.getElementById('controlsTop').innerHTML = '';
                return;
            }

            const q = filteredQuestions[currentQuestion];
            const container = document.getElementById('questionContainer');
            const controlsTop = document.getElementById('controlsTop');
            
            // Render question with image at top if exists
            let html = '';
            if (q.image) {
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
            
            // Render controls top
            let controlsHtml = `<div class="category">${q.category || 'Matematika'}</div>`;
            if (q.image) {
                controlsHtml += `<button class="toggle-image-btn" onclick="toggleImage()">Zobrazit původní otázku</button>`;
            }
            controlsTop.innerHTML = controlsHtml;
            
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
            document.getElementById('sidebarProgressBar').style.width = `${progressPercent}%`;
            updateProgressFraction();
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
            feedback.textContent = allCorrect ? '✓ Správně!' : '✗ Špatně';
            document.getElementById('questionContainer').appendChild(feedback);
            
            updateStats();
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
        
        // Add keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (document.getElementById('settingsModal').classList.contains('visible') || 
                !document.getElementById('welcomeOverlay').classList.contains('hidden')) {
                return;
            }
            
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                if (currentQuestion > 0) {
                    previousQuestion();
                }
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                if (currentQuestion < filteredQuestions.length - 1) {
                    skipQuestion();
                }
            }
        });
        
        // Close settings modal when clicking outside
        document.getElementById('settingsModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeSettings();
            }
        });
        
        // Load saved preferences
        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            document.body.setAttribute('data-theme', savedTheme);
            
            const savedTextSize = localStorage.getItem('textSize') || '1';
            document.getElementById('textSizeSlider').value = savedTextSize;
            changeTextSize(savedTextSize);
            
            // Always show welcome on refresh (check sessionStorage instead of localStorage)
            const welcomeClosed = sessionStorage.getItem('welcomeClosed');
            if (welcomeClosed) {
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
    output_folder = Path("./questions")
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
    
    # Create Dockerfile
    dockerfile_content = """FROM nginx:alpine

# Copy the HTML file and images to nginx html directory
COPY index.html /usr/share/nginx/html/
COPY images /usr/share/nginx/html/images

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
"""
    with open(build_folder / "Dockerfile", 'w', encoding='utf-8') as f:
        f.write(dockerfile_content)
    
    # Create nginx.conf
    nginx_conf = """server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript application/json image/svg+xml;

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Serve index.html for all routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
"""
    with open(build_folder / "nginx.conf", 'w', encoding='utf-8') as f:
        f.write(nginx_conf)
    
    # Create .dockerignore
    dockerignore = """.git
.gitignore
*.md
.DS_Store
Thumbs.db
"""
    with open(build_folder / ".dockerignore", 'w', encoding='utf-8') as f:
        f.write(dockerignore)
    
    print(f"✓ Generated build/index.html with {len(questions)} questions")
    print(f"✓ Copied images to build/images/")
    print(f"✓ Created Dockerfile and nginx.conf for deployment")
    print(f"\nTo deploy on Railway:")
    print(f"1. cd build")
    print(f"2. Connect your Railway project")
    print(f"3. Railway will automatically detect and build the Dockerfile")

if __name__ == "__main__":
    main()
