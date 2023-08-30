#!/usr/bin/perl -w

use strict;
use warnings;
use Time::Piece;
use Time::Seconds;
use List::Util qw(sum max);
use Getopt::Long qw(GetOptions);
Getopt::Long::Configure qw(gnu_getopt);
use Scalar::Util qw(looks_like_number);
use Data::Dumper;

##Configuration variables
#########################
our $period_log=25000;
our $n_gen=250000000;
our $min_rate=0.00000001;
our $max_copies;
our $ascertainedValue=2;
our $nPrefixColumns=3;
our $inputExtension="csv";

##ARGV variables
################
our $output_format="human";
our $input_dir="";
our $sample_prior;
our $rlc;
our $epoch;
our $seed=20;
our $fixed;
my $usage="\nUsage: $0 [options] -i input_directory -f format<nexus,xml,human> -s seed \n\nOptions:\n--------\n-m/--max_copies: maximum number of copies considered in the datatype and therefore the transition matrix (default: maximum number of copies in the dataset). -p/--sample_prior: xml will make BEAST sample from the pior only (no data) --rlc: random local clock model --epoch: epoch model\n\n";
my $help;

######################################################
##MAIN
######################################################

##Getopt
######################################################
(! GetOptions(
        'input_dir|i=s' => \$input_dir,
        'format|f=s' => \$output_format,
        'sample_prior|p' => \$sample_prior,
		'rlc' => \$rlc,
		'epoch' => \$epoch,
		'seed|s=i' => \$seed,
		'fixed' => \$fixed,
		'max_copies|m=i' => \$max_copies,
        'help|h' => \$help,
                )) or ((($input_dir eq "") || (! -d $input_dir)) || $help) and die $usage;

chdir($input_dir) or die "The input directory $input_dir is not accesible";

srand $seed;

my @files=<*.$inputExtension>;
my @timestamp_files=<*_timestamps.txt>;

##Hash with patient: DOB timestamp
my $DOB_file="dobs.txt";
open(my $FILEDOB,$DOB_file);
my @line_dobs=<$FILEDOB>;
close($FILEDOB);
my %dobs;
my %fbes; #first date with BE
my @temp;

##DOBS parsing
foreach my $dobline (@line_dobs)
{
	chomp($dobline);
	@temp=split(" ",$dobline);
	$dobs{$temp[0]}=$temp[1];
	$fbes{$temp[0]}=$temp[2];
	#print("DEBUG. Key: $temp[0], dobStamp: $dobs{$temp[0]}, fbesStamp: $fbes{$temp[0]}\n"); #
}

##Stats file
my $stats_file="stats.txt";
open(my $STATS,">$stats_file");
print($STATS "file n_leaves delta_time n_sites\n");


##Hash with patient: Epoch timestamps
my %epochs;

if($epoch) {
	my $epoch_file="epochs.txt";
	open(my $FILEEPOCH,$epoch_file);
	my @line_epochs=<$FILEEPOCH>;
	close($FILEEPOCH);
	my $case;

	##Epoch parsing
	foreach my $epochline (@line_epochs)
	{
		chomp($epochline);
		my @temp=split(" ",$epochline);
		$case=shift @temp;
		$epochs{$case}=\@temp;
	}
}

##DEBUG:
#foreach my $patient (keys %epochs)
#{
#	print("DEBUG: Patient $patient, epochs: ".join(",",@{$epochs{$patient}},"\n"));
#}

#Function reference to use to convert number of copies to characters
my $convertFun;

