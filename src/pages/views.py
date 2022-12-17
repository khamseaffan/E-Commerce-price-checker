from django.http import HttpResponse
from django.shortcuts import render
# from .models import price_finder
# Create your views here.


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from collections import defaultdict

class price_finder:
	def __init__(self):
		PATH = "C:\Program Files (x86)\chromedriver.exe"
		options = webdriver.ChromeOptions()
		options.add_argument("start-maximized")
		options.add_experimental_option("excludeSwitches", ["enable-automation"])
		options.add_experimental_option('useAutomationExtension', False)
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.driver = webdriver.Chrome(PATH,options = options)
		self.prices = defaultdict(None)
		self.links = defaultdict(None)

	def amazon_price_return(self,item_name,surpass):
		if surpass == -1:
			print("skipped amazon")
			self.prices['amazon'] = "-1"
			self.links['amazon'] = "0"
			return
		print("searching amazon")
		self.driver.get("https://www.amazon.in/")
		print("connected to amazon")
		try:
			search = self.driver.find_element_by_id("twotabsearchtextbox")
			search.send_keys(item_name)
			search.send_keys(Keys.RETURN)
			search_results = WebDriverWait(self.driver,10).until(
				EC.presence_of_element_located((By.CLASS_NAME,"s-main-slot"))
				)
			price = search_results.find_element_by_class_name("a-price-whole")
			link = search_results.find_element_by_class_name('a-link-normal').get_attribute('href')
			print(link)
			self.links['amazon'] = link
			print_price = price.text
			self.prices['amazon'] = print_price
		except:
			self.prices['amazon'] = "-1"
			self.links['amazon'] = "0"

	def flipkart_price_return(self,item_name,surpass):
		if surpass == -1:
			print("skipped flipkart")
			self.prices['flipkart'] = "-1"
			self.links['flipkart'] = "0"
			return
		print("searching flipkart")
		# item_name = "APPLE iPhone 11 (Purple, 64 GB)"
		self.driver.get("https://www.flipkart.com/")
		print("connected to flipkart")
		try:
			search = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input')
			search.send_keys(item_name)
			search.send_keys(Keys.RETURN)
			search_results = WebDriverWait(self.driver,10).until(
				EC.presence_of_element_located((By.CLASS_NAME,"_2kHMtA"))
			)
			# print(search_results)
			price = search_results.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a/div[2]/div[2]/div[1]/div/div[1]')
			link = search_results.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a').get_attribute('href')
			self.links['flipkart'] = link
			print(link)
			print_price = price.text
			# print(print_price[1:])
			# time.sleep(10)
			self.prices['flipkart'] = print_price[1:]
		except:
			self.prices['flipkart'] = "-1"
			self.links['flipkart'] = '0'

	def croma_price_return(self,item_name,surpass):
		if surpass == -1:
			print("skipped croma")
			self.prices['croma'] = "-1"
			self.links['croma'] = "0"
			return
		print("searching croma")
		# item_name = "APPLE iPhone 11 (Purple, 64 GB)"
		self.driver.get("https://www.croma.com/")
		print("connected to croma")
		try:
			search = self.driver.find_element_by_xpath('//*[@id="search"]')
			search.send_keys(item_name)
			search.send_keys(Keys.RETURN)
			search_results = WebDriverWait(self.driver,10).until(
				EC.presence_of_element_located((By.CLASS_NAME,"cp-product"))
			)
			# print(search_results)
			price = search_results.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div/div[3]/ul/li[1]/div/div[2]/div[2]/div[1]/span[1]/span[2]')
			print_price = price.text
			link = search_results.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div/div[3]/ul/li[1]/div/div[2]/div[1]/h3/a').get_attribute('href')
			self.links['croma'] = link
			print(link)
			self.prices['croma'] = print_price[1:]
		except:
			self.prices['croma'] = "-1"
			self.links['croma'] = "0"

	def print_prices(self):
		self.driver.quit()
		print(self.prices)
		print(self.links)


def result(prices,best_price_key,links,request,*args,**kwargs):
	for i in prices.keys():
		if prices[i] == "-1":
			prices[i] = "Product Not Found"
		else:
			prices[i] = "₹" + prices[i]
	return render(request,"result.html",{'amazon_price':prices['amazon'],'flipkart_price':prices['flipkart'],'croma_price':prices['croma'],'best_price':prices[best_price_key],'amazon_link':links['amazon'],'flip_link':links['flipkart'],'croma_link':links['croma'],'best_price_link':links[best_price_key]})

def home_view(request,*args,**kwargs):
	if request.method == 'POST':
		link_dict = request.POST
		item_name = link_dict['item']
		print(link_dict)
		finder = price_finder()
		if 'amazon' in link_dict:
			finder.amazon_price_return(item_name=item_name,surpass=0)
		else:
			finder.amazon_price_return(item_name='',surpass = -1)
		if 'flipkart' in link_dict:
			finder.flipkart_price_return(item_name=item_name,surpass=0)
		else:
			finder.flipkart_price_return(item_name='',surpass = -1)
		if 'croma' in link_dict:
			finder.croma_price_return(item_name=item_name,surpass=0)
		else:
			finder.croma_price_return(item_name='',surpass = -1)
		finder.print_prices()
		price_copy = finder.prices
		if finder.prices['croma'] != "-1":
			finder.prices['croma'] = finder.prices['croma'][:-3]
		finder.print_prices()
		copy = {}
		copy['amazon'] = int(price_copy['amazon'].replace(",",""))
		copy['flipkart'] = int(price_copy['flipkart'].replace(",",''))
		copy['croma'] = int((price_copy['croma'].replace(",",'')))
		# print((copy['croma']))
		mini_value = copy['amazon']
		mini_key = 'amazon'
		if mini_value == -1:
			mini_value = copy['flipkart']
			mini_key = 'flipkart'
		if mini_value == -1:
			mini_value = copy['croma']
			mini_key = 'croma'
		for i in copy.keys():
			if mini_value > copy[i] and copy[i] != -1:
				mini_value=copy[i]
				mini_key = i
		best_price_key = mini_key
		print(best_price_key)
		return result(finder.prices,best_price_key,finder.links,request)
		return render(request,"result.html")
	return render(request,"index.html",{})

