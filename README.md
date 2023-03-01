# OurvleApi
Unofficial API to interface with OurVle through python

## Getting Started:
##### Install package with pip
```
pip install OurvleApi
```
##### Import the package
```
from OurvleApi import ourvle
```
# Features:
#### Without Login
- View and read news
- Get help information
- login
#### With Login:
- View all your courses
- Get detailed information about your courses, including the lecturers, resources. news and links

## Functions:
### Without Login

##### ourvle.news()

- Returnts a list of News objects (sourced from the front page)
```
news_list = ourvle.news()
```

##### ourvle.help()

- Prints a string of helpful information

##### ourvle.login(username,password)

- Accepts strings for username and password
- Returns a Client object
- Prints the name of the user
```
client = login(username,password)
  ==> Alexander McIntosh
```

### With Login
#### Client:

##### Client.session
- Returns a session object with the necessary cookies to traverse the website

##### Client.course_list
- Returns a list of Course objects
```
my_courses = client.course_list
print(my_courses)
  ==> [COMP1161, COMP1210,...]
print(my_courses[1])
  ==> COMP1210 | S2_2022/23 Mathematics for Computing ['Fake Name', 'Faker Name']
```

##### Client.user
- Returns a string of the name of the current user
```
client.user
  ==> Alexander McIntosh
```

### Course:
##### Course.name
- Returns a string of the course name
```
test_course = my_courses[1]
test_course.name
  ==> S2_2022/23 Mathematics for Computing
```
##### Course.code
- Returns a string of the course code
```
test_course.code
  ==> COMP1210
```
##### Course.link
- Returns a string of the link to the course page
```
  ==> https://ourvle.mona.uwi.edu/course/....
```
##### Course.teachers
- Returns a list of dictionaries with the course teachers' information
```
test_course.teachers
  ==> [{'role': 'Lecturer', 'name': 'Fake Name', 'profile_link': 'https://ourvle.mona.uwi.edu/user....'}, {'role': 'Tutor', 'name': 'Faker Name', 'profile_link': 'https://ourvle.mona.uwi.edu/user....'}]
```
##### Course.resources()
- returns a list of dictionaries with the course resources organized by topic (or section)
```
test_course.resources()
  ==> [{'section_name': 'General', 'resources': []}, {'section_name': 'COURSE OUTLINE', 'resources': [{'name': 'Outline File', 'details': '175.8KB PDF document', 'link': 'https://ourvle.mona.uwi....},....]
```
##### Course.links()
- returnsa a list of dictionaries with the course links organized by topic (or section) including links to online classes.
```
test_course.links()
  ==> [{'section_name': 'General', 'links': []}, {'section_name': 'COURSE OUTLINE', 'links': []}, {'section_name': 'ZOOM ONLINE TEACHING CORNER', 'links': [{'name': 'ZOOM LECTURES  (ONLINE) - Mona and WJC_Tuesdays', 'link': 'https://ourvle.mona.uwi.edu/....}]
```
#### (experimental)
##### Course.blocks()
- Returns a list of dictionaries with information in blocks located around the course page (if any)
```
test_course.blocks()
  ==> []
```
##### Course.news()
- Returns a list of dictionaries with information about items in the course news block (if any)
```
test_course.news()
  ==> [{'date': '31 Jan, 21:55', 'author': Fake Name, 'topic': 'ONLINE Tutorial', 'link': 'https://ourvle.mona.uwi.edu/...}]
```

### News:
##### News.topic
- Returns the topic of the news post as a string
```
test_news = news_list[0]
test_news.topic
  ==> 'Unavailability of UWI Mona ICT Services; December 28 - 31, 2022'
```
##### News.author
- Returns the author of the news post as a string
```
test_news.author
  ==> 'OurVle Administrator'
```
##### News.date
- Returns the date the news was posted as a string
```
test_news.date
  ==>'Tue, 27 Dec 2022, 1:32 PM'
```
##### News.link
- Returns the link to the news post as a string
```
test_news.link
  ==> 'https://ourvle.mona.uwi.edu/mod/forum/....'
```
##### News.content()
- Reuturns the content of the news post as a string
```
test_news.content()
  ==> 'TO WHOM IT MAY CONCERN\n\xa0\nGood day.\nAs per a Mona Messaging announcement sent on Dec.... Regards,'
```
# DISCLAIMER: 
This API is not affiliated with, endorsed by, or sponsored by the University of the West Indies (UWI) or OurVle. The information provided through this API is intended for educational and informational purposes only and is not guaranteed to be accurate or up-to-date. The University of the West Indies and OurVle are the sole owners of all rights, title, and interest in OurVle. Use of this API is subject to the terms and conditions outlined by the University of the West Indies and OurVle. By using this API, you agree to indemnify and hold harmless the University of the West Indies and OurVle for any and all claims arising from your use of this API.

