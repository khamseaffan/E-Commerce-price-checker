from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from collections import defaultdict

PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(PATH,options = options)

class price_finder:
	def __init__(self):
		self.prices = defaultdict(None)

	def amazon_price_return(self,item_name):
		print("searching")
		# item_name = "APPLE iPhone 11 (Purple, 64 GB)"
		driver.get("https://www.amazon.in/")
		# print(driver.title)
		search = driver.find_element_by_id("twotabsearchtextbox")
		search.send_keys(item_name)
		search.send_keys(Keys.RETURN)
		search_results = WebDriverWait(driver,10).until(
			EC.presence_of_element_located((By.CLASS_NAME,"s-main-slot"))
			)
		# print(search_results)
		price = search_results.find_element_by_class_name("a-price-whole")
		print_price = price.text
		self.prices['amazon'] = print_price
		return print_price

	def flipkart_price_return(self,item_name):
		# item_name = "APPLE iPhone 11 (Purple, 64 GB)"
		driver.get("https://www.flipkart.com/")
		search = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input')
		search.send_keys(item_name)
		search.send_keys(Keys.RETURN)
		search_results = WebDriverWait(driver,10).until(
			EC.presence_of_element_located((By.CLASS_NAME,"_2kHMtA"))
		)
		# print(search_results)
		price = search_results.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a/div[2]/div[2]/div[1]/div/div[1]')
		# print(price.text)
		print_price = price.text
		# print(print_price[1:])
		# time.sleep(10)
		self.prices['flipkart'] = print_price
		return print_price[1:]

	def croma_price_return(self,item_name):
		item_name = "APPLE iPhone 11 (Purple, 64 GB)"
		driver.get("https://www.croma.com/")
		search = driver.find_element_by_xpath('//*[@id="search"]')
		search.send_keys(item_name)
		search.send_keys(Keys.RETURN)
		search_results = WebDriverWait(driver,10).until(
			EC.presence_of_element_located((By.CLASS_NAME,"cp-product"))
		)
		# print(search_results)
		price = search_results.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div/div[3]/ul/li[1]/div/div[2]/div[2]/div[1]/span[1]/span[2]')
		print_price = price.text
		# print(print_price)
		# time.sleep(10)
		self.prices['croma'] = print_price
		return print_price[1:]

	def print_prices(self):
		driver.quit()
		print(self.prices)


# finder = price_finder()
# finder.amazon_price_return()
# finder.flipkart_price_return()
# finder.croma_price_return()
# finder.print_prices()
	
