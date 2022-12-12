from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    training_type: str = "Тип тренировки: {};"
    duration: str = "Длительность: {:.3f} ч.;"
    distance: str = "Ср. скорость: {:.3f} км/ч;"
    speed: str = "Ср. скорость: {:.3f} км/ч;"
    calories: str = "Потрачено ккал: {:.3f}."
    MESSAGE = (
        training_type,
        duration,
        distance,
        speed,
        calories
    )

    def get_message(self) -> None:
        t = asdict(self)
        message = self.MESSAGE.format(*t.values())
        return message


class Training:
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        distance = self.get_distance()
        speed = distance / self.duration
        return speed

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()

        return InfoMessage(
            type(self).__name__,
            duration,
            distance,
            speed,
            calories
        )


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:

        speed = self.get_mean_speed()
        calories_run = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER
             * speed + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight
            / self.M_IN_KM
            * (self.duration
               * self.MIN_IN_H)
        )
        return calories_run


class SportsWalking(Training):
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: float = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        speed: float = self.get_mean_speed()
        callories_wlk = (((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                         + ((speed * self.KMH_IN_MSEC)**2
                           / (self.height / self.CM_IN_M))
                           * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                           * self.weight)
                          * (self.duration
                          * self.MIN_IN_H)))
        return callories_wlk


class Swimming(Training):
    LEN_STEP = 1.38
    CALORIES_SWM_FIRST: float = 1.1
    CALORIES_SWM_SECOND: int = 2

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float, count_pool: float):
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed_swm = (
            self.lenght_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )
        return speed_swm

    def get_spent_calories(self) -> float:
        speed_swm = self.get_mean_speed()
        calories_swm: float = ((speed_swm + self.CALORIES_SWM_FIRST)
                               * self.CALORIES_SWM_SECOND
                               * self.weight
                               * self.duration)
        return calories_swm


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    name_train: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in name_train:
        return name_train[workout_type](*data)

    raise ValueError("Тренировка не найдена")


def main(training: Training) -> None:
    """Главная функция."""
    message_train = training.show_training_info()
    print(message_train.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
