# scaper_python

Create database and table

CREATE DATABASE IF NOT EXISTS LinkHumansTest;
CREATE TABLE `ambitionbox` (
  `id` int(100) NOT NULL,
  `company_name` varchar(150) NOT NULL,
  `date` date NOT NULL,
  `job_title` varchar(150) NOT NULL,
  `location` varchar(100) NOT NULL,
  `likes` text DEFAULT NULL,
  `dislikes` text DEFAULT NULL,
  `url_review` varchar(200) NOT NULL,
  `job_status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `ambitionbox`
  ADD PRIMARY KEY (`id`);
ALTER TABLE `ambitionbox`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25148748;
  
 
I have run in Pycharm so I have created virtual environment and install below: 
pymysql, 
requests, 
bs4

Use BeautifulSoup for html parser

Change the connection string: add your hostname, username, password, dbname

id in table have the value of review id(rid) as unique-identifier 
There are different functions which help to find location, job title, like and dislike, change date format, job status

Take one review then check if not exist then insert into table so on. 
Take one review then check if exist then take second so on.

Below are the paramters description:
n for stop while loop
page for take all feb month reviews using changing page 
