"Testing using the backend API to extract product details"

"""
- Inspect Website 
- Network 
- Filter for 'XHR' or 'Fetch/XHR'
- find the row that has a 'Response' containing product information 
(usually appears in a JSON structure, you can try clicking 'LOAD MORE' 
at buttom of the page and usually appears as a new row)

Once located 
copy the Name with 'Copy as Curl'

Open Postman: 
- New Request (HTTP Symbol)
- In GET Request past Curl command and hit Send

Once you get an output 
- Click on Headers and you can manipulate headers to alter the GET request
- (in Asos example there's an offset key and a limit key and we know the total number of items available)
- On the right side of Postman there's a </> symbol for 'Generating Code' click on Python Requests 
- Copy to Clipboard
- remove references for payload
"""

"Note headers contain cookie"

import requests
import pandas as pd

"Unable to alter limit for some reason"

offset_value = 0 
url = f"https://www.asos.com/api/product/search/v2/categories/5775?offset={offset_value}&includeNonPurchasableTypes=restocking&store=COM&lang=en-GB&currency=GBP&rowlength=3&channel=desktop-web&country=GB&keyStoreDataversion=11a1qu9-40&advertisementsPartnerId=100712&advertisementsOptInConsent=false"

headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'asos-c-name': '@asosteam/asos-web-product-listing-page',
  'asos-c-plat': 'web',
  'asos-c-ver': '1.2.0-47f50f69-80',
  'asos-cid': 'fe64ec3e-ae81-4695-963c-26973469784c',
  'cookie': 'featuresId=57ff8bac-6d20-4225-9648-4cc2ae6ec6b0; browseCountry=GB; browseCurrency=GBP; browseLanguage=en-GB; browseSizeSchema=UK; storeCode=COM; currency=1; floor=1001; asos-anon12=e12c4db233ea4d1ca4809ef237f596b0; asos=PreferredSite=&currencyid=1&currencylabel=GBP&topcatid=1001&customerguid=e12c4db233ea4d1ca4809ef237f596b0; OptanonAlertBoxClosed=2024-07-28T19:19:52.683Z; eupubconsent-v2=CQCdtdgQCdtdgAcABBENA_FwAAAAAAAAAAYgAAAAAAAA.YAAAAAAAAAAA; OTAdditionalConsentString=1~; geocountry=GB; asos_drmlp=b91fdd0c49d9dd6a4bac8c376bd01e13; AMCVS_C0137F6A52DEAFCC0A490D4C%40AdobeOrg=1; AMCV_C0137F6A52DEAFCC0A490D4C%40AdobeOrg=-1303530583%7CMCMID%7C60372865044947032469206356652289197590%7CMCAID%7CNONE%7CMCOPTOUT-1725125495s%7CNONE%7CvVersion%7C3.3.0; siteChromeVersion=au=12&com=12&de=12&dk=12&es=12&fr=12&it=12&nl=12&pl=12&roe=12&row=12&ru=12&se=12&us=12; keyStoreDataversion=11a1qu9-40; stc-welcome-message=cappedPageCount=2; ak_bmsc=3F4C10D8C06E10873BB7F47ED51CD842~000000000000000000000000000000~YAAQHwEVAo5+/JWRAQAAbTkQqRjb7UJGGlIkGWRnDY8tj24JQRBuTYIE7v/LbdMuE4fEYTvqF8iqh6RYxB8O6oI1WKSqm9eaF+m/Zg88mI2zOxMqrbs2gyhwtFpAJV6zgKNSrq+sQxWrToAeL8EIM3nzY1EPyYmqrE+AvXSkrpuCdSWr2wHDxQZAYKsJx4E+l1ahmjFOjJyLk7bqK65augPJ2zZkr9He6bE5cei6NSoFqmrQNIQwYyM6Nel+O+nLCqOU4NPwtoZPDJ3GBO2/s3+zRahuulv5YidpKyoXIKRGH6mFmSVQ43ntDKcLsiOPR9IuIft8wbg9rIi9eLVHHZMPEkhdTqSS6GsK71iHs+qNXaRk8G83oA66gxzpq/PMBNzbuNokr5W7cTQwHrEeQjoGQi5Rjys4eiySSFuAF/cG; asos-b-sdv629=11a1qu9-40; _s_fpv=true; asos-ts121=d3f9240837314bd98c4a015434f78ad1; _abck=0B6F896C33DBBD58C1D1A96AB1FBDA74~0~YAAQHwEVAk+A/JWRAQAA8mYQqQyO4I3f31HFCZD7BniRvM2iKCD8o0hVHBzomdfyfJgpto6aRy23bvDtaOjEkdlEKMWvL5R49swwup6VsGu5L/FtaXJCfWz/4yJ8mjEQwfn/ag2svp0D0SXjDIbbkCfVXGjVAJLYT3zBP76biVVh1ghT5zyHp7BNxa/7pBGeRjA68nD9l4tK4im4r1X08v+Iw9B1rnoCKxfqIZL3OvR2anSYoCPvWITa1lmN5olJe6qZWq2nE/ImKKW2F+VhYebrWcHiRZBvEIvd84R6V24ErSHJc+QXmsyfb50Oqw2fKJ1jREf0vdXVksUKrkeEoL58dV8l/ybl6bjXRLndPOcRG4S0rlEOkk3QkV/G7BSk/lqTCWfJf+1kRPG1qyZsVKW12ObSYBQayqUfiUZm2Rn2djLuJsJPtF/OT27txrpQUy2J5VTiPzKv+UJ8P/bsXtYZ7GfoGmBNSYj5ZEfMu6FP5j7WByz0zCw=~-1~-1~1725121900; asos-perx=e12c4db233ea4d1ca4809ef237f596b0||d3f9240837314bd98c4a015434f78ad1; s_cc=true; bm_sz=CCFF8898A2C2985A6B2EBCF6C516C789~YAAQHwEVAuaB/JWRAQAA7pAQqRgvBq8qOZZSbRS5IBWb4pJBhI+6lL29ZVz/V8cxF5P78X1vZfEXUSNZHUynIcsgWweXVV4pCvq2B8/N8jLRYaYuKluq5St92kP0rt74EyWCVK/QOyciWrWg/E9OZjTI02aWmFKTYrfyvD2gm6U3OAUZH7IIiApSH0tQNJONRyAkdpJHAtqXHC3pFacWmWXb2SPDw0gcFNfNl9PHP1OzgVGozWZJNgtouyKs1RVU3xgtnLlKbvrhDe4W4gr6yN18lyHymL0TwzA4JBGGOpU//Q+8y5LQMHd3+Tc7eqiedtMk7rFzytqnMTRA1fzpLae4i0KyvdAlxRylfw9NXKOYrLI+8OtF+F3HwBAZ39khjQ1+Qj/WpAlvD1XY0PdH1I5LE3r5A7wpxd77hG5o27/zWb9MxIm3/Z6MZJSLLEMQ2yDKLXsn5MixCUcrx20IUexzuOfq~3683376~3617076; plp_columsCount=threeColumns; bm_mi=3A494C84DF946BF5A2F64A70E75C7CF4~YAAQHwEVApKC/JWRAQAAmZoQqRi/Fff5vn8CNv+Rt8ikzdXHmkA7XIUZsfrM+Qv6aufaokoZKZACX7CK+EeVYQ2nup+0bcItn8KZ2wy+VBeRd70/vYL2WDs/AVLa2gQKf2jIL+lRiIOhjuoi09wpDfOqFFB7wxLKw0Z1tubG88CnHzIEQKklFl8r0Wr6BaLfzoxFd+P9MV2pG1uNfpLj5Krn9p3m0pLdeoTpldRvRAuZwuF8OA+53fidPJC32R13Pt8qjpztYo+ChjvGMhH30deLYJkTZRPgx5rZVH0OALXnJpgCyFuk5wfUF+EHo9BuCNUvaYgyp/wwq7AxVRk666FtDM1BvA==~1; bm_sv=162F114694155BAE2EA183BFA4393FC3~YAAQHwEVApOC/JWRAQAAmZoQqRhkRoC0gu31VneSU3K1x+cyjlzP/dufzzArwJUiO89xE2IEfUYr+MFsjoW4UFY2xjkoyDjR9Vy/8bGarbOFEjPvam0U734yZSDepgRSjaKl2/K4ZadJZ1GE9ziXA0O82LbmYz0+Uc0sGxXdFRdSNJo6XTbzh40AjkdAz35bvGnQ4XzgLOdshWZPDJT4qKDtUs7YMfdjbQtmI7tGGDA9G1LmGJtgLTHf8PegJXo=~1; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Aug+31+2024+16%3A32%3A04+GMT%2B0100+(British+Summer+Time)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=fb34c2c9-83dc-4d05-96a0-a0a6d238b4d2&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A0%2CC0001%3A1%2CC0003%3A0%2CV2STACK42%3A0&geolocation=GB%3BENG&AwaitingReconsent=false; s_pers=%20s_vnum%3D1725145200541%2526vn%253D1%7C1725145200541%3B%20gpv_p6%3D%2520%7C1725120110023%3B%20eVar225%3D4%7C1725120121483%3B%20visitCount%3D1%7C1725120121497%3B%20gpv_e231%3D681c3857-d1b2-4f3e-ba8f-d8e22c4e0090%7C1725120124594%3B%20s_invisit%3Dtrue%7C1725120124595%3B%20s_nr%3D1725118324596-Repeat%7C1756654324596%3B%20gpv_e47%3Dno%2520value%7C1725120124596%3B%20gpv_p10%3Ddesktop%2520com%257Ccategory%2520page%257C5775%2520refined%7C1725120124597%3B; s_sq=asoscomprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Ddesktop%252520com%25257Ccategory%252520page%25257C5775%252520refined%2526link%253DLOAD%252520MORE%2526region%253Dplp%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c; _abck=0B6F896C33DBBD58C1D1A96AB1FBDA74~-1~YAAQHMYQAk4FuJaRAQAAE8kfqQwQURMBlcyjMAkgZZ6pWK5UplQ1wmhcGPuhS46pn/0nsvsF4yQaHnDKsdv5dbVhdgYVe7PboVl3i7XgKYWPqSvB3pg8whlawFs0MSPw+qTPqJLx3NtXZkiEC9cPt8c9nVtjKsQEM8UyO9Y4UCAGBReWboyE3W8aGEGIrzE2koH2OkUZBKMDsEgv0zPlh+7VBzvZsnjS9FRuVScksn38pHM6SCFo5CLd9F6iD+8JbtCbcP3wcyuWvOitbdkVyKkQjvMuELYt2V6woG34fWSHEXnGE3HTZSb6zGJE5uD3vj0nOXp+3XKm0k4Kz6ggJI4pqnYIo4KzDY7JkCQjWn6aoXWaPx18w0FLmXJtMvIAwFBE2HK9eAACfySTjzVZxvaqXbBEQAp8M7driGFzHnckUhoqe7vl4StEcxCAZupvNkoHoCVBbe6doHky8AGWXa+X/9nlsUFi0TaBZeHGDAOqrGos5hF8Wi4=~0~-1~1725121900; ak_bmsc=3F4C10D8C06E10873BB7F47ED51CD842~000000000000000000000000000000~YAAQHMYQAk8FuJaRAQAAE8kfqRijzA6I/Ht6WOmmBBnb41RhdYnIOCe0IzZc+q1oMcZtpDpPaCMmyUgFaMrYdvWAEofxCZydBjll/cf/RJcufdSzqsl50XH5th4tjshAGU55Nkm7GdrWiswTLSJ1wJfmInKcWuMuQad2QGfdcYa+ghK197NXByD/Jg2B5Cv5bkU9/7TjeekyB6FRN/hAl7Hsi1mcXJ1NAfKKeuSx5O+T4W57Opi/R4QWzQOFOYddU6gL8HbmaVykfq0I8hAZVfU/dImfYsJPIo0Xycc5Lz1sANjhH0qVEfh4f0yyOuC20YmK5V/LnP/6RQERyB3xgrUWswEfbapwBNjLn6vjq2p3H4ghi/hWCAvRo01pYGm3aZWkGwv/R7NejTi2SL9aqpT4dqtJdu9p2AqN3W+tq8KEf/o3T4ZoHDx1gQ==',
  'priority': 'u=1, i',
  'referer': 'https://www.asos.com/men/shoes-boots-trainers/trainers/cat/?cid=5775&page=2',
  'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers)
Total_values = response.json()['itemCount']
print('Total number of items identified: ',Total_values)

data = []
while offset_value < Total_values:
    for product in response.json()['products']:
        "ID, Name, Current Price, Brand Name, ProductCode, Url , Image Url"
        data.append([product['id'],product['name'],product['price']['current']['value'],product['brandName'],product['productCode'],product['url'],product['imageUrl']])
        print('-----ADDING------')
        print([product['id'],product['name'],product['price']['current']['value'],product['brandName'],product['productCode'],product['url'],product['imageUrl']])
    offset_value += 72

print('Data from ',len(data),' items has been collected')

df = pd.DataFrame(data,columns = ['ID', 'Name', 'Current Price', 'Brand Name', 'ProductCode', 'Url' , 'Image Url']).drop_duplicates()
df.to_csv('asos-trainers.csv',index = False)

