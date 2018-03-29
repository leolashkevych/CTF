import hashlib 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

user = ''
passwd = ''
driver = webdriver.Firefox()

driver.get('https://ringzer0team.com/login')
user_elem = driver.find_element_by_name('username')
user_elem.send_keys(user)
pass_elem = driver.find_element_by_name('password')
pass_elem.send_keys(passwd)
pass_elem.send_keys(Keys.RETURN)

url = 'https://ringzer0team.com/challenges/13'
driver.get(url)
message = driver.find_element_by_class_name("message")
print(message.text[26:-24])
message_text = hashlib.sha512(message.text[26:-24])
hashed = message_text.hexdigest()
print(hashed)
driver.get('%s/%s' % (url, hashed))

