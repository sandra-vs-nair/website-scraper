# -----------------------------------------------------------
# Creating a real-estate website scraper using python.
#
# (C) 2020 Sandra VS Nair, Trivandrum
# email sandravsnair@gmail.com
# -----------------------------------------------------------

import requests,pandas
from bs4 import BeautifulSoup

#Creating dataframe with column headings.
df=pandas.DataFrame(columns=["Price","Address","Bedrooms","Full Baths","Half Baths","Lot Size"])

#Base url of the website containing information on properties of Rock springs area.
base_url="http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=0&s="

#To move through each search result page.
for page in range(0,30,10):
    url=base_url+str(page)
    r = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) \
                 Gecko/20100101 Firefox/61.0'})
    #Getting the content of the html page.
    c=r.content

    #Parsing the content.
    soup=BeautifulSoup(c,"html.parser")

    #Extracting all div sections in the html pages with class name propertyRow.
    #These divs represent properties for sale.
    divs=soup.find_all("div",{"class":"propertyRow"})

    #Extracting the needed information of each property listed.
    for div in divs:
        price=div.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")
        address=div.find_all("span",{"class":"propAddressCollapse"})[0].text
        address+=" "
        address+=div.find_all("span",{"class":"propAddressCollapse"})[1].text
        #Using try...except since the below informations may not be present for all properties.
        try:
            bed=div.find("span",{"class":"infoBed"}).find("b").text
        except:
                bed="--"
        try:
            fullbath=div.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            fullbath="--"
        try:
            halfbath=div.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            halfbath="--"
        
        lotsize="--"
        for item in div.find_all("div",{"class":"columnGroup"}):
            for featureGroup, featureName in zip(item.find_all("span",{"class","featureGroup"}),item.find_all("span",{"class","featureName"})):
                if "Lot Size" in featureGroup.text:
                    lotsize=featureName.text.replace(",","")
                    
        #Appending the information of a property to the data frame.
        df=df.append({"Price":price,"Address":address,"Bedrooms":bed,"Full Baths":fullbath,\
                  "Half Baths":halfbath,"Lot Size":lotsize},ignore_index=True)

#Writing the information to a csv file.
df.to_csv("RealEstate.csv",mode="w")