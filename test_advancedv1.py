import pyautogui
import random
import time
import math
import sys
from datetime import datetime, timedelta

class HumanMouseMover:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.current_x, self.current_y = pyautogui.position()
        self.session_end_time = None
        self.start_time = None
        
        # Параметры человеческих движений
        self.human_params = {
            'min_speed': 0.12,      # Минимальная скорость (сек на 100 пикселей)
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
            # Прокрутка колесом мыши
            scroll_direction = random.choice([-1, 1])
            scroll_amount = random.randint(1, 15) * scroll_direction
            
            # Иногда делаем несколько быстрых скроллов
            if random.random() < 0.3:
                for _ in range(random.randint(4, 7)):
                    pyautogui.scroll(scroll_amount, _pause=False)
                    time.sleep(random.uniform(0.05, 0.12))
            else:
                pyautogui.scroll(scroll_amount, _pause=False)
                time.sleep(random.uniform(0.08, 0.15))
            
            print(f"  ↕ Прокрутка колесом: {scroll_amount}")
            
        elif action == "middle_only":
            # Движение мышкой с зажатой центральной кнопкой мыши
            print(f"  🖱️  Средняя кнопка + движение")
            
            # Нажимаем среднюю кнопку мыши
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.06, 0.12))
            
            # Делаем движение при зажатой кнопке
            drag_distance = random.randint(50, 150)
            drag_x = self.current_x + random.randint(-drag_distance, drag_distance)
            drag_y = self.current_y + random.randint(-drag_distance, drag_distance)
            
            # Плавное движение при зажатой кнопке
            drag_duration = random.uniform(0.2, 0.4)
            steps = int(drag_duration * 60)
            
            for i in range(steps):
                t = i / steps
                current_x = self.current_x + (drag_x - self.current_x) * t
                current_y = self.current_y + (drag_y - self.current_y) * t
                pyautogui.moveTo(current_x, current_y)
                time.sleep(drag_duration / steps)
            
            # Небольшая пауза в конечной позиции
            time.sleep(random.uniform(0.05, 0.15))
            
            # Отпускаем среднюю кнопку
            pyautogui.mouseUp(button='middle')
            
            # Обновляем позицию после перетаскивания
            self.current_x, self.current_y = drag_x, drag_y
            
        elif action == "shift_middle":
            # Движение мыши с зажатой центральной клавишей и клавишей Shift
            print(f"  ⇧🖱️  Shift + средняя кнопка + движение")
            
            # Нажимаем Shift
            pyautogui.keyDown('shift')
            time.sleep(random.uniform(0.04, 0.08))
            
            # Нажимаем среднюю кнопку мыши
            pyautogui.mouseDown(button='middle')
            time.sleep(random.uniform(0.06, 0.10))
            
            # Делаем движение при зажатых клавишах
            drag_distance = random.randint(40, 120)
            drag_x = self.current_x + random.randint(-drag_distance, drag_distance)
            drag_y = self.current_y + random.randint(-drag_distance, drag_distance)
            
            # Плавное движение при зажатых клавишах
            drag_duration = random.uniform(0.15, 0.3)
            steps = int(drag_duration * 50)
            
            for i in range(steps):
                t = i / steps
                current_x = self.current_x + (drag_x - self.current_x) * t
                current_y = self.current_y + (drag_y - self.current_y) * t
                pyautogui.moveTo(current_x, current_y)
                time.sleep(drag_duration / steps)
            
            # Небольшая пауза в конечной позиции
            time.sleep(random.uniform(0.05, 0.12))
            
            # Отпускаем среднюю кнопку
            pyautogui.mouseUp(button='middle')
            time.sleep(random.uniform(0.03, 0.07))
            
            # Отпускаем Shift
            pyautogui.keyUp('shift')
            
            # Обновляем позицию после перетаскивания
            self.current_x, self.current_y = drag_x, drag_y
            
        # ЗАКОММЕНТИРОВАННЫЕ ФУНКЦИИ
        # elif action == "scroll_right_edge":
        #     # Скролл в крайней правой части экрана
        #     print(f"  ↕ Скролл у правого края")
        #     
        #     # Перемещаемся к правому краю
        #     scroll_x = self.screen_width - 150  # 150px от правого края
        #     scroll_y = random.randint(100, self.screen_height - 100)
        #     
        #     pyautogui.moveTo(scroll_x, scroll_y, duration=random.uniform(0.3, 0.5))
        #     time.sleep(0.2)
        #     
        #     # Делаем несколько скроллов вверх и вниз
        #     for _ in range(random.randint(1, 5)):
        #         # Скролл вверх (от 5 до 10 шагов)
        #         scroll_up_steps = random.randint(5, 10)
        #         for _ in range(scroll_up_steps):
        #             pyautogui.scroll(1, _pause=False)
        #             time.sleep(random.uniform(0.05, 0.1))
        #         
        #         time.sleep(random.uniform(0.2, 0.4))
        #         
        #         # Скролл вниз (от 5 до 10 шагов)
        #         scroll_down_steps = random.randint(5, 10)
        #         for _ in range(scroll_down_steps):
        #             pyautogui.scroll(-1, _pause=False)
        #             time.sleep(random.uniform(0.05, 0.1))
        #         
        #         time.sleep(random.uniform(0.3, 0.6))
        # 
        # elif action == "double_click":
        #     # Двойное нажатие левой кнопкой мыши
        #     print(f"  👆 Двойной клик")
        #     time.sleep(random.uniform(0.1, 0.2))
        #     pyautogui.doubleClick()
        #     time.sleep(random.uniform(0.1, 0.3))
        # 
        # elif action == "single_left_click":
        #     # Одиночное нажатие левой кнопки мыши
        #     print(f"  👆 Одиночный левый клик")
        #     time.sleep(random.uniform(0.1, 0.2))
        #     pyautogui.click()
        #     time.sleep(random.uniform(0.1, 0.3))
        # 
        # elif action == "right_click_sequence":
        #     # Последовательность правых кликов
        #     print(f"  👉 Последовательность правых кликов")
        #     
        #     # Первый правый клик
        #     time.sleep(random.uniform(0.1, 0.2))
        #     pyautogui.rightClick()
        #     time.sleep(random.uniform(0.3, 0.5))
        #     
        #     # Перемещаемся на 500 пикселей и делаем второй правый клик
        #     second_x = self.current_x + random.randint(-500, 500)
        #     second_y = self.current_y + random.randint(-500, 500)
        #     
        #     # Ограничиваем координаты
        #     second_x = max(50, min(self.screen_width - 50, second_x))
        #     second_y = max(50, min(self.screen_height - 50, second_y))
        #     
        #     # Перемещаемся и кликаем
        #     pyautogui.moveTo(second_x, second_y, duration=random.uniform(0.3, 0.6))
        #     time.sleep(random.uniform(0.1, 0.2))
        #     pyautogui.rightClick()
        #     time.sleep(random.uniform(0.2, 0.4))
    
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
        
        # Распределение вероятностей для четырёх активных действий
        actions = [
            ("move", 0.30),           # 30% - простое движение мыши
            ("scroll", 0.25),         # 25% - прокрутка колесом
            ("middle_only", 0.25),    # 25% - Средняя кнопка + движение
            ("shift_middle", 0.20),   # 20% - Shift + средняя кнопка + движение
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

def main():
    print("=" * 60)
    print("🖱️  СКРИПТ ДВИЖЕНИЯ МЫШИ (4 АКТИВНЫХ ДЕЙСТВИЯ)")
    print("=" * 60)
    print("Активные действия:")
    print("  1. Движение мыши (30% вероятности)")
    print("  2. Прокрутка колесом мыши (25% вероятности)")
    print("  3. Движение с зажатой средней кнопкой (25% вероятности)")
    print("  4. Движение с зажатыми Shift + средней кнопкой (20% вероятности)")
    print("\nЗакомментированные действия:")
    print("  5. Скролл у правого края экрана")
    print("  6. Двойной левый клик")
    print("  7. Одиночный левый клик")
    print("  8. Последовательность правых кликов")
    print("\nНастройки:")
    print("  • Интервалы: 1-6 секунд")
    print("  • Скорость: оптимизирована для быстрых движений")
    print("  • Таймер: 1 час непрерывной работы")
    print("=" * 60)
    
    # Инициализация
    mouse = HumanMouseMover()
    mouse.set_session_duration(hours=1)
    
    # Настройки безопасности
    pyautogui.FAILSAFE = True
    # Исправлено: pyautogui.PAUSE - это атрибут, а не функция
    pyautogui.PAUSE = 0.003  # Минимальная пауза для максимальной плавности
    
    try:
        action_count = 0
        
        while True:
            # Проверяем время сессии
            if not mouse.check_session_time():
                print("\n✅ Сессия завершена по времени (1 час)")
                break
            
            # Случайный интервал между действиями (1-6 секунд)
            base_wait = random.randint(1, 3)  # Исправлено: Уменьшил интервал до максимум 3 секунды
            variation = random.uniform(0.8, 1.2)
            wait_time = max(0.8, base_wait * variation)
            
            # Показываем статус
            action_count += 1
            remaining = mouse.get_remaining_time()
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"\n[{current_time}] "
                  f"Действие #{action_count:03d} | "
                  f"Осталось: {remaining} | "
                  f"Следующее через: {wait_time:.1f}сек")
            
            # Просто ждём без обратного отсчёта (чтобы не мешать)
            time.sleep(wait_time)
            
            # Выполняем случайное действие
            mouse.random_action()
            
            # Короткая пауза после действия
            time.sleep(random.uniform(0.05, 0.15))
            
    except KeyboardInterrupt:
        print(f"\n\n✅ Ручная остановка. Всего действий: {action_count}")
    except pyautogui.FailSafeException:
        print(f"\n\n⚠️  Аварийная остановка (мышь в углу экрана)")
    except Exception as e:
        print(f"\n\n❌ Ошибка: {e}")
    finally:
        if mouse.start_time:
            duration = datetime.now() - mouse.start_time
            total_seconds = duration.total_seconds()
            print(f"\n📊 СТАТИСТИКА:")
            print(f"  ⏱️  Общая длительность: {int(total_seconds//3600)}:{int((total_seconds%3600)//60):02d}:{int(total_seconds%60):02d}")
            print(f"  🎯 Всего действий: {action_count}")
            if action_count > 0 and total_seconds > 0:
                avg_interval = total_seconds / action_count
                print(f"  ⏳ Средний интервал: {avg_interval:.1f} секунд")
                print(f"  📈 Действий в час: {int(action_count / total_seconds * 3600)}")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    # Важное предупреждение
    print("⚠️  ВНИМАНИЕ:")
    print("Скрипт будет перемещать мышь и выполнять действия:")
    print("  - Простое перемещение курсора")
    print("  - Прокрутку колесом мыши")
    print("  - Движение с зажатой средней кнопкой")
    print("  - Движение с зажатыми Shift + средней кнопкой")
    print("\nУбедитесь, что нет открытых важных окон!")
    print("Для остановки: Ctrl+C или переместите мышь в верхний левый угол.")
    print("\nДля запуска нажмите Enter, для отмены закройте окно.")
    input()
    
    main()


#Как активировать закомментированные функции:
#Раскомментируйте нужный блок кода в методе perform_action
#Добавьте действие в список actions в методе random_action
#Настройте вероятность в весах

#Todolist:
# Редкие нажатия
# Добавить рандомное нажатие Esc
# двойной щелчок цкм
# перемещение по вкладкам (узнать координаты)
# Добавить таймер передж начвалом действаий в 10 секунд