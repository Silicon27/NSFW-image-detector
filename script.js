const fs = require('fs');
const http = require('http');
const FormData = require('form-data');

const image = fs.readFileSync('/path/to/image.png'); 

// Encode the image to base64
const base64Image = Buffer.from(image).toString('base64');

const form = new FormData();
form.append('file', base64Image, { filename: 'me.jpg' });

const options = {
  hostname: 'localhost',
  port: 5000,
  path: '/', 
  method: 'POST',
  headers: form.getHeaders(),
};

// Make the POST request
const req = http.request(options, (res) => {
  console.log(`statusCode: ${res.statusCode}`);
  
  res.on('data', (data) => {
    console.log(data.toString());
  });
});

req.on('error', (error) => {
  console.error(error);
});


form.pipe(req);


