from datetime import datetime
from googletrans import Translator
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

# Initialize the translator
translator = Translator()

# Define the locations (latitude, longitude) for each clinic in Pune
locations = {
    'A': (18.5204, 73.8567),
    'B': (18.5091, 73.8854),
    'C': (18.5058, 73.8701),
    'D': (18.5316, 73.8567),
    'E': (18.5023, 73.8867),
    'F': (18.4631, 73.8496),
    'G': (18.5416, 73.8017),
    'H': (18.5258, 73.8102),
    'I': (18.5200, 73.8477),
    'J': (18.5324, 73.8603)
}
languages = {
    '1': {'code': 'en', 'greeting': "Welcome to Health Resource Locator"},
    '2': {'code': 'hi', 'greeting': "हेल्थ रिसोर्स लोकेटर में आपका स्वागत है"},  # Hindi
    '3': {'code': 'mr', 'greeting': "हेल्थ रिसोर्स लोकेटरमध्ये आपले स्वागत आहे"},  # Marathi
    '4': {'code': 'pa', 'greeting': "ਹੈਲਥ ਰਿਸੋਰਸ ਲੋਕੇਟਰ ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ"},  # Punjabi
    '5': {'code': 'ml', 'greeting': "ഹെൽത്ത് റിസോഴ്‌സ് ലോക്കേറ്ററിൽ സ്വാഗതം"},  # Malayalam
    '6': {'code': 'bn', 'greeting': "হেলথ রিসোর্স লোকেটরে আপনাকে স্বাগতম"},  # Bengali
    '7': {'code': 'te', 'greeting': "హెల్త్ రిసోర్స్ లోకేటర్‌లో స్వాగతం"},  # Telugu
    '8': {'code': 'as', 'greeting': "স্বাস্থ্য উৎস লোকেটৰত আপোনাক স্বাগতম"},  # Assamese
    '9': {'code': 'ur', 'greeting': "ہیلتھ ریسورس لوکیٹر میں خوش آمدید"},  # Urdu
    '10': {'code': 'ta', 'greeting': "ஹெல்த் ரிசோர்ஸ் லொக்கேட்டரின் வரவேற்கின்றேன்"},  # Tamil
}

