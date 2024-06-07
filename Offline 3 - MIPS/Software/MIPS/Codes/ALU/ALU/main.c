 
/*
	A1_Group1
	8 February, 2024
*/
 
 #define F_CPU 1000000
 #include <util/delay.h>
 #include <avr/io.h>
 

// the following definitions are based on our assigned permutation


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


 int main(void)
 {
	 // JTAG is being enabled so that C pins may be used for general IO correctly
	 
	 MCUCSR |= (1<<JTD);
	 MCUCSR |= (1<<JTD);		// JTAG needs to be enabled twice
	 
	 DDRA=0b11111111;	// all A pins configured as output
	 DDRB=0b00000000;	// all B pins configured as input
	 DDRC=0b00000000;	// all C pins configured as input
	 DDRD=0b00000000;	// all D pins configured as input

	 PORTA = 0b00000001;

	 int register1_value;
	 int register2_value;
	 
	 int ALUop;
	 
	 int output_value = 0x00;
	 
	 // zero flag
	 int ZF = 0;
	 
	 int beqf;
	 int bneqf;
	 
	 int branch_decision;

	 while (1)
	 {
		 // lower 4 bits of PIND denotes ALUop
		 ALUop = PIND & 0x0F;
		 
		 // lower 4 bits of PINB denotes register1 value
		 register1_value = PINB & 0x0F;
		 
		 // upper 4 bits of PINB denotes register1 value
		 register2_value =  (PINB >> 4);
		 
		 int flags = PIND;
		 
		 // as per the design of control unit, index-4 bit of PIND denotes beqf
		 beqf = (flags & 0b00010000)>>4;
		 
		 // as per the design of control unit, index-5 bit of PIND denotes bneqf
		 bneqf = (flags & 0b00100000)>>5;

		 if (ALUop == add || ALUop ==addi || ALUop == lw || ALUop == sw)
		 {
			 output_value = (register1_value + register2_value) & 0x0F;
		 }
		 else if (ALUop == sub || ALUop == subi || ALUop == beq || ALUop == bneq)
		 {
			 output_value = (register1_value - register2_value +16 ) & 0x0F;
		 }
		 else if (ALUop == sll)
		 {
			 output_value = register1_value << register2_value;
			 output_value &= 0x0F;
		 }
		 else if (ALUop == srl)
		 {
			 output_value = register1_value >> register2_value;
		 }
		 else if (ALUop == and || ALUop == andi)
		 {
			 output_value = register1_value & register2_value;
		 }
		 else if (ALUop == or || ALUop == ori)
		 {
			 output_value = register1_value | register2_value;
		 }
		 else if (ALUop == nor)
		 {
			 output_value = register1_value | register2_value;
			 output_value = (output_value ^ 15);	// inverting bits
		 }
		 else if (ALUop == j)
		 {
			 output_value = 0;	// this is an arbitrary value
		 }

		 if (output_value%16 == 0)
		 {
			 ZF = 1;
		 }
		 else
		 {
			 ZF = 0;
		 }
		 
		 branch_decision = ( ZF & beqf )|( ( !ZF ) & bneqf );
		 
		 unsigned char out = output_value | (branch_decision<<4);
		 PORTA = out;
		 
		 _delay_ms(25);
	 }
 }