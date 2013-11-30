/* **************************************************************
   
   AdSampling.c -Source Code of AdStartSampling sample program
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
#define SIZE 2000000

ADBOARDSPEC    BoardSpec;
ADSMPLREQ      AdSmplConfig;        // Sampling conditions setting structure
unsigned char  bSmplData[SIZE];  // Sampling data storage area
unsigned short wSmplData[SIZE];  // Sampling data storage area
unsigned int   dwSmplData[SIZE]; // Sampling data storage area

int main(void)
{
	int            ret, dnum;
	unsigned long  ulSmplNum;           // Number of the sampling data acquisition
	unsigned long  i;
	
	//system("clear");
	//printf("Enter the device number.: ");
	//scanf("%d", &dnum);
	dnum = 1;	

	// Open a device.
	ret = AdOpen(dnum);
	if(ret){
		printf("Open error: ret=%Xh\n", ret);
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
	if(ret){
		printf("AdGetSamplingConfig error: ret=%Xh\n", ret);
		AdClose(dnum);
		exit(EXIT_FAILURE);
	}
	
	// Retrieve 1024 continuous data from CH1 and CH2.
	AdSmplConfig.ulChCount = 1;
	AdSmplConfig.SmplChReq[0].ulChNo = 1;
	AdSmplConfig.SmplChReq[0].ulRange = AD_5V;
	AdSmplConfig.ulSingleDiff = AD_INPUT_SINGLE;
	AdSmplConfig.fSmplFreq = 2000000.0;

	AdSmplConfig.ulSmplNum = SIZE;
	ret = AdSetSamplingConfig(dnum, &AdSmplConfig);
	if (ret) {
		printf("AdSetSamplingConfig error: ret=%Xh\n", ret);
		AdClose(dnum);
		exit(EXIT_FAILURE);
	}
	
	// Start the sampling with synchronous mode.
	printf("Starting sampling%d\n", EOF);
	ret = AdStartSampling(dnum, FLAG_SYNC);
	if (ret) {
		printf("AdStartSampling error: ret=%Xh\n", ret);
		AdClose(dnum);
		exit(EXIT_FAILURE);
	}
	
	// Retrieve the sampling data to wSmplData
	ulSmplNum = SIZE;
	if (BoardSpec.ulResolution <= 8) {
		ret = AdGetSamplingData(dnum, bSmplData, &ulSmplNum);
	} else if(BoardSpec.ulResolution > 8 && BoardSpec.ulResolution <= 16) {
		ret = AdGetSamplingData(dnum, wSmplData, &ulSmplNum);
	} else {
		ret = AdGetSamplingData(dnum, dwSmplData, &ulSmplNum);
	}
	if (ret) {
		printf("AdGetSamplingData error: ret=%Xh\n", ret);
		AdClose(dnum);
		exit(EXIT_FAILURE);
	}

	FILE *f = fopen("data.dat", "w");
	
	// Display the retrieved result.
	if (BoardSpec.ulResolution <= 8) {
		for (i = 0; i < ulSmplNum; i++) {
			fprintf(f,"%d\n", bSmplData[i]);
		}
	} else if(BoardSpec.ulResolution > 8 && BoardSpec.ulResolution <= 16) {
		for (i = 0; i < ulSmplNum; i++) {
			fprintf(f, "%d\n", wSmplData[i]);
		}
	} else {
		for (i = 0; i < ulSmplNum; i++) {
			fprintf(f, "%d\n", dwSmplData[i]);
		}
	}
	
	// Close the device.
	AdClose(dnum);
	
	return 0;
}
