import os
from flask import Flask, render_template, request
from prognoz_ms import PrognozMSCalculator

app = Flask(__name__)
calc = PrognozMSCalculator()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        try:
            # Сбор и валидация данных из формы
            height = float(request.form.get('height', 0))
            weight = float(request.form.get('weight', 0))
            waist = float(request.form.get('waist', 0))
            gender = request.form.get('gender', 'female')

            # Базовая проверка диапазонов
            if height <= 50 or height >= 250:
                raise ValueError("Рост должен быть в диапазоне 50–250 см")
            if weight <= 20 or weight >= 300:
                raise ValueError("Вес должен быть в диапазоне 20–300 кг")
            if waist <= 30 or waist >= 200:
                raise ValueError("Окружность талии должна быть в диапазоне 30–200 см")
            if gender not in ('female', 'male'):
                raise ValueError("Некорректный пол")

            # Формирование словаря для ядра
            data = {
                'height': height,
                'weight': weight,
                'waist': waist,
                'gender': gender,
                'age_35_above': 'age_35_above' in request.form,
                'no_higher_edu': 'no_higher_edu' in request.form,
                'not_capital': 'not_capital' in request.form,
                'in_marriage': 'in_marriage' in request.form,
                'has_children': 'has_children' in request.form,
                'night_shifts': 'night_shifts' in request.form,
                'industry_risk': 'industry_risk' in request.form,
            }

            result = calc.calculate_risk(data)

        except ValueError as e:
            error = f"Ошибка ввода: {e}"
        except Exception:
            error = "Произошла внутренняя ошибка. Проверьте введённые данные."

    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    # Render передаёт порт через переменную окружения PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)