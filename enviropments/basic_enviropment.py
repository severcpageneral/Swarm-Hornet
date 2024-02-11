import gym
from gym import spaces
import numpy as np

class BasicEnv(gym.Env):
    def __init__(self):
        super(BasicEnv, self).__init__()  # Исправлено на BasicEnv
        self.length = 5000
        self.width = 5000
        self.height = 100
        self.action_space = spaces.Discrete(4)  # Пример: 4 направления движения
        self.observation_space = spaces.Box(low=0, high=1, 
                                            shape=(self.length, self.width, self.height), 
                                            dtype=np.float32)
        
    def step(self, action):
        # Обновление состояния среды в ответ на действие
        self._update_state(action)
        self._update_fuel(action)  # Обновление топлива на основе совершенного действия

        # Вычисление награды и штрафов
        reward = 0
        if self._found_target():
            reward += MAX_REWARD  # Максимальная награда за нахождение Target
        if self._is_in_noise():
            reward -= MIN_PENALTY  # Штраф за нахождение в области Noise

        # Проверка завершения эпизода
        done = self._reached_end() or self._out_of_fuel()

        # Дополнительная информация
        info = {}

        # Наблюдение (новое состояние среды)
        observation = self._get_observation()
        return observation, reward, done, info
    
    def _distance(self, point_a, point_b):
        """Вычисление расстояния между двумя точками."""
        return np.linalg.norm(np.array(point_a) - np.array(point_b))

    def _found_target(self):
        """Проверка нахождения цели в полусфере радиусом 50 px вокруг дрона."""
        return self._distance(self.drone_position, self.target_position) <= 50

    def _is_in_noise(self):
        """Проверка нахождения дрона в шумовой области (сфера радиусом 50 px)."""
        for noise_sphere in self.noise_spheres:
            if self._distance(self.drone_position, noise_sphere['center']) <= 50:
                return True
        return False

    def _reached_end(self):
        """Проверка достижения дроном точки End."""
        return self._distance(self.drone_position, self.end_position) <= 10

    def _out_of_fuel(self):
        """Проверка на исчерпание топлива."""
        return self.fuel_remaining <= 0

    def _update_fuel(self, action):
        """Обновление остатка топлива на основе действия."""
        # Предполагаем, что 'action' содержит вектор перемещения
        distance_moved = np.linalg.norm(action)
        self.fuel_remaining -= distance_moved
        # Обновить fuel_remaining в соответствии с расходом топлива
    
    def reset(self):
        # 1. Установка топлива в 100
        self.fuel_remaining = 100

        # 2. Случайные координаты для точки Home в нижних 20% среды
        self.home_position = self._random_position(lower_percent=0, upper_percent=20, on_ground=True)

        # 3. Помещение дрона на старт в точку Home
        self.drone_position = self.home_position

        # 4. Случайные координаты для точки End в нижних 20% среды
        self.end_position = self._random_position(lower_percent=0, upper_percent=20, on_ground=True)

        # 5. Случайные координаты для точки Target в верхних 20% среды
        self.target_position = self._random_position(lower_percent=80, upper_percent=100, on_ground=False)

        # Возвращение начального наблюдения (может быть изменено в зависимости от вашей среды)
        initial_observation = self._get_observation()
        return initial_observation

    def _random_position(self, lower_percent, upper_percent, on_ground):
        # Генерация случайных координат в заданном процентном диапазоне высоты
        z = 0 if on_ground else np.random.uniform(self.height_range * lower_percent / 100, self.height_range * upper_percent / 100)
        x = np.random.uniform(0, 5000)  # Укажите здесь диапазон для X
        y = np.random.uniform(0, 5000)  # Укажите здесь диапазон для Y
        return [x, y, z]

    def _get_observation(self):
        # Получение текущего наблюдения о состоянии среды
        # Это зависит от вашей конкретной реализации наблюдений
        pass

    def render(self, mode='human'):
        # Визуализация среды
        pass