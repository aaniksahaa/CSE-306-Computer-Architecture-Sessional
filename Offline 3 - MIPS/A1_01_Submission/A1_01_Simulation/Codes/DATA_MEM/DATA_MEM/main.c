
/*
	A1_Group1
	8 February, 2024
*/

#include <avr/io.h>
#define F_CPU 1000000
#include <util/delay.h>

unsigned char memory_array[16];

int main(void)
{	
	// JTAG is being enabled so that C pins may be used for general IO correctly
	
	MCUCSR |= (1<<JTD);
	MCUCSR |= (1<<JTD);		// JTAG needs to be enabled twice
	
	
	DDRA=0b11111111;	// all A pins configured as output
	DDRB=0b00000000;	// all B pins configured as input
	DDRC=0b00000000;	// all C pins configured as input
	DDRD=0b00001111;	// lower 4 pins of D are set as output
	
	
	// level refers of clock level
	int current_level = 0;
	int previous_level = 0;
	
	int mem_read;
	int mem_write;
	
	int write_data;
	
	unsigned int address;
	
	// the data at the intended address
	unsigned int output_data;
	
	// helper variables to extract bits
	unsigned int b;
	unsigned int d;
	
	for(int i=0; i<16; i++){
		memory_array[i]=13;
	}
	
	while (1)
	{
		b = PINB ;
		
		// the upper 4 bits of PINB are inputted as write_data
		write_data = b>>4;
		
		//	the lower 4 bits of PINB are inputted as address
		address = b & 0b00001111;
		
		d = PIND;
		
		previous_level = current_level;
		
		// the following are being inputted through PIND
		// now they are being extracted
		
		// index-4 bit of d denotes mem_write
		mem_write= (d & 0b00010000)>>4;
		
		// index-5 bit of d denotes mem_read
		mem_read = (d & 0b00100000)>>5;
		
		// index-6 bit of d denotes current_level
		current_level = (d & 0b01000000)>>6;
		
		
		output_data = memory_array[address];
		
		// lower 4 bits of D are used to output the data read from the memory
		PORTD = (output_data & 0b00001111);
		
		// Note that, writing will occur in the opposite half cycle
		// Since we detected the falling edge previously, at this stage, we
		// detect the rising edge and then write the data
		
		if(previous_level==0 && current_level==1){
			if(mem_write == 1){
				// writing data to memory
				memory_array[address] = write_data;
			}
		}
		_delay_ms(10);
		
		
	}
}