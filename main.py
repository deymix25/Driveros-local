import flet as ft
from engine import DriverEngine

def main(page: ft.Page):
    page.title = "DriverOS Local - Rosario"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK

    engine = DriverEngine(fuel_cost_per_km=120.0, home_zone="Zona Oeste")

    fuel_input = ft.TextField(
        label="Costo Combustible ($ ARS / km)",
        value="120",
        keyboard_type=ft.KeyboardType.NUMBER
    )

    home_zone_input = ft.TextField(
        label="Zona de Hogar (Rosario)",
        value="Zona Oeste"
    )

    status_text = ft.Text("Estado: Listo para monitorear", size=16, color=ft.colors.GREEN_400)

    def on_profile_change(e):
        engine.profile = "RETURN_HOME" if e.control.value else "STANDARD"
        page.update()

    def on_save(e):
        try:
            engine.fuel_cost = float(fuel_input.value)
            engine.home_zone = home_zone_input.value
            status_text.value = f"Configuración guardada: ${engine.fuel_cost}/km - Modo: {engine.profile}"
            status_text.color = ft.colors.BLUE_400
        except ValueError:
            status_text.value = "Error: Ingrese un valor numérico válido"
            status_text.color = ft.colors.RED_400
        page.update()

    page.add(
        ft.Text("DriverOS Local", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Asistente de rentabilidad para Uber, DiDi y Cabify"),
        ft.Divider(),
        fuel_input,
        home_zone_input,
        ft.Switch(label="Modo Rumbo a Casa (Límite horario)", on_change=on_profile_change),
        ft.ElevatedButton("Guardar Ajustes", on_click=on_save),
        ft.Divider(),
        status_text
    )

if __name__ == "__main__":
    ft.app(target=main)
