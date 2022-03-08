import pymysql
import requests
from bs4 import BeautifulSoup

conn = pymysql.connect(
    host='localhost',
    user='root',
    password="",
    db='LinkHumansTest',
)
cur = conn.cursor()


# Find job title
def before(value, a):
    # Find first part and return slice before it.
    pos_a = value.find(a)
    if pos_a == -1: return before(value, "in")
    return value[0:pos_a]


# Find location
def after(value, a):
    # Find and validate first part.
    pos_a = value.rfind(a)
    if pos_a == -1: return ""
    # Returns chars after the found string.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value): return ""
    return value[adjusted_pos_a:]


# Find job status
def status(value):
    if 'Current Employee' in value.rpartition('·')[0]:
        return 'Current Employee'
    elif 'Former Employee' in value.rpartition('·')[0]:
        return 'Former Employee'
    elif 'Anonymous' in value.rpartition('·')[0]:
        return 'Anonymous'
    else:
        return ''


# Find like and dislike
def review(children, a):
    for child in children:
        if child.find('h3').text == a:
            if child.p.text != '':
                return child.p.text.strip(' ')
            else:
                return ''
        else:
            if len(children) > 1:
                continue
            else:
                return ''

# Change date format
def find_date(value):
    year = value.rpartition(' ')[2].strip(' ')
    month = find_month(year.partition(' ')[2].strip(' '))
    day = value.partition(' ')[0].strip(' ')
    return year + "-" + month + "-" + day

# Find month from text to numeric
def find_month(value):
    if value == 'Jan':
        return '01'
    elif value == 'Feb':
        return '02'
    elif value == 'March':
        return '03'
    elif value == 'April':
        return '04'
    elif value == 'May':
        return '05'
    elif value == 'June':
        return '06'
    elif value == 'July':
        return '07'
    elif value == 'Aug':
        return '08'
    elif value == 'Sep':
        return '09'
    elif value == 'Oct':
        return '10'
    elif value == 'Nov':
        return '11'
    elif value == 'Dec':
        return '12'
    else:
        return '02'


# Main code start here
n = True
page = 1
while n:
    r = requests.get('https://www.ambitionbox.com/reviews/amazon-reviews?sort_by=latest&page=' + str(page))
    soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.findAll('div', class_='ab_comp_review_card')

    for div in divs:
        rid = div['id'].split('-')[1]
        if 'Feb' in div.find('div').span.text.replace('posted on ', ''):
            date = div.find('div', class_='review-info').span.text.replace('posted on ', '').strip(' ')
            final_date = find_date(date)
            data = {
                'date': final_date,
                'title': before(div.find('div', class_='review-wrap').div.h2.text, "for").strip(' '),
                'location': after(div.find('div', class_='review-wrap').div.h2.text, "in").strip(' '),
                'company_name': div.find('div', class_='user-wrap').p.text.rpartition('·')[2].strip('\n').strip('\t'),
                'like': review(
                    div.find('div', class_='review-content-cont').div.findChildren('div', recursive=False), 'Likes'),
                'dislike': review(
                    div.find('div', class_='review-content-cont').div.findChildren('div', recursive=False),
                    'Dislikes'),
                'url_review': 'https://www.ambitionbox.com/reviews/amazon-reviews?rid=' + str(rid),
                'status': status(div.find('div', class_='user-wrap').p.text).strip(' ')
            }

            # Check for duplicate
            cur.execute("SELECT id FROM AmbitionBox WHERE id ='" + rid + "'")
            result = cur.fetchone()

            if not result:
                # Insert data
                insert = "INSERT INTO AmbitionBox(id, company_name, date, job_title, location, likes, dislikes, url_review, job_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"

                cur.execute(insert, (rid, data['company_name'], data['date'], data['title'], data[
                    'location'], data['like'], data['dislike'], data['url_review'], data['status']))
            else:
                continue
        elif 'Jan' in div.find('div').span.text.replace('posted on ', ''):
            n = False
        else:
            continue
    page = page + 1

conn.commit()

print("Data insert done")
