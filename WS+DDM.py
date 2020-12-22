from urllib.request import urlopen, Request
import re
from bs4 import BeautifulSoup

print('INTRINSIC VALUE CALCULATOR (DDM) + WEB SCRAPER \n\n\n')
print("Note that intrinsic value calculated is based on 3-5 year averages, as well as current P/E ratio.")
print("Hence this calculator should only be used as a first check.")
print("Please ensure that the stock website has 'Final Dividend' and 'Interim Dividend' labelled properly in the factsheet. Factsheets that don't identify these clearly are faulty. ")
print('||')
print('\/')
website = input("Enter URL of stock information site (malaysiastock.biz): ")
url = Request(website, headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(url)
r = page.read()
html = r.decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
divs_per_year = []
year = int(input("Enter the current year: "))
req_return = float(input("Enter required rate of return (%). Enter 8 for historical broad market rate of return, or any number you deem suitable: "))

def find_dividends():
  global divs_per_year, year
  match = soup.find_all('td')
  yrs = [str(year) for year in range(2010,year+2)]
  l = []
  for index,i in enumerate(match):
    for year in yrs:
      if year in i.get_text():
        check = match[index+1]
        if "Interim Dividend" or "Final Dividend" in check.get_text:
          l.append(match[index+2].get_text())
  for index2,k in enumerate(l):
    if k == 'Final Dividend' and index2+1 < len(l)-1:
      divs_per_year.append(float(l[index2+1]))
      last = 'F'
    elif 'Interim Dividend' in k and index2+1 < len(l)-1 and len(divs_per_year) != 0:
      divs_per_year[-1] += float(l[index2+1])
      last = 'I'
  if last == 'F':
    divs_per_year.pop()

def multi_stage_DDM(tv, k = 0.08):
  global divs_per_year 
  div_growth = ((divs_per_year[-1]/divs_per_year[0])**(1/5))-1
  divs_per_year = [i/100 for i in divs_per_year]
  true_val = 0
  new_div = divs_per_year[-1]
  for year_less_1 in range(0,3):
    true_val += new_div/((1+k)**(year_less_1+1))
    new_div += new_div*div_growth
  true_val += tv/((1+k)**3)
  return true_val

def find_info():
  match2 = soup.find_all('div', {'class': 'corporateInfoValue_FinancialInfo'})
  for count,i in enumerate(match2):
    for index_after3 in range(4,len(i.get_text())):
      if i.get_text()[index_after3] == ' ':
        space = index_after3
    if count == 7:
      cagr = float(i.get_text()[3:space])
    elif count == 2:
      eps = float(i.get_text()[3:space])
    elif count == 3:
      pe = float(i.get_text()[3:space])
  return (cagr/100), (eps/100), pe

def find_tv(cagr,eps,pe,years = 3):
  final = eps
  for _ in range(0,years-1):
    final += (final*cagr)
  return (final*pe)

find_dividends()
cagr, eps, pe = find_info()
tv = find_tv(cagr, eps, pe, len(divs_per_year))
true = multi_stage_DDM(tv, (req_return/100))
print('||')
print('\/')
print("The intrinsic value of the stock (by DDM using historical data) is:",round(true,2))
print('||')
print('\/')
print("NOTE THAT THIS IS VALUE SHOULD ONLY BE USED AS A FIRST CHECK. DDM IS MUCH MORE EFFECTIVE WHEN FORECASTED VALUES ARE USED, ALONG WITH LONG-TERM HISTORICAL AVERAGES.")