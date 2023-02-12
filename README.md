# OurvleScraper
Unofficial API to interface with OurVle through python

## Getting Started:
##### Install package with pip
```
pip install ourvle
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
#### Without Login
```
ourvle.news()
- Returnts a list of News objects (sourced from the front page)
Usage: 
- news_list = ourvle.news()

ourvle.help()
- Prints a string of helpful information

ourvle.login(username,password)
- Accepts strings for username and password
- Returns a Client object
- Prints the name of the user
Usage:
- client = login(username,password)
- ==> Alexander McIntosh
```
#### With Login
##### Client:
```
Client.course_list
- returns a list of Course objects
- Usage:
  - my_courses = client.course_list
  - print(my_courses)
  - ==> [COMP1161, COMP1210,...]

Client.user
- Returns a string of the name of the current user
```

# DISCLAIMER: 
This API is not affiliated with, endorsed by, or sponsored by the University of the West Indies (UWI) or OurVle. The information provided through this API is intended for educational and informational purposes only and is not guaranteed to be accurate or up-to-date. The University of the West Indies and OurVle are the sole owners of all rights, title, and interest in OurVle. Use of this API is subject to the terms and conditions outlined by the University of the West Indies and OurVle. By using this API, you agree to indemnify and hold harmless the University of the West Indies and OurVle for any and all claims arising from your use of this API.

# Temporary Demos:


https://user-images.githubusercontent.com/113714949/218294185-bba2d391-b8d5-4204-b95b-73e627fe9fc7.mov






https://user-images.githubusercontent.com/113714949/218294257-c7ce3ebf-13f3-443d-96a0-2ea39abf98e1.mov


