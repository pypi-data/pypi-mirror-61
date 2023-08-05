/*
 *	ДАННЫЙ ПРИМЕР ФИКСИРУЕТ УДЕРЖАНИЕ КНОПКИ:
 * В stdout будет выведено "ON" если кнопка
 * удерживается дольше фиксированного времени.
 */

#include <iostream>
#include <signal.h>

#include "../iarduino_I2C_Encoder.h"
iarduino_I2C_Encoder enc(0x09);

void loop(void);

void interrupt_handler(int s)
{
	printf("\e[00m\n");
	printf("Caught signal %d\n", s);
	exit(1);
}

int main()
{
	struct sigaction sigIntHandler;

	sigIntHandler.sa_handler = interrupt_handler;
	sigemptyset(&sigIntHandler.sa_mask);
	sigIntHandler.sa_flags = 0;

	// Инициируем работу с энкодером.
	enc.begin();
	for (;;) {
		sigaction(SIGINT, &sigIntHandler, NULL);
		loop();
	}

	return 0;
}

void loop()
{
	// bool f = enc.getButton(KEY_HOLD_05);  // Считываем удержание дольше 0,5 сек
	bool f = enc.getButton(KEY_HOLD_10);     // Считываем удержание дольше 1,0 сек
	// bool f = enc.getButton(KEY_HOLD_20);  // Считываем удержание дольше 2,0 сек

	if (f)
		printf("\e[01;32m%s\n", "ON ");
	else
		printf("\e[01;31m%s\n", "OFF");

	delay(100);
}
