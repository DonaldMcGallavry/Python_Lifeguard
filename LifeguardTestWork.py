# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 19:39:16 2024

@author: Swiborg
"""

import math
import unittest

def get_user_input():
    """Запрашивает значения у пользователя и возвращает их."""
    d1 = float(input("Введите кратчайшее расстояние от спасателя до кромки воды (в ярдах): "))
    d2 = float(input("Введите кратчайшее расстояние от утопающего до берега (в футах): "))
    h = float(input("Введите боковое смещение между спасателем и утопающим (в ярдах): "))
    V = float(input("Введите скорость движения спасателя по песку (в милях в час): "))
    n = float(input("Введите значение n: "))
    theta1 = float(input("Введите направление движения спасателя по песку (в градусах): "))
    return d1, d2, h, V, n, theta1

def convert_units(d2, V):
    """Преобразует единицы измерения и возвращает преобразованные значения."""
    d2_yards = d2 / 3  # преобразуем футы в ярды
    V_feet_per_hour = V * 5280 / 3  # преобразуем мили в ярды
    return d2_yards, V_feet_per_hour

def calculate_time(d1, d2_yards, h, V_feet_per_hour, n, theta1):
    """Выполняет необходимые вычисления и возвращает время в секундах."""
    if V_feet_per_hour <= 0:
        raise ValueError("Скорость должна быть больше нуля.")

    # Преобразование угла в радианы
    theta1_radians = math.radians(theta1)

    # Вычисление x
    x = d1 * math.tan(theta1_radians)

    # Вычисление L1 и L2
    L1 = math.sqrt(x**2 + d1**2)
    L2 = math.sqrt((h - x)**2 + d2_yards**2)

    # Вычисление общего времени t в часах
    t_hours = (L1 + n - L2) / V_feet_per_hour  # время в часах

    if t_hours < 0:
        raise ValueError("Время не может быть отрицательным. Проверьте входные параметры.")

    # Преобразование времени в секунды
    t_seconds = t_hours * 3600  # 1 час = 3600 секунд
    return t_seconds

def display_result(theta1, t_seconds):
    """Выводит результат пользователю."""
    print(f"Если спасатель начнёт движение под углом θ1, равным {theta1:.0f} градусам, он достигнет утопающего через {t_seconds:.1f} секунд.")

def main():
    d1, d2, h, V, n, theta1 = get_user_input()
    d2_yards, V_feet_per_hour = convert_units(d2, V)
    t_seconds = calculate_time(d1, d2_yards, h, V_feet_per_hour, n, theta1)
    display_result(theta1, t_seconds)

# Модульные тесты
class TestRescueTimeCalculator(unittest.TestCase):

    def test_convert_units(self):
        d2 = 12  # футы
        V = 3    # мили в час
        d2_yards, V_feet_per_hour = convert_units(d2, V)
        self.assertAlmostEqual(d2_yards, 4.0)  # 12 футов = 4 ярда
        self.assertAlmostEqual(V_feet_per_hour, 5280)  # 3 мили = 5280 футов

    def test_calculate_time(self):
        d1 = 10  # ярды
        d2_yards = 4  # ярды
        h = 3  # ярды
        V_feet_per_hour = 5280  # футы в час
        n = 2
        theta1 = 45  # градусы
        t_seconds = calculate_time(d1, d2_yards, h, V_feet_per_hour, n, theta1)
        self.assertGreaterEqual(t_seconds, 0)  # Время должно быть неотрицательным

    def test_calculate_time_zero_speed(self):
        d1 = 10  # ярды
        d2_yards = 4  # ярды
        h = 3  # ярды
        V_feet_per_hour = 0  # скорость
        n = 2
        theta1 = 45  # градусы
        with self.assertRaises(ValueError) as context:
            calculate_time(d1, d2_yards, h, V_feet_per_hour, n, theta1)
        self.assertEqual(str(context.exception), "Скорость должна быть больше нуля.")

    def test_calculate_time_negative_time(self):
        d1 = 10  # ярды
        d2_yards = 4  # ярды
        h = 3  # ярды
        V_feet_per_hour = 10  # футы в час
        n = 2
        theta1 = 0  # градусы
        with self.assertRaises(ValueError) as context:
            calculate_time(d1, d2_yards, h, V_feet_per_hour, n, theta1)
        self.assertEqual(str(context.exception), "Время не может быть отрицательным. Проверьте входные параметры.")

if __name__ == "__main__":
    main()
    unittest.main()

