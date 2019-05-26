#DESC	1.2 * DESCRIPTOR INFORMATION ***********************
*
*	Dataset Type and Format:
*
DSRC	EXP
XTYP	IDX
ZTYP	NODATA
IKKF	REAL
YTYP	IGD
BSEQ	BIG
*
*	Item Formats:
*
YFMT	D
IRFMT	D
*
*	Documentational Text:
*
IRUNI	''
YNAM	'Sample Angle'
XUNI	'G'
TITL	'CuPc_film_angle_dep_297K'
XNAM	'Field'
YUNI	'deg'
IRNAM	'Intensity'
*
*	Data Ranges and Resolutions:
*
XPTS	1024
YPTS	24
YWID	345.0
XMIN	2547.0
YMIN	0.0
XWID	1218.57
*
************************************************************
*
#SPL	1.2 * STANDARD PARAMETER LAYER
*

OPER    ss2151
SFOR    
B0MA    0.0015
B0MF    100000
STAG    C
A2RS    24
MWFQ    9369025000.0
DATE    05/23/19
RCAG    60
A1RS    1024
RCPH    0.0
RCTC    0
EXPT    CW
AXS2    SANX
AXS3    
AXS1    B0VL
AVGS    4
SPTP    0.12
RCHM    1
OXS1    IADC
A2SW    15.0
A2LL    0.0
CMNT    
A1SW    0.12194
A1CT    0.31559
RCOF    0.0
MWPW    0.006325
TIME    15:48:37
SAMP    
*
************************************************************
*
#DSL	1.0 * DEVICE SPECIFIC LAYER
*

.DVC     freqCounter, 1.0

FrequencyMon       9.369025 GHz
QMonitBridge       On

.DVC     goniometer, 1.0

InfoText           Connect to Hardware - Initialize Goniometer - Define Zero Angle
Type               EMB_Goniometer
Angle              345.000 deg
Increment          0.125 deg

.DVC     ramp2, 1.0

NbPoints           24
SweepWidth         15.000 deg
SweepData          deg
NbCycles           1
sweepType          Ramp up
StartValue         0.000 deg
Flyback            False

.DVC     signalChannel, 1.0

TuneCaps           50
HighPass           True
SweepTime          122.88 s
Enable3rdHarm90    False
ResLength          40 mm
QuadMode           False
SetAllOrd          False
Resonator          1
EliDelay           1.0 us
ModAmp             15.0 G
DoubleModFreq      5.0 kHz
ModPhase           0.0
ResCenter          62.5 mm
Resolution         1024
ModFreq            100.0 kHz
Enable5thHarm      False
Gain               60 dB
Offset             0.0 %
IsCalibExp         False
DModDetectSCT      First
Enable2ndHarm90    False
AllowShortCt       False
InputPlugB         AC3
InputPlugA         AC3
ExtTrigger         False
SctNorm            True
Enable3rdHarm      False
Enable4thHarm      False
DualDetect         OFF
Calibrated         True
SctRevision        Allegro
EnableImag         Disable
SpuRevision        MultiHarmonic
EnableDisp         False
ConvFact           9.271e-09
ConvTime           120.0 ms
Enable1stHarm      True
TimeConst          0
AFCTrap            True
Enable5thHarm90    False
SpuExtension       True
SetOrdDef          False
Enable2ndHarm      False
Integrator         False
Harmonic           1
Enable1stHarm90    False
DoubleModAcc       1
AllegroMode        True
TimeExp            False
DoubleMode         False
Enable4thHarm90    False
PolyCof            {2;3,9;0} 0.0,0.99652,0.0,0.0,0.00737177,0.0,0.0,-0.00559614,0.0,0.0,-2.88221e-05,0.0,0.0,1.00404e-05,0.0,0.0,3.43695e-08,0.0,0.0,-5.0404e-09,0.0,0.0,-1.4783e-11,0.0,0.0,-1.29132e-12,0.0
ExtLockIn          False
GainB              60 dB
dModSW             True

.DVC     acqStart, 1.0


.DVC     fieldSweep, 1.0


.DVC     recorder, 1.0

NbScansToDo        4
NbScansAcc         4
BaselineCorr       On
NbScansDone        4
ReplaceMode        Off
SmoothMode         Manual
SmoothPoints       1

.DVC     scanEnd, 1.0


.DVC     fieldCtrl, 1.0

FieldFlyback       On
GFactor            2.0
FieldWait          Wait LED off
SetToSampleG       False
SweepWidth         1219.4 G
CenterField        3155.9 G
MeasuringHall      False
SweepDirection     Up
Delay              0.0 s
AllegroMode        True
WidthTM            200.0 G
StaticFieldMon     3155.9 G

.DVC     mwBridge, 1.0

BridgeCalib        50.5
Power              6.325 mW
AcqFineTuning      Slice
AcqScanFTuning     Off
QValue             8317.6
AcqSliceFTuning    On
PowerAtten         15.0 dB
QValueErr          28.5
*
************************************************************
