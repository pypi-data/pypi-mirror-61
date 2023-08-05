/*
 *	ПРИМЕР РАБОТЫ С КНОПОЧНЫМ ПЕРЕКЛЮЧАТЕЛЕМ:
 * При каждом нажатии на кнопку булева переменная
 * будет менять своё значение на противоположное
 */
#include <iostream>
// Подключаем библиотеку для работы с энкодером I2C-flash.
#include "../iarduino_I2C_Encoder.h"
// Инстанциируем объект, указывая адрес модуля на шине I2C.
iarduino_I2C_Encoder enc(0x09);

void loop(void);

int main()
{
	enc.begin();
	for (;;)
		loop();
}
void loop()
{
	//   Считываем состояние кнопочного переключателя энкодера
	bool f = !!enc.getButton(KEY_TRIGGER);
	std::cout << f << '\n';
	delay(100);
}
