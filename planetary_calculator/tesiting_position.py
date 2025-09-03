# demo_runner.py

from planetary_calculator import calculate_planetary_positions


def main():
    # Dummy input values
    birth_year = "1990"
    birth_month = "5"
    birth_day = "15"
    birth_hour = "14"
    birth_minute = "30"
    district = "Mumbai"
    state = "Maharashtra"
    country = "India"
    user_name = "TestUser"

    # Call planetary position calculation
    result = calculate_planetary_positions(
        birth_year,
        birth_month,
        birth_day,
        birth_hour,
        birth_minute,
        district,
        state,
        country,
        user_name
    )

    # Print results
    if result["success"]:
        print(f"\n✅ Planetary positions for {user_name} ({result['location']})")
        print(f"📍 Coordinates: {result['coordinates']}\n")
        for position in result["positions"]:
            print(position)
    else:
        print(f"\n❌ Error: {result['error']}")

if __name__ == "__main__":
    main()
