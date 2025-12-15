import pyautogui
import random
import time
import math
import sys
import subprocess
import importlib.util
from datetime import datetime, timedelta

# Функция для проверки и установки зависимостей
def check_and_install_dependencies():
    """Проверяет наличие зависимостей и устанавливает их при необходимости"""
    required_packages = ['pyautogui']
    
    print("🔍 Проверка зависимостей...")
    
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            print(f"❌ Библиотека '{package}' не установлена. Устанавливаю...")
            
            python_exe = sys.executable
            pip_cmd = [python_exe, "-m", "pip", "install", package]
            
            try:
                print(f"   Установка {package}...", end=' ', flush=True)
                
                result = subprocess.run(
                    pip_cmd,
                    check=True,
                    capture_output=True,
                    text=True
                )
                
                print("✅ Успешно!")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Ошибка установки {package}: {e.stderr}")
                print("Попробуйте установить вручную: pip install pyautogui")
                input("Нажмите Enter для выхода...")
                sys.exit(1)
            except Exception as e:
                print(f"❌ Неизвестная ошибка: {e}")
                print("Попробуйте установить вручную: pip install pyautogui")
                input("Нажмите Enter для выхода...")
                sys.exit(1)
        else:
            print(f"✅ Библиотека '{package}' установлена")
    
    print("✅ Все зависимости проверены!\n")

# Проверяем и устанавливаем зависимости перед запуском
check_and_install_dependencies()

