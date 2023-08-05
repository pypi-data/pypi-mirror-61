/*	ПРИМЕР РАБОТЫ С КНОПКОЙ ЭНКОДЕРА:
 * В stdout выводится состояние кнопки в момент
 * запуска программы.
 */

#include <cstdio>
// Подключаем библиотеку для работы с энкодером I2C-flash.
#include "../iarduino_I2C_Encoder.h"

// Инстанциируем объект энкодера с адресом
iarduino_I2C_Encoder enc(0x09);

int main()
{
	// Инициируем работу с энкодером.
	enc.begin();
	// Считываем состояние кнопки энкодера в переменную f.
	bool f = enc.getButton(KEY_PRESSED);
	printf("%s", f ? "ON \n" : "OFF\n");
}
