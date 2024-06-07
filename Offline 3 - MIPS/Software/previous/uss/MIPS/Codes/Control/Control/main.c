
#define F_CPU 1000000
#include <util/delay.h>
#include <avr/io.h>

// generated based on our provided serial
// like 1 is sw and .....


# define add 0x0F
# define addi 0x0B
# define sub 0x0D
# define subi 0x01
# define and 0x08
# define andi 0x07
# define or 0x0C
# define ori 0x0E
# define sll 0x05
# define srl 0x00
# define nor 0x03
# define sw 0x04
# define lw 0x06
# define beq 0x02
# define bneq 0x09
# define j 0x0A



// defining our operations for producing ALUOP and selectors for each and every mux . ALUOP is not needed actually . This part is done in our circuit

unsigned char memArr[32];
int controlMem[16] = { 0xd04, 0x304, 0x240, 0x806, 0x110, 0xb04, 0x12c, 0x704, 0x606, 0x280, 0x001, 0x104, 0x406, 0x206, 0x504, 0x006 };

int main(void)
{
	// To use PC2,3,4,5 pins for general I/O operations, JTAG must be disabled.(Enable JTD twice)
	MCUCSR |= (1<<JTD);
	MCUCSR |= (1<<JTD);
	
	
	DDRA=0xFF;
	DDRB=0X00;
	DDRD=0X00;
	DDRC=0XFF;

	//DDRA=0X00; // ShowAddr A0 to A4; A5-> showaddrflag
	
	// opc BL
	// mRrWrDj AL
	// bNbEm2RmW AH
	// aluOPaluSRC CL


	PORTA = 0b11111111; // assign it as output
	PORTB = 0b00000000; // will take input for register1 and shift operation
	PORTD = 0b00000000; // takes input for register 2
	PORTC = 0b00001111; // shows output in the LSB part



	while (1)
	{
		unsigned int operation = PINB & 0b00001111;
		// taking input such as ADD OR , based on 4 bits
		// actually 0-15

		int ctrlOUT1 = controlMem[operation]%256;
		// now we have the value for each mux and aluop in int form
		
		PORTA = ctrlOUT1 & 0b11111111;
		// getting complete last 8 bit address in portA

		ctrlOUT1 = controlMem[operation]/256;
		
		PORTC = (ctrlOUT1 & 0b00001111)|( (operation<<4) & 0b11110000);
		//this will have the remaining 4 bits

		// combining PORTA and PORTC = mux selectors + ALUOP

		_delay_ms(10);
	}
}
//Control