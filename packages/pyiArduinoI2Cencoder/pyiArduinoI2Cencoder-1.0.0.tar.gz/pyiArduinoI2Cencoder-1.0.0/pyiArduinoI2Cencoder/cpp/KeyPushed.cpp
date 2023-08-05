/*
 *	ДАННЫЙ ПРИМЕР ФИКСИРУЕТ НАЖАТИЕ КНОПКИ:
 * При каждом нажатии кнопки, будет выводится
 * строка "test\n" в stdout
 */
#include <cstdio>

// Подключаем библиотеку для работы с энкодером I2C-flash.
#include "../iarduino_I2C_Encoder.h"
// Инстанциируем объект, указывая адрес модуля на шине I2C.
iarduino_I2C_Encoder enc(0x09);

void loop();

int main()
{
	// Инициируем работу с энкодером.
	enc.begin();
	for (;;)
		loop();
}

void loop()
{
	/*	Фиксируем событие нажатия кнопки:	*/

	// Если кнопка энкодера нажимается, то ...
	if (enc.getButton(KEY_PUSHED)) {
		// выводим текст в stdout
		printf("test\n");
	}
	delay(100);
}
