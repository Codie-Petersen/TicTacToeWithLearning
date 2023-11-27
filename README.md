# Template ChatGPT Plugin README

This README provides comprehensive documentation for setting up and using the Template ChatGPT Plugin. The template includes essential scripts and files for creating a plugin that can be used with ChatGPT. 

## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)
- [Configuring Your Plugin](#configuring-your-plugin)
  - [ai-plugin.json](#ai-pluginjson)
  - [help.json](#helpjson)
  - [logo.png](#logopng)
  - [openapi.yaml](#openapiyaml)
- [Customizing Your Plugin](#customizing-your-plugin)
  - [info.py](#infopy)
  - [app.py](#apppy)
  - [run_app.py](#run_apppy)
  - [.env](#env)
- [Customizing Routes](#customizing-routes)
  - [Adding Blueprints](#creating-a-new-blueprint-file)
  - [New Blueprint Example](#new-route-example)
  - [ChatGPT Access](#modifying-openapiyaml)
- [Running Your Plugin](#running-your-plugin)
- [Plugin Usage](#plugin-usage)

## Introduction

The Template ChatGPT Plugin is a starting point for creating custom plugins that extend the functionality of ChatGPT. This template provides a structure and essential files to help you create your own ChatGPT plugin.

## Getting Started

### Requirements

Before you begin, ensure you have the following requirements:

- Python 3.7 or higher
- [Quart](https://pgjones.gitlab.io/quart/)
- [Quart-CORS](https://gitlab.com/pgjones/quart-cors)

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Codie-Petersen/AIPluginTemplate
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Configuring Your Plugin

### ai-plugin.json

This file is required by OpenAI and serves as the manifest for your plugin. You need to customize it as follows:

- `name_for_human`: The human-readable name of your plugin.
- `name_for_model`: A short name for your plugin, referenced by the AI.
- `description_for_human`: A user-friendly description of your plugin.
- `description_for_model`: A description of your plugin for the AI.
- `logo_url`: The URL to your plugin's logo image.
- `contact_email`: Your contact email address.
- `legal_info_url`: A URL to legal information related to your plugin.
- Ensure the `auth` and `api` sections match your plugin's requirements.

### help.json

This is a custom file that provides information and instructions about your plugin to the user:

- `instructions`: Instructions displayed to users in Markdown format.
- `functions`: Information about available functions.
- `description`: A brief description of your plugin.
- `creator`: Your name or company name.
- `name`: Your plugin's name.
- `version`: The version number of your plugin.
- `contact`: Your contact email address.

### logo.png

Replace this file with your plugin's logo image. It's referenced in `ai-plugin.json`.

### openapi.yaml

This file defines your plugin's OpenAPI documentation. Customize it as needed:

- `title`: Your plugin's name.
- `description`: A description of your plugin.
- `version`: The version number.
- `servers`: Define the URL where your plugin is hosted.
- Customize the paths, responses, and schemas as per your plugin's functionality.

## Customizing Your Plugin

### info.py

This script defines basic infromation and connectivity routes and functionality of your plugin. You can extend it to include custom routes and functions. You should ensure new functionality is related to generic information about the plugin and the developers.

### app.py

The `App` class initializes your plugin app. Customize it by setting the app name, host, and port. You can also configure CORS settings here. Register custom quart blueprints here that contain your plugin's functionality.

### run_app.py

This script runs your plugin. Customize the app name, CORS settings, and port as needed.

### .env

This file contains environment variables for your plugin:

- `CORS_ON`: Set to `"True"` to enable CORS.
- `CONFIG_ROUTE`: The path to your plugin's configuration files.
- `IS_LOCAL`: Set to `"True"` if your plugin is running locally.
- `PORT`: The port on which your plugin will run.

## Running Your Plugin

To run your plugin, execute the following command:

```bash
python run_app.py
```

This will start your plugin on the specified host and port.

## Customizing Routes

### Creating a New Blueprint File

To add new functionality to your ChatGPT plugin, it's essential to create custom blueprint files within the "routes" directory. These blueprints help organize and modularize your code. To create a new blueprint, follow these steps:

1. **Create a New File**: Start by creating a new Python file in the "routes" directory. Name it descriptively, reflecting the purpose of the functionality you're adding. For example, if you're creating a blueprint for a calculator feature, you might name it "calculator.py."

2. **Import Required Modules**: In your new blueprint file, import the necessary modules, such as "quart" and any other dependencies specific to your functionality. 

3. **Define Your Blueprint**: Create an instance of the `Blueprint` class, as demonstrated in "info.py." This allows you to define routes and associated functions for your new functionality. Customize the blueprint name and CORS settings as needed.

4. **Define Routes**: Within your blueprint, define the routes using `@blueprint.route()`. Each route corresponds to a specific API endpoint and should have an associated function to handle requests.

5. **Implement Functionality**: In each route function, implement the desired functionality. You can interact with data, call external services, or perform any necessary operations. Make sure to return the appropriate response to the client.

6. **Register Your Blueprint**: Finally, register your blueprint in the "app.py" file using `app.register_blueprint(your_blueprint)`. This ensures your routes are accessible through your app.

By following this pattern, you can easily expand your ChatGPT plugin's functionality with new blueprints and routes.

---

### New Route Example

Here's an example "calculator.py" script that would go into the "/plugin/routes" folder:

```python
from quart import Blueprint, request
from plugin.__init__ import CORS_ON, CONFIG_ROUTE, IS_LOCAL, PORT
from quart_cors import cors
import quart

calculator_blueprint = Blueprint("calculator", __name__)

# Enable CORS if configured
if CORS_ON:
    calculator_blueprint = cors(calculator_blueprint, allow_origin="*")

@calculator_blueprint.route("/calculate", methods=["POST"])
async def calculate():
    """
    A route to perform calculations based on user input.
    Example input JSON: {"expression": "2 + 2"}
    """
    try:
        data = await request.get_json()
        expression = data.get("expression")
        if expression is None:
            return quart.Response("Invalid input.", status=400)
        
        result = evaluate_expression(expression)
        return quart.Response(result, status=200)
    except Exception as e:
        return quart.Response(f"Error: {str(e)}", status=500)

def evaluate_expression(expression):
    """A helper function to evaluate mathematical expressions."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return str(e)
```

In this "calculator.py" script, we have created a new blueprint named `calculator_blueprint` for handling calculations. Here's a breakdown of the key components:

- **Blueprint Definition**: We create the `calculator_blueprint` instance.

- **Route Definition**: We define a single route named "/calculate" using `@calculator_blueprint.route()`. This route accepts POST requests to calculate mathematical expressions.

- **Route Function (`calculate()`)**: This function handles incoming POST requests. It expects JSON data with an "expression" field, performs the calculation using the `evaluate_expression()` helper function, and returns the result as a response.

- **Helper Function (`evaluate_expression()`)**: This function evaluates the mathematical expression provided and returns the result.

You can customize this example blueprint to handle various types of calculations or other functionality relevant to your plugin. After creating your "calculator.py" blueprint, you'll need to register it in the "app.py" file to make it accessible within the app. Here's how to do that:

1. **Import the Blueprint**: At the top of your "app.py" file, import the blueprint you created in "calculator.py." It should look something like this:

   ```python
   from plugin.routes.calculator import calculator_blueprint
   ```

   Ensure that the import path matches your directory structure and the name of your blueprint file.

2. **Register the Blueprint**: In the `App` class constructor, register your new blueprint. Locate the `__init__` method in the `App` class and add the following line to register the blueprint:

   ```python
   self.app.register_blueprint(calculator_blueprint)
   ```

   Your `App` class constructor should now look something like this:

   ```python
   class App():
       """Define the app and all of its routes and components."""

       def __init__(self, name=__name__, host="0.0.0.0", port=5000, cors_on=False):
           """Initialize the app."""
           self.app = quart.Quart(name)
           if cors_on:
               self.app = cors(self.app, allow_origin="*")
           self.app.register_blueprint(info)
           self.app.register_blueprint(calculator_blueprint)  # New blueprint.
           self.host = host
           self.port = port
   ```

Now, your "calculator.py" blueprint is registered and accessible within your plugin server. Any routes defined in "calculator.py" can be accessed through the RESTful api. However, you will not be able to access it through ChatGPT until you add it to the OpenAPI specification.

---

### Modifying OpenAPI.yaml

Once you have new routes, you need to add definitions to the "openapi.yaml" file so ChatGPT knows how to access and use it. Here's how:

1. **Open `openapi.yaml`**: First, open your "openapi.yaml" file, which serves as the documentation for your plugin's API.

2. **Add a New Schema Definition for Calculator Response**: Under the `components` section, define a schema for the response of your calculator route. For example (don't duplicate "components" or "schemas"):

   ```yaml
   components:
     schemas:
       CalculatorResponse:
         type: string
         description: The result of the calculation.
   ```

   - `CalculatorResponse`: This is the name of your schema for the calculator response.
   - `type: string`: Indicates that the schema represents a string.
   - `description`: Provides a brief description of the result.

3. **Add a New Path**: To add a new route, you need to define a new path under the `paths` section of the YAML file. The path should start with a forward slash ("/") and reflect the endpoint you want to document and created in "calculator.py" blueprint routes. For example, if your new route is "/calculate," add the following lines (don't duplicate "paths"):

   ```yaml
   paths:
     /calculate:
       post:
         operationId: calculate
         summary: Perform a calculation.
         requestBody:
           required: true
           content:
             application/json:
               schema:
                 type: string
         responses:
           "200":
             description: OK
             content:
               application/json:
                 schema:
                   $ref: "#/components/schemas/CalculatorResponse"
           "400":
             description: Bad Request
           "500":
             description: Internal Server Error
   ```

   - `operationId`: This should match the operation name you use in your route function in "calculator.py."
   - `summary`: A brief description of what the route does.
   - `requestBody`: Defines the expected request body format. In this example, it expects a string.
   - `responses`: Defines possible responses with descriptions and content types.
   - `schema: $ref`: Use `$ref` to reference the schema you defined earlier. The `#` symbol signifies that the reference is within the same document, followed by the path to the schema ("CalculatorResponse" in this case).
   

4. **Save and Close**: Save your changes to the "openapi.yaml" file.

Now, you've added a schema definition for the calculator route's response and referenced it within the path definition. This ensures that your API documentation accurately describes the structure of responses from the "/calculate" endpoint, making it possible for ChatGPT to access your new functionality.


## Plugin Usage

Once your plugin is running, it can be accessed by other applications or services using its defined routes. Refer to your `openapi.yaml` for API documentation.
