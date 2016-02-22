
"""
Build SpeakerDependentSDK16 static library, share with VR+SI.

Copyright (c) 2016, C.C.LIN(Viisin)
License: MIT (see LICENSE for details)
"""

from GPCE4Project import *

try:
	project = GPCE4Project('SpeakerDependentSDK16.lib', 'C:\\Program Files (x86)\\Generalplus\\unSPIDE 3.0.10\\toolchain')
	project.setIntermediateFolder('Debug')
	project.addCFlag('-Os')
	project.addIncludePath('./SD')
	project.addIncludePath('./VR/SpeakerIndependentSDKK16')
	project.addReferencePath('SD')
	#project.addSourceFile('SpeakerDependentSDK16_Ram.asm')
	project.addSourceFile('SpeakerDependentSDK16_Wrap.asm')
	project.addSourceFile('SpeakerDependentTrain16.asm')
	project.addSourceFile('SpeakerDependentTrain16api.c')
	project.addSourceFile('DataFlash16.c')
	project.addSourceFile('gpce4_memory.c')
	project.addSourceFile('FixGMModel16.c')
	project.addSourceFile('FixGMModel16_StateScore.asm')
	project.addSourceFile('SDFeaturePoolManager16.c')
	project.addSourceFile('SDTrainer16.c')
	project.buildLibrary()
	print('FINISHED.')
except Exception as e:
	print('\nHALT.')
	print(e)
