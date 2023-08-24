


def get_base_xml(param1,param2):
    base_xml = """<?xml version="1.0" standalone="yes"?>
<beast>
<taxa id="taxa">
	<taxon id="seq00001">
		<date value="60.0" direction="forwards" units="years"/>
	</taxon>
	<taxon id="seq00003">
		<date value="60.0" direction="forwards" units="years"/>
	</taxon>
	<taxon id="seq00005">
		<date value="60.0" direction="forwards" units="years"/>
	</taxon>
	<taxon id="seq00004">
		<date value="60.0" direction="forwards" units="years"/>
	</taxon>
	<taxon id="seq00010">
		<date value="55.0" direction="forwards" units="years"/>
	</taxon>
	<taxon id="seq00009">
		<date value="55.0" direction="forwards" units="years"/>
	</taxon>
	<taxon id="seq00006">
		<date value="60.0" direction="forwards" units="years"/>
	</taxon>
	<taxon id="seq00007">
		<date value="55.0" direction="forwards" units="years"/>
	</taxon>
	<taxon id="seq00011">
		<date value="55.0" direction="forwards" units="years"/>
	</taxon>
	<taxon id="seq00008">
		<date value="55.0" direction="forwards" units="years"/>
	</taxon>
	<taxon id="seq00002">
		<date value="60.0" direction="forwards" units="years"/>
	</taxon>
</taxa>

<generalDataType id="cnv">
	<state code="@"/> <!-- Genotype: 0,0 ; Beast State: 0 -->
	<state code="A"/> <!-- Genotype: 0,1 ; Beast State: 1 -->
	<state code="B"/> <!-- Genotype: 0,2 ; Beast State: 2 -->
	<state code="C"/> <!-- Genotype: 0,3 ; Beast State: 3 -->
	<state code="D"/> <!-- Genotype: 0,4 ; Beast State: 4 -->
	<state code="E"/> <!-- Genotype: 0,5 ; Beast State: 5 -->
	<state code="F"/> <!-- Genotype: 0,6 ; Beast State: 6 -->
	<state code="G"/> <!-- Genotype: 1,0 ; Beast State: 7 -->
	<state code="H"/> <!-- Genotype: 1,1 ; Beast State: 8 -->
	<state code="I"/> <!-- Genotype: 1,2 ; Beast State: 9 -->
	<state code="J"/> <!-- Genotype: 1,3 ; Beast State: 10 -->
	<state code="K"/> <!-- Genotype: 1,4 ; Beast State: 11 -->
	<state code="L"/> <!-- Genotype: 1,5 ; Beast State: 12 -->
	<state code="M"/> <!-- Genotype: 2,0 ; Beast State: 13 -->
	<state code="N"/> <!-- Genotype: 2,1 ; Beast State: 14 -->
	<state code="O"/> <!-- Genotype: 2,2 ; Beast State: 15 -->
	<state code="P"/> <!-- Genotype: 2,3 ; Beast State: 16 -->
	<state code="Q"/> <!-- Genotype: 2,4 ; Beast State: 17 -->
	<state code="R"/> <!-- Genotype: 3,0 ; Beast State: 18 -->
	<state code="S"/> <!-- Genotype: 3,1 ; Beast State: 19 -->
	<state code="T"/> <!-- Genotype: 3,2 ; Beast State: 20 -->
	<state code="U"/> <!-- Genotype: 3,3 ; Beast State: 21 -->
	<state code="V"/> <!-- Genotype: 4,0 ; Beast State: 22 -->
	<state code="W"/> <!-- Genotype: 4,1 ; Beast State: 23 -->
	<state code="X"/> <!-- Genotype: 4,2 ; Beast State: 24 -->
	<state code="Y"/> <!-- Genotype: 5,0 ; Beast State: 25 -->
	<state code="Z"/> <!-- Genotype: 5,1 ; Beast State: 26 -->
	<state code="["/> <!-- Genotype: 6,0 ; Beast State: 27 -->
	<ambiguity code="-" states="@ABCDEFGHIJKLMNOPQRSTUVWXYZ["/>
	<ambiguity code="?" states="@ABCDEFGHIJKLMNOPQRSTUVWXYZ["/>
</generalDataType>
<alignment id="alignment">
	<dataType idref="cnv"/>
	<sequence>
		<taxon idref="seq00001"/>
		HHGGHMGAHNHAHHHMAGBHHGHHHNGHBHHMH
	</sequence>
	<sequence>
		<taxon idref="seq00003"/>
		HHGHIMGAHNHAHHHMAGBHHHHHHNGHBHHHH
	</sequence>
	<sequence>
		<taxon idref="seq00005"/>
		HHGHHMGAHNNAHIHMAGBAOHHHHNGHBNHHH
	</sequence>
	<sequence>
		<taxon idref="seq00004"/>
		HHGHHMGAHNNAMIHMAGBAOHHHHNGHBNBHH
	</sequence>
	<sequence>
		<taxon idref="seq00010"/>
		HHGHHMGAHNHAHHHMAGBHHHHHHNGHBHHHH
	</sequence>
	<sequence>
		<taxon idref="seq00009"/>
		HHGHHMGAHNHAHHHMAGBHHHHHHHGHHHHHH
	</sequence>
	<sequence>
		<taxon idref="seq00006"/>
		IGGHHMGAHNHAHHHMAGBHHHNHJHGHHHHHH
	</sequence>
	<sequence>
		<taxon idref="seq00007"/>
		HHGHHMGAHNHAHHHMAGBHHHHGHHGHHHHHH
	</sequence>
	<sequence>
		<taxon idref="seq00011"/>
		HHGHHMGAHNHAHHHMAGBHHHHHHHGGHHHHB
	</sequence>
	<sequence>
		<taxon idref="seq00008"/>
		HHGHHMGAHNHAHHAMAGBHHHMHHHGHHHHHH
	</sequence>
	<sequence>
		<taxon idref="seq00002"/>
		HHGHHMGAINHAHHAMAGBHHHMHHHGHHHHHH
	</sequence>
</alignment>
<ascertainedCharacterPatterns id="patterns">
	<alignment idref="alignment"/>
	<state code='H'/>
</ascertainedCharacterPatterns>

<!--
<patterns id="patterns" from="1" strip="false">
	<alignment idref="alignment"/>
</patterns>
-->
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

<!-- The strict clock (Uniform rates across branches)                        -->
<!--
<strictClockCenancestorBranchRates id="branchRates">
	<rate>
		<parameter id="clock.rate" value="1"/>
	</rate>
</strictClockCenancestorBranchRates>
-->

<randomLocalClockModelCenancestor id="branchRates" ratesAreMultipliers="false">
	<treeModel idref="treeModel"/>
	<rates>
		<parameter id="localClock.relativeRates"/>
	</rates>
	<rateIndicator>
		<parameter id="localClock.changes"/>
	</rateIndicator>
	<clockRate>
		<parameter id="clock.rate" value="1.0" lower="0.0"/>
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
</rateCovarianceStatistic>

<frequencyModel id="frequencies">
	<dataType idref="cnv"/>
	<frequencies>
		<parameter id="cnv.frequencies" value="0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"/>
	</frequencies>
</frequencyModel>

<CNVModel id="cnv_subsmodel">
	<frequencies>
		<frequencyModel idref="frequencies"/>
	</frequencies>
	<gain_rate>
		<parameter id="cnv.gain" value="1" lower="0"/>
	</gain_rate>
	<loss_rate>
		<parameter id="cnv.loss" value="1" lower="0"/>
	</loss_rate>
	<conversion_rate>
		<parameter id="cnv.conversion" value="1" lower="0"/>
	</conversion_rate>
</CNVModel>

<siteModel id="siteModel">
	<substitutionModel>
		<CNVModel idref="cnv_subsmodel"/>
	</substitutionModel>
</siteModel>

<cenancestorTreeLikelihood id="treeLikelihood" useAmbiguities="false">
	<patterns idref="patterns"/>
	<treeModel idref="treeModel"/>
	<siteModel idref="siteModel"/>
	<cenancestorHeight>
		<parameter id="luca_height" value="5.0" upper="60.0" lower="5.0" /> <!-- Without the value it does not add the bounds -->
	</cenancestorHeight>
	<cenancestorBranch>
		<parameter id="luca_branch" value="1" upper="55.0" lower="0.0"/>
		<!-- Value 1 as a safe starting value -->
	</cenancestorBranch>
	<randomLocalClockModelCenancestor idref="branchRates"/>
</cenancestorTreeLikelihood>

<operators id="operators" optimizationSchedule="default">
	<scaleOperator scaleFactor="0.25" weight="0.25">
                <parameter idref="cnv.loss"/>
	</scaleOperator>
	<scaleOperator scaleFactor="0.25" weight="0.25">
                <parameter idref="cnv.conversion"/>
	</scaleOperator>
	<scaleOperator scaleFactor="0.5" weight="10.0">
                <parameter idref="clock.rate"/>
	</scaleOperator>
	<scaleOperator scaleFactor="0.75" weight="15">
		<parameter idref="localClock.relativeRates"/>
	</scaleOperator>
	<bitFlipOperator weight="15">
			<parameter idref="localClock.changes"/>
	</bitFlipOperator>
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
                </down>
        </upDownOperator>

</operators>

<!-- Define MCMC                                                             -->
<mcmc id="mcmc" chainLength="2000" autoOptimize="true" operatorAnalysis="validation.ops">
	<posterior id="posterior">
		<prior id="prior">
                        <coalescentLikelihood idref="coalescent"/>
			<oneOnXPrior>
				<parameter idref="constant.popSize"/>
			</oneOnXPrior>
		
			<!-- Clock (gain) Rate Prior. More than 50 SGAs/breakpoint/year seems an unreasonable enough value to use as upper bound-->
			<!-- 
			<uniformPrior lower="0.0" upper="50">
				<parameter idref="clock.rate"/>
			</uniformPrior>
			-->
			<!-- Clock (gain) Rate Prior. -->
			<!--<logNormalPrior mean="-4.0" stdev="2.5" offset="0.0" meanInRealSpace="false">
                        	<parameter idref="clock.rate"/>
                        </logNormalPrior>-->
			<oneOnXPrior>
				<parameter idref="clock.rate"/>
			</oneOnXPrior>
			<poissonPrior mean="0.6931471805599453" offset="0.0">
				<statistic idref="rateChanges"/>
			</poissonPrior>
			<gammaPrior shape="0.5" scale="2.0" offset="0.0">
				<parameter idref="localClock.relativeRates"/>
			</gammaPrior>
			<!-- Loss and conversion (relative to gain) rate priors-->
			<exponentialPrior mean="1.0" offset="0.0">
				<parameter idref="cnv.loss"/>
			</exponentialPrior>
			<exponentialPrior mean="1.0" offset="0.0">
				<parameter idref="cnv.conversion"/>
			</exponentialPrior>

                        <!-- Cenancestor Prior on the height, since it is easier to have a meaningful prior on it (time of the initial development of the BE fragment) -->
                        <uniformPrior lower="5.0" upper="60.0">
                        	<parameter idref="luca_height"/>
                        </uniformPrior>
		</prior>
		<likelihood id="likelihood">
			<cenancestorTreeLikelihood idref="treeLikelihood"/>
		</likelihood>
	</posterior>
	<operators idref="operators"/>

	<!-- write log to screen                                                     -->
	<log id="screenLog" logEvery="200">
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
			<parameter idref="cnv.loss"/>
		</column>
		<column label="rel_conv_rate" sf="6" width="12">
			<parameter idref="cnv.conversion"/>
		</column>
		<column label="gain_rate" sf="6" width="12">
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
		<column lable="nchanges" sf="6" width="5">
			<statistic idref="rateChanges"/>
		</column>
	</log>

	<!-- write log to file                                                       -->
	<log id="fileLog" logEvery="200" fileName="validation.log" overwrite="false">
		<posterior idref="posterior"/>
		<prior idref="prior"/>
		<likelihood idref="likelihood"/>
		<parameter idref="cnv.loss"/>
		<parameter idref="cnv.conversion"/>
		<parameter idref="treeModel.rootHeight"/>
		<parameter idref="luca_height"/>
		<parameter idref="luca_branch"/>
            	<parameter idref="localClock.relativeRates"/>
            	<parameter idref="localClock.changes"/>
		<parameter idref="constant.popSize"/>
		<parameter idref="clock.rate"/>
		<coalescentLikelihood idref="coalescent"/>
		<statistic idref="rateChanges"/>
		<rateStatisticCenancestor idref="meanRate"/>
		<rateStatisticCenancestor idref="coefficientOfVariation"/>
		<rateCovarianceStatistic idref="covariance"/>
	</log>

	<!-- write tree log to file                                                  -->
	<logTree id="treeFileLog" logEvery="200" nexusFormat="true" fileName="validation.trees" sortTranslationTable="true">
	                <treeModel idref="treeModel"/>
	                <trait name="rate" tag="rate">
	                        <randomLocalClockModelCenancestor idref="branchRates"/>
	                </trait>
	                <trait name="rates" tag="relRates">
	                        <randomLocalClockModelCenancestor idref="branchRates"/>
	                </trait>
	                <trait name="rateIndicator" tag="indicator">
	                        <randomLocalClockModelCenancestor idref="branchRates"/>
	                </trait>
	                <posterior idref="posterior"/>
	<!--            <rateStatisticCenancestor idref="meanRate"/>-->
	</logTree>
</mcmc>
<report>
	<property name="timer">
		<mcmc idref="mcmc"/>
	</property>
</report>
</beast>
    """
    return base_xml