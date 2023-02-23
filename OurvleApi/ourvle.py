import requests
from bs4 import BeautifulSoup
import threading


def news():
    news_link = "https://ourvle.mona.uwi.edu/mod/forum/view.php?f=13"
    news_page = requests.get(news_link)
    news_soup = BeautifulSoup(news_page.content, "html.parser")
    discussions = news_soup.find("tbody")
    news_list = []
    for discussion in discussions.find_all('tr'):
        news_list.append(News(discussion))
    return news_list


def help():
    front_page = requests.get("https://ourvle.mona.uwi.edu/")
    soup = BeautifulSoup(front_page.content, 'html.parser')
    help_block = soup.find(id="inst62134")
    print(help_block.find(class_="content").text)


def login(username:str, password:str):
    login_page = "https://ourvle.mona.uwi.edu/login/index.php?authldap_skipntlmsso=1"
    payload = {
        "username": username,
        "password": password
    }
    session = requests.post(login_page, data=payload)
    cookies = session.cookies
    soup = BeautifulSoup(session.content, "html.parser")
    if session.history:
        cookies = session.history[0].cookies
    return Client(soup, cookies)


class Client:
    def __init__(self, soup: BeautifulSoup, cookies):
        self.__front_page = soup
        try:
            self.user = self.__front_page.find(class_="profilepic")['alt']
        except TypeError:
            raise TypeError('Login Failed. Check your Details.')
        self.__cookies = cookies
        self.course_list = self.__get_course_list()
        print(self.user)

    def __get_course_list(self):
        course_list = []
        course_container = self.__front_page.find(class_="courses frontpage-course-list-enrolled")
        courses = course_container.find_all(class_="coursebox")
        for course in courses:
            course_list.append(Course(course, self.__cookies))
        return course_list

    def __test(self):
        with requests.Session() as session:
            session.cookies = self.__cookies
            page = session.get("https://ourvle.mona.uwi.edu/course/view.php?id=21087",
                               cookies=self.__cookies)
            print(page.text)


class Course:
    def __init__(self, soup: BeautifulSoup, cookies):
        self.__info = soup.find(class_="coursename")
        self.link = self.__info.find('a')['href']
        self.__info_text = self.__info.text.split('|')
        self.code = self.__info_text[0].strip()
        self.name = self.__info_text[1]
        self.__cookies = cookies
        self.__page_soup = None
        self.__all_content = None
        self.__topics = None
        self.__resources = None
        self.__links = None
        self.__blocks = None
        self.__news = None
        self.__content = soup.find(class_="content")
        self.teachers = []
        for teacher in self.__content.find_all("li"):
            data = {"role": teacher.text.split(":")[0].strip(),
                    "name": teacher.find('a').text,
                    "profile_link": teacher.find('a')['href']}
            self.teachers.append(data)
        self.__res_thread = threading.Thread(target=self.resources, args=())
        self.__link_thread = threading.Thread(target=self.links, args=())
        self.__res_thread.start()
        self.__link_thread.start()

    def resources(self):
        if not self.__resources:
            if not self.__page_soup:
                page = requests.get(self.link, cookies=self.__cookies)
                self.__page_soup = BeautifulSoup(page.content, "html.parser")
                self.__all_content = self.__page_soup.find(class_="course-content")
                self.__topics = self.__all_content.find_all(class_="content")
            resource_list = []
            for topic in self.__topics:
                topicName = topic.find(class_="sectionname")
                if not topicName:
                    continue
                topicName = topicName.text
                topic_resources = topic.find_all(class_='modtype_resource')
                d1 = {"section_name": topicName}
                res = []
                for TR in topic_resources:
                    link = TR.find('a')['href']
                    res_name = TR.find(class_="instancename").text.strip()
                    if TR.find(class_="resourcelinkdetails"):
                        res_details = TR.find(class_="resourcelinkdetails").text.strip()
                    else:
                        res_details = "N/A"
                    data = {"name": res_name,
                            "details": res_details,
                            "link": link}
                    res.append(data)
                d1['resources'] = res
                resource_list.append(d1)
            self.__resources = resource_list
            return resource_list
        else:
            return self.__resources

    def links(self):
        if not self.__links:
            if not self.__page_soup:
                page = requests.get(self.link, cookies=self.__cookies)
                self.__page_soup = BeautifulSoup(page.content, "html.parser")
                self.__all_content = self.__page_soup.find(class_="course-content")
                self.__topics = self.__all_content.find_all(class_="content")
            link_list = []
            for topic in self.__topics:
                topicName = topic.find(class_="sectionname")
                if not topicName:
                    continue
                topicName = topicName.text
                topic_links = topic.find_all(class_='modtype_url') + topic.find_all(class_='modtype_lti')
                d1 = {"section_name": topicName}
                lnk = []
                for TL in topic_links:
                    link = TL.find('a')['href']
                    lnk_name = TL.find(class_="instancename").text.strip()
                    data = {"name": lnk_name.rstrip(" External Tool"),
                            "link": link}
                    lnk.append(data)
                d1['links'] = lnk
                link_list.append(d1)
            self.__links = link_list
            return link_list

        else:
            return self.__links

    def blocks(self):
        if not self.__blocks:
            if not self.__page_soup:
                page = requests.get(self.link, cookies=self.__cookies)
                self.__page_soup = BeautifulSoup(page.content, "html.parser")

            blocks = self.__page_soup.find_all(class_="block_html")
            block_list = []
            for block in blocks:
                title = block.find('h2').text.strip()
                content = "".join(block.find(class_='content').text.split('\r\n')).strip()
                data = {
                    "title": title,
                    "content": content
                }
                block_list.append(data)
            self.__blocks = block_list
            return block_list
        else:
            return self.__blocks

    def news(self):
        if self.__news:
            return self.__news

        if not self.__page_soup:
            page = requests.get(self.link, cookies=self.__cookies)
            self.__page_soup = BeautifulSoup(page.content, "html.parser")
        news_block = self.__page_soup.find(class_="block_news_items")
        if not news_block.find(class_="post"):
            title = news_block.find('h2').text.strip()
            content = news_block.find(class_="content").text.strip()
            return {"title": title,
                    "content": content}

        news_list = []
        posts = news_block.find_all(class_="post")
        for post in posts:
            date = post.find(class_="date").text
            author = post.find(class_="name").text
            topic = post.find(class_='info').text
            link = post.find('a')['href']

            data = {
                "date": date,
                "author": author,
                "topic": topic,
                "link": link
            }
            news_list.append(data)
        self.__news = news_list
        return news_list

    def __str__(self):
        return f"{self.code}"

    def __repr__(self):
        return self.code


class News:
    def __init__(self, soup: BeautifulSoup):
        self.__soup = soup
        # print(soup)
        self.topic = soup.find(class_="topic").text
        self.author = soup.find(class_="author").text
        self.replies = soup.find(class_="replies").text
        self.date = soup.find(class_="lastpost").text.lstrip(self.author)
        self.author_photo = soup.find(class_="picture").find('img')['src']
        self.link = soup.find(class_="topic").find('a')['href']

    def content(self):
        msg_page = requests.get(self.link)
        msg_soup = BeautifulSoup(msg_page.content, "html.parser")

        return msg_soup.find(class_="posting").text.strip()

    def __str__(self):
        return f"{self.topic} | {self.author}"

    def __repr__(self):
        return self.topic
