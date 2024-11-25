from scraper import LieferandoAPI
import logging

if __name__ == "__main__":
    try:
        api = LieferandoAPI(delay_seconds=2.0)
        address = "Abt Rudolf Strasse 43, 73479 Ellwangen"

        result = api.get_restaurants_by_address(address)
        filename = api.save_response(result, address)

        print(f"Successfully retrieved and saved data for {address}")
        print(f"Response keys: {result.keys()}")
        print(f"Data saved to: {filename}")

    except Exception as e:
        logging.error(f"Error in main: {str(e)}", exc_info=True)