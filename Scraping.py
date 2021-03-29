from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
from email_sending import *
from database import *
from sqlalchemy.orm import sessionmaker


session = sessionmaker(bind=engine)()
new_aca_lesson_list = []


def info_for_every_lesson(url):
    with urlopen(url) as resp:
        data = resp.read()

    dict_for_info = {}

    soup = BeautifulSoup(data, 'html.parser')
    div = soup.find("div", {"id": "header"})
    dict_for_info["course_name"] = div.h1.string

    dict_for_info["course_id"] = (os.path.basename(url)).split(".")[0]
    dict_for_info["course_url"] = url

    tab = soup.find("table", attrs={"class": "table"})
    string_in_tab = tuple(tab.stripped_strings)
    if 'Price:' in string_in_tab or 'Tuition fee:' in string_in_tab:
        if 'Price:' in string_in_tab:
            idx = string_in_tab.index('Price:')
        else:
            idx = string_in_tab.index('Tuition fee:')
        dict_for_info["price"] = string_in_tab[idx + 1].strip("*")
    if 'Level:' in string_in_tab:
        idx_1 = string_in_tab.index('Level:')
        dict_for_info["level"] = string_in_tab[idx_1 + 1]

    div_1 = soup.find("div", attrs={"id": "tutors"})
    tutors_comp = list(div_1.stripped_strings)

    existing_lesson = session.query(Lesson).filter(Lesson.course_id == dict_for_info["course_id"]).one_or_none()
    if not existing_lesson:
        new_lesson = Lesson(**dict_for_info)
        session.add(new_lesson)
        new_aca_lesson_list.append(dict_for_info["course_id"])
    else:
        existing_lesson.course_name = dict_for_info["course_name"]
        existing_lesson.price = dict_for_info.get("price", None)
        existing_lesson.level = dict_for_info.get("level", None)
    last_version_of_lesson = session.query(Lesson).filter(Lesson.course_id == dict_for_info["course_id"]).one_or_none()

    while tutors_comp:
        tut_dict = {"full_name": tutors_comp.pop(0),
                    "company": tutors_comp.pop(0), "lesson_id": last_version_of_lesson.lesson_id}
        new_tutor = Tutor(**tut_dict)
        session.add(new_tutor)
    session.commit()


def first_scraping_step(path):
    with open(path, "r", encoding="utf8") as file:
        data = file.read()

    stack = []
    soup = BeautifulSoup(data, 'html.parser')
    lev_val = ("intro-level", "intermediate-level", "advanced-level")
    for sub_lev in lev_val:
        div_1 = soup.find('div', attrs={"id": {sub_lev}})
        sub_item = div_1.find_all("a")
        for item in sub_item:
            if item.get("href"):
                stack.append(item["href"])

    url_list = []
    for url in stack:
        if "en/" not in url:
            url = f"https://aca.am/en/{url.strip('./')}"
        else:
            if not url.startswith("http"):
                url = f"https://aca.am/{url.strip('../')}"
        url_list.append(url)
    print(url_list)
    for one_url in url_list:
        info_for_every_lesson(one_url)

    send_email_for_new_lessons(new_aca_lesson_list, session)


def enter_first_aca_page():
    aca_path = "https://aca.am/en/index.html"
    with urlopen(aca_path) as response:
        if response.getcode() == 200:
            with open("aca_en.html", "wb") as fd:
                fd.write(response.read())
    first_scraping_step("aca_en.html")


if __name__ == "__main__":
    enter_first_aca_page()
