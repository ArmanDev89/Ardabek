from django.shortcuts import render, redirect
import json
import openai
from django.contrib import auth
from django.contrib.auth.models import User

from django.utils import timezone

openai_api_key = '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'  # Replace YOUR_API_KEY with your openai apikey
openai.api_key = openai_api_key


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

    # Обработка данных формы
    elif request.method == 'POST':
        topic = request.POST.get('topic')
        request.session['topic'] = topic
        return redirect('generate')


def generate(request):
    topic = request.session.get('topic', '')
    prompt = f'сгенерируй 6 универсальных и уникальных идей с необычным геймплеем для образовательных на русском языке игр по теме {topic} чтобы можно было поиграть в классе с учениками, игра должна быть реализуема в рамках обычного класса и не должна использовать дополнительные вещи как виртуальная реальность, программы построения лабиринты и тд. Напиши ответ  в точном формате словаря со словарями файла без лишних слов и символов с ключами используй только словари Name. Detailed description of game, Detailed discription of game rules'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    ideas = response['choices'][0]['message']['content']
    ideas = json.loads(ideas)
    # Преобразование ответа в список словарей

    return render(request, 'generate.html', {'ideas': ideas})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('index')
            except:
                error_message = 'Error creating account'
            return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = "Password don't match"
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')







def logout(request):
    auth.logout(request)
    return redirect('login')
