#Write a python script to construct the following pattern

#1.a - Pyramid
n = int(input("Enter the number of rows"))
# outer loop to handle number of rows  
for i in range(0, n):  
    # inner loop to handle number of columns  
    # values is changing according to outer loop  
        for j in range(0, i + 1):
            print("* ", end="")       
        print() 
#1.b - Two Pyramid
rows = int(input("Enter the number of rows: "))
  
# Outer loop will print the number of rows  
for i in range(0, rows):  
    # This inner loop will print the stars  
    for j in range(0, i + 1):  
        print("*", end=' ')  
    # Change line after each iteration  
    print(" ")  
# For second pattern  
for i in range(rows + 1, 0, -1):  
    for j in range(0, i - 1):  
        print("*", end=' ')  
    print(" ")

#2. Write a program to calculate and print the factorial of a number using a for loop.
fact = int(input("Enter number to find factorial "))
if fact >0:
    for i in range(1,fact):
        fact = fact*i
    print(fact)
elif fact==0:
    print("Factorial of 0 is 1")
else:
    print(" Factorial does not exist for negative numbers")

#3. Write a Python script using nested for loop to create a chess board, 
# use table width = 270px and take 30px as cell height and width. 
# You need to output HTML in a file on the local file system which when 
# opened in the browser looks like a chess board.
Html = '''
<html> 
     <head> 
  <title></title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  </head>
  <body> 
  <h3>Chess Board using Nested For Loop</h3>
   <table width="270px" cellspacing="0px" cellpadding="0px" border="1px">
'''
for row in range(1,9):
    Html = Html + '<tr>'
    for col in range(1,9):
        total = row+col
        if total%2==0:
            Html = Html +'<td height=30px width=30px bgcolor=#FFFFFF></td>'
            
        else:
            Html = Html +'<td height=30px width=30px bgcolor=#000000></td>'
            
    Html = Html +'</tr>'

Html = Html +'''</table>
  </body>
  </html>
'''

with open('Chess_Board.html', "w") as myfile:
    myfile.write(Html)
