from selenium import webdriver
from bs4 import BeautifulSoup

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta # 'soomis_official_recipes2_doc' 이라는 이름의 db를 만듭니다.

driver = webdriver.Chrome('/Users/cho/Downloads/chromedriver')
# 크롬 실행

url = 'https://m.post.naver.com/my/series/detail.nhn?seriesNo=472832&memberNo=3669297'
# 공홈 레시피 url
driver.get(url)
driver.implicitly_wait(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')

soomis_recipes = soup.select('#el_list_container > ul > ul > li')

soomis_official_recipes_doc = {
	'image': '',
	'name': '',
	'title': '',
	'posting_day': '',
	'description': '',
	'author': '',
	'url': ''
}

# 출력 양식 설정
for soomis_recipe in soomis_recipes:
	# print(soomis_recipe)

	# el_list_container > ul > ul > li:nth-child(1) > a > div.spot_post_name > span
	title = soomis_recipe.select_one('a > div.spot_post_name > span').text.strip().split(' ')[1]
	print(title)
	image = str(soomis_recipe.select_one('a > div.spot_thumb_area > img').attrs['src'])
	print(image)
	name = '수미네반찬'
	print(name)
	posting_day =str(soomis_recipe.select_one('a > p').text.strip()).split()[0]
	print(posting_day)
	description = '수미네 반찬 공식 레시피'
	print(description) #수미네 반찬 공식 레시피
	author = '수미네반찬 블로그'
	print(author) #수미네 반찬
	pre_url = str(soomis_recipe.select_one('a').get('href'))
	url = 'https://m.post.naver.com' + pre_url
	print(url + '\n')


	soomis_official_recipes_doc = {
		'image': image,
		'name': name,
		'title': title,
		'posting_day': posting_day,
		'description': description,
		'author': author,
		'url': url,
	}

db.soomis_official_recipes2_doc.insert_one(soomis_official_recipes_doc)
