#!/usr/bin/perl -wT

use strict;
use CGI;
use Fcntl qw( :DEFAULT :flock );

use constant UPLOAD_DIR     => "/home/jiangbo/public_html/perl";
use constant BUFFER_SIZE    => 16_384;
use constant MAX_FILE_SIZE  => 1_048_576;       # Limit each upload to 1 MB
use constant MAX_DIR_SIZE   => 100 * 1_048_576; # Limit total uploads to 100 MB
use constant MAX_OPEN_TRIES => 100;

$CGI::DISABLE_UPLOADS   = 0;
$CGI::POST_MAX          = MAX_FILE_SIZE;

my $q = new CGI;
$q->cgi_error and error( $q, "Error transferring file: " . $q->cgi_error );

my $file      = $q->param( "file" )     || error( $q, "No file received." );
my $filename  = $q->param( "filename" ) || error( $q, "No filename entered." );
#my $file      = "Garden.jpg";
#my $filename  = "myGarden.jpg";
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
print $q->redirect('http://cs99.bradley.edu/~mnyamagouda/contact.html');
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
