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
        
        # РАБОЧАЯ ОБЛАСТЬ (добавлено)
        # Левая верхняя часть: 240х200
        # Правая нижняя часть: 1520х980
        self.work_area_x1, self.work_area_y1 = 240, 200
        self.work_area_x2, self.work_area_y2 = 1520, 980
        
        # Координаты вкладок (x1, y1, x2, y2)
        self.tab_coordinates = [
            (237, 176, 354, 187),  # Вкладка 1
            (388, 176, 478, 187),  # Вкладка 2
            (531, 177, 630, 187),  # Вкладка 3
            (688, 177, 748, 187)   # Вкладка 4
        ]
        
        # Параметры человеческих движений
        self.human_params = {
            'min_speed': 0.03,      # Быстрые минимальные скорости
            'max_speed': 2.0,       # Максимальная скорость для баланса
            'jitter_amount': 2.5,   # Добавлена небольшая тряска
            'pause_variation': 0.2, # Меньше вариация пауз
            'curve_intensity': 1.5, # Увеличенная кривизна для синусоид
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
            # ЗАКОММЕНТИРОВАНО: убрали щелчок мыши
            # self.switch_to_random_tab()
            self.last_tab_switch = current_time
            return True
        return False
    
    def switch_to_random_tab(self):
        """Кликает по случайной вкладке (ЗАКОММЕНТИРОВАНО)"""
        tab = random.choice(self.tab_coordinates)
        x1, y1, x2, y2 = tab
        
        # Выбираем случайную точку внутри области вкладки
        click_x = random.randint(x1, x2)
        click_y = random.randint(y1, y2)
        
        # Быстро перемещаемся и кликаем
        print(f"  📑 Переключение на вкладку с координатами ({click_x}, {click_y})")
        pyautogui.moveTo(click_x, click_y, duration=random.uniform(0.1, 0.3))
        time.sleep(random.uniform(0.05, 0.1))
        # ЗАКОММЕНТИРОВАНО: убрали щелчок мыши
        # pyautogui.click()
        time.sleep(random.uniform(0.2, 0.4))
        
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
            time.sleep(random.uniform(0.05, 0.15))
            self.last_esc_press = current_time
            return True
        return False
    
    def get_human_speed(self, distance, action_type="default"):
        """Рассчитывает человеческую скорость для заданного расстояния с учетом типа действия"""
        # Все скорости быстрые
        if action_type == "long_move":
            # Быстрые движения даже для "длинных" перемещений
            if distance < 100:
                base_speed = random.uniform(0.1, 0.3)
            elif distance < 300:
                base_speed = random.uniform(0.2, 0.5)
            elif distance < 600:
                base_speed = random.uniform(0.3, 0.7)
            else:
                base_speed = random.uniform(0.4, 1.0)
                
        elif action_type == "fast_move":
            # Очень быстрые движения
            if distance < 100:
                base_speed = random.uniform(0.05, 0.2)
            elif distance < 300:
                base_speed = random.uniform(0.1, 0.3)
            elif distance < 600:
                base_speed = random.uniform(0.15, 0.4)
            else:
                base_speed = random.uniform(0.2, 0.6)
                
        else:  # default - быстрые движения
            if distance < 100:
                base_speed = random.uniform(0.08, 0.25)
            elif distance < 300:
                base_speed = random.uniform(0.15, 0.4)
            elif distance < 600:
                base_speed = random.uniform(0.2, 0.6)
            else:
                base_speed = random.uniform(0.3, 0.9)
            
        # Минимальная вариация для предсказуемой скорости
        variation = random.uniform(0.95, 1.05)
        speed = base_speed * variation
        
        return min(self.human_params['max_speed'], 
                  max(self.human_params['min_speed'], speed))
    
    def add_human_jitter(self, x, y):
        """Добавляет микро-подёргивания как у человека (добавлена тряска)"""
        jitter_x = random.uniform(-self.human_params['jitter_amount'], 
                                 self.human_params['jitter_amount'])
        jitter_y = random.uniform(-self.human_params['jitter_amount'], 
                                 self.human_params['jitter_amount'])
        return x + jitter_x, y + jitter_y
    
    def human_curve_move(self, start_x, start_y, end_x, end_y, duration_factor=1.0):
        """Естественное кривое движение как у человека"""
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        duration = self.get_human_speed(distance, "fast_move") * duration_factor
        
        # Интенсивность кривизны
        curve_intensity = self.human_params['curve_intensity'] * random.uniform(0.8, 1.2)
        
        # Создаём контрольную точку для кривой
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Случайное отклонение от прямой линии
        dx = end_x - start_x
        dy = end_y - start_y
        perpendicular_x = -dy * 0.3
        perpendicular_y = dx * 0.3
        
        # Определяем направление кривизны (случайное)
        curve_dir = random.choice([-1, 1])
        control_x = mid_x + perpendicular_x * curve_intensity * curve_dir * random.uniform(0.1, 0.3)
        control_y = mid_y + perpendicular_y * curve_intensity * curve_dir * random.uniform(0.1, 0.3)
        
        # Минимальное количество шагов для скорости
        steps = max(8, int(duration * 30))
        
        for i in range(steps):
            t = i / steps
            
            # Квадратичная кривая Безье
            x = (1-t)**2 * start_x + 2*(1-t)*t * control_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * control_y + t**2 * end_y
            
            # Добавляем тряску
            x, y = self.add_human_jitter(x, y)
            
            # Ограничиваем в пределах экрана
            x = max(1, min(self.screen_width - 2, x))
            y = max(1, min(self.screen_height - 2, y))
            
            pyautogui.moveTo(x, y)
            
            # Равномерная скорость
            time.sleep(duration / steps)
    
    def fast_linear_move(self, start_x, start_y, end_x, end_y, duration_factor=1.0):
        """Быстрое прямое движение с ускорением"""
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        duration = self.get_human_speed(distance, "fast_move") * duration_factor
        
        # Минимальное количество шагов
        steps = max(5, int(duration * 20))
        
        for i in range(steps):
            t = i / steps
            
            # Минимальное easing для скорости
            if t < 0.3:
                eased_t = t * 1.1  # Легкое ускорение
            elif t > 0.7:
                eased_t = 0.9 + (t - 0.7) * 0.5  # Легкое замедление
            else:
                eased_t = t  # Постоянная скорость
            
            x = start_x + (end_x - start_x) * eased_t
            y = start_y + (end_y - start_y) * eased_t
            
            # Добавляем тряску
            x, y = self.add_human_jitter(x, y)
            
            pyautogui.moveTo(x, y)
            time.sleep(duration / steps)
    
    def human_sinusoid_move(self, start_x, start_y, end_x, end_y, duration_factor=1.0):
        """Синусоидальное движение с человеческими вариациями"""
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        duration = self.get_human_speed(distance, "fast_move") * duration_factor
        
        # Увеличенные параметры синусоиды для заметных волн
        frequency = random.uniform(1.5, 2.5)  # Увеличенная частота
        amplitude = random.uniform(35, 75) * (distance / 500)  # Увеличенная амплитуда
        
        angle = math.atan2(end_y - start_y, end_x - start_x)
        steps = max(12, int(duration * 35))  # Увеличенное количество шагов для плавности
        
        for i in range(steps):
            t = i / steps
            
            # Линейная интерполяция
            linear_x = start_x + (end_x - start_x) * t
            linear_y = start_y + (end_y - start_y) * t
            
            # Синусоидальное отклонение с затуханием
            offset = math.sin(t * frequency * math.pi) * amplitude * (1 - t*0.7)
            offset_x = offset * math.sin(angle + math.pi/2)
            offset_y = offset * math.cos(angle + math.pi/2)
            
            target_x = linear_x + offset_x
            target_y = linear_y + offset_y
            
            # Добавляем тряску
            target_x, target_y = self.add_human_jitter(target_x, target_y)
            
            # Ограничиваем в пределах экрана
            target_x = max(1, min(self.screen_width - 2, target_x))
            target_y = max(1, min(self.screen_height - 2, target_y))
            
            pyautogui.moveTo(target_x, target_y)
            time.sleep(duration / steps)
    
    def smooth_move_with_action(self, start_x, start_y, end_x, end_y, action="move"):
        """Плавное движение с человеческой скоростью и действием"""
        self.current_x, self.current_y = start_x, start_y
        
        # Минимальные коэффициенты длительности
        duration_factors = {
            "move": random.uniform(0.8, 1.5),
            "scroll": 1.0,
            "middle_only": random.uniform(0.8, 1.3),
            "shift_middle": random.uniform(0.8, 1.3),
            "double_middle_click": 1.0,
        }
        
        duration_factor = duration_factors.get(action, 1.0)
        
        # УВЕЛИЧЕНО количество синусоидных движений (70%)
        move_types = [
            (self.fast_linear_move, 0.30),     # 30% - быстрые прямые
            (self.human_sinusoid_move, 0.70),  # 70% - синусоидальные движения (увеличено)
        ]
        
        move_func = random.choices(
            [m[0] for m in move_types],
            weights=[m[1] for m in move_types]
        )[0]
        
        # Выполняем движение
        move_func(start_x, start_y, end_x, end_y, duration_factor)
        
        # Обновляем позицию
        self.current_x, self.current_y = pyautogui.position()
        
        # Выполняем дополнительное действие
        self.perform_action(action)
        
        # Короткие паузы после действия
        post_action_pauses = {
            "move": random.uniform(0.05, 0.15),
            "scroll": random.uniform(0.1, 0.25),
            "middle_only": random.uniform(0.1, 0.2),
            "shift_middle": random.uniform(0.1, 0.2),
            "double_middle_click": random.uniform(0.05, 0.15),
        }
        
        time.sleep(post_action_pauses.get(action, 0.1))
    
    def perform_action(self, action):
        """Выполняет одно из указанных действий"""
        if action == "move":
            # Быстрое движение мыши
            if random.random() < 0.1:
                micro_x = self.current_x + random.randint(-5, 5)
                micro_y = self.current_y + random.randint(-5, 5)
                pyautogui.moveTo(micro_x, micro_y, duration=random.uniform(0.03, 0.08))
            print(f"  → Перемещение мыши")
            
        elif action == "scroll":
            # Скроллы с добавлением длинных прокруток
            scroll_pattern = random.choice(['single_big', 'multiple_small', 'fast_burst', 'page_scroll'])
            
            if scroll_pattern == 'single_big':
                # Быстрый большой скролл
                scroll_amount = random.randint(40, 80) * random.choice([-1, 1])
                print(f"  ↕ Быстрый скролл: {scroll_amount}")
                pyautogui.scroll(scroll_amount)
                time.sleep(random.uniform(0.1, 0.2))
                
            elif scroll_pattern == 'multiple_small':
                # Несколько быстрых скроллов
                num_scrolls = random.randint(2, 4)
                scroll_direction = random.choice([-1, 1])
                print(f"  ↕ Несколько скроллов: {num_scrolls}")
                
                for i in range(num_scrolls):
                    pyautogui.scroll(scroll_direction * random.randint(10, 20))
                    time.sleep(random.uniform(0.03, 0.08))
                    
            elif scroll_pattern == 'fast_burst':
                # Очень быстрая серия скроллов
                scroll_amount = random.randint(20, 40) * random.choice([-1, 1])
                print(f"  ↕ Быстрая серия: {scroll_amount}")
                
                for _ in range(random.randint(2, 3)):
                    pyautogui.scroll(scroll_amount // random.randint(2, 3))
                    time.sleep(random.uniform(0.02, 0.05))
            
            else:  # page_scroll - очень длинная прокрутка на страницу
                # Длинная прокрутка (как прокрутка страницы)
                scroll_amount = random.randint(800, 1200) * random.choice([-1, 1])
                print(f"  ↕ Прокрутка страницы: {scroll_amount}")
                
                # Делаем плавную прокрутку несколькими частями
                chunks = random.randint(3, 6)
                chunk_size = scroll_amount // chunks
                
                for chunk in range(chunks):
                    # Небольшая случайность в размере каждого чанка
                    current_chunk = chunk_size * random.uniform(0.8, 1.2)
                    pyautogui.scroll(int(current_chunk))
                    
                    # Естественные паузы между частями прокрутки
                    if chunk < chunks - 1:  # Не делаем паузу после последнего чанка
                        time.sleep(random.uniform(0.1, 0.2))
                
                time.sleep(random.uniform(0.3, 0.5))  # Пауза после длинной прокрутки
            
        elif action == "middle_only":
            # Быстрое движение с зажатой средней кнопкой
            print(f"  🖱️  Средняя кнопка + движение")
            
            # Быстро нажимаем
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.03, 0.07))
            
            # Быстрое перемещение
            drag_distance = random.randint(100, 250)
            drag_x = self.current_x + random.randint(-drag_distance, drag_distance)
            drag_y = self.current_y + random.randint(-drag_distance, drag_distance)
            
            # Быстрое движение
            drag_duration = random.uniform(0.3, 0.7)
            pyautogui.moveTo(drag_x, drag_y, duration=drag_duration)
            time.sleep(random.uniform(0.05, 0.1))
            
            # Быстро отпускаем
            pyautogui.mouseUp(button='middle')
            
            # Обновляем позицию
            self.current_x, self.current_y = drag_x, drag_y
            
        elif action == "shift_middle":
            # Быстрое движение с Shift + средней кнопкой
            print(f"  ⇧🖱️  Shift + средняя кнопка + движение")
            
            # Быстрые нажатия
            pyautogui.keyDown('shift')
            time.sleep(random.uniform(0.02, 0.05))
            
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.03, 0.06))
            
            # Быстрое перемещение
            drag_distance = random.randint(150, 300)
            drag_x = self.current_x + random.randint(-drag_distance, drag_distance)
            drag_y = self.current_y + random.randint(-drag_distance, drag_distance)
            
            # Быстрое движение
            drag_duration = random.uniform(0.4, 0.9)
            pyautogui.moveTo(drag_x, drag_y, duration=drag_duration)
            time.sleep(random.uniform(0.08, 0.15))
            
            # Быстрые отпускания
            pyautogui.mouseUp(button='middle')
            time.sleep(random.uniform(0.02, 0.04))
            pyautogui.keyUp('shift')
            
            # Обновляем позицию
            self.current_x, self.current_y = drag_x, drag_y
            
        elif action == "double_middle_click":
            # Быстрый двойной щелчок
            print(f"  🖱️🖱️ Двойной щелчок")
            
            # Быстрые щелчки
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.02, 0.04))
            pyautogui.mouseUp(button='middle')
            
            time.sleep(random.uniform(0.05, 0.1))
            
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.02, 0.04))
            pyautogui.mouseUp(button='middle')
            
            time.sleep(random.uniform(0.1, 0.2))
    
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
    
    def get_target_position(self, action):
        """Получает целевую позицию в зависимости от типа действия"""
        margin = 100
        
        # Для перемещения и скролла - весь экран
        if action in ["move", "scroll"]:
            target_x = random.randint(margin, self.screen_width - margin)
            target_y = random.randint(margin, self.screen_height - margin)
        # Для остальных действий - только рабочая область
        else:
            target_x = random.randint(self.work_area_x1, self.work_area_x2)
            target_y = random.randint(self.work_area_y1, self.work_area_y2)
        
        return target_x, target_y
    
    def random_action(self):
        """Случайное действие"""
        # Распределение вероятностей
        actions = [
            ("move", 0.35),           # 35% - быстрое движение
            ("scroll", 0.30),         # 30% - быстрый скролл
            ("middle_only", 0.15),    # 15% - быстрое с ЦКМ
            ("shift_middle", 0.15),   # 15% - быстрое с Shift+ЦКМ
            ("double_middle_click", 0.05),  # 5% - быстрый двойной клик
        ]
        
        action = random.choices(
            [a[0] for a in actions],
            weights=[a[1] for a in actions]
        )[0]
        
        # Получаем целевую позицию в зависимости от типа действия
        target_x, target_y = self.get_target_position(action)
        
        # Выполняем движение
        self.smooth_move_with_action(
            self.current_x, self.current_y, 
            target_x, target_y, 
            action
        )
        
        # Обновляем позицию
        self.current_x, self.current_y = target_x, target_y
        
        # Увеличиваем счётчик
        self.action_count += 1
        
        # Редкое нажатие Esc
        self.random_esc_press()

