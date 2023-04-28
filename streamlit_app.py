<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Streamline App</title>
    <style>
      /* Style the form */
      form {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 50px;
      }
      
      input[type="text"] {
        padding: 10px;
        margin-bottom: 20px;
        width: 300px;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
      }
      
      input[type="submit"] {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }
      
      input[type="submit"]:hover {
        background-color: #45a049;
      }
    </style>
  </head>
  <body>
    <h1>Streamline App</h1>
    <form>
      <label for="api-key">API Key:</label>
      <input type="text" id="api-key" name="api-key" placeholder="Enter your API key">
      <label for="url">URL:</label>
      <input type="text" id="url" name="url" placeholder="Enter a URL">
      <input type="submit" value="Submit">
    </form>
    
    <script>
      // Get the form element and add an event listener for form submission
      const form = document.querySelector('form');
      form.addEventListener('submit', handleSubmit);
      
      // Define the handleSubmit function
      function handleSubmit(event) {
        // Prevent the default form submission behavior
        event.preventDefault();
        
        // Get the values from the API key and URL input fields
        const apiKey = document.getElementById('api-key').value;
        const url = document.getElementById('url').value;
        
        // Use the values to make an API request or perform some other action
        console.log(apiKey, url);
      }
    </script>
  </body>
</html>
