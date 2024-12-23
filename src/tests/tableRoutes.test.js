const request = require('supertest');
const express = require('express');
const bodyParser = require('body-parser');

const app = require('../app');
app.use(bodyParser.json()); // Middleware for parsing JSON

describe('Table Routes', () => {
    // Test for fetching all records
    // test('GET /api/tables should fetch all records', async () => {
    //     const response = await request(app).get('/api/tables');
    //     expect(response.statusCode).toBe(200);
    //     expect(Array.isArray(response.body)).toBe(true);
    // });

    // Test for filtering records
    // test('POST /api/tables/filter should filter records based on filters', async () => {
    //     const filters = { denumire: 'Teava PVC 1 inch', pret: [10, 50] };
    //     const response = await request(app)
    //         .post('/api/tables/filter')
    //         .send(filters);
    //     expect(response.statusCode).toBe(200);
    //     expect(Array.isArray(response.body)).toBe(true);
    // });

    // // Test for deleting a record
    // test('DELETE /api/tables/:id should delete a record', async () => {
    //     const recordId = 1; // Example record ID
    //     const response = await request(app).delete(`/api/tables/${recordId}`);
    //     expect(response.statusCode).toBe(200);
    //     expect(response.body.message).toBe('Record deleted successfully');
    // });

    // Test for updating a product record
    // test('PUT /api/tables/products/:id should update a product record', async () => {
    //     const updatedProductData = {
    //         id: 1,
    //         denumire: 'Teava PVC 1 inch',
    //         cantitate: 30,
    //         pret: 15.99,
    //         unitate_masura: 'M',
    //     };
    //     const response = await request(app)
    //         .put(`/api/tables/update`)
    //         .send(updatedProductData);
    //     expect(response.statusCode).toBe(200);
    //     // expect(response.body.message).toBe('Product updated successfully');
    // });

    // Test for creating a new product record
    test('POST /api/tables/products/add should create a new product record', async () => {
        const new_doc_req = {
            doc: {
                furnizor: 'SC Rominstal SRL',
                data_intrare: '2021-07-01',
                data_scadenta: '2021-07-30',
                tip: 1,
                document_number: '1234567',
            },
            supplier: {
                denumire: 'SC Rominstal SRL',
                cod_fiscal: '123456',
                reg_com: '123456',
                adresa: 'Str. X',
                banca: 'BCR',
                cont_bancar: 'RO123456',
                telefon: '123456',
                email: 'daniel.mocanu@gmail.com'
            },
            products: [
                {
                    denumire: 'Robinet Inchidere 1 inch',
                    cantitate: 30,
                    pret: 152.99,
                    unitate_masura: 'Buc',
                },
                {
                    denumire: 'Teava Inox 1 inch',
                    cantitate: 20,
                    pret: 25.99,
                    unitate_masura: 'Buc',
                },
            ],
        }
        const response = await request(app)
            .post('/api/tables/docs/add')
            .send(new_doc_req);
        expect(response.statusCode).toBe(200);
    });
});
