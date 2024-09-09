import json

# Load the JSON file
with open('my_er_diagram.json', 'r') as file:
    data = json.load(file)

# Filter the JSON for a specific app
filtered_data = {
    'graphs': [
        app for app in data['graphs']
        if app['app_name'] == 'dump_data'
    ]
}

# Save the filtered JSON
with open('filtered_app.json', 'w') as file:
    json.dump(filtered_data, file, indent=4)
