#Driver Path
#Example C:/selenium/chromedriver/bin/chromedriver.exe
chrome_driver_path = ''

# Credentials
# Example:
# email: someuser@gmail.com
# password: xxxxxxxxxxxxxxxxxxxxx
email = '' 
password = ''

#Amount of users data you want to scrape 
count = 50

#Keywords that will be used to filter through google search
keywords = [
    'London',
    'Python Developer'
]

#File name that script.py will store data
file_name = 'results_file.csv'

#Delay while switching between linkedin profiles 
# !Increase if you think your internet is slow or having hard time while switching profiles!
delay = 1.5
