/*
 *	ПРИМЕР ЧТЕНИЯ ТАКТОВ ПОВОРОТА ЭНКОДЕРА:
 * В данном примере считываются такты поворотов
 * энкодера, отдельно вправо и отдельно влево.
 *
 */

#include <iostream>

//  Подключаем библиотеку для работы с энкодером I2C-flash.
#include "../iarduino_I2C_Encoder.h"

//  Инстанциируем объект, указывая адрес модуля на шине I2C.
iarduino_I2C_Encoder enc(0x09);

void loop(void);

int main()
{
	//  Инициируем работу с энкодером.
	enc.begin();
	for (;;)
		loop();
}

void loop()
{
	int turnL=0, turnR=0;

	/*	Считываем такты поворота энкодера:	*/

	turnL=enc.getEncoder(ENC_TURN_LEFT);
	turnR=enc.getEncoder(ENC_TURN_RIGHT);

	//  Выводим считанные данные:
	if (turnL) {
		std::cout << "-";
		std::cout << turnL;
		std::cout << '\n';
	}
	if (turnR) {
		std::cout << "+" ;
		std::cout << turnR ;
		std::cout << '\n';
	}

	delay(100);
}
