/**
 * ArabicOCR - Main JavaScript
 * Handles file uploads, API calls, and UI interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const removeFileBtn = document.getElementById('remove-file');
    const uploadProgress = document.getElementById('upload-progress');
    const progressBar = document.getElementById('progress-bar');
    const progressPercentage = document.getElementById('progress-percentage');
    const processButton = document.getElementById('process-button');
    const enableTranslation = document.getElementById('enable-translation');
    const translationLanguage = document.getElementById('translation-language');
    const enableTransliteration = document.getElementById('enable-transliteration');
    const resultsSection = document.getElementById('results-section');
    const uploadSection = document.getElementById('upload-section');
    const arabicResult = document.getElementById('arabic-result');
    const translationResult = document.getElementById('translation-result');
    const transliterationResult = document.getElementById('transliteration-result');
    const exportButton = document.getElementById('export-button');
    const backButton = document.getElementById('back-button');
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingMessage = document.getElementById('loading-message');
    const translationTabItem = document.getElementById('translation-tab-item');
    const transliterationTabItem = document.getElementById('transliteration-tab-item');
    
    // State variables
    let selectedFile = null;
    let extractedText = '';
    let translatedText = '';
    let transliteratedText = '';
    
    // Initialize tabs
    initTabs();
    
    // Event Listeners
    
    // File Drop Area
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropArea.classList.add('border-indigo-500', 'bg-indigo-50');
        dropArea.classList.remove('border-gray-300');
    }
    
    function unhighlight() {
        dropArea.classList.remove('border-indigo-500', 'bg-indigo-50');
        dropArea.classList.add('border-gray-300');
    }
    
    // Handle file drop
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            handleFiles(files[0]);
        }
    }
    
    // Handle file input change
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            handleFiles(this.files[0]);
        }
    });
    
    // Remove file button
    removeFileBtn.addEventListener('click', function() {
        resetFileInput();
    });
    
    // Enable/disable translation language dropdown
    enableTranslation.addEventListener('change', function() {
        translationLanguage.disabled = !this.checked;
    });
    
    // Process button
    processButton.addEventListener('click', processFile);
    
    // Export button
    exportButton.addEventListener('click', exportToDocx);
    
    // Back button
    backButton.addEventListener('click', function() {
        resultsSection.classList.add('hidden');
        uploadSection.classList.remove('hidden');
        resetFileInput();
    });
    
    // Functions
    
    // Handle selected file
    function handleFiles(file) {
        // Check file type
        const validTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg'];
        if (!validTypes.includes(file.type)) {
            alert('Invalid file type. Please upload a PDF, PNG, or JPG file.');
            resetFileInput();
            return;
        }
        
        // Check file size (max 10MB)
        const maxSize = 10 * 1024 * 1024; // 10MB in bytes
        if (file.size > maxSize) {
            alert('File is too large. Maximum size is 10MB.');
            resetFileInput();
            return;
        }
        
        // Update UI
        selectedFile = file;
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileInfo.classList.remove('hidden');
        processButton.disabled = false;
    }
    
    // Reset file input
    function resetFileInput() {
        fileInput.value = '';
        selectedFile = null;
        fileInfo.classList.add('hidden');
        processButton.disabled = true;
        uploadProgress.classList.add('hidden');
        progressBar.style.width = '0%';
        progressPercentage.textContent = '0%';
    }
    
    // Format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Process the file
    async function processFile() {
        if (!selectedFile) return;
        
        // Show loading overlay
        loadingOverlay.classList.remove('hidden');
        loadingMessage.textContent = 'Processing file...';
        
        // Get selected OCR engine
        const ocrEngine = document.querySelector('input[name="ocr-engine"]:checked').value;
        
        // Create form data
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('engine', ocrEngine);
        
        try {
            // Upload file and process OCR
            const response = await fetch('/api/ocr/upload', {
                method: 'POST',
                body: formData,
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    uploadProgress.classList.remove('hidden');
                    progressBar.style.width = percentCompleted + '%';
                    progressPercentage.textContent = percentCompleted + '%';
                }
            });
            
            if (!response.ok) {
                throw new Error('OCR processing failed');
            }
            
            const data = await response.json();
            extractedText = data.text;
            
            // Update UI with extracted text
            arabicResult.innerHTML = formatTextWithLineBreaks(extractedText);
            
            // Process translation if enabled
            if (enableTranslation.checked) {
                loadingMessage.textContent = 'Translating text...';
                await processTranslation();
                translationTabItem.classList.remove('hidden');
            } else {
                translationTabItem.classList.add('hidden');
            }
            
            // Process transliteration if enabled
            if (enableTransliteration.checked) {
                loadingMessage.textContent = 'Transliterating text...';
                await processTransliteration();
                transliterationTabItem.classList.remove('hidden');
            } else {
                transliterationTabItem.classList.add('hidden');
            }
            
            // Show results section
            uploadSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');
            
            // Hide loading overlay
            loadingOverlay.classList.add('hidden');
            
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing the file. Please try again.');
            loadingOverlay.classList.add('hidden');
        }
    }
    
    // Process translation
    async function processTranslation() {
        try {
            const targetLanguage = translationLanguage.value;
            
            const response = await fetch('/api/translation/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: extractedText,
                    target_language: targetLanguage
                })
            });
            
            if (!response.ok) {
                throw new Error('Translation failed');
            }
            
            const data = await response.json();
            translatedText = data.translated_text;
            
            // Update UI with translated text
            translationResult.innerHTML = formatTextWithLineBreaks(translatedText);
            
        } catch (error) {
            console.error('Translation error:', error);
            translatedText = 'Translation failed: ' + error.message;
            translationResult.innerHTML = translatedText;
        }
    }
    
    // Process transliteration
    async function processTransliteration() {
        try {
            const response = await fetch('/api/translation/transliterate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: extractedText
                })
            });
            
            if (!response.ok) {
                throw new Error('Transliteration failed');
            }
            
            const data = await response.json();
            transliteratedText = data.transliterated_text;
            
            // Update UI with transliterated text
            transliterationResult.innerHTML = formatTextWithLineBreaks(transliteratedText);
            
        } catch (error) {
            console.error('Transliteration error:', error);
            transliteratedText = 'Transliteration failed: ' + error.message;
            transliterationResult.innerHTML = transliteratedText;
        }
    }
    
    // Export to DOCX
    async function exportToDocx() {
        try {
            loadingOverlay.classList.remove('hidden');
            loadingMessage.textContent = 'Generating DOCX file...';
            
            const response = await fetch('/api/export/docx', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    arabic_text: extractedText,
                    translated_text: translatedText,
                    transliterated_text: transliteratedText
                })
            });
            
            if (!response.ok) {
                throw new Error('DOCX export failed');
            }
            
            // Create a blob from the response
            const blob = await response.blob();
            
            // Create a download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'arabic_ocr_results.docx';
            
            // Append to the document and trigger the download
            document.body.appendChild(a);
            a.click();
            
            // Clean up
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            loadingOverlay.classList.add('hidden');
            
        } catch (error) {
            console.error('Export error:', error);
            alert('An error occurred while exporting to DOCX. Please try again.');
            loadingOverlay.classList.add('hidden');
        }
    }
    
    // Initialize tabs
    function initTabs() {
        const tabLinks = document.querySelectorAll('#results-tabs a');
        const tabContents = document.querySelectorAll('.tab-pane');
        
        tabLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all tabs
                tabLinks.forEach(tab => {
                    tab.classList.remove('text-indigo-600', 'border-indigo-600');
                    tab.classList.add('text-gray-500', 'border-transparent');
                });
                
                // Add active class to clicked tab
                this.classList.remove('text-gray-500', 'border-transparent');
                this.classList.add('text-indigo-600', 'border-indigo-600');
                
                // Hide all tab contents
                tabContents.forEach(content => {
                    content.classList.add('hidden');
                    content.classList.remove('active');
                });
                
                // Show the corresponding tab content
                const tabId = this.getAttribute('data-tab');
                const tabContent = document.getElementById(tabId);
                tabContent.classList.remove('hidden');
                tabContent.classList.add('active');
            });
        });
    }
    
    // Format text with line breaks for HTML display
    function formatTextWithLineBreaks(text) {
        return text.replace(/\n/g, '<br>');
    }
});