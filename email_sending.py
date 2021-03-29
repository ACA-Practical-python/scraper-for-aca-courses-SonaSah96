from smtplib import SMTP_SSL
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
from database import *


def send_email_for_new_lessons(new_lesson_list, session):
    courses = session.query(Lesson).filter(Lesson.course_id.in_(new_lesson_list)).all()
    course_info = ""
    idx = 1
    for course in courses:
        tutors = session.query(Tutor).filter(Tutor.lesson_id == course.lesson_id).all()
        all_tutors = ",".join(f"Tutor:{tutor.full_name}-comp:{tutor.company}" for tutor in tutors)
        course_info += f"{idx}) Name:{course.course_name} Price:{course.price} Level:{course.level} Link:{course.course_url} "\
                       f"Tutors:{all_tutors} \n"
        idx += 1
    context = ssl.create_default_context()
    input_pass = getpass()
    with SMTP_SSL("smtp.gmail.com", context=context) as smtp_server:
        smtp_server.login("sonasah1919@gmail.com", password=input_pass)
        msg_text = f"""Hi Dear user,\nPlease find below the updated list of suggested courses\n{course_info}Best wishes\nACA administration"""
        context_text = MIMEText(msg_text, "plain")
        message = MIMEMultipart("multipart")
        message.attach(context_text)
        message["Subject"] = "ACA new courses"
        message["From"] = "sonasah1919@gmail.com"
        message["To"] = "sonasah1919@gmail.com"
        smtp_server.sendmail("sonasah1919@gmail.com", ["sonasah1919@gmail.com"], msg=message.as_string())



