import os
import json
import pdfplumber
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Research
from transformers import pipeline
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# AI Detector setup
ai_detector = pipeline(
    "text-classification",
    model=os.path.join(settings.BASE_DIR, "models/roberta-base-openai-detector"),
    device=-1
)

# DeepSeek client
deepseek_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


@login_required
def dashboard(request):
    researches = Research.objects.filter(user=request.user)
    print("Researches:", researches)  # Debug print
    return render(request, 'core/dashboard.html', {'researches': researches})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'core/register.html', {'form': form})
    return render(request, 'core/register.html', {'form': UserCreationForm()})


@login_required
def upload_research(request):
    if request.method == 'POST':
        try:
            research_file = request.FILES['file']
            if not research_file.name.endswith('.pdf'):
                return render(request, 'core/upload.html', {'error': 'Only PDF files are allowed'})

            research = Research.objects.create(user=request.user, file=research_file)

            with pdfplumber.open(research.file.path) as pdf:
                pdf_text = "\n".join([page.extract_text() for page in pdf.pages])

                # Check AI content
                research.ai_probability = check_ai_content(pdf_text)

                # Extract basic metadata
                if pdf.pages:
                    first_page = pdf.pages[0].extract_text()
                    if first_page:
                        research.title = first_page.split('\n')[0][:255]

            research.save()
            return redirect('summarize', research_id=research.id)

        except Exception as e:
            return render(request, 'core/upload.html', {'error': str(e)})

    return render(request, 'core/upload.html')


def check_ai_content(text):
    result = ai_detector(text[:1000])[0]
    return result['score'] if result['label'] == 'AI' else 1 - result['score']


def summarize_research(request, research_id):
    research = Research.objects.get(id=research_id)
    return render(request, 'core/summary.html', {'research': research})


def stream_summary(request, research_id):
    research = Research.objects.get(id=research_id)

    def generate():
        with pdfplumber.open(research.file.path) as pdf:
            pdf_text = "\n".join([page.extract_text() for page in pdf.pages])

        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": """Generate structured summary with proper markdown formatting:
    # Title
    [Title]

    - **Date**: [Date]
    - **Location**: [Location]
    - **Keywords**: [Keyword1, Keyword2]
    - **Abstract**: [Abstract text]

    ## Detailed Summary
    [Detailed summary text]

    Use proper spacing around punctuation and markdown syntax."""},
                {"role": "user", "content": f"Research content:\n{pdf_text}"},
            ],
            stream=True
        )

        buffer = ''
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                # Handle markdown formatting
                # content = content.replace('**', ' **').replace('  **', ' **')
                # content = content.replace('####', '#### ')
                # content = content.replace('###', '### ')
                # content = content.replace('##', '## ')
                # content = content.replace('#', '# ')

                # Split into meaningful chunks
                for char in content:
                    if char in [' ', '\n', '*', '#', ':'] and buffer:
                        yield f"data: {json.dumps({'content': buffer})}\n\n"
                        buffer = ''
                    buffer += char

                if buffer:
                    yield f"data: {json.dumps({'content': buffer})}\n\n"
                    buffer = ''

    return StreamingHttpResponse(generate(), content_type='text/event-stream')


@csrf_exempt
def translate_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')

        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Translate the text to the Chinese language"},
                {"role": "user", "content": f"Translate: {text}"},
            ]
        )

        return JsonResponse({'translation': response.choices[0].message.content})

    return JsonResponse({'error': 'Invalid request'}, status=400)