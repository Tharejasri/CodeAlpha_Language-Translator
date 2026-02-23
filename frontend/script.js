// API base URL - update this to your backend URL
const API_BASE_URL = 'http://localhost:5000/api';

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    loadLanguages();
    setupEventListeners();
    
    // Add character counter
    document.getElementById('inputText').addEventListener('input', updateCharCount);
});

// Update character count
function updateCharCount() {
    const text = document.getElementById('inputText').value;
    document.getElementById('charCount').textContent = text.length + ' characters';
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('translateBtn').addEventListener('click', handleTranslate);
    document.getElementById('swapLangs').addEventListener('click', swapLanguages);
    document.getElementById('clearInput').addEventListener('click', clearInput);
    document.getElementById('copyBtn').addEventListener('click', copyToClipboard);
    document.getElementById('speakBtn').addEventListener('click', speakTranslation);
}

// Load supported languages
async function loadLanguages() {
    try {
        showLoading('Loading languages...');
        
        const response = await fetch(`${API_BASE_URL}/languages`);
        const data = await response.json();
        
        hideLoading();
        
        if (data.error) {
            showError(data.error);
            // Fallback languages if API fails
            useFallbackLanguages();
            return;
        }
        
        if (data.languages && data.languages.length > 0) {
            populateLanguageSelects(data.languages);
        } else {
            useFallbackLanguages();
        }
    } catch (error) {
        hideLoading();
        showError('Failed to load languages. Using default languages.');
        console.error('Error:', error);
        useFallbackLanguages();
    }
}

// Fallback languages in case API fails
function useFallbackLanguages() {
    const fallbackLanguages = [
        { code: 'en', name: 'English' },
        { code: 'es', name: 'Spanish' },
        { code: 'fr', name: 'French' },
        { code: 'de', name: 'German' },
        { code: 'it', name: 'Italian' },
        { code: 'pt', name: 'Portuguese' },
        { code: 'ru', name: 'Russian' },
        { code: 'ja', name: 'Japanese' },
        { code: 'ko', name: 'Korean' },
        { code: 'zh', name: 'Chinese' },
        { code: 'ar', name: 'Arabic' },
        { code: 'hi', name: 'Hindi' },
        { code: 'sr', name: 'Serbian' },
        { code: 'hr', name: 'Croatian' },
        { code: 'bs', name: 'Bosnian' },
        { code: 'nl', name: 'Dutch' },
        { code: 'el', name: 'Greek' },
        { code: 'pl', name: 'Polish' },
        { code: 'tr', name: 'Turkish' }
    ];
    
    populateLanguageSelects(fallbackLanguages);
}

// Populate language dropdowns
function populateLanguageSelects(languages) {
    const sourceSelect = document.getElementById('sourceLang');
    const targetSelect = document.getElementById('targetLang');
    
    // Clear existing options (except auto-detect)
    sourceSelect.innerHTML = '<option value="auto">Auto Detect</option>';
    targetSelect.innerHTML = '';
    
    // Sort languages by name
    languages.sort((a, b) => a.name.localeCompare(b.name));
    
    // Add language options
    languages.forEach(lang => {
        if (lang.code) {
            const option1 = document.createElement('option');
            option1.value = lang.code;
            option1.textContent = lang.name;
            sourceSelect.appendChild(option1);
            
            const option2 = document.createElement('option');
            option2.value = lang.code;
            option2.textContent = lang.name;
            targetSelect.appendChild(option2);
        }
    });
    
    // Set default selections
    targetSelect.value = 'es'; // Spanish as default target
}

// Handle translation
async function handleTranslate() {
    const inputText = document.getElementById('inputText').value;
    const sourceLang = document.getElementById('sourceLang').value;
    const targetLang = document.getElementById('targetLang').value;
    
    if (!inputText.trim()) {
        showError('Please enter text to translate');
        return;
    }
    
    // Show loading
    showLoading('Translating...');
    hideError();
    
    try {
        console.log('Sending translation request:', {
            text: inputText,
            source_lang: sourceLang,
            target_lang: targetLang
        });
        
        const response = await fetch(`${API_BASE_URL}/translate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: inputText,
                source_lang: sourceLang,
                target_lang: targetLang
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `Server error: ${response.status}`);
        }
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Display translation
        document.getElementById('outputText').textContent = data.translated_text || 'No translation returned';
        
    } catch (error) {
        showError('Translation failed: ' + error.message);
        console.error('Translation error:', error);
    } finally {
        hideLoading();
    }
}

// Swap languages
function swapLanguages() {
    const sourceSelect = document.getElementById('sourceLang');
    const targetSelect = document.getElementById('targetLang');
    
    if (sourceSelect.value !== 'auto') {
        const temp = sourceSelect.value;
        sourceSelect.value = targetSelect.value;
        targetSelect.value = temp;
        
        // Also swap the text if there's a translation
        const inputText = document.getElementById('inputText').value;
        const outputText = document.getElementById('outputText').textContent;
        
        if (outputText && outputText !== 'Translation will appear here...') {
            document.getElementById('inputText').value = outputText;
            document.getElementById('outputText').textContent = 'Translation will appear here...';
            updateCharCount();
        }
    }
}

// Clear input
function clearInput() {
    document.getElementById('inputText').value = '';
    document.getElementById('outputText').textContent = 'Translation will appear here...';
    document.getElementById('charCount').textContent = '0 characters';
    hideError();
}

// Copy to clipboard
function copyToClipboard() {
    const outputText = document.getElementById('outputText').textContent;
    
    if (outputText && outputText !== 'Translation will appear here...') {
        navigator.clipboard.writeText(outputText).then(() => {
            // Show temporary success message
            const copyBtn = document.getElementById('copyBtn');
            const originalIcon = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => {
                copyBtn.innerHTML = originalIcon;
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
            showError('Failed to copy to clipboard');
        });
    }
}

// Text to speech
function speakTranslation() {
    const outputText = document.getElementById('outputText').textContent;
    const targetLang = document.getElementById('targetLang').value;
    
    if (outputText && outputText !== 'Translation will appear here...') {
        // Stop any ongoing speech
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(outputText);
        utterance.lang = targetLang;
        utterance.rate = 0.9; // Slightly slower
        utterance.pitch = 1;
        
        window.speechSynthesis.speak(utterance);
    }
}

// Show loading
function showLoading(message = 'Loading...') {
    document.getElementById('loading').style.display = 'flex';
    document.querySelector('.loader-container p').textContent = message;
}

// Hide loading
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Hide error
function hideError() {
    document.getElementById('error').style.display = 'none';
}