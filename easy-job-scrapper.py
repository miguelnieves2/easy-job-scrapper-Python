from unittest import result
import requests # python3 -m pip install requests beautifulsoup4
# BeautifulSoup nos va a permitir hacer Scrapping
from bs4 import BeautifulSoup

# definir la url a la cual nosotros queremos realizar la busqueda
url = "https://www.seek.co.nz/python-jobs?salaryrange=100000-99999&salarytype=annual"

# Preguntarse si estamos ejecutando el archivo directamente
if "__main__" == __name__ :
    # llamamos a la url que creamos antes y le indicamos a "BeautifulSoup" que el contenido que nos esta devolviendo a este llamado, lo parsee 
    page = requests.get(url);
    soup = BeautifulSoup(page.content,"html.parser")

    # definir la funcion con la cual nosotros vamos a ir a buscar las etiquetas
    def has_data_search(tag):
        # en el caso de la pagina seek, cada bloque html de oferta laboral cuenta con un atributo que se llama "data-search-sol-meta", asi que lo que haremos sera buscar los elementos que contengan solo esta propiedad
        return tag.has_attr("data-search-sol-meta")
    
    # llamar al metodo de "find_all" de nuestro html ya parseado, y le pasamos la funcion que creamos "has_data_search"
    results = soup.find_all(has_data_search)

    # devolvera un listado de resultados los cuales nosotros lo vamos a iterar y le vamos a dar el nombre de job
    for job in results:
        try:
            # y vamos buscar dentro del html que acabamos de obtener, un elemento "a" que contenga el atributo "data-automation" y que su valor sea "jobTitle", ahi es donde se encuentra el titulo de la oferta laboral
            titleElement = job.find("a", attrs={"data-automation": "jobTitle"})

            title = titleElement.get_text()
            company = job.find("a", attrs={"data-automation": "jobCompany"}).get_text()
            joblink = "https://www.seek.co.nz" + titleElement["href"]
            salary = job.find("span", attrs={"data-automation": "jobSalary"})
            salary = salary.get_text() if salary else 'n/a'

            # Construir un String en cual le estamos indicando el titulo de la oferta laboral, le empezamos a pasar el titulo, empresa, salario y link de la empresa

            job = "Titulo: {}\nEmpresa: {}\nSalario: {}\nLink: {}a\n" 
            # Lo formateamos
            job = job.format(title, company, salary, joblink);

            print(job)
        except Exception as e:
            print("Exception: {}".format(e))
            pass