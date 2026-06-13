from fontTools.varLib.plot import stops
from rich.console import Console
from art import text2art
import json
import os
from PIL import Image
from art import tprint
from colorama import init, Fore, Back, Style

init(autoreset=True)
console = Console(force_terminal=True)
point_global = 0    
cities_passed = 0
routes_file = "routes.json"


def load_routes():
    if os.path.exists(routes_file):
        with open(routes_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        console.print("Файл маршрутов не найден!", style="bold red")
        return {}

def menu():

    tprint("Tour-simulator", font="slant")
    console.print("Добро пожаловать в «Тур-симулятор»! ", style="bold italic  #E0FFFF on  #5F9EA0")
    console.print("Выберите действие:\n"
                  "1. 🗺️Начать новое путешествие\n"
                  "2. 🏆Достижения и бонусы — получить награды за пройденные туры\n"
                  "3. ❓Справка и помощь — узнать, как пользоваться приложением\n"
                  "4. 🚪Выйти\n")
    while True:
        actions = input("Выберите пункт меню (1–4):\t ")
        if actions == "1":
            one_new_travel()
            break
        elif actions == "2":
            show_achievements()
            break
        elif actions == "3":
            show_help()
            break
        elif actions == "4":
            console.print("До новых встреч в «Тур-симуляторе»!", style="bold green")
            exit()
        else:
            console.print("Ошибка: введите число от 1 до 4.", style="bold red")

def one_new_travel():

    console.print("\n\n\nВыберите город для путешествия:\n", style='bold underline yellow')

    routes = load_routes()
    cities = routes.get("cities", [])

    if not cities:
        console.print("Маршруты пока не загружены.", style="bold red")
        menu()
        return
    for num, city in enumerate(cities, 1):
        console.print(f"{num}. {city['name']} ")
        chet = 0
    while True:
        try:
            choose = int(input("Введите номер города:\t"))
            if 1 <= choose <= len(cities):
                opted_city = cities[choose - 1]
                choose_city(opted_city)

                break

            else:
                console.print("такого города нет в списке.", style="bold red")
        except ValueError:
                console.print("введите номер города цифрой.", style="bold red")




def choose_city(city):
    global cities_passed
    cities_passed += 1
    console.print(f"--------------------------------------------------------------------------------\nОтправимся в путешествие в {city['name']}", style="bold blue")
    console.print(city['description'], style="italic")

    stops = city.get('stops', [])


    for number, stop in enumerate(stops,1):
        console.print(f"\nОстановка {number}: {stop['name']} ", style="bold  green")
        console.print(stop['description'])
        image_path = stop.get("image_path")
        
        response = input("Хотите посмотреть картинку? (да/нет): ").strip().lower()
        if response in ['да', 'yes', 'y', 'д']:
            try:
                from PIL import Image
                img = Image.open(image_path)
                img.show()
                break
            except Exception as e:
                    print(f"Не удалось открыть картинку: {e}")
                    return False
        elif response in ['нет', 'no', 'n', 'н']:
                print("Окей")
                
        else:
                print("Пожалуйста, введите 'да' или 'нет'.")


        if number < len(stops):
            input("\nНажмите Enter для перехода к следующей остановке...\n\n")


    for number, stop in enumerate(stops, 1):
        console.print("ВИКТОРИНА", style='bold blue')
        if 'quiz' in stop:
            console.print(f"{stop['quiz']['question']}.", style="italic")
            answer = input("Ваш ответ: ").strip().lower()
        if answer == stop['quiz']['answer']:
            console.print("✔️ Правильно! +10 очков!", style="bold green")
            update_achievements(10)
        else:
            console.print(f"❌ Неверно. Это {stop['quiz']['answer']}.", style="bold red")

    console.print("--------------------------------------------------------------------------------\n\n\n\n Тур завершён! Вы получили бонус: +50 очков достижений!", style="bold green")
    update_achievements(50)
    menu()



def update_achievements(points):
    global point_global
    point_global += points
    console.print(f"Получено {points} очков достижений! Всего: {point_global}", style="  yellow")


def show_achievements():

    console.print("🏆 Ваши достижения:", style="bold underline yellow")
    console.print(f"• Настоящий путешественник: {cities_passed}3 тура", style="green")

    console.print(f"• Очки достижений: {point_global}", style="magenta")
    input("\nНажмите Enter, чтобы вернуться в меню...")
    menu()

def show_help():

    console.print("\n\n❓Справка и помощь:", style="bold underline #800000 on white")
    console.print("1. Для выбора пункта меню введите его номер.")
    console.print("2. В туре используйте Enter для перехода между остановками.")
    console.print("3. Мини‑игры помогут заработать бонусы.\n\n\n")
    input("\nНажмите Enter, чтобы вернуться в меню...")
    menu()
if __name__ == "__main__":
    menu()