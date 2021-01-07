
import re
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from selenium.webdriver.common.by import By
base_url = "https://vnstoic.com/category/daily-stoic/"
driver=webdriver.Chrome(executable_path="chromedriver.exe")
driver.maximize_window()
driver.implicitly_wait(10) #10 is in seconds
def extractTitle(rawTitle):
    regex = r'^(Daily Stoic #)(\d+)(:)(.*)'
    matches = re.finditer(regex, rawTitle, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
    return [match.group(2), match.group(4)]

def buildFileName(index):
    s = "part{:04d}.html".format(index)
    return s
def getLinks(base_url):
    driver.get(base_url)
    content = driver.find_element_by_id("content")
    nextPageUrl = ''
    try:
        paging = content.find_element_by_id("paging")
        next = paging.find_elements_by_class_name("next")
        nextPageUrl = next[0].get_attribute("href")
    except:
        print("has no next")
    articles = content.find_elements_by_tag_name("article")
    urls = [[[hlink.get_attribute('href') for hlink in heading.find_elements_by_tag_name("a")] for heading in article.find_elements_by_tag_name("h2")] for article in articles]
    [[[getContent(url) for url in hls] for hls in ars] for ars in urls]
    if nextPageUrl:
        getLinks(nextPageUrl)
def getContent(url):
    if not url.startswith( 'https://vnstoic.com/daily-stoic' ) or "#" in url:
        return
    driver.get(url)
    content = driver.find_element_by_id("content")
    headingElement = content.find_element_by_xpath("//*[@id=\"content\"]/div/div/article/h1")
    blockquoteElement = content.find_element_by_xpath("//*[@id=\"content\"]/div/div/article/div[3]/blockquote/p")
    authorElement = content.find_element_by_xpath("//*[@id=\"content\"]/div/div/article/div[3]/blockquote/cite")
    paragraphElements = content.find_elements_by_xpath("//*[@id=\"content\"]/div/div/article/div[3]/*[self::blockquote|self::p]")
    paragraphs = []
    for element in paragraphElements:
        if element.get_attribute("style") == "text-align: right;":
            break
        paragraph = None
        if element.tag_name == "p":
            paragraph = {
                "tag": "p",
                "text": element.get_attribute('innerHTML')
            }
        elif element.tag_name == "blockquote":
            found = element.find_elements(By.TAG_NAME, "cite")
            cite = None
            if len(found) > 0:
                cite = found[0].text.lower()
            paragraph = {
                "tag": "blockquote",
                "text": element.find_element(By.TAG_NAME, "p").get_attribute('innerHTML'),
                "cite": cite
            }
        if paragraph is not None:
            paragraphs.append(paragraph)
    print(headingElement.text)
    print(blockquoteElement.text)
    print(authorElement.text)
    title = 'Daily Stoic'
    extractedHeading = extractTitle(headingElement.text)
    index = extractedHeading[0]
    content = {
        'title': title,
        'index': index,
        'chapter': extractedHeading[1].strip(),
        'quote': blockquoteElement.text,
        'author': authorElement.text,
        'paragraphs': paragraphs
    }
    writeAPage(content, index)

def writeAPage(content, index):
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    template = env.get_template('template.html')

    output = template.render(content=content)
    fileName = buildFileName(int(index))
    f = open("output/" + fileName, "w", encoding="utf-8")
    f.write(output)
    f.close()

getLinks(base_url)
driver.close()