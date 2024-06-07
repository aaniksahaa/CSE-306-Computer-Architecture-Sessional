
#include <avr/io.h>
#define F_CPU 1000000
#include <util/delay.h>

unsigned char memArr[16];

int main(void)
{
	MCUCSR|=(1<<JTD);
	MCUCSR|=(1<<JTD);
	
	
	DDRA=0XFF;
	DDRB=0x00;
	DDRC=0x00;
	DDRD=0x0F;
	
	int currclk = 0;
	int prevclk = 0;
	int memread;
	int memwrite;
	int writedata;
	unsigned int addr;
	unsigned int dataout;
	unsigned int b;
	unsigned int d;
	
	for(int i=0; i<16; i++){
		memArr[i]=13;
	}
	
	while (1)
	{
		b = PINB ;
		writedata = b>>4;
		addr = b%16;
		d = PIND;
		prevclk = currclk;
		currclk = (d & 0b01000000)>>6;
		memread = (d & 0b00100000)>>5;
		memwrite= (d & 0b00010000)>>4;
		
		dataout = memArr[addr];
		
		//if(mem2reg==1) PORTA = dataout;
		//else PORTA = addr;
		
		PORTD = (dataout & 0b00001111);
		
		if(prevclk==0 && currclk==1 && memwrite==1){
			memArr[addr] = writedata;
		}
		_delay_ms(10);
		
		
	}
}

//Data Memory