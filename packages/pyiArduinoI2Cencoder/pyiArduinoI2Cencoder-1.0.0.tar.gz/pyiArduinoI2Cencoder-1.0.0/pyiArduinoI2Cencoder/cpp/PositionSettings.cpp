// ПРИМЕР НАСТРОЙКИ ПОКАЗАНИЙ ПОЗИЦИИ ВАЛА:

#include <cstdio>

// Подключаем библиотеку для работы с энкодером I2C-flash.
#include "../iarduino_I2C_Encoder.h"

// Инстанциируем объект, указывая адрес модуля на шине I2C.
iarduino_I2C_Encoder enc(0x09);

void loop(void);
int main()
{
	// Инициируем работу с энкодером.
	enc.begin();
	// Указываем считать до 5 полных оборотов, без отрицательных значений.
	enc.setPosSettings(5, false);
	for (;;)
		loop();
}

void loop()
{
	int16_t p = enc.getPosition();
	// Выводим текущую позицию вала энкодера.
	printf("%d\n", p);
	delay(500);
}
