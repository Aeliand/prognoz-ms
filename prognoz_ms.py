# -*- coding: utf-8 -*-
"""
Наименование: ПРОГНОЗ-МС (PROGNOZ-MS)
Назначение: Вычислительный модуль нелинейной стратификации рисков метаболического синдрома
Версия: 1.3 (Оптимизированный лаконичный интерфейс, универсальная терминология)
Автор: Авторский коллектив исследователей проекта ПРОГНОЗ-МС
Год: 2026
"""

class PrognozMSCalculator:
    def __init__(self):
        pass

    def calculate_risk(self, data):
        # 1. Расчет и проверка ИМТ (Входной фильтр)
        height_m = data['height'] / 100.0
        bmi = data['weight'] / (height_m ** 2)

        if bmi < 25.0 or bmi >= 30.0:
            return {
                'status': 'error',
                'message': f"Ошибка: ИМТ {bmi:.1f}. Вход только для группы избыточного веса (ИМТ 25.0–29.9)."
            }

        score = 0.0

        # 2. Блок антропометрических маркеров
        whtr = data['waist'] / data['height']
        if whtr >= 0.5:
            score += 1.0

        if data['gender'] == 'female' and data['waist'] >= 80:
            score += 1.0
        elif data['gender'] == 'male' and data['waist'] >= 94:
            score += 1.0

        # 3. Блок социально-профессиональных триггеров по матрице логистической регрессии
        if data['night_shifts']:
            score += 2.0
        if data['no_higher_edu']:
            score += 1.5
        if data['in_marriage']:
            score += 1.5
        if data['age_35_above']:
            score += 1.0
        if data['gender'] == 'female':
            score += 1.0
        if data['industry_risk']:
            score += 0.5
        if data['has_children']:
            score += 0.5
        if data['not_capital']:
            score += 0.5

        if score > 10.0:
            score = 10.0

        # 4. ЛАКОНИЧНЫЙ ВЫВОД ДЛЯ ЭКРАНА ВРАЧА (Без избыточного текстового шума)
        if 0.0 <= score <= 3.0:
            risk_zone = 'green'
            risk_title = "НИЗКИЙ РИСК"
            action = "Рекомендована стандартная модификация образа жизни. Контроль ИМТ через 12 месяцев."
        elif 3.1 <= score <= 6.0:
            risk_zone = 'yellow'
            risk_title = "УМЕРЕННЫЙ РИСК"
            action = "Контроль веса в динамике. При отсутствии эффекта от диетотерапии через 3 месяца — рассмотреть медикаментозную терапию."
        else:
            risk_zone = 'red'
            risk_title = "ВЫСОКИЙ РИСК"
            action = "Показано углубленное обследование для исключения коморбидных патологий и решение вопроса о назначении медикаментозной терапии."

        return {
            'status': 'success',
            'bmi': round(bmi, 1),
            'whtr': round(whtr, 2),
            'total_score': round(score, 1),
            'risk_zone': risk_zone,
            'risk_title': risk_title,
            'action': action
        }

# Тестовая проверка работы ядра
if __name__ == "__main__":
    calc = PrognozMSCalculator()
    test_patient = {
        'height': 165, 'weight': 76.0, 'waist': 88, 'gender': 'female',
        'age_35_above': True, 'no_higher_edu': False, 'not_capital': True,
        'in_marriage': True, 'has_children': True, 'night_shifts': True, 'industry_risk': True
    }
    res = calc.calculate_risk(test_patient)
    print(f"[{res['risk_title']}] Баллов: {res['total_score']}\nТактика: {res['action']}")
