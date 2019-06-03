#DESC	1.2 * DESCRIPTOR INFORMATION ***********************
*
*	Dataset Type and Format:
*
DSRC	EXP
BSEQ	BIG
IKKF	CPLX
XTYP	IDX
YTYP	NODATA
ZTYP	NODATA
*
*	Item Formats:
*
IRFMT	D
IIFMT	D
*
*	Data Ranges and Resolutions:
*
XPTS	2048
XMIN	-2000.000000
XWID	3998.046875
*
*	Documentational Text:
*
TITL	'LSPPBTTTdoped:2'
IRNAM	'Intensity'
IINAM	''
XNAM	'Field'
IRUNI	''
IIUNI	''
XUNI	'G'
*
************************************************************
*
#SPL	1.2 * STANDARD PARAMETER LAYER
*
OPER    xuser
DATE    09/18/17
TIME    16:51:34
CMNT    
SAMP    
SFOR    
STAG    C
EXPT    CW
OXS1    IADC
AXS1    B0VL
AXS2    NONE
AXS3    
A1CT    0.00
A1SW    0.4
MWFQ    9.397989e+09
MWPW    0.2
AVGS    1
SPTP    0.03
RCAG    60
RCHM    1
B0MA    3e-05
B0MF    70000
RCPH    0.0
RCOF    -3.4
A1RS    2048
RCTC    0
*
************************************************************
*
#DSL	1.0 * DEVICE SPECIFIC LAYER
*

.DVC     acqStart, 1.0


.DVC     fieldCtrl, 1.0

AllegroMode        True
CenterField        0.00 G
Delay              0.0 s
FieldFlyback       On
FieldWait          Wait LED off
GFactor            2.000000
MeasuringHall      False
SetToSampleG       False
StaticFieldMon     -0.000 G
SweepDirection     Up
SweepWidth         4000.0 G
WidthTM            10.0 G

.DVC     fieldSweep, 1.0


.DVC     freqCounter, 1.0

FrequencyMon       9.397989 GHz
QMonitBridge       On

.DVC     goniometer, 1.0

Angle              0.000 deg
Increment          0.125 deg
InfoText           Connect to Hardware - Initialize Goniometer - Define Zero Angle
Type               EMB_Goniometer

.DVC     mwBridge, 1.0

AcqFineTuning      Never
AcqScanFTuning     Off
AcqSliceFTuning    Off
BridgeCalib        50.5
Power              200.0 mW
PowerAtten         0.0 dB
QValue             1800

.DVC     recorder, 1.0

BaselineCorr       Off
NbScansAcc         1
NbScansDone        1
NbScansToDo        1
ReplaceMode        Off
SmoothMode         Manual
SmoothPoints       1

.DVC     scanEnd, 1.0


.DVC     signalChannel, 1.0

AFCTrap            True
AllegroMode        True
AllowShortCt       False
Calibrated         True
ConvFact           9.271e-09
ConvTime           30.00 ms
DModDetectSCT      First
DoubleModAcc       1
DoubleModFreq      5.000 kHz
DoubleMode         False
DualDetect         0/90 Degrees
EliDelay           1.0 us
Enable1stHarm      True
Enable1stHarm90    False
Enable2ndHarm      False
Enable2ndHarm90    False
Enable3rdHarm      False
Enable3rdHarm90    False
Enable4thHarm      False
Enable4thHarm90    False
Enable5thHarm      False
Enable5thHarm90    False
EnableDisp         True
EnableImag         Disable
ExtLockIn          False
ExtTrigger         False
Gain               60 dB
GainB              60 dB
Harmonic           1
HighPass           True
InputPlugA         AC3
InputPlugB         DC
Integrator         False
IsCalibExp         False
ModAmp             0.300 G
ModFreq            70.00 kHz
ModPhase           0.0
Offset             -3.4 %
PolyCof            {2;3,9;0} 0,0.99652,0,0,0.00737177,0,0,-0.00559614,0,0,-2.88221e-05,0,0,1.00404e-05,0,0,3.43695e-08,0,0,-5.0404e-09,0,0,-1.4783e-11,0,0,-1.29132e-12,0
QuadMode           True
ResCenter          62.5 mm
ResLength          40 mm
Resolution         2048
Resonator          1
SctNorm            True
SctRevision        Allegro
SetAllOrd          False
SetOrdDef          False
SpuExtension       True
SpuRevision        MultiHarmonic
SweepTime          61.44467 s
TimeConst          0
TimeExp            False
TuneCaps           111
dModSW             True

*
************************************************************
