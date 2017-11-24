#!/usr/bin/perl
# Sript to parse corpora in XML, and produce well balanced random splits.
# Input format:
# 
# <corpus source="LLL">
#   <document id="LLL.d0" origId="11069677">
#     <sentence id="LLL.d0.s0" origId="11069677-3" text="In vivo studies of the activity of four of the kinases, KinA, KinC, KinD (ykvD) and KinE (ykrQ), using abrB transcription as an indicator of Spo0A~P level, revealed that KinC and KinD were responsible for Spo0A~P production during the exponential phase of growth in the absence of KinA and KinB.">
#       <entity charOffset="170-173" id="LLL.d0.s0.e0" origId="29" text="KinC" type="agent" />
#       <entity charOffset="179-182" id="LLL.d0.s0.e1" origId="31" text="KinD" type="agent" />
#       <entity charOffset="205-211" id="LLL.d0.s0.e2" origId="35" text="Spo0A~P" type="target" />
#       <pair e1="LLL.d0.s0.e0" e2="LLL.d0.s0.e1" id="LLL.d0.s0.p0" interaction="False" />
#       <pair e1="LLL.d0.s0.e0" e2="LLL.d0.s0.e2" id="LLL.d0.s0.p1" interaction="True" />
#       <pair e1="LLL.d0.s0.e1" e2="LLL.d0.s0.e2" id="LLL.d0.s0.p2" interaction="True" />
# ...
# output:
#  <corpus> +- <corpus>0.txt
#           |
#           +- <corpus>1.txt
#           |
#           ...
#  where each .txt file has a list of document IDs, one per line


use strict;
use warnings;

use XML::Parser;
use List::Util qw(shuffle); # first max maxstr min minstr reduce sum
use Data::Dumper;
 

# main

if ($#ARGV < 0)
{
	print "Usage $0 <corpus.xml> ...\n";
	exit -1;
}

my $parser = new XML::Parser;

my $splits = 10;

my @docs = ();

# Kersten:
my @IDs = ();
my @indexes = ();
my $index = 0;

my %trueExamples = ();
my %falseExamples = ();

$parser->setHandlers(
	Start => \&startElement,
	End => \&endElement,
	Char => \&characterData,
	Default => \&default);

# quoting
my $q = '$$';

# current values
my ($corpus, $document, $sentence, $entity, $pair);

foreach my $xmlfile (@ARGV)
{
	die "Cannot find file $q$xmlfile$q"
		unless -f $xmlfile;

	$parser->parsefile($xmlfile);
}


# subs

sub startElement 
{

	my( $parseinst, $element, %attrs ) = @_;
	SWITCH: {
		# <corpus source="LLL">
		if ($element eq 'corpus') {
			$corpus = $attrs{'source'};
			last SWITCH;
		}
		# <document id="LLL.d0" origId="11069677">
		if ($element eq 'document') {
			$document = $attrs{'id'} or warn();
			my $origId = $attrs{'origId'} || $attrs{'origID'} or warn();

			# save
			push(@docs, $document);
			# Kersten:
			push(@IDs, $origId);
			push(@indexes, $index);
			$index = $index + 1;

			$trueExamples{$document} = 0;
			$falseExamples{$document} = 0;
			last SWITCH;
		}
		# <sentence id="LLL.d0.s0" origId="11069677-3" text="In vivo studies of the activity of four of the kinases, KinA, KinC, KinD (ykvD) and KinE (ykrQ), using abrB transcription as an indicator of Spo0A~P level, revealed that KinC and KinD were responsible for Spo0A~P production during the exponential phase of growth in the absence of KinA and KinB.">
		if ($element eq 'sentence') {
			$sentence = $attrs{'id'} or warn();
			my $origId = $attrs{'origId'} || $attrs{'origID'} || $attrs{'seqId'} || "";
			my $text = $attrs{'text'} or warn();

			last SWITCH;
		}
		# <entity charOffset="205-211" id="LLL.d0.s0.e2" origId="35" text="Spo0A~P" type="target" />
		if ($element eq 'entity') {
			$entity = $attrs{'id'} or warn("entity:id");
			my $origId = $attrs{'origId'} || $attrs{'origID'} || "";
			my $text = $attrs{'text'} or warn();
			my $type = $attrs{'type'} || "";# warn();
			my ($begin, $end, $begin2, $end2) = ($attrs{'charOffset'} =~ m/^(\d+)-(\d+)(?:,(\d+)-(\d+))?(.+)?$/) or warn($attrs{'charOffset'});
			warn($attrs{'charOffset'}) if defined $5;
			if (!defined $begin2) {$begin2='NULL';$end2='NULL';}
			last SWITCH;
		}
		#       <pair e1="LLL.d0.s0.e0" e2="LLL.d0.s0.e1" id="LLL.d0.s0.p0" interaction="False" />
		if ($element eq 'pair') {
			$pair = $attrs{'id'} or warn();
			my $e1 = $attrs{'e1'} or warn();
			my $e2 = $attrs{'e2'} or warn();
			my ($interaction) = $attrs{'interaction'} or warn();

			my $groundTruth;
			$groundTruth = 0 if $interaction =~ /False/i;
			$groundTruth = 1 if $interaction =~ /True/i;
            
			warn() unless defined $groundTruth;
            
            $trueExamples{$document}++ if $groundTruth;
            $falseExamples{$document}++ if !$groundTruth;

			last SWITCH;
		}
	}
}

sub endElement 
{
    my( $parseinst, $element ) = @_;

    if ($element eq 'corpus') {
        my $dir = $corpus;
        print STDERR "Splitting corpus '$corpus' ...\n";
        mkdir $dir;
        
        my @fhs = ();
        for my $i (0..($splits-1))
        {
            my $file = "$dir/$corpus" . scalar($i + 1) . ".txt";
            open($fhs[$i], '>', $file) or die $!;
        }
        
        
        my %splitTrue = ();
        # Kersten:
        @indexes = shuffle @indexes;
        # old:
        #@docs = shuffle @docs;
        foreach my $i (0..$#indexes)
        {
            my $split = int(($i/(0.0 + $#docs+1)) * $splits);
            my $fh = $fhs[$split];
            # Kersten:
            my $doc = $docs[$indexes[$i]];
            my $ID = $IDs[$indexes[$i]];
            # old:
            #my $doc = $docs[$i];

            # old:
            #print $fh "$doc\n"
            # Kersten:
            print $fh "$ID $doc\n";
            # old:
            #print $fh "$doc\n";
            $splitTrue{$split} += ($trueExamples{$doc} + 0);
        }
        
        for my $i (0..($splits-1))
        {
            close($fhs[$i]);
        }
        
        print STDERR Dumper(\%splitTrue);
        
        @docs = ();
    }
}

sub characterData
{
	my( $parseinst, $data ) = @_;
}

sub default 
{	
	my( $parseinst, $data ) = @_;
        # do nothing, but stay quiet
}
