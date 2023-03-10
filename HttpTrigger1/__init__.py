import json
import logging
import http3
from xml.etree.ElementTree import XML, fromstring
from bs4 import BeautifulSoup
import azure.functions as func

client = http3.Client()

def call_api(url: str):
    r = client.get(url, verify=False)
    return r.text

def humanize_text_description(description: str) -> str:
    soup = BeautifulSoup(description)
    return soup.get_text()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    result_1 = call_api("https://news.google.com/rss?hl=es-419&gl=MX&ceid=MX:es-419")
 
    my_xml = fromstring(result_1)
    results = []
    for news in my_xml.iter('item'):
        title = news.find('title').text
        link = news.find('link').text
        pub_date = news.find('pubDate').text
        description = humanize_text_description(news.find('description').text)
        results.append({'title': title, 'link': link, 'pub_date': pub_date, 'description': description})
    response = {"data": results}
    return func.HttpResponse(
        json.dumps(response),
        mimetype="application/json"
    )
    