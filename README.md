# ArabicOCR

A full-stack web application for extracting, translating, and transliterating Arabic text from images and PDFs.

## Features

- **File Upload**: Support for PDF (multi-page) and image files (PNG, JPG, JPEG)
- **OCR Engine Selection**: Choose between Qari-OCR (local), Mistral OCR (API), or both
- **Arabic Text Extraction**: Maintain proper Arabic script rendering with UTF-8 support
- **Post-Processing**:
  - Translation: Arabic → English (or other languages) using OpenAI GPT-4o or Google Translate
  - Transliteration: Arabic → Latin script
- **Output Download**: Generate a .docx file with original text, translation, and transliteration
- **Responsive UI**: Clean, modern interface built with TailwindCSS

## Tech Stack

- **Backend**: Python (FastAPI)
- **Frontend**: HTML, TailwindCSS, JavaScript
- **OCR**: Qari-OCR (local) + Mistral OCR (API)
- **Translation**: OpenAI GPT-4o API or Google Translate API
- **Transliteration**: Python Arabic transliteration libraries
- **PDF Processing**: pdf2image + Poppler
- **Document Export**: python-docx
- **Deployment**: Docker

## Setup Instructions

### Prerequisites

- Python 3.9+
- Docker and Docker Compose (for containerized deployment)
- Poppler (for PDF processing)
- API keys for Mistral AI and OpenAI (or Google Translate)

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/arabic-ocr.git
   cd arabic-ocr
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install git+https://github.com/mush42/qari-ocr.git
   ```

4. Install Poppler:
   - **Windows**: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/) and add to PATH
   - **macOS**: `brew install poppler`
   - **Linux**: `apt-get install poppler-utils`

5. Create a `.env` file based on `.env.example` and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   MISTRAL_API_KEY=your_mistral_api_key_here
   TRANSLATION_SERVICE=openai  # or google
   ```

6. Run the application:
   ```bash
   python -m app.main
   ```

7. Open your browser and navigate to `http://localhost:8000`

### Docker Deployment

1. Make sure Docker and Docker Compose are installed on your system

2. Create a `.env` file based on `.env.example` with your API keys

3. Build and start the Docker container:
   ```bash
   docker-compose up -d --build
   ```

4. Access the application at `http://localhost:8000`

## API Endpoints

- **POST /api/ocr/upload**: Upload and process files with OCR
- **POST /api/translation/translate**: Translate Arabic text
- **POST /api/translation/transliterate**: Transliterate Arabic text to Latin script
- **POST /api/export/docx**: Generate and download a DOCX file

## Cloud Deployment

The application can be deployed to various cloud platforms:

### Railway

1. Create a new project on [Railway](https://railway.app/)
2. Connect your GitHub repository
3. Add environment variables from `.env.example`
4. Deploy the application

### Render

1. Create a new Web Service on [Render](https://render.com/)
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt && pip install git+https://github.com/mush42/qari-ocr.git`
4. Set the start command: `python -m app.main`
5. Add environment variables from `.env.example`

### AWS EC2

1. Launch an EC2 instance
2. Install Docker and Docker Compose
3. Clone your repository
4. Create a `.env` file with your API keys
5. Run `docker-compose up -d --build`
6. Configure security groups to allow traffic on port 8000

## License

MIT

## Acknowledgements

- [Qari-OCR](https://github.com/mush42/qari-ocr) for Arabic OCR capabilities
- [Mistral AI](https://mistral.ai/) for advanced OCR API
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [TailwindCSS](https://tailwindcss.com/) for the UI design