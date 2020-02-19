from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import time

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

driver = webdriver.Chrome('/Users/cho/Downloads/chromedriver') # 크롬을 연다. (★chromedriver.exe 의 경로를 제대로 설정해주는 것이 중요함)

# 공홈 레시피 url
url = 'https://m.post.naver.com/my/series/detail.nhn?seriesNo=472832&memberNo=3669297'
driver.get(url)
#서버 과부하 방지
# driver.implicitly_wait(3)

#스크롤 다
SCROLL_PAUSE_TIME = 0.5
cnt_up = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
for cnt in range(1, 4):
	driver.find_element_by_xpath('//*[@id="more_btn"]/button').click()
	# btn 클릭후 스크롤 하단으로 내리기 반복
	while True:

		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height
		soup = BeautifulSoup(driver.page_source, 'html.parser')
		soomis_official_recipes = soup.select('#el_list_container > ul')

		for i in range(10):
			for soomis_official_recipe in soomis_official_recipes:
				soomis_official_recipes_doc = {
					'image': '',
					'name': '',
					'title': '',
					'posting_day': '',
					'description': '',
					'author': '',
				}

				# #el_list_container > ul:nth-child(11) > ul > li:nth-child(1) > a 수미네 반찬 레시피북 예약소
				# 1page에 20개의
				#몇번 뽑았는지 확인용
				print('count' + str(cnt_up))
				#
				# # 세미님이랑 얘기한 후 뽑아 내는거 결정
				# ul > li > a > div.spot_post_name > span
				title = soomis_official_recipe.select_one('a > div.spot_post_name > span').text.strip()
				print(title)
				#
				# # 이미지 파일을 따로 저장하면 길이는 줄어들겠지만 용량이 걱정
				image = str(soomis_official_recipe.select_one('a > div.spot_thumb_area > img').attrs['src'])
				print('imgFile : ' + image + '\n')
				#
				# name = '수미네반찬'
				# print(name)

				#posting_day 수정 필요 없음
				# posting_day = str(soomis_official_recipe.select_one('a > p').text.split()[0])
				# print(posting_day)
				#
				# description = '수미네 반찬 공식 레시피'
				# print(description) #수미네 반찬 공식 레시피
				#
				# author = '수미네반찬 블로그'
				# print(author) #수미네 반찬

				#url 수정 안해도 됨
				# pre_url = str(soomis_official_recipe.select_one('a').get('href'))
				# url = 'https://m.post.naver.com' + pre_url
				# print(url + '\n')


				# soomis_official_recipes_doc = {
				#     'image': image,
				#     'name': name,
				#     'title': title,
				#     'posting_day': posting_day,
				#     'description': description,
				#     'author': author,
				#     'url': url
				# }
				cnt_up += 1
				#
				# #db에 뽑은 data 저장
				# db.soomis_official_recipes2_doc.insert_one(soomis_official_recipes_doc)


# driver.close()

