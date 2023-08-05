//	ПРИМЕР ФИКСИРУЕТ СМЕНУ СОСТОЯНИЯ КНОПКИ:
// В stdout будет выводится сообщение при каждом нажатии и отпускании кнопки.

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
	// Если состояние кнопки изменилось, то ...
	if (enc.getButton(KEY_CHANGED)) {
		// Выводим текст в stdout
		std::cout << "Click" << '\n';
	}
}
