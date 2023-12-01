// Install the mysql library by running: npm install mysql
const mysql = require('mysql');
const express = require('express');
const app = express();

// Create a MySQL connection
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'your_username',
  password: 'your_password',
  database: 'your_database'
});

// Connect to the MySQL server
connection.connect();

// Run the query
const query = 'SELECT * FROM your_table';
connection.query(query, (error, results) => {
  if (error) throw error;

  // Display the result table
  console.table(results);

  // Create a chart using the results
  // You can use any charting library of your choice, such as Chart.js or Google Charts
  // Here's an example using Chart.js:
  const labels = results.map(row => row.label);
  const data = results.map(row => row.value);

  const ctx = document.getElementById('chart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Chart',
        data: data,
        backgroundColor: 'rgba(0, 123, 255, 0.5)'
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
});

// Start the server
app.listen(3000, () => {
  console.log('Server is running on port 3000');
});