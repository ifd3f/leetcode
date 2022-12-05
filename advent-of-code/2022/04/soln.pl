#!/usr/bin/env perl

use strict;
use warnings;

sub parseline {
    my @halved = split(/,/, $_[0]);
    my @el = split(/-/, $halved[0]);
    my @er = split(/-/, $halved[1]);
    return (\@el, \@er);
}

sub fully_contains {
    my ($al, $ar) = @{ $_[0] };
    my ($bl, $br) = @{ $_[1] };
    
    return ($al <= $bl && $br <= $ar) || ($bl <= $al && $ar <= $br);
}

sub has_overlap {
    my ($al, $ar) = @{ $_[0] };
    my ($bl, $br) = @{ $_[1] };
    
    return $al <= $br && $bl <= $ar;
}


open(my $fd, "input")
    or die "error: $!";

my $p1total = 0;
while (my $line = <$fd>) {
    chomp($line);
    $p1total += fully_contains(parseline($line));
}
print "Part 1: $p1total\n";

open(my $fd, "input")
    or die "error: $!";

my $p2total = 0;
while (my $line = <$fd>) {
    chomp($line);
    $p2total += has_overlap(parseline($line));
}
print "Part 2: $p2total\n";

close $fd;

