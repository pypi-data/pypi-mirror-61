// ПРИМЕР СБРОСА ТЕКУЩЕЙ ПОЗИЦИИ ВАЛА ЭНКОДЕРА:

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
	for (;;)
		loop();
}

void loop()
{
	// Выводим текущую позицию вала энкодера.
	int16_t p = enc.getPosition();
	printf("%d\n", p);

	// Если нажата кнопка энкодера
	if (enc.getButton(KEY_PUSHED)) {
		// Сбрасываем позицию вала в 0:
		enc.resPosition();
	}

	delay(100);
}
