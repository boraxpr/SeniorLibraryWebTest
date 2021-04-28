import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from collections import namedtuple
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = namedtuple('url', 'url')
login = url('https://localhost:44313/Identity/Account/Login')
request = url('https://localhost:44313/Requests')
roles = url('https://localhost:44313/Roles')
userroles = url('https://localhost:44313/UserRoles')
upload = url('https://localhost:44313/Upload')
download = url('https://localhost:44313/Download/Download?id=1')

usr = "ictadmin"
password = "123Pa$$word."

with requests.session() as session:
    # login test
    response = session.get(login.url, verify=False)
    token = BeautifulSoup(response.text, features='html.parser').find('input', {'name': '__RequestVerificationToken'})['value']
    states = ["__RequestVerificationToken", "Email", "RememberMe"]
    login_data = {"Input.Email": usr, "Input.Password": password, "__RequestVerificationToken": token}
    post_request = session.post(login.url, data=login_data, verify=False)
    soup = BeautifulSoup(post_request.content, features="html.parser")
    result = (post_request.status_code == 200)
    print("Login test : %s" % result)
    # # END login
    # # request test
    r = session.get(request.url, verify=False)
    soup = BeautifulSoup(r.content, features="html.parser")
    data = []
    table = soup.find('table', attrs={'class': 'table'})
    table_data = table.tbody.find_all("tr")
    head = []
    td = table_data[0].find("td", attrs={'class': 'SubmittorEmail'})
    td_list = td.text.replace(' ', '').replace('\r', '').split('\n')
    test = [i for i in td_list if i]
    print("Request test : %s" % test[0])

    # Userroles test
    r = session.get(userroles.url, verify=False)
    soup = BeautifulSoup(r.content, features="html.parser")
    print("UserRoles test : %s" % (soup.title.text == "UserRoles - SeniorLibrary"))

    # Roles test
    r = session.get(roles.url, verify=False)
    soup = BeautifulSoup(r.content, features="html.parser")
    print("Roles test : %s" % (soup.title.text == "Roles - SeniorLibrary"))

    # Upload test
    r = session.get(upload.url, verify=False)
    soup = BeautifulSoup(r.content, features="html.parser")
    print("Upload test [Access] : %s" % (soup.title.text == "Index - SeniorLibrary"))

    r = session.post(upload.url, files={"files": open("SP-Webtest.pdf", 'rb')})
    if r.ok:
        print("Upload test [file upload] : True")
    else:
        print("Upload test [file upload] : False")

    # Download test
    r = session.get(download.url, verify=False)
    soup = BeautifulSoup(r.content, features="html.parser")
    print("Download test [Access] : %s" % (soup.title.text == "Download - SeniorLibrary"))
    r = session.post(download.url, verify=False)
    print("Download test [file download] : %s" % (type(r.content) == bytes))
