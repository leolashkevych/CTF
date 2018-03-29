import hashlib 
import binascii
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

url = 'https://ringzer0team.com/challenges/14'
driver.get(url)
message = driver.find_element_by_class_name("message")
message_text = message.text[26:-24]
print(message_text + '\n**********\n')

bins = int('0b' + message_text, 2)
conv_bins = binascii.unhexlify('%x' % bins)
print(conv_bins + '\n**********\n')

hash_message_text = hashlib.sha512(conv_bins)
hashed = hash_message_text.hexdigest()
print(hashed)
driver.get('%s/%s' % (url, hashed))

