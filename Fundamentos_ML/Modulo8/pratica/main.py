from bs4 import BeautifulSoup
import requests

# Projeto simples que realiza o scrapping no site Wheater.com, para a cidade de Brasilia e extrai informações e previões do clima para o dia

def get_wheater():
    # realizando o scrapping no site weather.com
    html_text = requests.get('https://weather.com/pt-BR/clima/hoje/l/BRXX0043:1:BR?Goto=Redirected').text 
    soup = BeautifulSoup(html_text, 'lxml')

    # Temperatura e qualiadde do ar
    current_temp = soup.find('span', class_='CurrentConditions--tempValue--MHmYY').text
    air_quality = soup.find('text', class_='DonutChart--innerValue--3_iFF').text

    # previsoes para manha, tarde e noite
    prevs = soup.find_all('li', class_='Column--column--3tAuz Column--verticalStack--28b4K')
    daytime = []
    for index, prev in enumerate(prevs):
        daytime.append([])
        # Tempo da previsão
        daytime[index].append(prev.find('span', class_='Ellipsis--ellipsis--3ADai').text)
        # Previsão de temperatura
        daytime[index].append(prev.find('div', class_='Column--temp--1sO_J Column--verticalStack--28b4K').span.text)
        # Probabiliade de chuva
        daytime[index].append(prev.find('span', class_='Column--precip--3JCDO').text.replace('Probabilidade de chuva',''))
        # Clima
        daytime[index].append(prev.find('svg', class_='Column--weatherIcon--2w_Rf Icon--icon--2aW0V Icon--fullTheme--3Fc-5').text)
        if(index == 2):
            break

    print(f'Temperatura: {current_temp}')
    print(f'Qualidade do ar: {air_quality}')
    for i in daytime:
        print(f'Tempo da previsão: {i[0]}')
        print(f'Temperatura prevista: {i[1]}')
        print(f'Probabilidade de chuva: {i[2]}')
        print(f'Clima: {i[3]}\n')



if __name__ == '__main__':
    get_wheater()