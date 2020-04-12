from django.shortcuts import render, get_object_or_404

from .models import Issue, Question, Customer
from django.core.exceptions import ObjectDoesNotExist
from bs4 import BeautifulSoup
from urllib.request import urlopen

import re
# Create your views here.
def home(request):
    return render(request, "home.html")
def issue(request):
    issue = Issue.objects
    home_crwaling()
    return render(request, 'issue.html', {'issue':issue})


def home_crwaling():
    url = "https://github.com/leewoongi/Algorithm/issues"
    html = urlopen(url)
    source = html.read()
    html.close()

    soup = BeautifulSoup(source, "html.parser")
    r = re.compile('issue_[0-9]+_link')
    title = (soup.find_all('a', {'id' : r}))

    for t in title:
        tmp = str(t.get_text())
        obj, created = Issue.objects.get_or_create(title = tmp, defaults = {'title' : tmp})


def detail(request, issue_id):
    title = get_object_or_404(Issue,pk=issue_id)
    
    detail_crwaling(title)
   
    problems = title.question_set.all()
    return render(request,'detail.html', {'title' : title , 'problems' : problems})


def detail_crwaling(title):
    tmp_title = str(title)
    title_split = tmp_title.split(' ')

    issue_num = title_split[2:]
    issue_num = (",".join(issue_num))[1:]

    url = "https://github.com/leewoongi/Algorithm/issues/" + str(issue_num)
    html = urlopen(url)
    source = html.read() 
    html.close()

    soup = BeautifulSoup(source, 'html.parser')
    questions = soup.find_all('td' , {'class' : "d-block comment-body markdown-body js-comment-body"})
    questions = questions[0]
    questions = questions.get_text().split("\n")

    print("문제")
    print(questions)
    qqq = title.question_set
    
    index= 1
    for q  in questions:
        
        obj, create = qqq.get_or_create(question = questions[index] , question_link = questions[index +1],
                                                    defaults = {'question' : questions[index], 'question_link' : questions[index+1]})
        index+=2
        if index >= len(questions) - 1:
            break

    

    #문제 푼 사람들
    print("qqqqq")
    print(qqq)
    users = soup.find_all('a' , {'class' :"author link-gray-dark text-bold" , 'data-hovercard-type':"user"})
    solves = soup.find_all('div', {'class' : "commit-message pr-1 flex-auto min-width-0" })

    size = len(users)

    users_set = set()

    for index in range(0,size):
        users_set.add(users[index].get_text())

    print("유저 이름 모음")
    print(users_set)

    uuu = title.customer_set
    
    for user in users_set:
       ojb, create = uuu.get_or_create(name = user, defaults ={'name' : user})
    
    uuu = uuu.values()
    print(uuu)

    for index in range(0,size) :
        print(users[index].get_text() + " " + solves[index].get_text())

    print(len(qqq.values()))

    cus = Customer.objects

    print(cus)
    for q in qqq.values():
        question = get_object_or_404(Question, pk = q['id'])
        print(q['id'])



def back(request):
    title = Issue.objects
    problems = title.question_set.all()
    return render(request, 'back.html', {'title': title, 'problems':problems})


def portfolio(request):
    return render(request,'portfolio.html')
    

    