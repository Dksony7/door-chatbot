import openai
import requests
import re

# OpenAI API key
openai.api_key = "wBjYlt1APOeDrYcIQyNjrTAV"  # Replace with your actual key

# Function to fetch door details.  Improved error handling and input validation.
def get_door_details(size_str):
    try:
        # Regular expression to extract dimensions (handles various formats)
        match = re.match(r"(\d+(\.\d+)?)\s*[x×]\s*(\d+(\.\d+)?)", size_str, re.IGNORECASE)
        if not match:
            return "Invalid size format. Please use a format like 'width x height' (e.g., '32 x 80')."

        width, height = float(match.group(1)), float(match.group(3))

        response = requests.get(f"https://door-chatbot9oloollloololiiiool-ill.onrender.com/doors/{width}x{height}")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        if not data.get("details"):
            return f"No doors found for size {width}x{height}."

        message = f"Available doors for size {width}x{height}:\n"
        for door_type, designs in data["details"].items():
            message += f"\nType: {door_type.capitalize()}\n"
            for design in designs:
                message += (
                    f"- Design: {design['design']}, Stock: {design['stock']}\n"
                    f"Image: {design['image_path']}\n\n"
                )
        return message

    except requests.exceptions.RequestException as e:
        return f"Error fetching door details: {e}"
    except (KeyError, ValueError) as e:
        return f"Error processing door data: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# Chatbot response function.  Improved error handling and language handling.
def chatbot_response(user_query):
    try:
        # Handle door size queries using regular expression for robustness.
        size_match = re.search(r"(\d+(\.\d+)?)\s*[x×]\s*(\d+(\.\d+)?)", user_query, re.IGNORECASE)
        if size_match:
            size_str = size_match.group(0)
            return get_door_details(size_str)


        # OpenAI ChatCompletion response with improved system prompt for better language handling.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", #Consider using gpt-3.5-turbo for cost-effectiveness
            messages=[
                {"role": "system", "content": "You are a helpful assistant.  Respond in the user's language if possible. If you don't understand, politely ask for clarification."},
                {"role": "user", "content": user_query},
            ],
            temperature = 0.7 # Adjust as needed for creativity vs. accuracy
        )
        return response.choices[0].message["content"]

    except openai.error.OpenAIError as e:
        return f"Error communicating with OpenAI: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# Example usage
user_input = input("Ask me something: ")
print(chatbot_response(user_input))
            
