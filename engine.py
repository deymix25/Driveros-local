import re
from dataclasses import dataclass

@dataclass
class ParsedOffer:
    app_name: str
    raw_fare: float
    pickup_km: float
    trip_km: float
    duration_min: float
    destination_str: str

class DriverEngine:
    def __init__(self, fuel_cost_per_km: float, home_zone: str = "Zona Oeste"):
        self.fuel_cost = fuel_cost_per_km
        self.home_zone = home_zone
        self.profile = "STANDARD" # "STANDARD" o "RETURN_HOME"

    def evaluate_offer(self, offer: ParsedOffer) -> dict:
        total_km = offer.pickup_km + offer.trip_km
        total_time_hr = offer.duration_min / 60.0 if offer.duration_min > 0 else 0.25
        
        gross_ars = offer.raw_fare
        fuel_expense = total_km * self.fuel_cost
        net_ars = gross_ars - fuel_expense
        
        ars_per_km = net_ars / total_km if total_km > 0 else 0
        ars_per_hr = net_ars / total_time_hr if total_time_hr > 0 else 0

        # Regla base: Margen rentable (ej. mayor a 400 ARS/km netos)
        is_viable = (ars_per_km >= 400) and (offer.pickup_km <= 3.5)

        # Regla: Rumbo a Casa (Evalua si el destino coincide con la zona del hogar en Rosario)
        if self.profile == "RETURN_HOME":
            if self.home_zone.lower() in offer.destination_str.lower():
                return {
                    "status": "GREEN_HOME",
                    "ars_km": round(ars_per_km, 2),
                    "ars_hr": round(ars_per_hr, 2),
                    "app": offer.app_name
                }

        status = "GREEN" if is_viable else "RED"
        return {
            "status": status,
            "ars_km": round(ars_per_km, 2),
            "ars_hr": round(ars_per_hr, 2),
            "app": offer.app_name
        }

class OfferParser:
    @staticmethod
    def parse_nodes(app_name: str, text_nodes: list) -> ParsedOffer:
        fare = 0.0
        pickup_km = 0.0
        trip_km = 0.0
        duration = 0.0
        dest_parts = []

        for text in text_nodes:
            t = str(text).strip()
            if "$" in t or "ARS" in t:
                match = re.search(r'[\$]?\s?(\d+[\.,]?\d*)', t)
                if match:
                    try:
                        fare = float(match.group(1).replace('.', '').replace(',', '.'))
                    except ValueError:
                        pass
            elif "km" in t.lower():
                match = re.search(r'(\d+[\.,]?\d*)\s?km', t, re.IGNORECASE)
                if match:
                    val = float(match.group(1).replace(',', '.'))
                    if pickup_km == 0.0:
                        pickup_km = val
                    else:
                        trip_km = val
            elif "min" in t.lower():
                match = re.search(r'(\d+)\s?min', t, re.IGNORECASE)
                if match:
                    duration = float(match.group(1))
            elif any(zone in t for zone in ["Centro", "Norte", "Sur", "Oeste", "Fisherton", "Funes", "Garay"]):
                dest_parts.append(t)

        return ParsedOffer(
            app_name=app_name,
            raw_fare=fare,
            pickup_km=pickup_km,
            trip_km=trip_km,
            duration_min=duration,
            destination_str=" ".join(dest_parts)
        )