# Define clinic details (name, services, cost, rating, hours)
places = {
    'A': [
        {"name": "Green Valley Clinic", "services": ["General Medicine", "Dentistry"], "cost": 2000, "rating": 4.5, "hours": "8 AM - 8 PM"},
        {"name": "Sunrise Health Center", "services": ["Orthopedics", "Dermatology"], "cost": 2500, "rating": 4.3, "hours": "9 AM - 9 PM"},
        {"name": "Apex Pharmacy", "services": ["Prescription Medicines", "Immunizations"], "cost": 500, "rating": 4.7, "hours": "8 AM - 10 PM"},
        {"name": "Alpha Diagnostics", "services": ["Blood Tests", "MRI Scans"], "cost": 3000, "rating": 4.6, "hours": "7 AM - 8 PM"},
    ],
    'B': [
        {"name": "Blue Cross Clinic", "services": ["Pediatrics", "General Medicine"], "cost": 1800, "rating": 4.2, "hours": "8 AM - 8 PM"},
        {"name": "Healing Hands", "services": ["Gynecology", "Physiotherapy"], "cost": 3000, "rating": 4.6, "hours": "9 AM - 7 PM"},
        {"name": "Wellness Pharmacy", "services": ["Health Supplements", "Medication Refills"], "cost": 400, "rating": 4.7, "hours": "8 AM - 10 PM"},
        {"name": "Prime Diagnostics", "services": ["X-ray", "Ultrasound"], "cost": 2500, "rating": 4.4, "hours": "7 AM - 7 PM"},
    ],
    'C': [
        {"name": "Care First Clinic", "services": ["Cardiology", "Dermatology"], "cost": 1500, "rating": 4.1, "hours": "8 AM - 8 PM"},
        {"name": "Wellness Center", "services": ["General Medicine", "Dentistry"], "cost": 2000, "rating": 4.3, "hours": "9 AM - 9 PM"},
        {"name": "CityMed Pharmacy", "services": ["OTC Medicines", "Vaccinations"], "cost": 600, "rating": 4.6, "hours": "8 AM - 10 PM"},
        {"name": "QuickCheck Diagnostics", "services": ["COVID-19 Tests", "ECG"], "cost": 2000, "rating": 4.5, "hours": "7 AM - 7 PM"},
        {"name": "Flex Rehab", "services": ["Physiotherapy", "Neurological Rehabilitation"], "cost": 3400, "rating": 4.7, "hours": "8 AM - 6 PM"},
    ],
    'D': [
        {"name": "City Health Hub", "services": ["Orthopedics", "General Medicine"], "cost": 1800, "rating": 4.2, "hours": "8 AM - 8 PM"},
        {"name": "Advanced Care Clinic", "services": ["Cardiology", "Dermatology"], "cost": 1400, "rating": 4.3, "hours": "9 AM - 7 PM"},
        {"name": "HealthHub Pharmacy", "services": ["Compounding", "Health Check Supplies"], "cost": 700, "rating": 4.6, "hours": "8 AM - 10 PM"},
        {"name": "Precision Diagnostics", "services": ["CT Scans", "Allergy Testing"], "cost": 3500, "rating": 4.7, "hours": "7 AM - 7 PM"},
    ],
    'E': [
        {"name": "Medicare Clinic", "services": ["Pediatrics", "Cardiology"], "cost": 1800, "rating": 4.2, "hours": "8 AM - 8 PM"},
        {"name": "Bright Future Health Center", "services": ["Physiotherapy", "General Medicine"], "cost": 2000, "rating": 4.3, "hours": "9 AM - 6 PM"},
        {"name": "SmartMed Pharmacy", "services": ["OTC Medicines", "Vaccinations"], "cost": 600, "rating": 4.6, "hours": "8 AM - 10 PM"},
        {"name": "Instant Diagnostics", "services": ["Blood Tests", "MRI Scans"], "cost": 2500, "rating": 4.4, "hours": "7 AM - 7 PM"},
    ]
}

# Define distances between locations (example distances)
distances = {
    'A': {'B': 3.0, 'C': 2.5, 'D': 1.2, 'E': 4.5, 'F': 5.1, 'G': 7.2, 'H': 6.3, 'I': 0.9, 'J': 1.5},
    'B': {'A': 3.0, 'C': 1.0, 'D': 2.8, 'E': 0.7, 'F': 4.6, 'G': 5.3, 'H': 4.2, 'I': 2.3, 'J': 2.6},
    'C': {'A': 2.5, 'B': 1.0, 'D': 1.7, 'E': 1.4, 'F': 4.0, 'G': 5.7, 'H': 4.6, 'I': 2.0, 'J': 1.8},
    'D': {'A': 1.2, 'B': 2.8, 'C': 1.7, 'E': 3.2, 'F': 5.0, 'G': 6.5, 'H': 5.6, 'I': 0.5, 'J': 1.3},
    'E': {'A': 4.5, 'B': 0.7, 'C': 1.4, 'D': 3.2, 'F': 4.1, 'G': 5.4, 'H': 4.7, 'I': 3.9, 'J': 2.4},
    'F': {'A': 5.1, 'B': 4.6, 'C': 4.0, 'D': 5.0, 'E': 4.1, 'G': 4.6, 'H': 3.3, 'I': 4.8, 'J': 4.9},
    'G': {'A': 7.2, 'B': 5.3, 'C': 5.7, 'D': 6.5, 'E': 5.4, 'F': 4.6, 'H': 3.1, 'I': 7.6, 'J': 6.2},
    'H': {'A': 6.3, 'B': 4.2, 'C': 4.6, 'D': 5.6, 'E': 4.7, 'F': 3.3, 'G': 3.1, 'I': 6.5, 'J': 5.1},
    'I': {'A': 0.9, 'B': 2.3, 'C': 2.0, 'D': 0.5, 'E': 3.9, 'F': 4.8, 'G': 7.6, 'H': 6.5, 'J': 1.0},
    'J': {'A': 1.5, 'B': 2.6, 'C': 1.8, 'D': 1.3, 'E': 2.4, 'F': 4.9, 'G': 6.2, 'H': 5.1, 'I': 1.0}
}

