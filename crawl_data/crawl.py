from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient



def get_tours(url: str)-> list:
    # mở trình duyệt
    driver = webdriver.Chrome()
    driver.get(url)

    # đợi JS load dữ liệu
    time.sleep(5)

    # lấy HTML sau khi render
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # lấy tất cả tour
    tours = soup.find_all("div", class_="card-filter-desktop")
    for tour in tours:
        print(tour.get("id"))

    driver.quit()
    
    return tours


def get_information_of_tour(tour) -> dict:
    url = 'https://travel.com.vn' + tour.find('a').get('href')
    in4 = {}
    # print(url)
    # mở trình duyệt
    driver = webdriver.Chrome()
    driver.get(url)

    # đợi JS load dữ liệu
    time.sleep(5)

    # lấy HTML sau khi render
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # lấy tất cả tour
    ten_tour = soup.find("h2", class_="tour--header__title animate__fadeIn animate__animated").get_text()
    lich_trinh = soup.find_all('div', class_ = 'item-title-content')
    gia = soup.find('div', class_='price').find('p').get_text()
    
    
    in4['tên tour'] = ten_tour
    in4['lịch trình'] = []
    for ngay in lich_trinh:
        in4['lịch trình'].append(ngay.find('p').get_text())
    in4['giá'] = gia
    
    print(in4)

    driver.quit()
    
    return in4



def insertDB(tour: dict):
    
    # 1. Kết nối tới MongoDB (local hoặc Atlas)
    # Nếu dùng MongoDB local (chạy trên cổng mặc định 27017)
    client = MongoClient("mongodb://localhost:27017/")

    # Nếu dùng MongoDB Atlas thì thay bằng connection string của bạn:
    # client = MongoClient("mongodb+srv://username:password@cluster0.mongodb.net/")

    # 2. Chọn database và collection
    db = client["tour"]         # tạo hoặc kết nối tới database "mydatabase"
    collection = db["tour_in4"]      # tạo hoặc kết nối tới collection "customers"

    # 3. Insert một document
    result = collection.insert_one(tour)

    # 4. In ra ID của document vừa insert
    print("Inserted ID:", result.inserted_id)


if __name__ == '__main__':
    url = input()
    
    tours = get_tours(url)
    for tour in tours:
        in4_dict = get_information_of_tour(tour)
        insertDB(in4_dict)