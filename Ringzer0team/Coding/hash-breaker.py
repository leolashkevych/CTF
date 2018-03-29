from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import hashlib

user = ''
passwd = ''
challenge = '56'
dat_hash_text = 'ERROR'
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
print(message.text)
message_text = message.text[23:-21]
for num in range(10001):
    target = str(num)
    raw = hashlib.sha1(target)
    hashed = raw.hexdigest()

    if (hashed == message_text):
        print('match')
        dat_hash_text = num
        break
print(dat_hash_text)
driver.get('%s/%s' % (url, dat_hash_text))

