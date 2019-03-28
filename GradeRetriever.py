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

def getStandingsTable(soup):
    # Retrieves all rows from standings table on course webpage
    tables = soup.findAll('td', attrs={'width': '50%'})
    return tables[1]

def cleanRows(rows):
    extraStringType = type(rows[0])

    # Filter out extra NavigableString objects
    for obj in rows:
        if type(obj) == extraStringType:
            rows.remove(obj)

def getMenuContents(rows, menuTable, linkTable):
    for row in rows:
        # Gets row contents
        rowContents = row.contents
        removeListSpaces(rowContents)

        # Loops through tags in each row
        for tag in rowContents:
            tagContents = tag.contents
            removeListSpaces(tagContents)

            # Checks if link and not just text
            if len(tagContents[0].contents) > 1:
                menuTable.append(tagContents[0].contents[1].string)
                linkTable.append(tagContents[0].contents[1]['href'])

def printMenu(menuTable):
    # Print menu
    counter = 1
    for option in menuTable:
        print(str(counter) + '. ' + option)
        counter += 1
  

def getHeader(rows, finalTable):
    # Adds table header
    for x in range(3):
        finalRow = []
        currentRow = rows[0].contents
        cleanRows(currentRow)

        for col in currentRow:
            finalRow.append(unicode(col.text))

            # Accounts for one header covering multiple columns
            if 'colspan' in col.attrs:
                numCols = int(col.attrs['colspan'])
                for extraCols in range(numCols - 1):
                    finalRow.append('')

        finalTable.append(finalRow)
        del rows[0]

def getStudent(rows, number, finalTable):
    # Finds and adds student to table
    for student in rows:
        if unicode(student.contents[1].string) == number:
            studentRow = []
            for col in student.contents:
                studentRow.append(unicode(col.string))
                
            finalTable.append(studentRow)
            return

def removeTableSpaces(finalTable):
    # Removes all unnecessary spaces used for padding
    for row in finalTable:
        for col in row:
            if col == ' ':
                row.remove(col)

def removeListSpaces(theList):
    for obj in theList:
        if obj == ' ':
            theList.remove(obj)

def printStandings(finalTable):
    colWidths = []
    
    # Calculates column widths
    for col in range(len(finalTable[1])):
        currentMax = 0
        for row in range(len(finalTable)):
            if col < len(finalTable[row]) and len(finalTable[row][col]) > currentMax:
                currentMax = len(finalTable[row][col])
        colWidths.append(currentMax + 2)

    # Prints each row
    for row in finalTable:
        currentRow = ""
        for col in range(len(row)):
            currentRow += row[col].ljust(colWidths[col])
        print(currentRow)

def main():
    # Retrieve global input
    originalLink = raw_input("Enter Gradesource class link: ")
    number = raw_input("Enter secret number: ")

    # Setsup soup
    soup = setupSoup(originalLink)
    
    # Retrieves standings table
    table = getStandingsTable(soup)
    
    # Retrieve table rows
    rows = table.table.contents

    cleanRows(rows)

    menuTable = []
    linkTable = []

    getMenuContents(rows, menuTable, linkTable)

    option = ''

    while option != 'q':
        printMenu(menuTable)

        option = raw_input("Enter selection (q to quit): ")
        
        if option != 'q':
            # Switches link
            link = originalLink
            link = link.replace("index.html", str(linkTable[int(option) - 1]))

            # Reset soup
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
            removeTableSpaces(finalTable)

            # Prints the standings
            printStandings(finalTable)
            
            option = raw_input("Press any key to return to the menu (q to quit)... ")


main()
