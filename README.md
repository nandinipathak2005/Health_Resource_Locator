# Health Resource Locator

A console-based multilingual application designed to enhance accessibility to affordable healthcare services. This tool leverages graph algorithms to help users locate hospitals and clinics offering quality care at minimal costs, with customizable filtering options to meet individual needs.

## 🌟 Features
- **Multilingual Support**: Available in multiple languages to cater to diverse user groups.
- **Optimized Pathfinding**: Uses graph algorithms to find the nearest and most affordable healthcare services.
- **Customizable Filters**: Users can filter results based on multiple criteria such as:
  - **Budget Range**: Find healthcare services within a specific cost range.
  - **Proximity**: Locate hospitals and clinics closest to the user’s location.
  - **Available Services**: Filter by specific healthcare services (e.g., emergency care, pediatrics, etc.).
  - **Ratings**: Sort healthcare providers based on user ratings or overall reputation.
  - **Working Hours**: Find services that are open during preferred hours or days.
- **User-Centric Design**: Specifically aimed at helping low-income individuals find affordable and quality healthcare options.
- **Improves Healthcare Accessibility**: Bridges the gap between underserved communities and necessary healthcare services.
- **Map Integration**: Visualize healthcare providers' locations on a map using `folium`.

## 💡 Inspiration
Healthcare services are often difficult to access for low-income communities due to distance, cost, and lack of information. This application empowers users to make informed decisions by offering a comprehensive, easy-to-use tool for locating affordable and quality healthcare services based on personal preferences.

## 🚀 How It Works (with Map Integration)

1. **Input**:
   - The user provides their location, preferred language, and any filters they want to apply (budget, proximity, services, ratings, etc.).
   - Hardcoded locations for hospitals and clinics are used for now.

2. **Processing**:
   - The application uses graph algorithms (like **Dijkstra’s Algorithm**) to calculate the most efficient and affordable paths to healthcare services.
   - Filters are applied based on the user’s preferences to narrow down the results.
   - **Map Generation**: Using the `folium` library, the application creates a map with the healthcare providers' locations.

3. **Output**:
   - Displays a list of healthcare providers that match the criteria, sorted by distance, cost, or ratings as specified.
   - Generates a map to visualize the healthcare providers' locations.

## 🛠️ Technologies Used
- **Programming Language**: Python
- **Graph Algorithms**: Dijkstra’s Algorithm .
- **Multilingual Implementation**: Google Translate API.
- **Data Structures**: Graphs,Dictionaries,Lists.
- **Map Generation**: **`folium`** library for displaying healthcare provider locations on an interactive map.



