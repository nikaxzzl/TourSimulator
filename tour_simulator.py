from rich.console import Console
import json
import time
import os
from PIL import Image
from art import tprint
from rich.panel import Panel  
from rich.progress import track
import pyttsx3

console = Console(force_terminal=True)
point_global = 0    
cities_passed = 0
routes_file = "routes.json"
visited_cities = []
engine = pyttsx3.init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_yes_no_input(prompt):

    while True:
        response = input(prompt).strip().lower()
        if response in ['да', 'yes']:
            return True
        elif response in ['нет', 'no']:
            return False
        else:
            console.print("Пожалуйста, введите да или нет", style="red")


def load_routes():
    if os.path.exists(routes_file):
        with open(routes_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        console.print("Файл маршрутов не найден!", style="bold red")
        return {}

def menu():
    console.print("[bold cyan]")
    tprint("Tour-simulator", font="slant")
    console.print(
        Panel.fit(
            "Добро пожаловать в «Тур-симулятор»! ",
            
        )
    )
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
        status = (
            "[green](Пройден ✔)[/]"
            if city["name"] in visited_cities
            else "[yellow](Новый ⏳)[/]"
        )
        console.print(f"{num}. {city['name']} {status}")

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
    global cities_passed,  point_global, visited_cities
    
    city_name = city['name']
    is_already_visited = city_name in visited_cities
    clear_screen()

    console.print(
        f"[bold yellow]Отправляемся в путь по маршруту: {city['name']}...[/]"
    )
    for _ in track(range(20), description="[green]Сборы и дорога...[/]"):
        time.sleep(0.10)
    
    clear_screen()
    
    console.print(
        Panel(
            f"[bold text #ffffff]{city['description']}[/]",
            title=f"Добро пожаловать в {city['name']}!",
            style="bold blue",
        )
    )
    input("\nГотовы к путешествие?! Нажмите Enter, чтобы перейти к остановке...")

    stops = city.get('stops', [])
    console.print(f"\n[bold magenta][СИСТЕМА] Python нашёл в файле остановок для этого города: {len(stops)}[/]")
    time.sleep(2)
    for number, stop in enumerate(stops, 1):
        stop_name = stop.get('name', f"Маршрутная точка {number}")
        stop_description = stop.get('description', stop.get('descripton', stop.get('discription', "Описание этой локации временно недоступно.")))


        console.print(f"\n📍 [bold green]Остановка {number}: {stop_name}[/]")
        console.print(stop_description)

        # Озвучка
        if get_yes_no_input("Хотите прослушать описание остановки? (да/нет): "):
            try:
                text_to_speak = f"Остановка {number}: {stop_name}. {stop_description}"
                for bad_char in ['—', '–', '«', '»', '°', '\n', '\t', '•', '📍','"',"-"," "]:
                    text_to_speak = text_to_speak.replace(bad_char, ' ')
                engine.say(text_to_speak)
                engine.runAndWait()
            except Exception as e:
                console.print(f"[bold red]Ошибка озвучки на остановке {number}: {type(e).__name__}: {e}[/]", style="red")
        else:
            console.print("Окей, читаем самостоятельно.", style="yellow")

        # Картинки
        image_path = stop.get("image_path")
        if image_path and os.path.exists(image_path):
            if get_yes_no_input("Хотите посмотреть картинку? (да/нет): "):
                try:
                    img = Image.open(image_path)
                    img.show()
                    console.print("Картинка открыта!", style="green")
                except Exception as e:
                    console.print(f"[bold red]Ошибка открытия картинки на остановке {number}: {type(e).__name__}: {e}[/]", style="red")
            else:
                console.print("Окей, переходим дальше.", style="yellow")
        else:
            if image_path:
                console.print(f"[dim]Картинка не найдена: {image_path}[/dim]", style="dim")
            else:
                console.print("[dim]Фото для этой остановки не предусмотрено[/dim]", style="dim")

        # Ждём Enter БЕЗ очистки экрана
        if number < len(stops):
            input("\nНажмите Enter для перехода к следующей остановке...")
        else:
            input("\nЭкскурсия завершена! Нажмите Enter, чтобы перейти к викторине...")

# ОЧИСТКА ЭКРАНА ТОЛЬКО ОДИН РАЗ — перед викториной
    clear_screen()
    time.sleep(0.5)
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
        
    if not is_already_visited:
        cities_passed += 1
        visited_cities.append(city_name)
        update_achievements(50)
        console.print(
            "🎉 Тур завершён впервые! Вы получили бонус: +50 очков достижений!",
            style="bold green",
        )
    else:
        console.print(
            "⏳ Тур завершён! Вы уже проходили его раньше, поэтому новые очки не начислены.",
            style="yellow",
        )

    input("\nНажмите Enter, чтобы вернуться в меню...")
    menu()


def update_achievements(points):
    global point_global
    point_global += points

def show_achievements():
    
    console.print(Panel("🏆 ВАШИ ДОСТИЖЕНИЯ", style="bold gold3", expand=False))
    console.print(f"• Настоящий путешественник: [bold green]{cities_passed}[/] пройденных туров", style="white")

    console.print(f" Очки достижений: [bold yellow]{point_global}", style="magenta")
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