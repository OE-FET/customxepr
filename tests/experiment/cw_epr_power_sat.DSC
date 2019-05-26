#DESC	1.2 * DESCRIPTOR INFORMATION ***********************
*
*	Dataset Type and Format:
*
DSRC	EXP
BSEQ	BIG
IKKF	REAL
XTYP	IDX
YTYP	IGD
ZTYP	NODATA
*
*	Item Formats:
*
IRFMT	D
YFMT	D
*
*	Data Ranges and Resolutions:
*
XPTS	1024
XMIN	3340.550000
XWID	14.985352
YPTS	10
YMIN	0.002000
YWID	199.998000
*
*	Documentational Text:
*
TITL	'FI_ESR_device4_PowerSat_140K_Vg_70'
IRNAM	'Intensity'
XNAM	'Field'
YNAM	'Microwave Power'
IRUNI	''
XUNI	'G'
YUNI	'mW'
*
************************************************************
*
#SPL	1.2 * STANDARD PARAMETER LAYER
*
OPER    ss2151
DATE    10/09/16
TIME    04:31:31
CMNT    
SAMP    
SFOR    
STAG    C
EXPT    CW
OXS1    IADC
AXS1    B0VL
AXS2    MWPW
AXS3    
A1CT    0.334805
A1SW    0.0015
MWFQ    9.383332e+09
MWPW    2e-06
A2RS    10
A2LL    50.0
A2SW    1.0
AVGS    9
SPTP    0.16
RCAG    90
RCHM    1
B0MA    2e-05
B0MF    100000
RCPH    0.0
RCOF    0.0
A1RS    1024
RCTC    0
*
************************************************************
*
#DSL	1.0 * DEVICE SPECIFIC LAYER
*

.DVC     acqStart, 1.0


.DVC     delay2, 1.0

Delay              10000 ms

.DVC     fieldCtrl, 1.0

AllegroMode        True
CenterField        3348.05 G
Delay              0.0 s
FieldFlyback       On
FieldWait          Wait LED off
GFactor            2.002200
MeasuringHall      False
SetToSampleG       False
StaticFieldMon     3340.550 G
SweepDirection     Up
SweepWidth         15.0 G
WidthTM            200.0 G

.DVC     fieldSweep, 1.0


.DVC     freqCounter, 1.0

FrequencyMon       9.383332 GHz
QMonitBridge       On

.DVC     mwBridge, 1.0

AcqFineTuning      Never
AcqScanFTuning     Off
AcqSliceFTuning    Off
BridgeCalib        50.5
Power              0.002000 mW
PowerAtten         50.0 dB
QValue             5900

.DVC     ramp2, 1.0

Flyback            True
NbCycles           1
NbPoints           10
StartValue         50.0 dB
SweepData          50 40 30 25 20 15 10 5 2 0 dB
SweepWidth         1.0 dB
sweepType          User defined down

.DVC     recorder, 1.0

BaselineCorr       On
NbScansAcc         9
NbScansDone        9
NbScansToDo        9
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
ConvTime           160.00 ms
DModDetectSCT      First
DoubleModAcc       1
DoubleModFreq      5.000 kHz
DoubleMode         False
DualDetect         OFF
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
EnableDisp         False
EnableImag         Disable
ExtLockIn          False
ExtTrigger         False
Gain               90 dB
GainB              90 dB
Harmonic           1
HighPass           True
InputPlugA         AC3
InputPlugB         AC3
Integrator         False
IsCalibExp         False
ModAmp             0.200 G
ModFreq            100.00 kHz
ModPhase           0.0
Offset             0.0 %
PolyCof            {2;3,9;0} 0,0.99652,0,0,0.00737177,0,0,-0.00559614,0,0,-2.88221e-05,0,0,1.00404e-05,0,0,3.43695e-08,0,0,-5.0404e-09,0,0,-1.4783e-11,0,0,-1.29132e-12,0
QuadMode           False
ResCenter          62.5 mm
ResLength          40 mm
Resolution         1024
Resonator          1
SctNorm            True
SctRevision        Allegro
SetAllOrd          False
SetOrdDef          False
SpuExtension       True
SpuRevision        MultiHarmonic
SweepTime          163.84000 s
TimeConst          0
TimeExp            False
TuneCaps           50
dModSW             True

*
************************************************************
