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

url = 'https://ringzer0team.com/challenges/32'
driver.get(url)
message = driver.find_element_by_class_name("message")
message_text = message.text[26:-24]
print(message_text + '\n**********\n')

a = int(message_text[:message_text.find('+')])
print('a: '+ a)
bstart = message_text.find('+') + 2
b = int(message_text[bstart:message_text.find(' ', bstart)], 16)
print('b: '+ b)
cstart = message_text.find('-') + 2
c = int(message_text[cstart:message_text.find(' ', cstart)], 2)
print('c: ' + c)

ans = a + b - c
print(ans)
driver.get('%s/%s' % (url, ans))