class HumanMouseMover:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.current_x, self.current_y = pyautogui.position()
        self.session_end_time = None
        self.start_time = None
        self.last_tab_switch = datetime.now()
        self.last_esc_press = datetime.now()
        self.action_count = 0
        
        # Координаты вкладок (x1, y1, x2, y2)
        self.tab_coordinates = [
            (237, 176, 354, 187),  # Вкладка 1
            (388, 176, 478, 187),  # Вкладка 2
            (531, 177, 630, 187),  # Вкладка 3
            (688, 177, 748, 187)   # Вкладка 4
        ]
        
        # Параметры человеческих движений - ОБНОВЛЕНО
        self.human_params = {
            'min_speed': 0.1,       # Минимальная скорость
            'max_speed': 5.0,       # Максимальная скорость (увеличена для длинных движений)
            'jitter_amount': 1,     # Случайные микро-подёргивания
            'pause_variation': 0.4, # Большая вариация пауз между действиями
            'curve_intensity': 1.5, # Интенсивность кривизны траектории
        }
        
    def set_session_duration(self, hours=1):
        """Устанавливает длительность сессии"""
        self.start_time = datetime.now()
        self.session_end_time = self.start_time + timedelta(hours=hours)
        print(f"Сессия начата: {self.start_time.strftime('%H:%M:%S')}")
        print(f"Автоматическая остановка: {self.session_end_time.strftime('%H:%M:%S')}")
        
    def check_session_time(self):
        """Проверяет, не истекло ли время сессии"""
        if self.session_end_time and datetime.now() >= self.session_end_time:
            print(f"\n⏰ Время сессии истекло! Прошёл 1 час.")
            return False
        return True
    
    def countdown_timer(self, seconds=10):
        """Таймер обратного отсчёта"""
        print(f"🚀 Начало через {seconds} секунд...")
        for i in range(seconds, 0, -1):
            print(f"{i}...", end=' ', flush=True)
            time.sleep(1)
        print("Старт!\n")
    
    def check_and_switch_tabs(self):
        """Проверяет, не пора ли переключить вкладки (каждые 4 минуты)"""
        current_time = datetime.now()
        if (current_time - self.last_tab_switch).total_seconds() >= 240:  # 4 минуты = 240 секунд
            print("🔄 Время переключить вкладку!")
            self.switch_to_random_tab()
            self.last_tab_switch = current_time
            return True
        return False
    
    def switch_to_random_tab(self):
        """Кликает по случайной вкладке"""
        tab = random.choice(self.tab_coordinates)
        x1, y1, x2, y2 = tab
        
        # Выбираем случайную точку внутри области вкладки
        click_x = random.randint(x1, x2)
        click_y = random.randint(y1, y2)
        
        # Плавно перемещаемся и кликаем
        print(f"  📑 Переключение на вкладку с координатами ({click_x}, {click_y})")
        pyautogui.moveTo(click_x, click_y, duration=random.uniform(0.3, 0.6))
        time.sleep(random.uniform(0.1, 0.2))
        pyautogui.click()
        time.sleep(random.uniform(0.5, 0.8))
        
        # Обновляем текущую позицию
        self.current_x, self.current_y = click_x, click_y
    
    def random_esc_press(self):
        """Случайное нажатие клавиши Esc"""
        current_time = datetime.now()
        
        # Нажимаем Esc с вероятностью 10% и не чаще чем раз в 2 минуты
        if (random.random() < 0.1 and 
            (current_time - self.last_esc_press).total_seconds() >= 120):
            
            print("  ⎋ Нажатие Esc")
            pyautogui.press('esc')
            time.sleep(random.uniform(0.2, 0.4))
            self.last_esc_press = current_time
            return True
        return False
    
    def get_human_speed(self, distance, action_type="default"):
        """Рассчитывает человеческую скорость для заданного расстояния с учетом типа действия"""
        # Разные скорости для разных типов действий
        if action_type == "long_move":
            # Длинные плавные движения (2-6 секунд)
            if distance < 100:
                base_speed = random.uniform(0.3, 0.8)
            elif distance < 300:
                base_speed = random.uniform(0.5, 1.2)
            elif distance < 600:
                base_speed = random.uniform(0.8, 2.0)
            else:
                base_speed = random.uniform(1.2, 3.0)
                
        elif action_type == "fast_move":
            # Быстрые движения
            if distance < 100:
                base_speed = random.uniform(0.2, 0.4)
            elif distance < 300:
                base_speed = random.uniform(0.3, 0.7)
            elif distance < 600:
                base_speed = random.uniform(0.5, 1.2)
            else:
                base_speed = random.uniform(0.8, 1.8)
                
        else:  # default - средние движения
            if distance < 100:
                base_speed = random.uniform(0.3, 0.8)
            elif distance < 300:
                base_speed = random.uniform(0.5, 1.2)
            elif distance < 600:
                base_speed = random.uniform(0.8, 2.0)
            else:
                base_speed = random.uniform(1.2, 3.0)
            
        # Добавляем случайную вариацию
        variation = random.uniform(0.8, 1.2)
        speed = base_speed * variation
        
        return min(self.human_params['max_speed'], 
                  max(self.human_params['min_speed'], speed))
    
    def add_human_jitter(self, x, y):
        """Добавляет микро-подёргивания как у человека"""
        jitter = self.human_params['jitter_amount']
        return x + random.randint(-jitter, jitter), y + random.randint(-jitter, jitter)
    
    def human_curve_move(self, start_x, start_y, end_x, end_y, duration_factor=1.0):
        """Естественное кривое движение как у человека"""
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        duration = self.get_human_speed(distance, "long_move") * duration_factor
        
        # Интенсивность кривизны
        curve_intensity = self.human_params['curve_intensity'] * random.uniform(0.7, 1.3)
        
        # Создаём контрольную точку для кривой
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Случайное отклонение от прямой линии
        dx = end_x - start_x
        dy = end_y - start_y
        perpendicular_x = -dy * 0.5
        perpendicular_y = dx * 0.5
        
        # Определяем направление кривизны (случайное)
        curve_dir = random.choice([-1, 1])
        control_x = mid_x + perpendicular_x * curve_intensity * curve_dir * random.uniform(0.15, 0.6)
        control_y = mid_y + perpendicular_y * curve_intensity * curve_dir * random.uniform(0.15, 0.6)
        
        # Количество шагов зависит от скорости
        steps = max(20, int(duration * 50 * random.uniform(0.7, 1.3)))
        
        print(f"    Кривое движение: {distance:.0f}px за {duration:.1f}сек, {steps} шагов")
        
        for i in range(steps):
            # Периодические микро-паузы (реже для более быстрых движений)
            if not i % random.randint(8, 15):
                time.sleep(random.uniform(0.001, 0.003))
                
            t = i / steps
            
            # Квадратичная кривая Безье
            x = (1-t)**2 * start_x + 2*(1-t)*t * control_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * control_y + t**2 * end_y
            
            # Добавляем микро-подёргивания
            x, y = self.add_human_jitter(x, y)
            
            # Ограничиваем в пределах экрана
            x = max(1, min(self.screen_width - 2, x))
            y = max(1, min(self.screen_height - 2, y))
            
            pyautogui.moveTo(x, y)
            
            # Нелинейная скорость (ускорение/замедление)
            if t < 0.2 or t > 0.8:
                time.sleep(duration / steps * random.uniform(1.1, 1.4))
            else:
                time.sleep(duration / steps * random.uniform(0.9, 1.1))
    
    def fast_linear_move(self, start_x, start_y, end_x, end_y, duration_factor=1.0):
        """Быстрое прямое движение с ускорением"""
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        duration = self.get_human_speed(distance, "fast_move") * duration_factor * random.uniform(0.8, 1.2)
        
        steps = max(15, int(duration * 60))
        
        print(f"    Быстрое движение: {distance:.0f}px за {duration:.1f}сек, {steps} шагов")
        
        for i in range(steps):
            t = i / steps
            
            # Easing: ускорение в начале, замедление в конце
            if t < 0.3:
                eased_t = t * t * 1.3  # Более резкое ускорение
            elif t > 0.7:
                eased_t = 1 - (1-t)*(1-t)*1.3  # Более резкое замедление
            else:
                eased_t = t  # Постоянная скорость в середине
            
            x = start_x + (end_x - start_x) * eased_t
            y = start_y + (end_y - start_y) * eased_t
            
            pyautogui.moveTo(x, y)
            
            # Еще более быстрые шаги
            time.sleep(duration / steps * random.uniform(0.95, 1.05))
    
    def human_sinusoid_move(self, start_x, start_y, end_x, end_y, duration_factor=1.0):
        """Синусоидальное движение с человеческими вариациями"""
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        duration = self.get_human_speed(distance, "long_move") * duration_factor
        
        # Случайные параметры синусоиды
        frequency = random.uniform(1.5, 2.5)  # Меньшая частота для плавности
        amplitude = random.uniform(30, 80) * (distance / 500)
        
        angle = math.atan2(end_y - start_y, end_x - start_x)
        steps = max(25, int(duration * 80))
        
        print(f"    Синусоида: {distance:.0f}px за {duration:.1f}сек, {steps} шагов")
        
        for i in range(steps):
            t = i / steps
            
            # Линейная интерполяция
            linear_x = start_x + (end_x - start_x) * t
            linear_y = start_y + (end_y - start_y) * t
            
            # Синусоидальное отклонение с затуханием
            offset = math.sin(t * frequency * math.pi) * amplitude * (1 - t*t*0.8)
            offset_x = offset * math.sin(angle + math.pi/2) * random.uniform(0.8, 1.2)
            offset_y = offset * math.cos(angle + math.pi/2) * random.uniform(0.8, 1.2)
            
            target_x = linear_x + offset_x
            target_y = linear_y + offset_y
            
            # Ограничиваем в пределах экрана
            target_x = max(1, min(self.screen_width - 2, target_x))
            target_y = max(1, min(self.screen_height - 2, target_y))
            
            pyautogui.moveTo(target_x, target_y)
            
            # Вариация скорости для естественности
            sleep_time = duration / steps * random.uniform(0.95, 1.05)
            time.sleep(sleep_time)
    
    def smooth_move_with_action(self, start_x, start_y, end_x, end_y, action="move"):
        """Плавное движение с человеческой скоростью и действием"""
        self.current_x, self.current_y = start_x, start_y
        
        # Определяем коэффициент длительности в зависимости от действия
        duration_factors = {
            "move": random.uniform(2.0, 5.0),          # Длинные движения: 2-5x
            "scroll": 1.0,                            # Скролл не влияет на движение
            "middle_only": random.uniform(1.5, 3.0),  # Средние движения
            "shift_middle": random.uniform(1.5, 3.0), # Средние движения
            "double_middle_click": 1.0,               # Клики не влияют
        }
        
        duration_factor = duration_factors.get(action, 1.0)
        
        # Случайный выбор типа движения с разными вероятностями в зависимости от действия
        if action == "move":
            # Для простого перемещения чаще используем длинные движения
            move_types = [
                (self.human_curve_move, 0.40),     # 40% - кривые движения
                (self.human_sinusoid_move, 0.40),  # 40% - синусоиды
                (self.fast_linear_move, 0.20),     # 20% - быстрые прямые
            ]
        else:
            # Для других действий более равномерное распределение
            move_types = [
                (self.fast_linear_move, 0.45),     # 45% - быстрые прямые
                (self.human_curve_move, 0.35),     # 35% - кривые движения
                (self.human_sinusoid_move, 0.20),  # 20% - синусоиды
            ]
        
        move_func = random.choices(
            [m[0] for m in move_types],
            weights=[m[1] for m in move_types]
        )[0]
        
        # Выполняем движение с учетом коэффициента длительности
        move_func(start_x, start_y, end_x, end_y, duration_factor)
        
        # Обновляем позицию
        self.current_x, self.current_y = pyautogui.position()
        
        # Выполняем дополнительное действие
        self.perform_action(action)
        
        # Разная длительность паузы после действия
        post_action_pauses = {
            "move": random.uniform(0.1, 0.3),
            "scroll": random.uniform(0.2, 0.5),
            "middle_only": random.uniform(0.3, 0.6),
            "shift_middle": random.uniform(0.3, 0.6),
            "double_middle_click": random.uniform(0.2, 0.4),
        }
        
        time.sleep(post_action_pauses.get(action, 0.1))
    
    def perform_action(self, action):
        """Выполняет одно из указанных действий"""
        if action == "move":
            # Простое движение мыши - иногда добавляем микро-движение
            if random.random() < 0.3:
                micro_x = self.current_x + random.randint(-15, 15)
                micro_y = self.current_y + random.randint(-15, 15)
                micro_duration = random.uniform(0.1, 0.3)
                pyautogui.moveTo(micro_x, micro_y, duration=micro_duration)
            print(f"  → Перемещение мыши")
            
        elif action == "scroll":
            # ОБНОВЛЕНО: Человеческий скролл с разными паттернами
            scroll_pattern = random.choice(['single_big', 'multiple_small', 'fast_burst', 'slow_smooth'])
            
            if scroll_pattern == 'single_big':
                # Один большой скролл (как у человека)
                scroll_amount = random.randint(80, 250) * random.choice([-1, 1])
                print(f"  ↕ Один большой скролл: {scroll_amount}")
                pyautogui.scroll(scroll_amount)
                time.sleep(random.uniform(0.3, 0.6))
                
            elif scroll_pattern == 'multiple_small':
                # Несколько маленьких скроллов
                num_scrolls = random.randint(3, 8)
                scroll_direction = random.choice([-1, 1])
                print(f"  ↕ Несколько скроллов: {num_scrolls} по {scroll_direction}")
                
                for i in range(num_scrolls):
                    pyautogui.scroll(scroll_direction * random.randint(10, 25))
                    time.sleep(random.uniform(0.1, 0.25))
                    
            elif scroll_pattern == 'fast_burst':
                # Быстрая серия скроллов
                scroll_amount = random.randint(40, 80) * random.choice([-1, 1])
                print(f"  ↕ Быстрая серия скроллов: {scroll_amount}")
                
                # Делаем быструю серию из 2-4 скроллов
                for _ in range(random.randint(2, 4)):
                    pyautogui.scroll(scroll_amount // random.randint(2, 4))
                    time.sleep(random.uniform(0.05, 0.15))
                    
            else:  # slow_smooth
                # Медленный плавный скролл
                total_scroll = random.randint(60, 120) * random.choice([-1, 1])
                steps = random.randint(4, 8)
                scroll_per_step = total_scroll / steps
                print(f"  ↕ Медленный скролл: {total_scroll} за {steps} шагов")
                
                for step in range(steps):
                    # Немного случайности в каждом шаге
                    current_scroll = scroll_per_step * random.uniform(0.8, 1.2)
                    pyautogui.scroll(int(current_scroll))
                    time.sleep(random.uniform(0.2, 0.4))
            
        elif action == "middle_only":
            # Движение мышкой с зажатой центральной кнопкой мыши (улучшенное)
            print(f"  🖱️  Средняя кнопка + движение")
            
            # Нажимаем среднюю кнопку мыши
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.1, 0.2))
            
            # Увеличенная амплитуда перемещения с микро-движениями
            drag_distance = random.randint(200, 500)  # Увеличено
            drag_x = self.current_x + random.randint(-drag_distance, drag_distance)
            drag_y = self.current_y + random.randint(-drag_distance, drag_distance)
            
            # Плавное движение с естественными паузами
            drag_duration = random.uniform(1.0, 3.0)  # Увеличено
            steps = int(drag_duration * 100)
            
            for i in range(steps):
                t = i / steps
                
                # Случайные микро-паузы для естественности
                if random.random() < 0.01:
                    time.sleep(random.uniform(0.02, 0.05))
                
                current_x = self.current_x + (drag_x - self.current_x) * t
                current_y = self.current_y + (drag_y - self.current_y) * t
                pyautogui.moveTo(current_x, current_y)
                time.sleep(drag_duration / steps)
            
            # Пауза в конечной позиции
            time.sleep(random.uniform(0.2, 0.4))
            
            # Отпускаем среднюю кнопку
            pyautogui.mouseUp(button='middle')
            
            # Обновляем позицию после перетаскивания
            self.current_x, self.current_y = drag_x, drag_y
            
        elif action == "shift_middle":
            # Движение мыши с зажатой центральной клавишей и клавишей Shift (улучшенное)
            print(f"  ⇧🖱️  Shift + средняя кнопка + движение")
            
            # Нажимаем Shift
            pyautogui.keyDown('shift')
            time.sleep(random.uniform(0.08, 0.15))
            
            # Нажимаем среднюю кнопку мыши
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.1, 0.2))
            
            # Увеличенная амплитуда с сложной траекторией
            drag_distance = random.randint(250, 600)  # Увеличено
            drag_x = self.current_x + random.randint(-drag_distance, drag_distance)
            drag_y = self.current_y + random.randint(-drag_distance, drag_distance)
            
            # Сложное движение с переменной скоростью
            drag_duration = random.uniform(1.5, 4.0)  # Увеличено
            steps = int(drag_duration * 120)
            
            for i in range(steps):
                t = i / steps
                
                # Нерегулярные паузы
                if random.random() < 0.015:
                    time.sleep(random.uniform(0.03, 0.08))
                
                # Синусоидальная траектория для движения с Shift
                offset = math.sin(t * 2 * math.pi) * 20 * (1 - t)
                offset_x = offset * random.uniform(-1, 1)
                offset_y = offset * random.uniform(-1, 1)
                
                current_x = self.current_x + (drag_x - self.current_x) * t + offset_x
                current_y = self.current_y + (drag_y - self.current_y) * t + offset_y
                pyautogui.moveTo(current_x, current_y)
                
                # Переменная скорость
                speed_variation = 1.0
                if t < 0.2:
                    speed_variation = random.uniform(0.8, 1.0)  # Медленнее в начале
                elif t > 0.8:
                    speed_variation = random.uniform(0.7, 0.9)  # Медленнее в конце
                
                time.sleep((drag_duration / steps) * speed_variation)
            
            # Пауза в конечной позиции
            time.sleep(random.uniform(0.3, 0.6))
            
            # Отпускаем среднюю кнопку
            pyautogui.mouseUp(button='middle')
            time.sleep(random.uniform(0.08, 0.15))
            
            # Отпускаем Shift
            pyautogui.keyUp('shift')
            
            # Обновляем позицию после перетаскивания
            self.current_x, self.current_y = drag_x, drag_y
            
        elif action == "double_middle_click":
            # Двойной щелчок средней кнопкой мыши
            print(f"  🖱️🖱️ Двойной щелчок средней кнопкой")
            
            # Первый щелчок
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.08, 0.12))
            pyautogui.mouseUp(button='middle')
            
            # Разная пауза между щелчками как у человека
            pause_between = random.uniform(0.15, 0.35)
            time.sleep(pause_between)
            
            # Второй щелчок
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.08, 0.12))
            pyautogui.mouseUp(button='middle')
            
            # Пауза после двойного щелчка
            time.sleep(random.uniform(0.3, 0.5))
    
    def get_remaining_time(self):
        """Возвращает оставшееся время сессии"""
        if not self.session_end_time:
            return "∞"
        
        remaining = self.session_end_time - datetime.now()
        if remaining.total_seconds() <= 0:
            return "0:00"
        
        hours = int(remaining.total_seconds() // 3600)
        minutes = int((remaining.total_seconds() % 3600) // 60)
        seconds = int(remaining.total_seconds() % 60)
        
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    
    def random_action(self):
        """Случайное действие"""
        # Выбираем случайную целевую позицию (избегаем края экрана)
        margin = 100
        target_x = random.randint(margin, self.screen_width - margin)
        target_y = random.randint(margin, self.screen_height - margin)
        
        # Распределение вероятностей для пяти активных действий
        actions = [
            ("move", 0.30),           # 30% - простое движение мыши (увеличено для длинных движений)
            ("scroll", 0.25),         # 25% - прокрутка колесом
            ("middle_only", 0.15),    # 15% - Средняя кнопка + движение
            ("shift_middle", 0.20),   # 20% - Shift + средняя кнопка + движение
            ("double_middle_click", 0.10),  # 10% - Двойной щелчок средней кнопкой
        ]
        
        action = random.choices(
            [a[0] for a in actions],
            weights=[a[1] for a in actions]
        )[0]
        
        # Выполняем движение с выбранным действием
        self.smooth_move_with_action(
            self.current_x, self.current_y, 
            target_x, target_y, 
            action
        )
        
        # Обновляем позицию
        self.current_x, self.current_y = target_x, target_y
        
        # Увеличиваем счётчик действий
        self.action_count += 1
        
        # Редкое нажатие Esc
        self.random_esc_press()

def main():
    print("=" * 60)
    print("🖱️  УСОВЕРШЕНСТВОВАННЫЙ СКРИПТ ДВИЖЕНИЯ МЫШИ")
    print("=" * 60)
    print("Доступные действия:")
    print("  1. Движение мыши (30% вероятности) - РАЗНЫЕ ДЛИТЕЛЬНОСТИ!")
    print("  2. Прокрутка колесом мыши (25% вероятности) - ЧЕЛОВЕЧЕСКИЕ СКРОЛЛЫ!")
    print("  3. Движение с зажатой средней кнопкой (15% вероятности)")
    print("  4. Движение с зажатыми Shift + средней кнопкой (20% вероятности)")
    print("  5. Двойной щелчок средней кнопкой (10% вероятности)")
    print("\nОСНОВНЫЕ УЛУЧШЕНИЯ:")
    print("  • Разные длительности движений: от 0.5 до 5 секунд")
    print("  • Человеческие скроллы: 4 разных паттерна прокрутки")
    print("  • Увеличенная амплитуда перемещений: до 600 пикселей")
    print("  • Естественные паузы и микро-движения")
    print("\nДополнительные функции:")
    print("  • Редкое нажатие Esc (раз в 2 минуты, вероятность 10%)")
    print("  • Автоматическое переключение вкладок каждые 4 минуты")
    print("  • Таймер обратного отсчёта 10 секунд перед стартом")
    print("\nНастройки:")
    print("  • Интервалы: 1-6 секунд (увеличено)")
    print("  • Таймер: 1 час непрерывной работы")
    print("=" * 60)
    
    # Инициализация
    mouse = HumanMouseMover()
    mouse.set_session_duration(hours=1)
    
    # Таймер обратного отсчёта 10 секунд
    mouse.countdown_timer(10)
    
    # Настройки безопасности
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.003
    
    try:
        while True:
            # Проверяем время сессии
            if not mouse.check_session_time():
                print("\n✅ Сессия завершена по времени (1 час)")
                break
            
            # Проверяем, не пора ли переключить вкладки
            mouse.check_and_switch_tabs()
            
            # Разные интервалы между действиями (1-6 секунд)
            base_wait = random.choices([1, 2, 3, 4, 5, 6], weights=[0.2, 0.25, 0.2, 0.15, 0.1, 0.1])[0]
            variation = random.uniform(0.7, 1.3)
            wait_time = max(1.0, base_wait * variation)
            
            # Показываем статус
            remaining = mouse.get_remaining_time()
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"\n[{current_time}] "
                  f"Действие #{mouse.action_count + 1:03d} | "
                  f"Осталось: {remaining} | "
                  f"Следующее через: {wait_time:.1f}сек")
            
            # Ждём
            time.sleep(wait_time)
            
            # Выполняем случайное действие
            mouse.random_action()
            
            # Разная пауза после действия
            post_action_wait = random.uniform(0.1, 0.4)
            time.sleep(post_action_wait)
            
    except KeyboardInterrupt:
        print(f"\n\n✅ Ручная остановка. Всего действий: {mouse.action_count}")
    except pyautogui.FailSafeException:
        print(f"\n\n⚠️  Аварийная остановка (мышь в углу экрана)")
    except Exception as e:
        print(f"\n\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if mouse.start_time:
            duration = datetime.now() - mouse.start_time
            total_seconds = duration.total_seconds()
            print(f"\n📊 СТАТИСТИКА:")
            print(f"  ⏱️  Общая длительность: {int(total_seconds//3600)}:{int((total_seconds%3600)//60):02d}:{int(total_seconds%60):02d}")
            print(f"  🎯 Всего действий: {mouse.action_count}")
            if mouse.action_count > 0 and total_seconds > 0:
                avg_interval = total_seconds / mouse.action_count
                print(f"  ⏳ Средний интервал: {avg_interval:.1f} секунд")
                print(f"  📈 Действий в час: {int(mouse.action_count / total_seconds * 3600)}")
                print(f"  🔄 Переключений вкладок: {int(total_seconds / 240)}")
        print("=" * 60)
        
        # Пауза перед выходом
        input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    # Важное предупреждение
    print("⚠️  ВНИМАНИЕ:")
    print("Скрипт будет перемещать мышь и выполнять действия:")
    print("  - Длительные перемещения курсора (до 5 секунд)")
    print("  - ЧЕЛОВЕЧЕСКИЕ скроллы (4 разных паттерна)")
    print("  - Движение с зажатой средней кнопкой (увеличенная амплитуда)")
    print("  - Движение с зажатыми Shift + средней кнопкой (сложные траектории)")
    print("  - Двойной щелчок средней кнопкой")
    print("  - Редкие нажатия Esc")
    print("  - Автоматическое переключение вкладок каждые 4 минуты")
    print("\nУбедитесь, что нет открытых важных окон!")
    print("Для остановки: Ctrl+C или переместите мышь в верхний левый угол.")
    print("\nДля запуска нажмите Enter, для отмены закройте окно.")
    input()
    
    main()


# ============================================================
# ОСНОВНЫЕ ИЗМЕНЕНИЯ В ЭТОЙ ВЕРСИИ:
# ============================================================
# 
# 1. РАЗНЫЕ ДЛИТЕЛЬНОСТИ ДВИЖЕНИЙ:
#    • Простые перемещения мыши теперь длятся 2-5 секунд (коэффициент 2.0-5.0x)
#    • Добавлена система коэффициентов длительности для разных действий
#    • Для "move" действия чаще используются длинные движения (кривые и синусоиды)
# 
# 2. ЧЕЛОВЕЧЕСКИЕ СКРОЛЛЫ (4 паттерна):
#    • 'single_big': один большой скролл (80-150 шагов)
#    • 'multiple_small': несколько маленьких скроллов (3-8 раз по 10-25)
#    • 'fast_burst': быстрая серия скроллов
#    • 'slow_smooth': медленный плавный скролл
#    • Убраны искусственные паузы между отдельными шагами скролла
# 
# 3. УВЕЛИЧЕННАЯ АМПЛИТУДА ПЕРЕМЕЩЕНИЙ:
#    • middle_only: 200-500px (было 150-400px)
#    • shift_middle: 250-600px (было 200-500px)
#    • Добавлены сложные траектории для движения с Shift
# 
# 4. ЕСТЕСТВЕННЫЕ ПАУЗЫ И МИКРО-ДВИЖЕНИЯ:
#    • Разные паузы после разных действий
#    • Случайные микро-паузы во время длинных движений
#    • Переменная скорость движений (ускорение/замедление)
# 
# 5. РАЗНЫЕ ИНТЕРВАЛЫ МЕЖДУ ДЕЙСТВИЯМИ:
#    • 1-6 секунд вместо 1-3
#    • Взвешенная случайность (чаще 2-3 секунды, реже 5-6)
#    • Большая вариация (±30%)
# 
# 6. УЛУЧШЕННАЯ ОТЛАДОЧНАЯ ИНФОРМАЦИЯ:
#    • Показывает длительность и количество шагов для каждого движения
#    • Уточненные описания действий в консоли
# 
# 7. ОБНОВЛЕННЫЙ АЛГОРИТМ СКОРОСТИ:
#    • get_human_speed() теперь принимает тип действия
#    • Разные профили скорости: long_move, fast_move, default
#    • long_move: 1.5-6.0 секунд в зависимости от расстояния
#    • fast_move: 0.2-1.8 секунд
#    • default: 0.3-3.0 секунд
# 
# ============================================================
# РЕЗУЛЬТАТ:
# • Движения выглядят более человеческими и разнообразными
# • Скроллы теперь похожи на реальные человеческие прокрутки
# • Разные действия имеют разную длительность и характер
# • Общее поведение более естественное и менее роботизированное
# ============================================================