// ПРИМЕР ЧТЕНИЯ ТАКТОВ ПОВОРОТА ЭНКОДЕРА:

#include <iostream>

// Подключаем библиотеку для работы с энкодером I2C-flash.
#include "../iarduino_I2C_Encoder.h"
// Инстанциируем объект, указывая адрес модуля на шине I2C.
iarduino_I2C_Encoder enc(0x09);

void loop(void);

int main()
{
	// Инициируем работу с энкодером.
	enc.begin();
	for (;;)
		loop();
}

void loop()
{
	//  Считываем такты поворота энкодера:
	int turn=enc.getEncoder(ENC_TURN);

	//  Выводим считанные данные:
	if( turn ){ std::cout << turn << '\n'; }

	// Без задержки в stdout будут появляться только ±1.
	delay(100);
}
