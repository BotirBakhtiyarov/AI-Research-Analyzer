# Research Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1.7-green.svg)](https://www.djangoproject.com/)

**Research Analyzer** is an open-source Django web application designed to streamline the process of uploading, analyzing, and summarizing research documents in PDF format. Leveraging AI technologies, it detects AI-generated content using a RoBERTa-based model and generates structured summaries with the DeepSeek API. This tool is ideal for researchers, students, and professionals who need to efficiently process and understand academic papers.

## Features

- **User Authentication**: Secure registration, login, and logout functionality.
- **PDF Upload**: Upload research PDFs for analysis and summarization.
- **AI Content Detection**: Uses `roberta-base-openai-detector` to estimate AI-generated content probability.
- **Structured Summaries**: Generates markdown-formatted summaries streamed in real-time via the DeepSeek API.
- **Text Translation**: Translates text to Chinese using DeepSeek's language model.
- **Dashboard**: View and manage uploaded research documents.
- **Open Source**: Free to use, modify, and contribute to under the MIT License.

## Project Structure

```
research_analyzer/
├── research_analyzer/        # Django project settings
│   ├── settings.py
│   └── ...
├── core/                    # Main application logic
│   ├── models/              # Model directory
│   │   └── roberta-base-openai-detector/  # AI detection model
│   ├── models.py            # Database models
│   ├── views.py             # Application views
│   └── ...
├── templates/               # HTML templates
│   ├── research/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── summary.html
├── static/                  # Static files (CSS, JS, images)
├── media/                   # Uploaded files storage
└── .env                     # Environment variables
```

## Prerequisites

- Python 3.8 or higher
- Django 5.1.7
- Git

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/BotirBakhtiyarov/AI-Research-Analyzer.git
   cd AI-Research-Analyzer
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Example `requirements.txt`:
   ```
   django==5.1.7
   pdfplumber==0.11.4
   transformers==4.44.2
   openai==1.50.2
   python-dotenv==1.0.1
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory with your DeepSeek API key:
   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   ```

5. **Set Up the AI Detection Model:**
   Download the `roberta-base-openai-detector` model from [Hugging Face](https://huggingface.co/openai-community/roberta-base-openai-detector) and place it in `core/models/roberta-base-openai-detector/`. Alternatively, the `transformers` library can fetch it automatically on first run.

6. **Apply Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a Superuser (Optional):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Usage

1. **Register** or **log in** to access the dashboard.
2. **Upload** a PDF research document through the upload interface.
3. The application will:
   - Analyze the document for AI-generated content.
   - Extract basic metadata (e.g., title).
   - Generate a detailed, markdown-formatted summary.
4. View the summary on the summary page or translate text to Chinese as needed.

## Configuration

- **Debug Mode**: Set `DEBUG = False` in `settings.py` for production.
- **Allowed Hosts**: Update `ALLOWED_HOSTS` in `settings.py` for deployment.
- **Database**: SQLite is used by default; modify `DATABASES` in `settings.py` for alternatives like PostgreSQL.
- **Media Files**: Uploaded PDFs are stored in the `media/` directory.

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your feature description"
   ```
4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request with a clear description of your changes.

Please adhere to the [Code of Conduct](CODE_OF_CONDUCT.md) and follow the [Contributing Guidelines](CONTRIBUTING.md) (to be added).

## License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for details.

## Acknowledgments

- [Django](https://www.djangoproject.com/) - Web framework
- [Hugging Face Transformers](https://huggingface.co/) - AI model support
- [DeepSeek](https://www.deepseek.com/) - API for summarization and translation
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF text extraction

## Contact

For questions or suggestions, open an issue on GitHub or reach out to the maintainers at [botirbakhtiyarob@gmail.com](mailto:botirbakhtiyarob@gmail.com).

---

Happy researching! 🚀
```
