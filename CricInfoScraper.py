import requests
from bs4 import BeautifulSoup
import pandas as pd
import os.path
from colorama import Fore, Style

def scrape_results(reqUrl, page = 1, fileName = 'Data'):
    origUrl = reqUrl
    reqUrl = reqUrl + ";page=" + str(page)
    print("Getting Page" , str(page), "...")

    req = requests.get(reqUrl)
    soup = BeautifulSoup(req.content, "html.parser")
    tables = soup.find_all('table', class_ = 'engineTable')

    fields = [] # fields stores the various headers in the query

    dataTable = tables[2]

    tableHead = dataTable.thead.tr
    headers = tableHead.findAll('th')

    for header in headers:
        fields.append(header.text)

    field_count = fields.__len__()
    field_lists = [] 
    for i in range(field_count):
        field_lists.append([])

    # field_lists stores all the values of each column as an inidvidual list 

    rows = dataTable.tbody.findAll('tr')

    for row in rows:
        cols = row.findAll('td')
        j = 0
        for col in cols:
            field_lists[j].append(col.text) # append to the list of that column
            j += 1


    # The fields and the field lists are now converted to a dictionary like dict[field] = field_list 
    # so that it can be converted to a DataFrame
    resultDict = {}
    for i in range(len(fields)):
        resultDict[fields[i]] = field_lists[i] 
    
    df = get_result_dataframe(resultDict, fileName)

    df.dropna(axis = 1, how = 'all', inplace = True)
    # Since the Table on ESPN CricInfo contains some blank columns

    df.to_csv("Output/" + fileName, index = False)

    # If there are more pages, we make a recursive call doing the same for the next page
    if (check_more_pages(tables)):
        scrape_results(origUrl, page + 1, fileName)
    else:
        print(Fore.GREEN + "Output .csv file available in: " + os.path.abspath("Output/" + fileName))
        print(Style.RESET_ALL)


def check_more_pages(tables):
    pageInfoTable = tables[1]
    pageInfo = pageInfoTable.tr.td.text
    pageSplit = pageInfo.strip().split(' ')
    currPage = int(pageSplit[1])
    finalPage = int(pageSplit[3])
    if currPage < finalPage:
        return True

    return False

# If there is already some data in the CSV file, we read and convert it into a DataFrame
# and then append this page's data onto it
def get_result_dataframe(resultDict, fileName):
    currPageDf = pd.DataFrame(resultDict)
    prevDf = None
    filePath = "Output/" + fileName
    if (os.path.exists(filePath)):
        prevDf = pd.read_csv(filePath)
        prevDf = prevDf.append(currPageDf)

    if isinstance(prevDf, pd.DataFrame):
        return prevDf
    else: 
        return currPageDf      

def create_output_folder():
    if os.path.isdir("Output"):
        return
    else: 
        try: 
            os.mkdir("Output")
        except OSError as error:
            print(Fore.RED + error)
            print(Style.RESET_ALL)


if __name__ == '__main__':
    reqUrl = input("Enter the URL which from which to scrape the table: ")
    outputName = input("Enter the name of the output file(without extension): ")
    outputName += ".csv"

    create_output_folder()
    scrape_results(reqUrl = reqUrl, fileName = outputName)
    

    # Sample Request URLs:
    # https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;orderby=start;size=200;spanmin1=01+Jan+1975;spanval1=span;template=results;type=aggregate;view=match
    # https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;home_or_away=1;host=6;opposition=1;spanmin1=15+Mar+2001;spanval1=span;team=6;template=results;type=bowling;view=match
    # https://stats.espncricinfo.com/ci/engine/stats/index.html?class=3;team=6;template=results;type=team;view=results
    # https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;opposition=5;spanmin1=15+Mar+1995;spanval1=span;team=6;template=results;type=bowling