#!/usr/bin/perl -w
use strict; 
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use Fcntl qw(:flock);

my $cgi = new CGI;
# Read in the data from HTML form
my $username = $cgi->param( "username" );
my $password = $cgi->param( "password" ); 
#my $username = "cis393";
#my $password = "web"; 
my $login = "fail";
		
my $salt = "21";
my $enpass = crypt($password,$salt);
open(PASSWDDATA, "<passwd.txt") or die "Can not open passwd.txt";

#Read in the data from the passwd.txt file
my $line = <PASSWDDATA>;
#my $j = 1;
#while( !eof(PASSWDDATA))
while(1)
{
	my @namepass = split(' ',$line);
	if($namepass[0] eq $username && $namepass[1] eq $enpass)
	{
	  $login = "success";
	  last;
	}
	$line = <PASSWDDATA>; 
	if(eof(PASSWDDATA))
	{
		my @namepass = split(' ',$line);
		if($namepass[0] eq $username && $namepass[1] eq $enpass)
		{
	 		 $login = "success";
	  		 last;
		}
		last;
	}
}
close(PASSWDDATA);

#close(PASSWDDATA);
#displayOtherHTMLPage($cgi);

if($login eq "success")
{		
	print $cgi->redirect('http://cs99.bradley.edu/~mnyamagouda/Club.html');
}
else
{
	#print("<meta http-equiv='refresh' content='2;url=http://cs99.bradley.edu/~snayak/Danceclub/Login_page.html' />");
	print $cgi->redirect('http://cs99.bradley.edu/~mnyamagouda/login.html');
}


# creates the Other page

