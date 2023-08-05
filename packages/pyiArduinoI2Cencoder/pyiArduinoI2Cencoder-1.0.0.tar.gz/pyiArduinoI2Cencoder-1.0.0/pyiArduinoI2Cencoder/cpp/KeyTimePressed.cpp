/*
 * ДАННЫЙ ПРИМЕР ФИКСИРУЕТ УДЕРЖАНИЕ КНОПКИ:
 * В stdout будет вывоится время удержания кнопки
 */
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
	// Считываем время удержания кнопки (в миллисекундах)
	int t = enc.getButton(KEY_TIME_PRESSED);
	// Максимально фиксируемое время удержания: 25,5 секунд.
	printf("%d\n", t);
	delay(100);
}