# Dijkstra's Algorithm to find the shortest path from the current location
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = {node: False for node in graph}
    path = {}
    unvisited_nodes = list(graph.keys())

    while unvisited_nodes:
        min_node = None
        for node in unvisited_nodes:
            if min_node is None:
                min_node = node
            elif distances[node] < distances[min_node]:
                min_node = node

        for neighbor, weight in graph[min_node].items():
            if not visited[neighbor]:
                new_dist = distances[min_node] + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    path[neighbor] = min_node

        visited[min_node] = True
        unvisited_nodes.remove(min_node)

    return distances

# Check if the clinic is open at the desired time
def is_clinic_open(clinic_hours, visit_time):
    open_time, close_time = clinic_hours.split(" - ")
    open_time = datetime.strptime(open_time, "%I %p")
    close_time = datetime.strptime(close_time, "%I %p")
    return open_time <= visit_time <= close_time

def filter_clinics(places, reachable_places, max_cost=None, services=None, min_rating=None, visit_time=None):
    results = []
    if services:
        services = [service.lower() for service in services]  # Convert services to lowercase
    for place in reachable_places:
        if place in places:
            for clinic in places[place]:
                clinic_services = [s.lower() for s in clinic["services"]]
                clinic_rating = clinic.get("rating", 0)
                # Check if the clinic meets all the filter criteria
                if (max_cost is None or clinic["cost"] <= max_cost) and \
                   (services is None or any(service in clinic_services for service in services)) and \
                   (min_rating is None or clinic_rating >= min_rating):
                    clinic["distance"] = reachable_places[place]
                    if visit_time:
                        clinic_open_status = is_clinic_open(clinic["hours"], visit_time)
                        clinic["status"] = "Open" if clinic_open_status else "Closed"
                    clinic["lat"] = locations[place][0]
                    clinic["lon"] = locations[place][1]
                    results.append(clinic)
    return results

# Display the filtered results
def display_clinics(filtered_clinics):
    if not filtered_clinics:
        if selected_language != 'en':
            print(translate_text("No clinics match your criteria.",selected_language,languages))
        else:
            print("No clinics match your criteria.")
    else:
        for clinic in filtered_clinics:
            if selected_language !='en':
                st = translate_text("Name: ",selected_language,languages)
                st1 = translate_text(str(clinic['name']))
                print(st + st1)
                st = translate_text("Services:",selected_language,languages)
                st1 = translate_text(', '.join(clinic['services']))
                print(st + st1)
                st = translate_text("Cost: ",selected_language,languages)
                st1 = translate_text(str(clinic['cost']))
                print(st + st1)
                st = translate_text("Hours: ",selected_language,languages)
                st1 = translate_text(str(clinic['hours']))
                print(st + st1)
                st = translate_text("Rating: ",selected_language,languages)
                st1 = translate_text(str(clinic["rating"]))
                print(st + st1)
                st = translate_text("Distance: ",selected_language,languages)
                st1 = translate_text(str(clinic['distance']))
                print(st + st1)
                st = translate_text("Status: ",selected_language,languages)
                st1 = translate_text(str(clinic.get('status', 'N/A')))
                print(st + st1)
                print("------------------------------")
            else:
                print(f"Name: {clinic['name']}")
                print(f"Services: {', '.join(clinic['services'])}")
                print(f"Cost: {clinic['cost']}")
                print(f"Hours: {clinic['hours']}")
                print(f"Rating: {clinic['rating']}")
                print(f"Distance: {clinic['distance']} km")
                print(f"Status: {clinic.get('status', 'N/A')}")
                print("------------------------------")

