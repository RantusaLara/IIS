const http = require('http');
const fs = require('fs');
const { spawn } = require('child_process');
const filePath = __dirname + '/front-end.html';

const server = http.createServer((req, res) => {
  if (req.url === '/') {
    // Read the HTML file and send it as the response
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(500);
        res.end('Error loading index.html');
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(data);
      }
    });
  } else {
    // Handle other requests
    res.writeHead(404);
    res.end('Page not found');
  }
});

server.listen(3000, () => {
  console.log('Server listening on port 3000');
});
