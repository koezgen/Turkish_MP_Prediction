from selenium import webdriver
from bs4 import BeautifulSoup
import requests as req
import json
import os

LINK_LIST_PATH = "C:\\Users\\koezgen\\Desktop\\dir\\data\\mv_links"
TARGET_DIR = "C:\\Users\\koezgen\\Desktop\\dir\\data\\mv_jsons"
PARSED_LINKS_PATH = "C:\\Users\\koezgen\\Desktop\\dir\\data\\mv_links\\parsed_links.txt"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Ensure GUI is off, which speeds up the script
prefs = {"profile.managed_default_content_settings.images": 2, 
         "profile.default_content_settings.stylesheets": 2}
chrome_options.add_experimental_option("prefs", prefs)

session = req.Session()  # Use a session for http requests

def read_links_from_file(file_path):
    with open(file_path, 'r') as file:
        links = file.readlines()
    return links

def get_party_name(input_string):
    words = input_string.split()
    party_name = ' '.join(words[:-2])
    return party_name

def get_city_name(input_string):
    words = input_string.split()
    city_name = words[-2]
    return city_name

def extract_content_from_page(link):
    r = req.get(link)
    r.content

    parsed_data = {}
    base_url = 'https://www.tbmm.gov.tr'

    soup = BeautifulSoup(r.content, 'html.parser')

    profile = soup.find('div', {'class': 'col-8'})
    name = profile.find('div', {'id': 'milletvekili-adi'}).text.strip()
    term_text = profile.find('div', {'id': 'milletvekili-donem'}).text.strip()
    term = int(term_text.split('.')[0])
    city_party = profile.find('div', {'id': 'milletvekili-sehir'}).text.strip()
    party_name = get_party_name(city_party)
    city_name = get_city_name(city_party)

    parsed_data["name"] = name
    parsed_data["term"] = term
    parsed_data["party"] = party_name
    parsed_data["city"] = city_name

    general_list = soup.find('div', {'class': 'col-lg-8 col-md-12'})
    general_list = general_list.find('div', {'id': 'adres-alani'})
    general_list = general_list.find('div', {'class': 'col-md-12 generic-list-div'})
    # .find('ul').find_all('li')
    list_names = ['kanun_teklif_ilk', 'kanun_teklif', 'soru_önergeleri_yazili', 'soru_onergeleri_sozlu', 'genel_gorusme_ilk', 'genel_gorusme',
                  'mec_sorusturma_ilk', 'mec_sorusturma', 'mec_arastirma_ilk',
                  'mec_arastirma', 'gensoru_ilk', 'gensoru', ]

    base_url2 = "https://www.tbmm.gov.tr/milletvekili/"
    for i in range(0, len(list_names)):

        if term == 27 and i in [3, 10, 11]:
            parsed_data[list_names[i]] = 0

        else:
            href_address = general_list.find_all('a')[i]
            href_address = href_address.get('href')
            print(href_address)
            soup = BeautifulSoup(req.get(base_url2 + href_address).content, 'html.parser')
            div_element = soup.find('div', {'class': 'blog-content tbmm-div-list'})

            driver = webdriver.Chrome(options=chrome_options)

            driver.get(base_url2 + href_address)
            html_code2 = driver.page_source
            driver.quit()

            soup = BeautifulSoup(html_code2, 'html.parser')
            mecTable_wrapper = soup.find('div',
                                        {'id': 'mecTable_wrapper', 'class': 'dataTables_wrapper dt-bootstrap4 no-footer'})
            txt = mecTable_wrapper.find('div', {'class': 'dataTables_info'}).text.strip()
            ##txt=txt[:2]
            words = txt.split()
            first_two_words = " ".join(words[:2])

            if first_two_words != "Kayıt yok":
                count = first_two_words.split()[0]
                if (count.find(",")):
                    count = int(first_two_words.replace(',', '').split()[0])

                print(count)
            else:
                count = 0
                #print(count)

            parsed_data[list_names[i]] = count

    return parsed_data

def process_file(file_path):
    # Define the extraction path based on the original file name
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    extraction_path = os.path.join(TARGET_DIR, f"{file_name}.txt")

    try:
        links = read_links_from_file(file_path)

        for link in links:
            link = link.strip()  # Remove newline characters
            parsed_data = extract_content_from_page(link)

            # Save the parsed data to the extraction file
            with open(extraction_path, "a", encoding="utf-8") as f:
                f.write("{}\n".format(json.dumps(parsed_data, ensure_ascii=False)))

    except Exception as e:
        print(f"Failed to parse page. Error: {e}")

def parse_html_pages(LINK_LIST_PATH, TARGET_DIR, PARSED_LINKS_PATH):
    # Ensure target directory exists; if not, create it
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    # Get list of all files in the LINK_LIST_PATH
    files_list = [os.path.join(LINK_LIST_PATH, file) for file in os.listdir(LINK_LIST_PATH) if os.path.isfile(os.path.join(LINK_LIST_PATH, file))]

    # Create the parsed links file if it doesn't exist, or load the parsed links from file
    parsed_links = set()
    if os.path.exists(PARSED_LINKS_PATH):
        with open(PARSED_LINKS_PATH, 'r') as f:
            parsed_links = set(line.strip() for line in f)
    else:
        with open(PARSED_LINKS_PATH, 'w') as f:
            pass

    # Create a single driver instance to be used by all calls to extract_content_from_page()
    driver = webdriver.Chrome()

    try:
        for file_path in files_list:
            links = read_links_from_file(file_path)
            extraction_path = os.path.join(TARGET_DIR, f"{os.path.basename(file_path)}")

            for link in links:
                link = link.strip()  # Remove newline characters
                if link not in parsed_links:
                    try:
                        parsed_data = extract_content_from_page(link)
                        parsed_links.add(link)

                        # Save the link to the file immediately after parsing
                        with open(PARSED_LINKS_PATH, 'a') as f:
                            f.write('\n' + link + '\n')

                        # Check if the file already exists, if not create a new one
                        if not os.path.isfile(extraction_path):
                            with open(extraction_path, "w", encoding="utf-8") as f:
                                f.write("{}\n".format(json.dumps(parsed_data, ensure_ascii=False)))
                        else:
                            with open(extraction_path, "a", encoding="utf-8") as f:
                                f.write("{}\n".format(json.dumps(parsed_data, ensure_ascii=False)))

                    except Exception as e:
                        print(f"Failed to parse page {link}. Error: {e}")
                        with open(PARSED_LINKS_PATH, 'a') as f:
                            f.write(f"{link} ------ LINK WAS NOT PARSED DUE TO AN UNKNOWN ERROR ------\n")

    except Exception as e:
        print(f"Failed to parse page. Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    parse_html_pages(LINK_LIST_PATH, TARGET_DIR, PARSED_LINKS_PATH)