# Function to translate text
def translate_text(text,selected_language_code,languages):
    global selected_language
    for key, value in languages.items():
        if value['code'] == selected_language_code:
            target_language = value['code']
            break
    else:
        # Default to English if no match is found
        target_language = 'en'
    
    # Translate the text
    translated = translator.translate(text, src='en', dest=target_language)
    return translated.text

# Function to generate the map
def generate_map(filtered_clinics, user_location):
    if not filtered_clinics:
        print("No clinics to display on the map.")
        return

    # Create a folium map centered in Pune
    pune_map = folium.Map(location=[18.5204, 73.8567], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(pune_map)

    # Mark the user's location with a red pin
    folium.Marker(
        location=user_location,
        popup="Your Location",
        icon=folium.Icon(color="red")
    ).add_to(pune_map)

    for clinic in filtered_clinics:
        popup_message = ""
        if selected_language != 'en':
            for key, value in clinic.items():
                if key != 'lat' and key != 'lon':
                    popup_message += f"<b>{translate_text(key,selected_language,languages)}:</b> {translate_text(str(value),selected_language,languages)}<br>"
        else:
            for key, value in clinic.items():
                if key != 'lat' and key != 'lon':
                    popup_message += f"<b>{key}:</b> {value}<br>"

        folium.Marker(
            location=[clinic['lat'], clinic['lon']],
            popup=folium.Popup(popup_message, max_width=300),  # Increase popup width
            icon=folium.Icon(color="blue")
        ).add_to(marker_cluster)

        # Draw a line from the user's location to the clinic
        folium.PolyLine(
            locations=[user_location, [clinic['lat'], clinic['lon']]],
            color="blue",
            weight=2.5,
            opacity=1
        ).add_to(pune_map)

    # Save the map as an HTML file
    pune_map.save("clinics_map.html")
    print("Map has been saved as 'clinics_map.html'.")
# Main program
def main():
    global selected_language

    print("Welcome to the Health Resource Locator!")
    language = input("Select your language: \n1. English\n2. Hindi\n3. Marathi\n4. Punjabi\n5. Malyalam\n6. Bengali\n7. Telugu\n8. Assamese\n9. Urdu\n10. Tamil")
    

    
    if language in languages:
    # Set selected_language to the code of the chosen language
      selected_language = languages[language]['code'] 
      print(languages[language]['greeting'])
    else:
      print("Invalid choice, defaulting to English.")
      selected_language = 'en'


    if selected_language != 'en':
        st = translate_text("Enter your current location",selected_language,languages)
        user_location = input(st+" (A-J):").upper()
    else:
        user_location = input("Enter your current location (A-J): ").upper()
    if user_location not in distances:
        if selected_language != 'en':
            st = translate_text("Invalid location. Exiting program.",selected_language,languages)
            print(st)
        else:
            print("Invalid location. Exiting program.")
        return

    reachable_places = dijkstra(distances, user_location)

    # Remove the user's location from the reachable places
    reachable_places.pop(user_location, None)
    try:
        if selected_language != 'en':
            st = translate_text("Enter your maximum budget (or press Enter to skip): ",selected_language,languages)
            max_cost = int(input(st) or 0)
        else:
            max_cost = int(input("Enter your maximum budget (or press Enter to skip): ") or 0)
    except ValueError:
        max_cost = None

    # Extract all unique services from the places dictionary
    all_services = set()
    for city, facilities in places.items():
        for facility in facilities:
            all_services.update(facility["services"])

    # Display services and take input
    if(selected_language=='hi'):
         print(translate_text("Available services:",selected_language,languages))
    else:
     print("Available services:")
    for idx, service in enumerate(sorted(all_services), 1):
        if selected_language != 'en':
            print(f"{idx}. {translate_text(service,selected_language,languages)}")
        else:
            print(f"{idx}. {service}")
    if(selected_language=='hi'):
        selected_services_input = input(translate_text("Enter the numbers corresponding to the services you are looking for (comma separated): ",selected_language,languages))
    else:
     selected_services_input = input("Enter the numbers corresponding to the services you are looking for (comma separated): ")
    try:
        selected_service_indices = [int(x) - 1 for x in selected_services_input.split(',')]
        selected_services = [sorted(all_services)[i] for i in selected_service_indices]
        if selected_language != 'en':
            print(translate_text("You selected:",selected_language,languages)+', '.join(translate_text(service,selected_language,languages) for service in selected_services))
        else:
            print(f"You selected: {', '.join(selected_services)}")
    except (IndexError, ValueError):
        if selected_language != 'en':
            print(translate_text("Invalid service selection. Proceeding without a specific service filter.",selected_language,languages))
        else:
            print("Invalid service selection. Proceeding without a specific service filter.")
        selected_services = None

        # Get maximum distance
    try:
        if selected_language != 'en':
            st = translate_text("Enter maximum distance (in km, or press Enter to skip): ",selected_language,languages)
            max_distance = float(input(st) or float('inf'))
        else:
            max_distance = float(input("Enter maximum distance (in km, or press Enter to skip): ") or float('inf'))
        if max_distance < 0:
            if selected_language != 'en':
                raise ValueError(translate_text("Distance cannot be negative.",selected_language,languages))
            else:
                raise ValueError("Distance cannot be negative.")
    except ValueError:
        if selected_language != 'en':
            print(translate_text("Invalid input for distance. Defaulting to no distance limit.",selected_language,languages))
        else:
            print("Invalid input for distance. Defaulting to no distance limit.")
        max_distance = float('inf')

    # Get minimum rating
    try:
        if selected_language != 'en':
            min_rating = float(input(translate_text("Enter minimum rating (0-5, or press Enter to skip): ",selected_language,languages)) or 0)
        else:
            min_rating = float(input("Enter minimum rating (0-5, or press Enter to skip): ") or 0)
        if not (0 <= min_rating <= 5):
            if selected_language != 'en':
                raise ValueError(translate_text("Rating must be between 0 and 5.",selected_language,languages))
            else:
                raise ValueError("Rating must be between 0 and 5.")
    except ValueError:
        if selected_language != 'en':
            print(translate_text("Invalid input for rating. Defaulting to no rating filter.",selected_language,languages))
        else:
            print("Invalid input for rating. Defaulting to no rating filter.")
        min_rating = 0

    # Get visit time
    if selected_language != 'en':
        visit_time_input = input(translate_text("Enter your desired visit time (e.g., '10 AM', '2 PM'): ",selected_language,languages))
    else:
        visit_time_input = input("Enter your desired visit time (e.g., '10 AM', '2 PM'): ")
    try:
        visit_time = datetime.strptime(visit_time_input, "%I %p")
    except ValueError:
        if selected_language != 'en':
            print(translate_text("Invalid time format. Proceeding without time filter.",selected_language,languages))
        else:
            print("Invalid time format. Proceeding without time filter.")
        visit_time = None

    # Filter reachable places by distance
    reachable_places = {place: dist for place, dist in reachable_places.items() if dist <= max_distance}

    # Filter clinics based on criteria
    filtered_clinics = filter_clinics(
        places,
        reachable_places,
        max_cost=max_cost,
        services=selected_services,
        min_rating=min_rating,
        visit_time=visit_time
    )

    # Display filtered clinics
    if selected_language != 'en':
        print(translate_text("Here are the clinics that match your criteria:",selected_language,languages))
    print("\n--- Results ---")
    display_clinics(filtered_clinics)

    # Generate the map with the shortlisted clinics
    generate_map(filtered_clinics, locations[user_location])

if __name__ == "__main__":
    main()