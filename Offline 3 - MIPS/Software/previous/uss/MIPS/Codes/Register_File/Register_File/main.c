#include <avr/io.h>
#define F_CPU 1000000
#include <util/delay.h>

unsigned char regArr[16];
//0 -> zero lol
//1 -> t0
//2 -> t1
//3 -> t2
//4 -> t3
//5 -> t4
//6 -> sp



int main(void)
{
	MCUCSR|=(1<<JTD);
	MCUCSR|=(1<<JTD);
	
	
	DDRA=0XFF;
	DDRB=0x00;
	DDRC=0x00;
	DDRD=0x00;
	
	for(int i=1; i<16; i++){
		regArr[i]=15-i;
	}
	regArr[0]=0;
	regArr[6]=15;
	
	int currclk=0;
	int regwrite;
	int showreg;
	int reset;
	int prevclk=0;
	
	while (1)
	{
		int b = PINB;
		int muxout = b%16;
		int reg2 = b>>4;
		int d = PIND;
		int reg1 = d%16;
		int flg = PINC;
		prevclk = currclk;
		currclk = (flg & 0b0001);
		regwrite = (flg & 0b0010)>>1;
		showreg = (flg & 0b0100)>>2;
		reset = (flg & 0b1000)>>3;
		int wb = flg>>4;
		
		if(showreg==1){
			int in1 = PIND>>4;
			PORTA = regArr[in1];
		}
		else{
			if(reset==1){
				for(int i=0; i<16; i++){
					regArr[i]=0;
				}
			}
			else{
				PORTA = ( (regArr[reg2]<< 4) | regArr[reg1]%16)%256;
				if(prevclk==0 && currclk == 1 && regwrite){
					regArr[muxout] = wb;
				}
			}
		}
		_delay_ms(10);
	}
}
//Register File