from agent import get_weather_stateful

class DummyToolContext:
    def __init__(self, state=None):
        self.state = state or {}

def test_weather_known_city_celsius():
    ctx = DummyToolContext({"user_preference_temperature_unit": "Celsius"})
    result = get_weather_stateful("New York", ctx)
    assert result["status"] == "success"
    assert "25°C" in result["report"]
    print("test_weather_known_city_celsius passed.")

def test_weather_known_city_fahrenheit():
    ctx = DummyToolContext({"user_preference_temperature_unit": "Fahrenheit"})
    result = get_weather_stateful("London", ctx)
    assert result["status"] == "success"
    assert "59°F" in result["report"]
    print("test_weather_known_city_fahrenheit passed.")

def test_weather_unknown_city():
    ctx = DummyToolContext({"user_preference_temperature_unit": "Celsius"})
    result = get_weather_stateful("Paris", ctx)
    assert result["status"] == "error"
    assert "Paris" in result["error_message"]
    print("test_weather_unknown_city passed.")

def test_weather_default_unit():
    ctx = DummyToolContext({})
    result = get_weather_stateful("Tokyo", ctx)
    assert result["status"] == "success"
    assert "18°C" in result["report"]
    print("test_weather_default_unit passed.")

if __name__ == "__main__":
    test_weather_known_city_celsius()
    test_weather_known_city_fahrenheit()
    test_weather_unknown_city()
    test_weather_default_unit()
    print("All mock weather tests passed.") 