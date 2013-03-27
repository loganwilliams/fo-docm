/* **************************************************************
   
   AdInputAD.c -Source Code of AdInputAD sample program
   --------------------------------------------------------------
   Version 1.00-01
   --------------------------------------------------------------
   Date 2009/03/17
   --------------------------------------------------------------
   Copyright 2000,2009 Interface Corporation. All rights reserved.
   ************************************************************** */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "fbiad.h"

ADBOARDSPEC    BoardSpec;
ADSMPLREQ      AdSmplConfig;    // Sampling conditions setting structure
ADSMPLCHREQ    AdSmplChReq[2];  // Sampling conditions setting structure
unsigned char  bData[2];		// Output data storage area
unsigned short wData[2];		// Output data storage area
unsigned int   dwData[2];		// Output data storage area

int main(void)
{
	int	ret, dnum;
	
	dnum = 1;
	
	// Open a device.
	ret = AdOpen(dnum);
	if (ret) {
		printf("AdOpen error: ret=%Xh\n", ret);
		exit(EXIT_FAILURE);
	}
	
	// 
	ret = AdGetDeviceInfo(dnum, &BoardSpec);
	if(ret){
		printf("AdGetDeviceInfo error: ret=%Xh\n", ret);
		AdClose(dnum);
		exit(EXIT_FAILURE);
	}
	
	// Retrieve the sampling conditions.
	ret = AdGetSamplingConfig( dnum, &AdSmplConfig );
	if (ret) {
		printf("AdGetSamplingConfig error: ret=%Xh\n", ret);
		exit(EXIT_FAILURE);
	}
	
	// Retrieve the current input value to wData[0...1] from CH1 and CH2.
	AdSmplChReq[0].ulChNo = 1;
	AdSmplChReq[0].ulRange = AdSmplConfig.SmplChReq[0].ulRange;
	AdSmplChReq[1].ulChNo = 2;
	AdSmplChReq[1].ulRange = AdSmplConfig.SmplChReq[0].ulRange;
	
	if (BoardSpec.ulResolution <= 8) {
		ret = AdInputAD(dnum, 2, AD_INPUT_SINGLE, AdSmplChReq, bData);
	} else if(BoardSpec.ulResolution > 8 && BoardSpec.ulResolution <= 16) {
		ret = AdInputAD(dnum, 2, AD_INPUT_SINGLE, AdSmplChReq, wData);
	} else {
		ret = AdInputAD(dnum, 2, AD_INPUT_SINGLE, AdSmplChReq, dwData);
	}
	if (ret) {
		AdClose(dnum);
		printf("AdInputAD error: ret=%Xh\n", ret);
		exit(EXIT_FAILURE);
	}
	
	// Display the retrieved result.
	if (BoardSpec.ulResolution <= 8) {
		printf("%02X", bData[0]);
	} else if(BoardSpec.ulResolution > 8 && BoardSpec.ulResolution <= 16) {
		printf("%04X", wData[0]);
	} else {
		printf("%08X", dwData[0]);
	}
	
	// Close the device.
	AdClose(dnum);
	
	return 0;
}
