
/*
	A1_Group1
	8 February, 2024
*/

#include <avr/io.h>
#define F_CPU 1000000
#include <util/delay.h>


int main(void)
{
	DDRA=0b11111111;	// configuring all A pins as output
	DDRB=0b00000000;	// configuring all B pins as input
	DDRC=0b11111111;	// configuring all C pins as output
	DDRD=0b00000000;	// configuring all D pins as input
	
	// JTAG is being enabled so that C pins may be used correctly
	
	MCUCSR|=(1<<JTD);
	MCUCSR|=(1<<JTD);	// JTAG needs to be enabled twice
	
	unsigned char PC;
	
	int current_level = 0;
	int previous_level = 0;
	int reset =	0;
	
	while (1) {
		previous_level = current_level;
		
		// taking clock and reset flags as input in PIND and extracting them
		char b = PIND;
		
		// current_level is the LSB of PIND
		current_level = ( b & 0b00000001);
		
		// reset is the second bit(index 1) of PIND
		reset =    ( b & 0b00000010)>>1;
		
		
		if(reset==1){ PORTA = 0x00; }	//	resetting PC 
			
			
		else{
			// detecting falling edge
			if(current_level == 0){
				if(previous_level == 1){
					PC = PINB;
					PORTA = PC;
				}
			}
		}
	}
}