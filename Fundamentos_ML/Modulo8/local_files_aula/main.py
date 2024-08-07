# Importando o pacote
from bs4 import BeautifulSoup

# Abrindo o arquivo home.html em modo de leitura, retirado 
# do repositorio do curso
with open('home.html', 'r') as html_file:
    # Armazenando o conteudo lido em uma variavel chamada content
    content = html_file.read()

    # Criação da instancia do HTML "extruturado", utilizando 
    # o parser LXML(para HTML e)
    soup = BeautifulSoup(content, 'lxml')
    
    # função que mostra o HTML identado, bonito
    # print(soup.prettify())

    # Função que busca o primeiro elemento (nesse caso tag)
    # dentro do HTML
    # tags = soup.find('h5')

    # Retorna uma lista com todos os elementos que foram buscados
    # dentro do HTML (tem parametro para limitar)
    # tags = soup.find_all('h5')

    # # Encontrado todos os cursos dentro do arquivo
    # courses_html_tags = soup.find_all('h5')
    # for course in courses_html_tags:
    #     # Função que extrai apenas o texto das tags
    #     print(course.text)

    # Encontrando as tags div, com a classe card
    course_cards = soup.find_all('div', class_='card')

    # Iterando nas divs
    for course in course_cards:
        # É possivel utilizar atributos para selecionar o conteudo diretamente
        course_name = course.h5.text
        course_price = course.a.text.split()[-1]

        print(f'Nome: {course_name}\nPreco: {course_price}\n')