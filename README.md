# GradeSourceScrubber #
Simple python script that retrieves a student's overall standing in a course from GradeSource based on the student's secret number

# Installation
`sudo install.sh`

# Usage
Locally:  
`python3 GradeRetriever.py [GradeSource link] [secret number]`
  
Globally:  
`graderetriever [GradeSource link] [secret number]`

# Future Features (WIP)
* Storage of class URLs (and possibly secret numbers) beyond execution
  * Note: Storing secret numbers beyond execution can be a secuiry risk
* File output
* Cleaner method for displaying tables with large columns