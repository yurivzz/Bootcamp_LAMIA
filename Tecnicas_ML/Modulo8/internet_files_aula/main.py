from bs4 import BeautifulSoup
import time
import requests

# Objetivo principal da aula, resgatar do site TimesJobs 
# trabalhos de alguns dias atras, que utilizam python
def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=&txtKeywords=python&txtLocation=').text

    # Instancia do obj da biblioteca BeautifulSoup
    soup = BeautifulSoup(html_text, 'lxml')

    # jobs vai receber as tags li que tem como classe clearfix job-bx wht-shd-bx
    jobs =  soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    # Input para filtrar ablidades que o usuario não é familiar
    print('Put some skill that you are not familiar with')
    unfamiliar_skill = input('>')
    print(f'Filtering out {unfamiliar_skill}')

    # laço que itera em jobs (cards de emprego)
    for index, job in enumerate(jobs):
        # filtro que contém, data que foi postado e as habilidades que o usuario não é familiar
        publish_date = job.find('span', class_='sim-posted').span.text
        skills = job.find('span', class_='srp-skills').text.replace(' ','').strip()
        if 'few' in publish_date and unfamiliar_skill not in skills:
            # passando o filtro, o resto dos valores é coletado
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ','').strip()
            link = job.header.h2.a['href']
            # escrita dos dados em arquivos, para futuro acesso
            with open(f'posts/{index}.txt', 'w') as f:
                f.write(f'Company name: {company_name}\nRequired Skills: {skills}\nMore info: {link}')

            print(f'file saved {index}')


# automação para realizar o scrapping de 10 em 10 minutos (outra alternativa seria utilizar um daemon)
if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait*60)





