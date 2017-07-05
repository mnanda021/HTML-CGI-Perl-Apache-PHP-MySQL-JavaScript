# HTML-CGI-Perl-Apache-PHP-MySQL-JavaScript

1. HTML Forms  Design and develop Web pages with HTML5 Forms using Dreamweaver (or other Web page development software package approved by the instructor) to login as an existed member or register as a new member for a club web site.  (You may make up a fictitious club for this project.) The HTML5 forms should have as many major elements as possible such as Text and password fields; Checkboxes; Radio buttons; Submit and reset buttons; List and scrolling box; Text Area, and Filefield. 

2. CGI Scripts  Develop CGI scripts to accept and process the requests from the above HTML5 Forms on CS1.  
      1. Develop a login CGI script login.cgi  - Authenticate the user. The encrypted passwords could be stored in your script or an external file. (You may use “$encpwd=crypt($pwd,$salt);” to encrypt the password.) 
      2. Develop a register CGI script register.cgi  - Process the new membership info from the user  - Send a HTML5 page back to the user to display the process result  - (Extra Credit) Send an email back to the user to confirm the registration.  
      3. (Optional) Develop a data store CGI script to store the registration info either in external files or in a database.


A. HTML Forms

Modify the Web pages developed in assignment 1 with the 5 more additional HTML5 Web Page elements (not include the Audio and Video used in the Crap game) listed in the textbook.  

B. HTML Web Pages with JavaScript

Modify the Web pages developed in assignment 1 using JavaScript with the following features:

1. Input data validation 
All the input data items must be validated before been sent to the CGI/Perl script. You can design your own validation criteria for different fields.
(Please use both the alert function and innerHTML to display the errors.)
2. Rich web page presentation 
Make the web pages rich with the features similar to the examples on the textbook. The JavaScript must have the following:

-Selection control statement
-Repetition control statement (Display a table with alternate row background colors as shown on Fig 8.6 of the textbook.) 
-Functions
-Arrays
-Objects (should include a Date object on your web page to display the local date and time info.)
-Events.
3. Dynamic HTML presentation
-Add animations/slide show, pull-down DHTML menus, and computer games using JavaScript on the web page.
-Implement the Craps game listed in 9.6 of the textbook on your club website.
·          Craps Game Code
 Implement the Draw program listed in 13.3 of the textbook on your club website.
·         Draw Program Code
-You may also find and add more dynamic HTML applications on the Internet.



1. Setting up the Web Server, PHP, and MySQL on your laptop

Download and set up a web server that supports the PHP and a MySQL for hosting the PHP and MySQL database.
(You may use different port other than 8080 if the port is been used.)

2. Deploy and test the PHP and MySQL

Deploy and test a sample example from the server document.

Part II:
1. HTML/PHP Web pages

Design and develop Web pages with PHP to process the data from the winestore MySQL database. You must not assume that the user knows the SQL queries, so your GUI design can’t ask the user to enter the SQL commands.
Click the winestore.data link to download the SQL script to create the winestore database:
$mysql –u username –p
 >(type in password)
…
mysql> source winestore.data;
