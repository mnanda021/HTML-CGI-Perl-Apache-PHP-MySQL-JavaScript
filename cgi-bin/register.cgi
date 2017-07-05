#!/usr/bin/perl -w
use strict; 
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

my $obj = new CGI;
my $datastring ="";
my $datastring2 ="";
use strict;
use CGI;
use Fcntl qw( :DEFAULT :flock );

use constant UPLOAD_DIR     => "/home/mnyamagouda/public_html/cgi-bin/images";
use constant BUFFER_SIZE    => 16_384;
use constant MAX_FILE_SIZE  => 1_048_576;       # Limit each upload to 1 MB
use constant MAX_DIR_SIZE   => 100 * 1_048_576; # Limit total uploads to 100 MB
use constant MAX_OPEN_TRIES => 100;

$CGI::DISABLE_UPLOADS   = 0;
$CGI::POST_MAX          = MAX_FILE_SIZE;



my $firstname = $obj->param("firstname");
my $lastname = $obj->param("lastname");
my $email = &validate_email_address( $obj->param( "email" ) );
my $username =$obj->param("username");
my $password = $obj->param("password");
my $dob = $obj->param("dob");
my $address = $obj ->param("address");
my $country = $obj->param("country");
my $state = $obj->param("state");
my $age = $obj -> param("age");
my $work_phone = $obj->param("work_phone");
my $home_phone = $obj->param("home_phone");
my $social_security = $obj->param("social_security");
my $zip = $obj->param("zip");
my $gender = $obj->param("gender");
my @interests = $obj->param("interests");
my $interests2="";
foreach my $interest (@interests){
	$interests2 .="$interest\t";
}
my $education = $obj->param("education");
my $salt = "21";
my $enpass = crypt($password,$salt);

unless ( $email ) {
    print $obj->header( "text/html" ),
          $obj->start_html( "Invalid Email Address" ),
          $obj->h1( "Invalid Email Address" ),
          $obj->p( "The email address you entered is invalid. " .
                 "Please use your browsers Back button to " .
                 "return to the form and try again." );
          $obj->end_html;
    exit;
}

$datastring = "$firstname $lastname $email $username $enpass $dob $address $state $country $work_phone $home_phone $social_security $age $gender $interests2 $education\n";
open(OUTDATA,">>data.txt") or die "Error in opening the data.txt";
print OUTDATA $datastring;
close(OUTDATA);
$datastring2 = "$username $enpass\n";
open(OUTDATA,">>passwd.txt") or die "Error in opening the data.txt";
print OUTDATA $datastring2;
close(OUTDATA);

my $q = new CGI;
$q->cgi_error and error( $q, "Error transferring file: " . $q->cgi_error );