##Main loop
for my $file (@files)
{

	##File opening and reading
	chomp($file);
	my @data;
	my $fileTimestamps=$file;
	my $id=$file;
	$id=~s/^([^_]*).*\.$inputExtension$/$1/;
	$fileTimestamps=$id."_timestamps.txt";
	
	unless (defined($dobs{$id}) && defined($fbes{$id}) && -e $fileTimestamps)
	{
		die("ERROR: Problems parsing the DOB, FBES, or timeStamps files. ID: $id, file: $file, timestamps file: $fileTimestamps\n");
	}

	#Reading calls and times
	my $FILE;
	my $FILETIMES;
	open($FILE,"<",$file);
	open($FILETIMES,$fileTimestamps);
	my @cont= <$FILE>;
	my @time_lines= <$FILETIMES>;
	close($FILE);
	close($FILETIMES);
	
	#Getting times from dicts
	my $dob=$dobs{$id};
	my $fbe_stamp=$fbes{$id};
	my $timeobject_fbe=Time::Seconds->new($fbe_stamp-$dob);
	my $fbe=$timeobject_fbe->years;

	#Other file-specific variables
	my $this_max_copies;
	
	chomp($cont[0]);
	my @samples=split(" ",$cont[0]); #Header
	
	#print("DEBUG: ",join(",",@samples));

	##Parsing the alleles into the data array
	splice(@samples,0,$nPrefixColumns);# Keeping only sample names
	my @gens; #Genotypes
	my $temp;
	print("Working in $id, file $file, n_loci= ",scalar(@cont)-1 ,"\n");
	my $largestNCopiesData=0;
	
	for(my $i=0;$i<(scalar(@cont)-1);++$i) ###Locus. From 0 to size-2 instead of 0 to size-1 due to the header (using i+1 to read)
	{
		@gens=split(" ",$cont[$i+1]);
		chomp(@gens);
		splice(@gens,0,$nPrefixColumns);#Keeping only the genotypes

		#print("DEBUG: line $i ",scalar @gens," ",scalar @samples,"\n");
		for(my $j=0; $j<scalar(@samples); ++$j) ###Sample
		{
			$data[$j][$i]=$gens[$j];
			looks_like_number($gens[$j]) and $gens[$j]>$largestNCopiesData and $largestNCopiesData=$gens[$j];
		}
	}
	
	#Setting the working maximum number of copies for the datatype
	if(defined($max_copies) && $max_copies<$largestNCopiesData)
	{
		die "ERROR: detected $largestNCopiesData but selected a smaller number of copies to consider, $max_copies\n Use the -m/--max_copies argument to change this value and execute this script again\n";
	}
	elsif (!defined($max_copies))
	{
		$this_max_copies=$largestNCopiesData;
	}
	else
	{
		$this_max_copies=$max_copies;
	}

	if($this_max_copies>9 && $this_max_copies<ord('~')-64)
	{
		$convertFun=\&GenToAscii;
	}
	elsif($this_max_copies<ord('~')-64)
	{
		$convertFun= sub{$_[0]};
	}
	else
	{
		die "The current implementation of this script is not compatible with more than 62 copies of an allele\n";
	}

	#print("DEBUG: maximum number of copies used for file $file, $this_max_copies\n");

	##Timestamp hash
	my %times;
	foreach my $timeline (@time_lines)
	{
        	@temp=split(" ",$timeline);
        	$times{$temp[0]}=$temp[1];
        	#print("Key: $temp[0], timestamp: $temp[1]\n"); #DEBUG
	}

	my $OUTFILE;
	my $outname=$file;
	my $n_samples=scalar(@samples);
	my $n_char=scalar(@{$data[0]});
	my $max_date;
	my $min_dated_tip;

	##TODO: ADD EPOCH AND SUBSTITUTION RATE MATRIX SIZE
	##STATS output
	for (my $i=0;$i<$n_samples;++$i)
    {
        $times{$samples[$i]} or die "There is not timestamp information for the sample $samples[$i] in the file $fileTimestamps\n";
		my $timestamp=$times{$samples[$i]}-$dob;
		my $t_object=Time::Seconds->new($timestamp); ##Times in years since DOB
		my $time=$t_object->years;
		unless ($max_date)
		{
			$max_date=$time;
		}
		unless ($min_dated_tip)
		{
			$min_dated_tip=$time;
		}
		if ($time > $max_date)
		{
			$max_date=$time;
		}
		if ($time < $min_dated_tip)
		{
			$min_dated_tip=$time;
		}
    }

	my $fileid=$outname;
	$fileid=~s/\.$inputExtension//;
	my $deltaTime=$max_date-$min_dated_tip;
	print($STATS "$fileid $n_samples $deltaTime $n_char\n");
	##

	#Data output depending on the selected format
	#############################################
	if ($output_format=~/nexus/i)
	{
		$outname=~s/\.$inputExtension/\.nex/;
		open($OUTFILE,">$outname");
		print $OUTFILE "#NEXUS\n";
		print $OUTFILE "begin taxa;\n\tdimensions ntax=$n_samples;\n\ttaxlabels\n";
		for (my $i=0;$i<$n_samples;++$i)
		{
			print $OUTFILE "\t\t$samples[$i]\n";
		}
		print $OUTFILE ";\nend;\nbegin characters;\n\tdimensions nchar=$n_char;\n\tformat symbols=\"";
		
		for (my $i=0;$i<=$this_max_copies;++$i)
		{
			print $OUTFILE $convertFun->($i);
		}
		print $OUTFILE "\" missing=? gap=-;\nmatrix\n";
		for (my $i=0;$i<$n_samples;++$i)
        {
            print $OUTFILE "\t\t$samples[$i]\t";
			for(my $j=0;$j<$n_char;++$j)
			{
				print $OUTFILE $sample_prior?"?":$convertFun->($data[$i][$j]);
			}
			print $OUTFILE "\n";
        }
		print $OUTFILE ";\nend;";
	}
	elsif ($output_format=~/xml/i)
	{
		$outname=~s/\.$inputExtension/\.xml/;
		my $beast_outname=$outname;
		$beast_outname=~s/\.xml//;
		open($OUTFILE,">$outname");
		print $OUTFILE "<?xml version=\"1.0\" standalone=\"yes\"?>\n<beast>\n<taxa id=\"taxa\">\n";
		my $timestamp;
		$max_date=undef;
		$min_dated_tip=undef;
		my $most_recent_timestamp; ##We will need this to calculate time from the present if we use the epoch model
		my $ascertainedCode=$convertFun->($ascertainedValue);
		for (my $i=0;$i<$n_samples;++$i)
        {
            print $OUTFILE "\t<taxon id=\"$samples[$i]\">\n";
			#print "DEBUG: taxon $samples[$i], timestamp $times{$samples[$i]}\n"; #DEBUG
			$times{$samples[$i]} or die "There is not timestamp information for the sample $samples[$i] in the file $fileTimestamps\n";
			$timestamp=$times{$samples[$i]}-$dob;
			my $t_object=Time::Seconds->new($timestamp); ##Times in years since DOB
			my $time=$t_object->years;
			unless ($max_date)
			{
				$max_date=$time;
			}
			unless ($min_dated_tip)
			{
				$min_dated_tip=$time;
			}
			if ($time > $max_date)
			{
				$max_date=$time;
				$most_recent_timestamp=$times{$samples[$i]};
			}
			if ($time < $min_dated_tip)
			{
				$min_dated_tip=$time;
			}
			#print "DEBUG: sample timestamp $times{$samples[$i]}, DOB $dob, epochtime $timestamp, epochtime(years) $time\n"; #Debug
			print $OUTFILE "\t\t<date value=\"$time\" direction=\"forwards\" units=\"years\"/>";
			print $OUTFILE "\t</taxon>\n";
        }
		print $OUTFILE "</taxa>\n\n<generalDataType id=\"acna\">";
		my @states;

		my $state=0; #This is weird here I could just use i but it is inherited from alternatives with nested loops
		my $code;
		for (my $i=0;$i<=$this_max_copies;++$i)
        {
			$code=$convertFun->($i);
			push(@states,$code);
            print $OUTFILE "\n\t<state code=\"".$code."\"/> <!-- Genotype: $i ; Beast State: $state -->";
			$state+=1;
        }
		print $OUTFILE "\n\t<ambiguity code=\"-\" states=\"",join("",@states),"\"/>";
		print $OUTFILE "\n\t<ambiguity code=\"?\" states=\"",join("",@states),"\"/>";
		print $OUTFILE "\n</generalDataType>";
		print $OUTFILE "\n\n<alignment id=\"alignment\">\n\t<dataType idref=\"acna\"/>";

		for (my $i=0;$i<$n_samples;++$i)
        {
			print $OUTFILE "\n\t<sequence>\n\t\t<taxon idref=\"$samples[$i]\"/>\n\t\t";
            for(my $j=0;$j<$n_char;++$j)
            {
				print $OUTFILE $sample_prior?"?":$convertFun->($data[$i][$j]);
            }
            print $OUTFILE "\n\t</sequence>";
        }
        print $OUTFILE "\n</alignment>\n";
		my $diff_date=$max_date-$fbe;
		my $acna_operators=qq{<scaleOperator scaleFactor="0.25" weight="0.25">
			<parameter idref="acna.loss"/>
		</scaleOperator>};
		my $acna_priors=qq{<!-- Loss (relative to gain) rate priors-->
				<exponentialPrior mean="1.0" offset="0.0">
					<parameter idref="acna.loss"/>
				</exponentialPrior>
				<!-- I could also use a gammaPrior to spread the weight more -->};
		my $clock="";
		my $branch_model="";
		my $operators_clock="";
		my $clock_priors="";
		my $screenLog_columns="";
		my $fileLog_columns="";
		my $rlc_traits="";
		my @initialFreqs=(0)x$ascertainedValue;
		push(@initialFreqs,1);
		push(@initialFreqs,(0)x($this_max_copies+1-scalar @initialFreqs));
		my $freqsString=join(" ",@initialFreqs);

		if ($rlc)
		{
			$clock=qq{<!-- The random local clock -->
	<randomLocalClockModelCenancestor id="branchRates" ratesAreMultipliers="true">
		<treeModel idref="treeModel"/>
	        <rates>
	                <parameter id="localClock.relativeRates"/>
	        </rates>
	        <rateIndicator>
	                <parameter id="localClock.changes"/>
	        </rateIndicator>
	        <clockRate>
	                <parameter id="clock.rate" value="1.0" lower="$min_rate"/>
	        </clockRate>
	</randomLocalClockModelCenancestor>
	<sumStatistic id="rateChanges" name="rateChangeCount" elementwise="true">
	        <parameter idref="localClock.changes"/>
	</sumStatistic>
	<rateStatisticCenancestor id="meanRate" name="meanRate" mode="mean" internal="true" external="true">
	        <treeModel idref="treeModel"/>
	        <randomLocalClockModelCenancestor idref="branchRates"/>
	</rateStatisticCenancestor>
	<rateStatisticCenancestor id="coefficientOfVariation" name="coefficientOfVariation" mode="coefficientOfVariation" internal="true" external="true">
	        <treeModel idref="treeModel"/>
	        <randomLocalClockModelCenancestor idref="branchRates"/>
	</rateStatisticCenancestor>
	<rateCovarianceStatistic id="covariance" name="covariance">
	        <treeModel idref="treeModel"/>
	        <randomLocalClockModelCenancestor idref="branchRates"/>
	</rateCovarianceStatistic>};
			$branch_model=qq{randomLocalClockModelCenancestor};
			$operators_clock=qq{<scaleOperator scaleFactor="0.75" weight="15">
			<parameter idref="localClock.relativeRates"/>
		</scaleOperator>
		<bitFlipOperator weight="15">
			<parameter idref="localClock.changes"/>
		</bitFlipOperator>};
			$clock_priors=qq{<poissonPrior mean="0.6931471805599453" offset="0.0">
					<statistic idref="rateChanges"/>
				</poissonPrior>
				<gammaPrior shape="0.5" scale="2.0" offset="0.0">
					<parameter idref="localClock.relativeRates"/>
				</gammaPrior>};
			$screenLog_columns=qq{<column lable="nchanges" sf="6" width="2">
				<statistic idref="rateChanges"/>
			</column>};
			$fileLog_columns=qq{<statistic idref="rateChanges"/>
			<parameter idref="localClock.changes"/>
                        <parameter idref="localClock.relativeRates"/>
			<rateStatisticCenancestor idref="meanRate"/>
			<rateStatisticCenancestor idref="coefficientOfVariation"/>
			<rateCovarianceStatistic idref="covariance"/>};
			$rlc_traits=qq{<trait name="rates" tag="relRates">
                                <randomLocalClockModelCenancestor idref="branchRates"/>
                        </trait>
                        <trait name="rateIndicator" tag="indicator">
                                <randomLocalClockModelCenancestor idref="branchRates"/>
                        </trait>};
		} elsif($epoch)
		{
			#We need a rate, prior, operator, and log per epoch, that is t+1 transition times. 
			#The ancestral ones are set here, and its operators, priors, and log are set by default since they are shared among all clock models
			$clock=qq{<!-- The epoch clock (different uniform rates across branches within a given epoch) -->
	<rateCenancestorEpochBranchRates id="branchRates">
		<rate>
			<parameter id="clock.rate" value="1" lower="$min_rate"/>
		</rate>};
			$branch_model=q{rateCenancestorEpochBranchRates};

			my $iepoch=1;
			
			foreach my $tTime (@{$epochs{$id}})
			{
				##tTime is time in years backwards from the last sample, exacly what we need as transitionTime

				$clock.=qq{
		<epoch id="Epoch.$iepoch" transitionTime="$tTime">
			<parameter id="clock.rate.epoch.$iepoch" value="1" lower="$min_rate"/>
		</epoch>};
				$operators_clock=qq{<scaleOperator scaleFactor="0.75" weight="15">
			<parameter idref="clock.rate.epoch.$iepoch"/>
		</scaleOperator>
		<upDownOperator scaleFactor="0.75" weight="3">
	      	<up>
	           	<parameter idref="clock.rate.epoch.$iepoch"/>
	       	</up>
	       	<down>
	           	<parameter idref="treeModel.allInternalNodeHeights"/>
	       	</down>
	    </upDownOperator>};
				$clock_priors.=qq{
	            <logNormalPrior mean="0.1" stdev="3" offset="0.0" meanInRealSpace="true">
	                <parameter idref="clock.rate.epoch.$iepoch"/>
				</logNormalPrior>};
				$fileLog_columns.=qq{<parameter idref="clock.rate.epoch.$iepoch"/>};
				$screenLog_columns.=qq{<column label="clock.rate.epoch.$iepoch" sf="6" width="12">
					<parameter idref="clock.rate.epoch.$iepoch"/>
			</column>};
				$iepoch+=1;
			}

			$clock.=qq{
	</rateCenancestorEpochBranchRates>};
		
		} else
		{
			$clock=qq{<!-- The strict clock (Uniform rates across branches)                        -->
	<strictClockCenancestorBranchRates id="branchRates">
		<rate>
			<parameter id="clock.rate" value="1"/>
		</rate>
	</strictClockCenancestorBranchRates>};
			$branch_model=q{strictClockCenancestorBranchRates};
			$operators_clock="";
			$clock_priors="";
			$screenLog_columns="";
			$fileLog_columns="";
			$rlc_traits="";
		}
		if ($fixed)
		{
			$acna_operators="";
			$acna_priors="";
		}
		my $text = qq{
	
	<ascertainedCharacterPatterns id="patterns">
	        <alignment idref="alignment"/>
	        <state code='$ascertainedCode'/>
	</ascertainedCharacterPatterns>	
	
	<!-- A prior assumption that the population size has remained constant       -->
	<!-- throughout the time spanned by the genealogy.                           -->
	<constantSize id="constant" units="years">
		<populationSize>
			<parameter id="constant.popSize" value="1" lower="0.0"/>
		</populationSize>
	</constantSize>
	<!-- Generate a random starting tree under the coalescent process            -->
	<coalescentSimulator id="startingTree">
		<taxa idref="taxa"/>
		<constantSize idref="constant"/>
	</coalescentSimulator>
	<!-- Generate a tree model                                  -->
	<treeModel id="treeModel">
		<coalescentTree idref="startingTree"/>
		<rootHeight>
			<parameter id="treeModel.rootHeight"/>
		</rootHeight>
		<nodeHeights internalNodes="true">
			<parameter id="treeModel.internalNodeHeights"/>
		</nodeHeights>
		<nodeHeights internalNodes="true" rootNode="true">
			<parameter id="treeModel.allInternalNodeHeights"/>
		</nodeHeights>
	</treeModel>
	<!-- Generate a coalescent likelihood                                        -->
	<coalescentLikelihood id="coalescent">
		<model>
			<constantSize idref="constant"/>
		</model>
		<populationTree>
			<treeModel idref="treeModel"/>
		</populationTree>
	</coalescentLikelihood>
	$clock
	<frequencyModel id="frequencies">
		<dataType idref="acna"/>
		<frequencies>
			<parameter id="acna.frequencies" value="$freqsString"/>
		</frequencies>
	</frequencyModel>	
	<AbsoluteCNAModel id="acna_subsmodel">
		<frequencies>
			<frequencyModel idref="frequencies"/>
        </frequencies>
        <gain_rate>
			<parameter id="acna.gain" value="1" lower="0"/>
        </gain_rate>
        <relative_loss_rate>
			<parameter id="acna.loss" value="1" lower="0"/>
        </relative_loss_rate>
	</AbsoluteCNAModel>
	<siteModel id="siteModel">
		<substitutionModel>
			<AbsoluteCNAModel idref="acna_subsmodel"/>
		</substitutionModel>
	</siteModel>
	<cenancestorTreeLikelihood id="treeLikelihood" useAmbiguities="false">
		<patterns idref="patterns"/>
		<treeModel idref="treeModel"/>
		<siteModel idref="siteModel"/>
        	<cenancestorHeight>
        		<parameter id="luca_height" value="$diff_date" upper="$max_date" lower="$diff_date" />
        	</cenancestorHeight>
		<cenancestorBranch>
			<parameter id="luca_branch" value="1" upper="$fbe" lower="0.0"/>
			<!-- Value 1 as a safe starting value -->
		</cenancestorBranch>
		<$branch_model idref="branchRates"/>
	</cenancestorTreeLikelihood>	
	<operators id="operators" optimizationSchedule="default">
		<scaleOperator scaleFactor="0.5" weight="10.0">
			<parameter idref="clock.rate"/>
        </scaleOperator>
		$acna_operators
		<subtreeSlide size="2.5" gaussian="true" weight="15.0"> <!-- 2.5 years. They will be automatically optimized by BEAST though -->
			<treeModel idref="treeModel"/>
		</subtreeSlide>
		<narrowExchange weight="15.0">
			<treeModel idref="treeModel"/>
		</narrowExchange>
		<wideExchange weight="3.0">
			<treeModel idref="treeModel"/>
		</wideExchange>
		<wilsonBalding weight="3.0">
			<treeModel idref="treeModel"/>
		</wilsonBalding>
		<scaleOperator scaleFactor="0.75" weight="5.0">
			<parameter idref="treeModel.rootHeight"/>
		</scaleOperator>
		<uniformOperator weight="30.0">
			<parameter idref="treeModel.internalNodeHeights"/>
		</uniformOperator>
		$operators_clock
		<scaleOperator scaleFactor="0.2" weight="1.0"> <!-- We operate the branch since it is relative to the root. Operating luca_height is error prone, since it depends on the root -->
            <parameter idref="luca_branch"/>
        </scaleOperator>
		<scaleOperator scaleFactor="0.5" weight="3.0">
			<parameter idref="constant.popSize"/>
		</scaleOperator>
        <upDownOperator scaleFactor="0.75" weight="5.0">
            <up>
                <parameter idref="clock.rate"/>
            </up>
            <down>
                <parameter idref="treeModel.allInternalNodeHeights"/>
				<parameter idref="luca_branch"/>
            </down>
        </upDownOperator>
	</operators>
	<!-- Define MCMC                                                             -->
	<mcmc id="mcmc" chainLength="$n_gen" autoOptimize="true" operatorAnalysis="$beast_outname.ops">
		<posterior id="posterior">
			<prior id="prior">
            	<coalescentLikelihood idref="coalescent"/>
				<oneOnXPrior>
					<parameter idref="constant.popSize"/>
				</oneOnXPrior>
				<!-- Clock (gain) Rate Prior. -->
	            <logNormalPrior mean="0.1" stdev="3" offset="0.0" meanInRealSpace="true">
	            	<parameter idref="clock.rate"/>
	            </logNormalPrior>
				$breakpoint_priors
				$clock_priors
				<!-- Cenancestor Prior on the height, since it is easier to have a meaningfull prior on it (time of the initial development of the BE fragment) -->
                <uniformPrior lower="$diff_date" upper="$max_date">
                	<parameter idref="luca_height"/>
                </uniformPrior>
			</prior>
			<likelihood id="likelihood">
				<cenancestorTreeLikelihood idref="treeLikelihood"/>
			</likelihood>
		</posterior>
		<operators idref="operators"/>
		<!-- write log to screen                                                     -->
		<log id="screenLog" logEvery="$period_log">
			<column label="Posterior" dp="4" width="12">
				<posterior idref="posterior"/>
			</column>
			<column label="Prior" dp="4" width="12">
				<prior idref="prior"/>
			</column>
			<column label="Likelihood" dp="4" width="12">
				<likelihood idref="likelihood"/>
			</column>
			<column label="rel_loss_rate" sf="6" width="12">
				<parameter idref="acna.loss"/>
			</column>
			<column label="clock_rate" sf="6" width="12">
				<parameter idref="clock.rate"/>
			</column>
			<column label="rootHeight" sf="6" width="12">
				<parameter idref="treeModel.rootHeight"/>
			</column>
			<column label="luca_height" sf="6" width="12">
				<parameter idref="luca_height"/>
			</column>
			<column label="luca_branch" sf="6" width="12">
				<parameter idref="luca_branch"/>
			</column>
			$screenLog_columns
		</log>
		<!-- write log to file                                                       -->
		<log id="fileLog" logEvery="$period_log" fileName="$beast_outname.log" overwrite="false">
			<posterior idref="posterior"/>
			<prior idref="prior"/>
			<likelihood idref="likelihood"/>
			<parameter idref="acna.loss"/>
			<parameter idref="treeModel.rootHeight"/>
			<parameter idref="luca_height"/>
			<parameter idref="luca_branch"/>
			<parameter idref="constant.popSize"/>
			<parameter idref="clock.rate"/>
			<coalescentLikelihood idref="coalescent"/>
			$fileLog_columns
		</log>
		<!-- write tree log to file                                                  -->
		<logTree id="treeFileLog" logEvery="$period_log" nexusFormat="true" fileName="$beast_outname.trees" sortTranslationTable="true">
			<treeModel idref="treeModel"/>
			<trait name="rate" tag="rate">
				<$branch_model idref="branchRates"/>
			</trait>
			$rlc_traits
			<posterior idref="posterior"/>
		</logTree>
	</mcmc>
	<report>
		<property name="timer">
			<mcmc idref="mcmc"/>
		</property>
	</report>
</beast>
};
		print $OUTFILE "$text\n";
	}
	else
	{
		$outname=~s/\.$inputExtension/\.txt/;
		open($OUTFILE,">$outname");
		for(my $i=0;$i<scalar(@samples);++$i)
		{
			print $OUTFILE "$samples[$i] ";
			for(my $j=0;$j<$n_char;++$j)
			{
				print $OUTFILE $sample_prior?"?":$convertFun->($data[$i][$j]).",";
			}
			print $OUTFILE "\n";
		}
	}	
	close($OUTFILE);
}

close($STATS);
exit;

##FUNCTIONS
################

sub GenToAscii
{
	my ($n)=@_;
	$n eq "?" and return $n;
	return chr($n+64);#Ascii avoiding both ? and - since they are our ambiguities
}

