const express = require('express');
// const AuthController = require('../controllers/AuthController');
// const UserValidator = require('../validator/UserValidator');

const router = express.Router();
const TableController = require('../controllers/TableController');
const TableValidator = require('../validator/TableValidator');
const ParseController = require('../controllers/ParseController');

const tableController = new TableController();
const tableValidator = new TableValidator();
const parseController = new ParseController();

// Route for fetching all santier product records from the database
router.get('/', tableController.getAllRecords);

// ROute for filtering santier products by specific filters in json format
router.post('/filter', tableController.filterRecords);

// Route for deleting a record from the database
router.delete('/delete', tableController.deleteRecord);

// Route for updating a product record in the database
router.put('/update', tableValidator.productUpdateValidator, tableController.updateProduct);

// Route for creating a new product record in the database
router.post('/docs/add', tableValidator.productsCreateValidator, tableController.createProducts);

// Route for adding a document, supplier and the products extracted from the document

router.post('/parse', parseController.copyFile);
module.exports = router;
