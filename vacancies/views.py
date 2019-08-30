from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import math
from .models import Vacancy, UserProfile
from .forms import SortFilterForm
from datetime import timedelta, datetime, timezone


def scape_page_html(url):

    # open html-page and return
    uClient = urlopen(url)
    page_html = uClient.read()
    uClient.close()

    # create object of soup
    soup = BeautifulSoup(page_html, 'lxml')

    return soup


def get_data_page_dou(url):

    # create object of soup with function
    soup = scape_page_html(url)
    # find all vacancies for junior python developer
    lis = soup.find('div', id='vacancyListId').find('ul', class_='lt').find_all('li', class_='l-vacancy')
    print(len(lis))

    for li in lis:
        try:
            # find title of vacancy
            title = li.find('a', class_="vt").text.strip()
        except:
            title = ''

        try:
            # get a link
            url = li.find('a', class_="vt").get('href')
        except:
            url = ''

        try:
            # get a company who propose
            company = li.find('a', class_="company").text.strip()
        except:
            company = ''

        try:
            # get a city
            city = li.find('span', class_="cities").text
        except:
            city = ''

        new_vacancy = Vacancy()
        new_vacancy.title = title
        new_vacancy.url = url
        new_vacancy.company = company
        new_vacancy.city = city
        new_vacancy.save()


def get_data_page_djinni(url):

    # create object of soup with function
    soup = scape_page_html(url)
    # find all vacancies for junior python developer
    lis = soup.find('ul', class_='list-unstyled list-jobs').find_all('li', class_='list-jobs__item')
    print(len(lis))

    for li in lis:
        try:
            # find title of vacancy
            title = li.find('div', class_='list-jobs__title').find('a',
                                                                   class_="profile").text.strip()
        except:
            title = ''

        try:
            # get a link
            url = 'https://djinni.co' + li.find('div', class_='list-jobs__title').find('a', class_="profile").get(
                'href')
        except:
            url = ''

        try:
            # get a company which propose job and city
            a_company = li.find('div', class_="list-jobs__details").find_all('a')[1].next_element.next_element
            a_city = a_company.next_element.next_element.strip()

            # try to find a words without symbols
            a_company = a_company.strip().replace('\n', '')
            a_company = re.findall(r'\w+', a_company)
            a_city = re.findall(r'\w+', a_city)

            # make sure that name of company is correct and here after 'at' or 'in'
            for i in range(len(a_company)):
                if a_company[i] == 'at' or a_company[i] == 'в':
                    result = a_company[i + 1:]

            # make our reselt a string
            a_company_result = ''
            for i in range(len(result)):
                a_company_result += str(result[i]).upper()
                if i + 1 < len(result):
                    a_company_result += ' '

            # make pur results a string
            a_city_result = ''
            for j in range(len(a_city)):
                a_city_result += str(a_city[j])
                if j + 1 < len(a_city):
                    a_city_result += ','

            company = a_company_result
            city = a_city_result

        except:
            company = ''
            city = ''

        new_vacancy = Vacancy()
        new_vacancy.title = title
        new_vacancy.url = url
        new_vacancy.company = company
        new_vacancy.city = city
        new_vacancy.save()


def get_data_page_rabota(url):

    # create object of soup
    soup = scape_page_html(url)
    # find all vacancies for junior python developer
    lis = soup.find('table', class_='f-vacancylist-tablewrap').find_all('article', class_='f-vacancylist-vacancyblock')
    print(len(lis))

    for li in lis:
        try:
            # find title of vacancy
            title = li.find('a', class_="f-visited-enable ga_listing").text.strip()
        except:
            title = ''

        try:
            # get a link
            url = 'https://rabota.ua' + li.find('a', class_="f-visited-enable ga_listing").get('href')
        except:
            url = ''

        try:
            # get a company who propose
            company = li.find('a', class_="f-text-dark-bluegray f-visited-enable").text.strip()
        except:
            company = ''

        try:
            # get a city
            city = li.find('div', class_="f-vacancylist-characs-block fd-f-left-middle").find('p',
                                                                                              class_='fd-merchant').text.strip()
            print(city)
        except:
            city = ''

        new_vacancy = Vacancy()
        new_vacancy.title = title
        new_vacancy.url = url
        new_vacancy.company = company
        new_vacancy.city = city
        new_vacancy.save()


def scrape(request):
    user_p = UserProfile.objects.filter(user=request.user).first()
    user_p.last_scape = datetime.now(timezone.utc)
    user_p.save()
    vacancies = Vacancy.objects.all().delete()
    get_data_page_dou('https://jobs.dou.ua/vacancies/?category=Python&exp=0-1')
    get_data_page_djinni('https://djinni.co/jobs/?exp_level=no_exp&primary_keyword=Python')
    get_data_page_rabota('https://rabota.ua/jobsearch/vacancy_list?rubricIds=439&parentId=1&profLevelIDs=2')

    return redirect('/')


def base_view(request):

    user_p = UserProfile.objects.filter(user=request.user).first()
    now = datetime.now(timezone.utc)
    time_difference = now - user_p.last_scape
    time_difference_in_minutes = time_difference / timedelta(minutes=60)
    next_scrape = 24 - time_difference_in_minutes
    if time_difference_in_minutes <= 24:
        hide_me = True
    else:
        hide_me = False
        vacancies = Vacancy.objects.all().delete()

    # next_scrape = 50
    # hide_me = True
    vacancies = Vacancy.objects.all()
    sites = ['dou', 'djinni', 'rabota']
    form_filter = SortFilterForm(request.GET)
    list_of_cities = [['Киев', 'Київ'], ['Львов', 'Львів'], ['Харків', 'Харьков'], ['віддалена робота', 'удаленно']]
    if form_filter.is_valid():

        if form_filter.cleaned_data['ordering_by_site'] == 'Все сайты':
                vacancies = vacancies
        else:
            vacancies = vacancies.filter(url__icontains=form_filter.cleaned_data['ordering_by_site'])

        if form_filter.cleaned_data['ordering_by_city']:

            if form_filter.cleaned_data['ordering_by_city'] == 'Все':
                vacancies = vacancies
            for cities in list_of_cities:
                if form_filter.cleaned_data['ordering_by_city'] in cities:
                    vacancies = vacancies.filter(city__in=cities)
                if form_filter.cleaned_data['ordering_by_city'] == 'другие города':
                    vacancies = vacancies.exclude(city__in=cities)

    context = {
        'vacancies': vacancies,
        'form_filter': form_filter,
        'hide_me': hide_me,
        'next_scrape': math.ceil(next_scrape),
        'sites': sites,
    }

    return render(request, 'base.html', context)