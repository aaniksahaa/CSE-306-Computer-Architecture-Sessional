
/*
	A1_Group1
	8 February, 2024
*/

#include <avr/io.h>
#define F_CPU 1000000
#include <util/delay.h>

// Registers: 0 - $zero, 1 - $t0, 2 - $t1, 3 - $t2, 4 - $t3, 5 - $t4, 6 - $sp, 7 - $hd

// here $hd = hidden register

unsigned char register_array[16];


int main(void)
{
	// JTAG is being enabled so that C pins may be used for general IO correctly
	
	MCUCSR|=(1<<JTD);
	MCUCSR|=(1<<JTD);	// JTAG needs to be enabled twice
	
	
	DDRA=0b11111111;	// all A pins configured as output
	DDRB=0b00000000;	// all B pins configured as input
	DDRC=0b00000000;	// all C pins configured as input
	DDRD=0b00000000;	// all D pins configured as input
	
	for(int i=1; i<16; i++){
		// register_array[i]=15-i;
		register_array[i] = 0;
	}
	
	// initializing the $zero register as zero constant
	register_array[0]=0;
	
	// initializing the $sp register as highest address F(15)
	register_array[6]=15;
	
	int previous_level = 0;
	int current_level = 0;
	
	int register_write;
	int show_register;
	int reset;
	
	while (1)
	{
		int b = PINB;
		
		// mux output denoting write destination is inputted through the lower 4 bits of PINB
		int write_address = b & 0x0F;
		
		// register2_address is inputted through the upper 4 bits of PINB
		int register2_address = b>>4;
		
		int d = PIND;
		
		// register1_address is inputted through the lower 4 bits of PIND
		int register1_address = d & 0x0F;
		
		int flags = PINC;
		
		previous_level = current_level;
		
		// index-0 bit of PINC denotes current_level
		current_level = (flags & 0b0001);
		
		// index-1 bit of PINC denotes register_write
		register_write = (flags & 0b0010)>>1;
		
		// index-2 bit of PINC denotes show_register
		show_register = (flags & 0b0100)>>2;
		
		// index-3 bit of PINC denotes reset
		reset = (flags & 0b1000)>>3;
		
		// write-back value is inputted through the upper 4 bits of PINC
		int wb = flags >> 4;
		
		// we are showing the current-instruction's write-back value instead
		if(show_register == 1){
			// this is always grounded for now
		}
		else{
			if(reset == 1){
				for(int i=0; i<16; i++){
					register_array[i]=0;	// resetting array
				}
			}
			else{
				PORTA = ( (register_array[register2_address]<< 4) | (register_array[register1_address] & 0x0F )) & 0xFF ;
				// detecting rising edge
				if(previous_level==0 && current_level == 1){
					// checking if writing is necessary
					if(register_write == 1){
						register_array[write_address] = wb;
					}
				}
			}
		}
		_delay_ms(25);
	}
}