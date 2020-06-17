from selenium import webdriver


def browse_category(link):
    driver.get(link)
    driver.implicitly_wait(10)  # 10 is in seconds
    content = driver.find_element_by_id("content")
    articles = content.find_elements_by_tag_name("article")
    links = [
        [
            hyperlink.get_attribute("href")
            for hyperlink in article.find_elements_by_xpath("//*/h2/a")
        ]
        for article in articles
    ]

    [print(article_link) for article_link in links]


base_url = "https://vnstoic.com"
driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.maximize_window()
driver.implicitly_wait(10)  # 10 is in seconds
driver.get(base_url)
menu = driver.find_element_by_id("menu-vnstoic")
menuItems = menu.find_elements_by_tag_name("li")
links = [
    [
        hyperlink.get_attribute("href")
        for hyperlink in item.find_elements_by_tag_name("a")
    ]
    for item in menuItems
]
[[browse_category(link) for link in linkgr] for linkgr in links]
driver.close()
