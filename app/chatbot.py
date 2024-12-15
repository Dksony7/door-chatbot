import openai
import requests

# Set OpenAI API key
openai.api_key = "sk-svcacct-BtC1ulRO0lz3eK59g57OdROngIgfIZRPoDCalOUv6636dycRrs0G3B2FPrsT3BlbkFJS9HeMZfgCTpkIu1EJ-e2Cj-xoGtcQ84VE3pAcLSqV2pw8ArxDGC_SEKMcDQA"

# Function to fetch door details based on size
def get_door_details(size):
    try:
        response = requests.get(f"https://door-chatbot9oloollloololiiiool-ill.onrender.com/doors/{size}")
        if response.status_code != 200:
            return "Sorry, could not fetch the door details."

        data = response.json()
        if "details" not in data:
            return f"Size {size} ke liye koi door available nahi hai."

        message = f"Size {size} ke available doors:\n"
        for door_type, designs in data["details"].items():
            message += f"\nType: {door_type.capitalize()}\n"
            for design in designs:
                message += (
                    f"- Design: {design['design']}, Stock: {design['stock']}\n"
                    f"Image: {design['image_path']}\n\n"
                )
        return message.strip()  # Remove any trailing whitespace

    except Exception as e:
        return f"Error fetching door details: {e}"

# Main chatbot response function
def chatbot_response(user_query):
    try:
        # Check if the user query includes a size specification
        if "size" in user_query.lower():
            size = user_query.split()[-1].replace("×", "x")  # Format size correctly
            return get_door_details(size)

        # Generate a response using OpenAI's ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a multilingual assistant. Answer in the language of the user."},
                {"role": "user", "content": user_query},
            ]
        )
        return response.choices[0].message["content"]

    except Exception as e:
        return f"Error in generating response:\n\n{e}"

# Example usage
if __name__ == "__main__":
    user_query = input("Aapka sawaal: ")
    print(chatbot_response(user_query))
