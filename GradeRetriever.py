import requests
from bs4 import BeautifulSoup

def setupSoup(link):
    # Setup BeautifulSoup
    request = requests.get(link)
    return BeautifulSoup(request.text, 'html.parser')

def getRows(soup):
    # Retrieves standings table
    table = soup.find('table', attrs={'cellpadding': '3', 'cellspacing': '0','border': '1'})
    return table.contents

def cleanRows(rows):
    extraStringType = type(rows[0])

    # Filter out extra NavigableString objects
    for obj in rows:
        if type(obj) == extraStringType:
            rows.remove(obj)

def getHeader(rows, finalTable):
    # Adds table header
    for x in range(3):
        finalRow = []
        currentRow = rows[0].contents
        cleanRows(currentRow)

        for col in currentRow:
            finalRow.append(unicode(col.text))
        finalTable.append(finalRow)
        del rows[0]

def getStudent(rows, number, finalTable):
    # Finds and adds student
    for student in rows:
        if unicode(student.contents[1].string) == number:
            studentRow = []
            for col in student.contents:
                studentRow.append(unicode(col.string))
                
            finalTable.append(studentRow)
            return

def removeSpaces(finalTable):
    for row in finalTable:
        for col in row:
            if col == ' ':
                row.remove(col)

def printStandings(finalTable):
    colWidths = []
    
    for col in range(len(finalTable[1])):
        currentMax = 0
        for row in range(len(finalTable)):
            if col < len(finalTable[row]) and len(finalTable[row][col]) > currentMax:
                currentMax = len(finalTable[row][col])
        colWidths.append(currentMax + 2)

    #print(finalTable[3])
    #print(len(finalTable[3]))

    for row in finalTable:
        currentRow = ""
        for col in range(len(row)):
            #print(col)
            #print(len(row))
            currentRow += row[col].ljust(colWidths[col])
        print(currentRow)

    # Width and padding
    #colWidth = max(len(word) for row in finalTable for word in row)
    #for row in finalTable:
    #    print("".join(word.ljust(colWidth) for word in row))

def main():
    # Retrieve global input
    link = raw_input("Enter Gradesource class link: ")
    number = raw_input("Enter secret number: ")

    # Changes link to standings
    link = link.replace("index.html", "coursestand.html")

    # Setsup soup
    soup = setupSoup(link)
    
    # Retrieves standings table rows
    rows = getRows(soup)
    
    # Removes extra String objects
    cleanRows(rows)

    finalTable = []

    # Retrieve header
    getHeader(rows, finalTable)

    # Retrieve student
    getStudent(rows, number, finalTable)
    
    # Removes uneccesary spaces
    removeSpaces(finalTable)

    # Prints the standings
    printStandings(finalTable)


main()
