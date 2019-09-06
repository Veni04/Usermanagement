Question Generation System

Created html file for the Adding Question to the file and geneate the question paper.

For adding the question: There are 3 text boxes to add 1. Question
2. Difficulty Leve
3. For marks

On entering these details, the questions will store in csv file

While generating question paper: There are 3 option to select:
1.Total Marks
2. % of difficulty level

Assumtion is made in this section. While geneating question paper, the random numbers are genrated to make the total sum of the selected difficulty level. If those marks present in the csv file, then the question paper is created based on the marks.


To test this code, i have used djnago set up. Its possible to test with normal html viewer like any browser.

To add new question go to : http://127.0.0.1:8000/
To generate Question Paper go to : http://127.0.0.1:8000/paperGen_form/

Note: The url depends on the port and the path, where the main code deployed




