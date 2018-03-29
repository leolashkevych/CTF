from selenium import webdriver
from selenium.webdriver.common.keys import Keys

user = ''
passwd = ''
challenge = ''
driver = webdriver.Firefox()

driver.get('https://ringzer0team.com/login')
user_elem = driver.find_element_by_name('username')
user_elem.send_keys(user)
pass_elem = driver.find_element_by_name('password')
pass_elem.send_keys(passwd)
pass_elem.send_keys(Keys.RETURN)

url = 'https://ringzer0team.com/challenges/' + challenge
driver.get(url)
message = driver.find_element_by_class_name("message")
message_text = message.text[26:-24]
print(message_text)


driver.get('%s/%s' % (url, hashed))

