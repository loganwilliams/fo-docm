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
#include <sys/time.h>
#define SIZE 1048576

ADBOARDSPEC    BoardSpec;
ADSMPLREQ      AdSmplConfig;        // Sampling conditions setting structure
unsigned char  bSmplData[SIZE][2];  // Sampling data storage area
unsigned short wSmplData[SIZE][2];  // Sampling data storage area
unsigned int   dwSmplData[SIZE][2]; // Sampling data storage area

int main(void)
{
	int            ret, dnum;
	unsigned long  ulSmplNum;           // Number of the sampling data acquisition
	unsigned long  i;
	struct timeval tv;
	unsigned long time_in_micros;
	
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
	AdSmplConfig.ulChCount = 2;
	AdSmplConfig.SmplChReq[0].ulChNo = 1;
	AdSmplConfig.SmplChReq[0].ulRange = AD_5V;
	AdSmplConfig.SmplChReq[1].ulChNo = 2;	
	AdSmplConfig.SmplChReq[1].ulRange = AD_5V;
	AdSmplConfig.ulSingleDiff = AD_INPUT_SINGLE;
	AdSmplConfig.fSmplFreq = 5000000.0;

	AdSmplConfig.ulSmplNum = SIZE;
	ret = AdSetSamplingConfig(dnum, &AdSmplConfig);
	if (ret) {
		printf("AdSetSamplingConfig error: ret=%Xh\n", ret);
		AdClose(dnum);
		exit(EXIT_FAILURE);
	}
	
	// Start the sampling with synchronous mode.

	gettimeofday(&tv, NULL);
	time_in_micros = 1000000 * (tv.tv_sec % 60) + tv.tv_usec;

	printf("%lu\n", time_in_micros);
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
			fprintf(f,"%d, %d\n", bSmplData[i][0], bSmplData[i][1]);
		}
	} else if(BoardSpec.ulResolution > 8 && BoardSpec.ulResolution <= 16) {
		for (i = 0; i < ulSmplNum; i++) {
			fprintf(f, "%d, %d\n", wSmplData[i][0], wSmplData[i][1]);
		}
	} else {
		for (i = 0; i < ulSmplNum; i++) {
			fprintf(f, "%d, %d\n", dwSmplData[i][0], dwSmplData[i][1]);
		}
	}
	
	// Close the device.
	AdClose(dnum);
	
	return 0;
}
