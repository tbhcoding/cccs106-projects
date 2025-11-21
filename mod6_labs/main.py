# main.py
"""Weather Application using Flet v0.28.3"""

import flet as ft
from weather_service import WeatherService
from config import Config
import datetime


class WeatherApp:
    """Main Weather Application class."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()
        self.setup_page()
        self.build_ui()
        
    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        
        # Add theme switcher
        self.page.theme_mode = ft.ThemeMode.SYSTEM  # Use system theme
        
        # Custom theme Colors
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.BLUE,
        )
        
        self.page.padding = 20
        
        # Window properties are accessed via page.window object in Flet 0.28.3
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        self.page.window.center()
        
    
    def build_ui(self):
        
        """Build the user interface."""
        # Title
        self.title = ft.Text(
            "Weather App",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
        )
        
        # Theme toggle button
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            tooltip="Toggle theme",
            on_click=self.toggle_theme,
        )
        
        # Update the Column to include the theme button in the title row
        title_row = ft.Row(
            [
                self.title,
                self.theme_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # City input field
        self.city_input = ft.TextField(
            label="Enter city name",
            hint_text="e.g., London, Tokyo, New York",
            border_color=ft.Colors.BLUE_400,
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            on_submit=self.on_search,
        )
        
        #Forecast button
        self.forecast_button = ft.ElevatedButton(
            "Get Forecast",
            icon=ft.Icons.WAVES,
            on_click=lambda e: self.page.run_task(self.get_forecast),
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREEN_700,
            ),
        )

        # Search button
        self.search_button = ft.ElevatedButton(
            "Get Weather",
            icon=ft.Icons.SEARCH,
            on_click=self.on_search,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_700,
            ),
        )
        
        # Weather display container (initially hidden)
        self.weather_container = ft.Container(
            visible=False,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            padding=20,
        )
        
        # Error message
        self.error_message = ft.Text(
            "",
            color=ft.Colors.RED_700,
            visible=False,
        )
        
        # Loading indicator
        self.loading = ft.ProgressRing(visible=False)
        
        # Add all components to page
        self.page.add(
            ft.Column(
                [
                    title_row,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.city_input,
                    ft.Row([self.search_button, self.forecast_button], spacing=10),  # <-- Updated here
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.loading,
                    self.error_message,
                    self.weather_container,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )
        
    def toggle_theme(self, e):
        """Toggle between light and dark theme."""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_button.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_button.icon = ft.Icons.DARK_MODE
        self.page.update()
        
    def on_search(self, e):
        """Handle search button click or enter key press."""
        self.page.run_task(self.get_weather)
    
    async def get_weather(self):
        """Fetch and display weather data."""
        city = self.city_input.value.strip()
        
        # Validate input
        if not city:
            self.show_error("Please enter a city name")
            return
        
        # Show loading, hide previous results
        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.page.update()
        
        try:
            # Fetch weather data
            weather_data = await self.weather_service.get_weather(city)
            
            # Display weather
            await self.display_weather(weather_data)
            
        except Exception as e:
            self.show_error(str(e))
        
        finally:
            self.loading.visible = False
            self.page.update()
    
    async def display_weather(self, data: dict):
        """Display weather information."""
        # Extract data
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp", 0)
        feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)
        
        # In display_weather method, add animation to container
        self.weather_container.animate_opacity = 300
        self.weather_container.opacity = 0
        self.weather_container.visible = True
        self.page.update()

        # Fade in
        import asyncio
        await asyncio.sleep(0.1)
        self.weather_container.opacity = 1
        self.page.update()
        
        # Build weather display
        self.weather_container.content = ft.Column(
            [
                # Location
                ft.Text(
                    f"{city_name}, {country}",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                
                # Weather icon and description
                ft.Row(
                    [
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                            width=100,
                            height=100,
                        ),
                        ft.Text(
                            description,
                            size=20,
                            italic=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                
                # Temperature
                ft.Text(
                    f"{temp:.1f}°C",
                    size=48,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                ),
                
                ft.Text(
                    f"Feels like {feels_like:.1f}°C",
                    size=16,
                    color=ft.Colors.GREY_700,
                ),
                
                ft.Divider(),
                
                # Additional info
                ft.Row(
                    [
                        self.create_info_card(
                            ft.Icons.WATER_DROP,
                            "Humidity",
                            f"{humidity}%"
                        ),
                        self.create_info_card(
                            ft.Icons.AIR,
                            "Wind Speed",
                            f"{wind_speed} m/s"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
        
        self.weather_container.visible = True
        self.error_message.visible = False
        self.page.update()
    
    def create_info_card(self, icon, label, value):
        """Create an info card for weather details."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=30, color=ft.Colors.BLUE_700),
                    ft.Text(label, size=12, color=ft.Colors.GREY_600),
                    ft.Text(
                        value,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
            width=150,
        )
    
    def show_error(self, message: str):
        """Display error message."""
        self.error_message.value = f"❌ {message}"
        self.error_message.visible = True
        self.weather_container.visible = False
        self.page.update()

    # async def display_forecast(self, data: dict):
    #     forecast_items = data.get("list", [])
    #     if not forecast_items:
    #         self.show_error("No forecast data available")
    #         return

    #     forecast_list = []
    #     # Show forecast for about 24 hours (each entry is 3 hours apart, so 8 entries for 24 hours)
    #     for item in forecast_items[:8]:
    #         dt_txt = item.get("dt_txt", "")
    #         temp = item.get("main", {}).get("temp", 0)
    #         description = item.get("weather", [{}])[0].get("description", "").title()
    #         forecast_list.append(
    #             ft.Text(f"{dt_txt}: {temp:.1f}°C, {description}")
    #         )

    #     self.weather_container.content = ft.Column(
    #         [ft.Text("5-Day Forecast", size=24, weight=ft.FontWeight.BOLD)] + forecast_list,
    #         spacing=5,
    #     )
    #     self.weather_container.visible = True
    #     self.error_message.visible = False
    #     self.page.update()

    async def display_forecast(self, data: dict):
        forecast_items = data.get("list", [])
        if not forecast_items:
            self.show_error("No forecast data available")
            return

        # Group forecasts by day, pick the entry closest to 12:00 for each day
        daily = {}
        for item in forecast_items:
            dt_txt = item.get("dt_txt", "")
            dt = datetime.datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
            day = dt.date()
            hour = dt.hour
            # Keep the entry closest to 12:00 (noon) for each day
            if day not in daily or abs(hour - 12) < abs(datetime.datetime.strptime(daily[day]["dt_txt"], "%Y-%m-%d %H:%M:%S").hour - 12):
                daily[day] = item

        # Build UI cards for each day's forecast
        forecast_cards = []
        for day, item in list(daily.items())[:5]:  # show up to 5 days
            temp = item.get("main", {}).get("temp", 0)
            description = item.get("weather", [{}])[0].get("description", "").title()
            icon_code = item.get("weather", [{}])[0].get("icon", "01d")
            dt_txt = item.get("dt_txt", "")
            forecast_cards.append(
                ft.Row(
                    [
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                            width=40,
                            height=40,
                        ),
                        ft.Text(f"{day.strftime('%a, %b %d')}", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{temp:.1f}°C", size=16, color=ft.Colors.BLUE_900),
                        ft.Text(description, size=14, italic=True),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    spacing=15,
                )
            )

        self.weather_container.content = ft.Column(
            [ft.Text("5-Day Forecast", size=24, weight=ft.FontWeight.BOLD)] + forecast_cards,
            spacing=10,
        )
        self.weather_container.visible = True
        self.error_message.visible = False
        self.page.update()


    async def get_forecast(self):
        city = self.city_input.value.strip()
        if not city:
            self.show_error("Please enter a city name for forecast")
            return

        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.page.update()

        try:
            forecast_data = await self.weather_service.get_forecast(city)
            await self.display_forecast(forecast_data)
        except Exception as e:
            self.show_error(str(e))
        finally:
            self.loading.visible = False
            self.page.update()



def main(page: ft.Page):
    """Main entry point."""
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)
    
#call get_forecast from weather_service file to implement this to UI