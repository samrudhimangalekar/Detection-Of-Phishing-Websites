#import ipaddresspip
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
import requests
from googlesearch import search
import whois
from datetime import datetime
from datetime import date
import time
from dateutil.parser import parse as date_parse

# Calculates number of months
def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

# Generate data set by extracting the features from the URL
def generate_data_set(url):

    data_set = []

    # Converts the given URL into standard format
    if not re.match(r"^https?", url):
        url = "http://" + url


    # Stores the response of the given URL
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        response = ""
        soup = -999


    # Extracts domain from the given URL
    domain = re.findall(r"://([^/]+)/?", url)[0]
    if re.match(r"^www.",domain):
	       domain = domain.replace("www.","")

    # Requests all the information about the domain
    whois_response = whois.whois(domain)

    rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
        "name": domain
    })

    # Extracts global rank of the website
    try:
        global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
    except:
        global_rank = -1

    # 1.having_IP_Address
   # try:
    #    ipaddress.ip_address(url)
     #   data_set.append(-1)
    #except:
     #   data_set.append(1)

    # 2.URL_Length
    if len(url) < 54:
        data_set.append(1)
        print("URL length successful")
    elif len(url) >= 54 and len(url) <= 75:
        data_set.append(0)
        print("URL length successful")
    else:
        data_set.append(-1)
        print("URL length successful")

    # 4.having_At_Symbol
    if re.findall("@", url):
        data_set.append(-1)
        print("@ successful")
    else:
        data_set.append(1)
        print("@ successful")

    # 5.double_slash_redirecting
    list=[x.start(0) for x in re.finditer('//', url)]
    if list[len(list)-1]>6:
        data_set.append(-1)
        print("// successful")
    else:
        data_set.append(1)
        print("// successful")

    # 6.Prefix_Suffix
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        data_set.append(-1)
        print("prefix successful")
    else:
        data_set.append(1)
        print("prefix successful")

    # 7.having_Sub_Domain
    if len(re.findall(r"\.", url)) == 1:
        data_set.append(1)
        print("subdomain successful")
    elif len(re.findall(r"\.", url)) == 2:
        data_set.append(0)
        print("subdomain successful")
    else:
        data_set.append(-1)
        print("subdomain successful")

    # 8.SSLfinal_State
    try:
        if response.text:
            data_set.append(1)
            print("SSL successful")
    except:
        data_set.append(-1)
        print("SSL successful")

    # 9.Domain_registeration_length
    expiration_date = whois_response.expiration_date
    registration_length = 0
    try:
        expiration_date = min(expiration_date)
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        registration_length = abs((expiration_date - today).days)

        if registration_length / 365 <= 1:
            data_set.append(-1)
            print("reg length successful")
        else:
            data_set.append(1)
            print("reg length successful")
    except:
        data_set.append(-1)
        print("reg length successful")

    # 10.Favicon
    if soup == -999:
        data_set.append(-1)
        print("favicon successful")
    else:
        try:
            for head in soup.find_all('head'):
                for head.link in soup.find_all('link', href=True):
                    dots = [x.start(0) for x in re.finditer(r'\.', head.link['href'])]
                    if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                        data_set.append(1)
                        print("favicon successful")
                        raise StopIteration
                    else:
                        data_set.append(-1)
                        print("favicon successful")
                        raise StopIteration
        except StopIteration:
            pass

    #11. port
    try:
        port = domain.split(":")[1]
        if port:
            data_set.append(-1)
            print("port successful")
        else:
            data_set.append(1)
            print("port successful")
    except:
        data_set.append(1)
        print("port successful")

    #12. HTTPS_token
    if re.findall(r"^https://", url):
        data_set.append(1)
        print("https successful")
    else:
        data_set.append(-1)
        print("https successful")

    #13. Request_URL
    i = 0
    success = 0
    if soup == -999:
        data_set.append(-1)
        print("request successful")
    else:
        for img in soup.find_all('img', src= True):
           dots= [x.start(0) for x in re.finditer(r'\.', img['src'])]
           if url in img['src'] or domain in img['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        for audio in soup.find_all('audio', src= True):
           dots = [x.start(0) for x in re.finditer(r'\.', audio['src'])]
           if url in audio['src'] or domain in audio['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        for embed in soup.find_all('embed', src= True):
           dots=[x.start(0) for x in re.finditer(r'\.',embed['src'])]
           if url in embed['src'] or domain in embed['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        for iframe in soup.find_all('iframe', src= True):
           dots=[x.start(0) for x in re.finditer(r'\.',iframe['src'])]
           if url in iframe['src'] or domain in iframe['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        try:
           percentage = success/float(i) * 100
           if percentage < 22.0 :
              data_set.append(1)
              print("request successful")
           elif((percentage >= 22.0) and (percentage < 61.0)) :
              data_set.append(0)
              print("request successful")
           else :
              data_set.append(-1)
              print("req successful")
        except:
            data_set.append(1)
            print("req successful")



    #14. URL_of_Anchor
    percentage = 0
    i = 0
    unsafe=0
    if soup == -999:
        data_set.append(-1)
        print("anchor of upper if successful")
    else:
        for a in soup.find_all('a', href=True):
        # 2nd condition was 'JavaScript ::void(0)' but we put JavaScript because the space between javascript and :: might not be
                # there in the actual a['href']
            if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                unsafe = unsafe + 1
            i = i + 1


        try:
            percentage = unsafe / float(i) * 100
        except:
            data_set.append(1)
            print("anchor successful")

        if percentage < 31.0:
            data_set.append(1)
            print("anchor if successful")
        elif ((percentage >= 31.0) and (percentage < 67.0)):
            data_set.append(0)
            print("anchor elif successful")
        else:
            data_set.append(-1)
            print("anchor else successful")

    #15. Links_in_tags
    i=0
    success =0
    if soup == -999:
        data_set.append(-1)
        print("links successful")
    else:
        for link in soup.find_all('link', href= True):
           dots=[x.start(0) for x in re.finditer(r'\.',link['href'])]
           if url in link['href'] or domain in link['href'] or len(dots)==1:
              success = success + 1
           i=i+1

        for script in soup.find_all('script', src= True):
           dots=[x.start(0) for x in re.finditer(r'\.',script['src'])]
           if url in script['src'] or domain in script['src'] or len(dots)==1 :
              success = success + 1
           i=i+1
        try:
            percentage = success / float(i) * 100
        except:
            data_set.append(1)
            print("links successful")

        if percentage < 17.0 :
            data_set.append(1)
            print("links successful")
        elif((percentage >= 17.0) and (percentage < 81.0)) :
            data_set.append(0)
            print("links successful")
        else :
            data_set.append(-1)
            print("@ successful")

    #17. Submitting_to_email
    if response == "":
        data_set.append(-1)
    else:
        if re.findall(r"[mail\(\)|mailto:?]", response.text):
            data_set.append(-1)
            print("email successful")
        else:
            data_set.append(1)
            print("email successful")

    #18. Abnormal_URL
    if response == "":
        data_set.append(-1)
        print("abnor successful")
    else:
        if response.text == "":
            data_set.append(1)
            print("abnor successful")
        else:
            data_set.append(-1)
            print("abnor successful")

    #19. Redirect
    if response == "":
        data_set.append(-1)
        print("redi successful")
    else:
        if len(response.history) <= 1:
            data_set.append(-1)
            print("red successful")
        elif len(response.history) <= 4:
            data_set.append(0)
            print("red successful")
        else:
            data_set.append(1)
            print("red successful")

    #20. on_mouseover
    if response == "" :
        data_set.append(-1)
        print("mouse successful")
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            data_set.append(1)
            print("mouse successful")
        else:
            data_set.append(-1)
            print("mouse successful")

    #21. RightClick
    if response == "":
        data_set.append(-1)
        print("right successful")
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            data_set.append(1)
            print("right successful")
        else:
            data_set.append(-1)
            print("right successful")

    #22. popUpWidnow
    if response == "":
        data_set.append(-1)
        print("pop successful")
    else:
        if re.findall(r"alert\(", response.text):
            data_set.append(1)
            print("pop successful")
        else:
            data_set.append(-1)
            print("pop successful")

    #23. Iframe
    if response == "":
        data_set.append(-1)
        print("iframe successful")
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            data_set.append(1)
            print("iframe successful")
        else:
            data_set.append(-1)
            print("iframe successful")

    #24. age_of_domain
    if response == "":
        data_set.append(-1)
        print("age successful")
    else:
        try:
            registration_date = re.findall(r'Registration Date:</div><div class="df-value">([^<]+)</div>', whois_response.text)[0]
            if diff_month(date.today(), date_parse(registration_date)) >= 6:
                data_set.append(-1)
                print("age successful")
            else:
                data_set.append(1)
                print("age successful")
        except:
            data_set.append(1)
            print("age successful")

    #25. DNSRecord
    dns = 1
    try:
        dns = whois.whois(domain)
    except:
        dns=-1
    if dns == -1:
        data_set.append(-1)
        print("dns successful")
    else:
        if registration_length / 365 <= 1:
            data_set.append(-1)
            print("dns successful")
        else:
            data_set.append(1)
            print("dns successful")

    #26. web_traffic
    try:
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        rank= int(rank)
        if (rank<100000):
            data_set.append(1)
            print("traffic successful")
        else:
            data_set.append(0)
            print("traffic successful")
    except TypeError:
        data_set.append(-1)
        print("traffic successful")

    #27. Page_Rank
    try:
        if global_rank > 0 and global_rank < 100000:
            data_set.append(-1)
            print("rank successful")
        else:
            data_set.append(1)
            print("rank successful")
    except:
        data_set.append(1)
        print("rank successful")

    #28. Google_Index
    site=search(url, 5)
    if site:
        data_set.append(1)
        print("index successful")
    else:
        data_set.append(-1)
        print("index successful")

    #29. Links_pointing_to_page
    if response == "":
        data_set.append(-1)
        print("age successful")
    else:
        number_of_links = len(re.findall(r"<a href=", response.text))
        if number_of_links == 0:
            data_set.append(1)
            print("no of links successful")
        elif number_of_links <= 2:
            data_set.append(0)
            print("no of links successful")
        else:
            data_set.append(-1)
            print("no of links successful")

    print (data_set)
    return data_set
