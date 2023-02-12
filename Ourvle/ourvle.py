import requests
from bs4 import BeautifulSoup

user = "620151891"
passw = "82M%1P7d"


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


def login(username, password):
    login_page = "https://ourvle.mona.uwi.edu/login/index.php?authldap_skipntlmsso=1"
    payload = {
        "username": username,
        "password": password
    }
    session = requests.post(login_page, data=payload)
    cookies = session.cookies
    soup = BeautifulSoup(session.content, "html.parser")
    return Client(soup, cookies)


class Client:
    def __init__(self, soup, cookies):
        self.__front_page = soup
        self.__cookies = cookies
        self.course_list = self.__get_course_list()

    def __get_course_list(self):
        course_list = []
        course_container = self.__front_page.find(class_="courses frontpage-course-list-enrolled")
        courses = course_container.find_all(class_="coursebox")
        for course in courses:
            course_list.append(Course(course))
        return course_list


class Course:
    def __init__(self, soup: BeautifulSoup):
        self.__info = soup.find(class_="coursename")
        self.link = self.__info.find('a')['href']
        self.__info_text = self.__info.text.split('|')
        self.code = self.__info_text[0].strip()
        self.name = self.__info_text[1]

        self.__content = soup.find(class_="content")
        self.teachers = []
        for teacher in self.__content.find_all("li"):
            data = {"role": teacher.text.split(":")[0].strip(),
                    "name": teacher.find('a').text,
                    "profile_link": teacher.find('a')['href']}
            self.teachers.append(data)

    def __str__(self):
        return f"{self.__info.text} {[t['name'] for t in self.teachers]}"

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


print(news()[1])