def main():
    print("=" * 60)
    print("🖱️  УСОВЕРШЕНСТВОВАННЫЙ СКРИПТ ДВИЖЕНИЯ МЫШИ")
    print("=" * 60)
    print("Доступные действия:")
    print("  1. Быстрое движение мыши (35% вероятности)")
    print("  2. Быстрый скролл (30% вероятности)")
    print("  3. Быстрое движение с ЦКМ (15% вероятности)")
    print("  4. Быстрое движение с Shift+ЦКМ (15% вероятности)")
    print("  5. Быстрый двойной щелчок (5% вероятности)")
    print("\nОСНОВНЫЕ УЛУЧШЕНИЯ:")
    print("  • 70% синусоидальных движений (увеличено)")
    print("  • Добавлена небольшая тряска мышки")
    print("  • Рабочая область для действий с ЦКМ: 240x200 - 1520x980")
    print("  • Перемещение и скролл - по всему экрану")
    print("  • Убраны левые щелчки мыши")
    print("  • Очень длинные скроллы (прокрутка страницы)")
    print("  • Все движения быстрые и естественные")
    print("  • Увеличенная амплитуда синусоид")
    print("\nСКРОЛЛЫ (4 типа):")
    print("  • Single Big: 40-80 шагов")
    print("  • Multiple Small: 2-4 по 10-20 шагов")
    print("  • Fast Burst: быстрые серии")
    print("  • Page Scroll: 800-1200 шагов (прокрутка страницы)")
    print("\nДополнительные функции:")
    print("  • Редкое нажатие Esc (раз в 2 минуты)")
    print("  • Переключение вкладок БЕЗ щелчка каждые 4 минуты")
    print("  • Таймер обратного отсчёта 10 секунд")
    print("\nНастройки:")
    print("  • Интервалы: 1-3 секунды")
    print("  • Таймер: 1 час работы")
    print("  • Рабочая область: X:240-1520, Y:200-980")
    print("=" * 60)
    
    # Инициализация
    mouse = HumanMouseMover()
    mouse.set_session_duration(hours=1)
    
    # Таймер обратного отсчёта
    mouse.countdown_timer(10)
    
    # Настройки безопасности
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.001  # Минимальная пауза
    
    try:
        while True:
            # Проверяем время сессии
            if not mouse.check_session_time():
                print("\n✅ Сессия завершена по времени (1 час)")
                break
            
            # ПРОВЕРЯЕМ переключение вкладок (без щелчка)
            mouse.check_and_switch_tabs()
            
            # Короткие интервалы
            base_wait = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2])[0]
            variation = random.uniform(0.9, 1.1)
            wait_time = max(0.8, base_wait * variation)
            
            # Показываем статус
            remaining = mouse.get_remaining_time()
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"\n[{current_time}] "
                  f"Действие #{mouse.action_count + 1:03d} | "
                  f"Осталось: {remaining} | "
                  f"Следующее через: {wait_time:.1f}сек")
            
            # Ждём
            time.sleep(wait_time)
            
            # Выполняем действие
            mouse.random_action()
            
            # Короткая пауза
            time.sleep(random.uniform(0.03, 0.1))
            
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
        
        input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    # Предупреждение
    print("⚠️  ВНИМАНИЕ:")
    print("Скрипт будет БЫСТРО перемещать мышь и выполнять действия.")
    print("Добавлены длинные скроллы (прокрутка страницы).")
    print("Убраны левые щелчки мыши - только средняя кнопка и движения.")
    print("Рабочая область для ЦКМ действий: X:240-1520, Y:200-980")
    print("Для остановки: Ctrl+C или переместите мышь в верхний левый угол.")
    print("\nДля запуска нажмите Enter.")
    input()
    
    main()