const express = require('express');
const multer = require('multer');
const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');
const path = require('path');
const { url } = require('inspector');

// Set up storage options for multer
const storage = multer.memoryStorage(); // Stores files in memory
const upload = multer({ storage: storage });

class ParseController {
    constructor() {}

    copyFile = async (req, res) => {
        upload.single('file')(req, res, async (err) => {
            // Using multer middleware to handle file upload
            const file = req.file;
            
            if (!file) {
                console.error('No file uploaded');
                return res.status(400).send('No file uploaded');
            }

            // Create a FormData object to send the file as multipart/form-data
            const formData = new FormData();

            try {
                axios.post('http://parser:65432/process', req.file.buffer, {
                    headers: {
                        'Content-Type': 'application/octet-stream', // or the specific file MIME type
                    }
                })
                .then((response) => {
                    console.log('Response from python:', response.data);
                    res.status(200).send(response.data);
                })
                .catch((error) => {
                    console.error('Error when sending file:', error);
                    res.status(500).send('Failed to process file');
                });
            } catch (error) {
                console.error('Error when sending file:', error);
                res.status(500).send('Failed to process file');
            }
        });
    };
}

module.exports = ParseController;