my $file      = $q->param( "file" )     || error( $q, "No file received." );
my $filename  = $q->param( "filename" ) || error( $q, "No fil
ename entered." );
my $fh        = $q->upload( "file" );
my $buffer    = "";

if ( dir_size( UPLOAD_DIR ) + $ENV{CONTENT_LENGTH} > MAX_DIR_SIZE ) {
    error( $q, "Upload directory is full." );
}

# Allow letters, digits, periods, underscores, dashes
# Convert anything else to an underscore
$filename =~ s/[^\w.-]/_/g;
if ( $filename =~ /^(\w[\w.-]*)/ ) {
    $filename = $1;
}
else {
    error( $q, "Invalid file name; files must start with a letter or number." );
}

# Open output file, making sure the name is unique
until ( sysopen OUTPUT, UPLOAD_DIR . "/$filename", O_CREAT | O_RDWR | O_EXCL ) {
    $filename =~ s/(\d*)(\.\w+)$/($1||0) + 1 . $2/e;
    $1 >= MAX_OPEN_TRIES and error( $q, "Unable to save your file." );
}

# This is necessary for non-Unix systems; does nothing on Unix
binmode $fh;
binmode OUTPUT;

# Write contents to output file
while ( read( $fh, $buffer, BUFFER_SIZE ) ) {
    print OUTPUT $buffer;
}

close OUTPUT;

#print $q->header( "text/plain" ), "File received.";

 
sub dir_size {
    my $dir = shift;
    my $dir_size = 0;
    
    # Loop through files and sum the sizes; doesn't descend down subdirs
    opendir DIR, $dir or die "Unable to open $dir: $!";
    #while ( readdir DIR ) {
    #    $dir_size += -s "$dir/$_";
    #}
    return $dir_size;
}

sub error {
    my( $q, $reason ) = @_;
    
    print $q->header( "text/html" ),
          $q->start_html( "Error" ),
          $q->h1( "Error" ),
          $q->p( "Your upload was not procesed because the following error ",
                 "occured: " ),
          $q->p( $q->i( $reason ) ),
          $q->end_html;
    exit;
}
#file upload end


my $from="mnyamagouda\@mail.bradley.edu";
my $to=$obj->param("email");
my $subject="Registration Confirmation";
my $sendmailpath="/usr/sbin/sendmail";



#print $obj->header;
#print "Confirmation";



open (SENDMAIL, "| $sendmailpath -t");
print SENDMAIL "Subject: $subject\n";
print SENDMAIL "From: $from\n";
print SENDMAIL "To: $to\n\n";
print SENDMAIL "Thank you, $firstname\n\n";
print SENDMAIL "You are successfully registered to Fashion - Club. We help you to achieve your dreams!\n";
print SENDMAIL "Stay tuned to us.\n\n\n";
print SENDMAIL "Your Information\n\n\n";
print SENDMAIL "FirstName: $firstname\n";
print SENDMAIL "LastName: $lastname\n";
print SENDMAIL "Email:$email\n";
print SENDMAIL "Username: $username\n";
print SENDMAIL "Password: $password\n";
print SENDMAIL "Date of Birth: $dob\n";
print SENDMAIL "Gender: $gender\n";
print SENDMAIL "Country: $country\n";
print SENDMAIL "state: $state\n";
print SENDMAIL "Education: $education\n";
print SENDMAIL "Age: $age\n";
print SENDMAIL "work_phone: $work_phone\n";
print SENDMAIL "home_phone: $home_phone\n";
print SENDMAIL "social_security: $social_security\n";
print SENDMAIL "Interests:$interests2\t\n\n";
print SENDMAIL "Best\n";
print SENDMAIL "Fashion-Club!\n\n";
close (SENDMAIL);

print $obj->redirect('http://cs99.bradley.edu/~mnyamagouda/Club.html');




# email validation

sub validate_email_address {
    my $addr_to_check = shift;
    $addr_to_check =~ s/("(?:[^"\\]|\\.)*"|[^\t "]*)[ \t]*/$1/g;
    
    my $esc         = '\\\\';
    my $space       = '\040';
    my $ctrl        = '\000-\037';
    my $dot         = '\.';
    my $nonASCII    = '\x80-\xff';
    my $CRlist      = '\012\015';
    my $letter      = 'a-zA-Z';
    my $digit       = '\d';
    
    my $atom_char   = qq{ [^$space<>\@,;:".\\[\\]$esc$ctrl$nonASCII] };
    my $atom        = qq{ $atom_char+ };
    my $byte        = qq{ (?: 1?$digit?$digit | 
                              2[0-4]$digit    | 
                              25[0-5]         ) };
    
    my $qtext       = qq{ [^$esc$nonASCII$CRlist"] };
    my $quoted_pair = qq{ $esc [^$nonASCII] };
    my $quoted_str  = qq{ " (?: $qtext | $quoted_pair )* " };
    
    my $word        = qq{ (?: $atom | $quoted_str ) };
    my $ip_address  = qq{ \\[ $byte (?: $dot $byte ){3} \\] };
    my $sub_domain  = qq{ [$letter$digit]
                          [$letter$digit-]{0,61} [$letter$digit]};
    my $top_level   = qq{ (?: $atom_char ){2,4} };
    my $domain_name = qq{ (?: $sub_domain $dot )+ $top_level };
    my $domain      = qq{ (?: $domain_name | $ip_address ) };
    my $local_part  = qq{ $word (?: $dot $word )* };
    my $address     = qq{ $local_part \@ $domain };
    
    return $addr_to_check =~ /^$address$/ox ? $addr_to_check : "";
}

