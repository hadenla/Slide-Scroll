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

# Теперь импортируем остальные модули
import pyautogui
import random
import time
import math
from datetime import datetime, timedelta

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
        
        # Параметры человеческих движений
        self.human_params = {
            'min_speed': 0.22,      # Минимальная скорость (сек на 100 пикселей)
            'max_speed': 0.45,      # Максимальная скорость (немного быстрее)
            'jitter_amount': 2,     # Случайные микро-подёргивания
            'pause_variation': 0.25,# Вариация пауз между действиями
            'curve_intensity': 1.3, # Интенсивность кривизны траектории
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
    
    def get_human_speed(self, distance):
        """Рассчитывает человеческую скорость для заданного расстояния"""
        # Быстрые движения на короткие дистанции
        if distance < 100:
            base_speed = random.uniform(0.08, 0.18)
        elif distance < 300:
            base_speed = random.uniform(0.12, 0.25)
        elif distance < 600:
            base_speed = random.uniform(0.18, 0.35)
        else:
            base_speed = random.uniform(0.22, 0.45)
            
        # Добавляем случайную вариацию
        variation = random.uniform(0.85, 1.15)
        speed = base_speed * variation
        
        return min(self.human_params['max_speed'], 
                  max(self.human_params['min_speed'], speed))
    
    def add_human_jitter(self, x, y):
        """Добавляет микро-подёргивания как у человека"""
        jitter = self.human_params['jitter_amount']
        return x + random.randint(-jitter, jitter), y + random.randint(-jitter, jitter)
    
    def human_curve_move(self, start_x, start_y, end_x, end_y):
        """Естественное кривое движение как у человека"""
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        duration = self.get_human_speed(distance)
        
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
        steps = max(8, int(duration * 90 * random.uniform(0.7, 1.3)))
        
        for i in range(steps):
            # Периодические микро-паузы (реже для более быстрых движений)
            if not i % random.randint(4, 9):
                time.sleep(random.uniform(0.001, 0.002))
                
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
                time.sleep(duration / steps * random.uniform(1.05, 1.25))
            else:
                time.sleep(duration / steps * random.uniform(0.85, 1.05))
    
    def fast_linear_move(self, start_x, start_y, end_x, end_y):
        """Быстрое прямое движение с ускорением"""
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        duration = self.get_human_speed(distance) * random.uniform(0.6, 0.85)  # Быстрее
        
        steps = max(6, int(duration * 70))
        
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
            time.sleep(duration / steps * random.uniform(0.9, 1.1))
    
    def human_sinusoid_move(self, start_x, start_y, end_x, end_y):
        """Синусоидальное движение с человеческими вариациями"""
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        duration = self.get_human_speed(distance)
        
        # Случайные параметры синусоиды
        frequency = random.uniform(1.8, 3.5)  # Более высокая частота
        amplitude = random.uniform(25, 60) * (distance / 500)
        
        angle = math.atan2(end_y - start_y, end_x - start_x)
        steps = max(10, int(duration * 100))
        
        for i in range(steps):
            t = i / steps
            
            # Линейная интерполяция
            linear_x = start_x + (end_x - start_x) * t
            linear_y = start_y + (end_y - start_y) * t
            
            # Синусоидальное отклонение с затуханием
            offset = math.sin(t * frequency * math.pi) * amplitude * (1 - t*t)
            offset_x = offset * math.sin(angle + math.pi/2) * random.uniform(0.7, 1.3)
            offset_y = offset * math.cos(angle + math.pi/2) * random.uniform(0.7, 1.3)
            
            target_x = linear_x + offset_x
            target_y = linear_y + offset_y
            
            # Ограничиваем в пределах экрана
            target_x = max(1, min(self.screen_width - 2, target_x))
            target_y = max(1, min(self.screen_height - 2, target_y))
            
            pyautogui.moveTo(target_x, target_y)
            
            # Быстрая вариация скорости
            sleep_time = duration / steps * random.uniform(0.85, 1.05)
            time.sleep(sleep_time)
    
    def smooth_move_with_action(self, start_x, start_y, end_x, end_y, action="move"):
        """Плавное движение с человеческой скоростью и действием"""
        self.current_x, self.current_y = start_x, start_y
        
        # Случайный выбор типа движения
        move_types = [
            (self.fast_linear_move, 0.45),     # 45% - быстрые прямые (приоритет скорости)
            (self.human_curve_move, 0.35),     # 35% - кривые движения
            (self.human_sinusoid_move, 0.20),  # 20% - синусоиды
        ]
        
        move_func = random.choices(
            [m[0] for m in move_types],
            weights=[m[1] for m in move_types]
        )[0]
        
        # Выполняем движение
        move_func(start_x, start_y, end_x, end_y)
        
        # Обновляем позицию
        self.current_x, self.current_y = pyautogui.position()
        
        # Выполняем дополнительное действие
        self.perform_action(action)
        
        # Короткая микропауза после действия
        time.sleep(random.uniform(0.03, 0.10))
    
    def perform_action(self, action):
        """Выполняет одно из указанных действий"""
        if action == "move":
            # Простое движение мыши - иногда добавляем микро-движение
            if random.random() < 0.25:
                micro_x = self.current_x + random.randint(-8, 8)
                micro_y = self.current_y + random.randint(-8, 8)
                pyautogui.moveTo(micro_x, micro_y, duration=random.uniform(0.02, 0.06))
            print(f"  → Перемещение мыши")
            
        elif action == "scroll":
            # Улучшенная прокрутка колесом мыши (3-4 прокрутки)
            scroll_direction = random.choice([-1, 1])
            scroll_amount = random.randint(30, 40, 15, 20) * scroll_direction
            
            # Делаем несколько скроллов с естественными паузами
            for i in range(abs(scroll_amount)):
                pyautogui.scroll(scroll_direction, _pause=False)
                # Естественные паузы между скроллами
                time.sleep(random.uniform(0.15, 0.25))
            
            print(f"  ↕ Прокрутка колесом: {scroll_amount} шагов")
            
        elif action == "middle_only":
            # Движение мышкой с зажатой центральной кнопкой мыши (улучшенное)
            print(f"  🖱️  Средняя кнопка + движение")
            
            # Нажимаем среднюю кнопку мыши
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.08, 0.15))
            
            # Делаем движение при зажатой кнопке (длиннее и естественнее)
            drag_distance = random.randint(80, 200)
            drag_x = self.current_x + random.randint(-drag_distance, drag_distance)
            drag_y = self.current_y + random.randint(-drag_distance, drag_distance)
            
            # Более длительное и плавное движение
            drag_duration = random.uniform(0.3, 0.7)
            steps = int(drag_duration * 80)
            
            for i in range(steps):
                t = i / steps
                current_x = self.current_x + (drag_x - self.current_x) * t
                current_y = self.current_y + (drag_y - self.current_y) * t
                pyautogui.moveTo(current_x, current_y)
                time.sleep(drag_duration / steps)
            
            # Небольшая пауза в конечной позиции
            time.sleep(random.uniform(0.1, 0.2))
            
            # Отпускаем среднюю кнопку
            pyautogui.mouseUp(button='middle')
            
            # Обновляем позицию после перетаскивания
            self.current_x, self.current_y = drag_x, drag_y
            
        elif action == "shift_middle":
            # Движение мыши с зажатой центральной клавишей и клавишей Shift (улучшенное)
            print(f"  ⇧🖱️  Shift + средняя кнопка + движение")
            
            # Нажимаем Shift
            pyautogui.keyDown('shift')
            time.sleep(random.uniform(0.06, 0.12))
            
            # Нажимаем среднюю кнопку мыши
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.08, 0.15))
            
            # Делаем движение при зажатых клавишах (длиннее и с поворотами)
            drag_distance = random.randint(100, 250)
            drag_x = self.current_x + random.randint(-drag_distance, drag_distance)
            drag_y = self.current_y + random.randint(-drag_distance, drag_distance)
            
            # Длительное движение с возможными микро-паузами
            drag_duration = random.uniform(0.4, 0.9)
            steps = int(drag_duration * 100)
            
            for i in range(steps):
                t = i / steps
                
                # Иногда добавляем микро-паузы для естественности
                if random.random() < 0.02:
                    time.sleep(random.uniform(0.01, 0.03))
                
                current_x = self.current_x + (drag_x - self.current_x) * t
                current_y = self.current_y + (drag_y - self.current_y) * t
                pyautogui.moveTo(current_x, current_y)
                time.sleep(drag_duration / steps)
            
            # Пауза в конечной позиции
            time.sleep(random.uniform(0.15, 0.25))
            
            # Отпускаем среднюю кнопку
            pyautogui.mouseUp(button='middle')
            time.sleep(random.uniform(0.05, 0.1))
            
            # Отпускаем Shift
            pyautogui.keyUp('shift')
            
            # Обновляем позицию после перетаскивания
            self.current_x, self.current_y = drag_x, drag_y
            
        elif action == "double_middle_click":
            # Двойной щелчок средней кнопкой мыши
            print(f"  🖱️🖱️ Двойной щелчок средней кнопкой")
            
            # Первый щелчок
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.05, 0.08))
            pyautogui.mouseUp(button='middle')
            
            # Пауза между щелчками как у человека
            time.sleep(random.uniform(0.1, 0.2))
            
            # Второй щелчок
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.05, 0.08))
            pyautogui.mouseUp(button='middle')
            
            # Пауза после двойного щелчка
            time.sleep(random.uniform(0.2, 0.3))
    
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
        margin = 80
        target_x = random.randint(margin, self.screen_width - margin)
        target_y = random.randint(margin, self.screen_height - margin)
        
        # Распределение вероятностей для пяти активных действий
        actions = [
            ("move", 0.25),           # 25% - простое движение мыши
            ("scroll", 0.20),         # 20% - прокрутка колесом
            ("middle_only", 0.20),    # 20% - Средняя кнопка + движение
            ("shift_middle", 0.20),   # 20% - Shift + средняя кнопка + движение
            ("double_middle_click", 0.15),  # 15% - Двойной щелчок средней кнопкой
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
    print("  1. Движение мыши (25% вероятности)")
    print("  2. Прокрутка колесом мыши (20% вероятности)")
    print("  3. Движение с зажатой средней кнопкой (20% вероятности)")
    print("  4. Движение с зажатыми Shift + средней кнопкой (20% вероятности)")
    print("  5. Двойной щелчок средней кнопкой (15% вероятности)")
    print("\nДополнительные функции:")
    print("  • Редкое нажатие Esc (раз в 2 минуты, вероятность 10%)")
    print("  • Автоматическое переключение вкладок каждые 4 минуты")
    print("  • Таймер обратного отсчёта 10 секунд перед стартом")
    print("  • Улучшенные длинные скроллы (3-4 прокрутки)")
    print("\nНастройки:")
    print("  • Интервалы: 1-3 секунд")
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
            
            # Случайный интервал между действиями (1-3 секунды)
            base_wait = random.randint(1, 3)
            variation = random.uniform(0.8, 1.2)
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
            
            # Выполняем случайное действие
            mouse.random_action()
            
            # Короткая пауза после действия
            time.sleep(random.uniform(0.05, 0.15))
            
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
    print("  - Простое перемещение курсора")
    print("  - Прокрутку колесом мыши (3-4 шага)")
    print("  - Движение с зажатой средней кнопкой")
    print("  - Движение с зажатыми Shift + средней кнопкой")
    print("  - Двойной щелчок средней кнопкой")
    print("  - Редкие нажатия Esc")
    print("  - Автоматическое переключение вкладок каждые 4 минуты")
    print("\nУбедитесь, что нет открытых важных окон!")
    print("Для остановки: Ctrl+C или переместите мышь в верхний левый угол.")
    print("\nДля запуска нажмите Enter, для отмены закройте окно.")
    input()
    
    main()



#Что было добавлено и реализовано:
#1. Проверка зависимостей
#втоматическая проверка наличия pyautogui
#втоматическая установка при необходимости
#ведомления о процессе установки

# 2. Редкое нажатие Esc
#ажатие клавиши Esc с вероятностью 10%
#е чаще чем раз в 2 минуты
#стественные паузы после нажатия

# 3. Двойной щелчок средней кнопкой мыши
#овое действие с вероятностью 15%
#стественные паузы между щелчками
#обавлено в список доступных действий

# 4. Перемещение по вкладкам каждые 4 минуты
#оординаты 4 вкладок определены
#втоматическое переключение каждые 4 минуты
#лучайный выбор вкладки
#лавное перемещение и клик

# 5. Таймер обратного отсчёта 10 секунд
#тсчёт перед началом работы
#изуальный обратный отсчёт в консоли

# 6. Улучшенные скроллы и движения
#кроллы: 3-4 прокрутки с естественными паузами
#вижения с ЦКМ: увеличенная длительность (0.3-0.7 сек)
#вижения с Shift+ЦКМ: увеличенная длительность (0.4-0.9 сек) с микро-паузами

# 7. Удалены закомментированные функции
#се закомментированные блоки удалены
#ставлены только активные функции

# 8. Улучшенная статистика
#оказывает количество переключений вкладок
#лучшенное форматирование времени