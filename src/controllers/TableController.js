const httpStatus = require('http-status');
const TableService = require('../service/TableService');
const logger = require('../config/logger');


class TableController {
	constructor() {
		this.tableService = new TableService();
	}

	getAllRecords = async (req, res) => {
		try {
		// logger.info('Get all records');
			console.log('Get all records');
			const records = await this.tableService.getAllRecords();
			res.status(httpStatus.OK).send(records);
		} catch (e) {
			logger.error(e);
			res.status(httpStatus.BAD_GATEWAY).send(e);
		}
	};

	filterRecords = async (req, res) => {
		try {
			console.log(req.body);
			const records = await this.tableService.filterRecords(req.body);
			res.status(httpStatus.OK).send(records);
		} catch (e) {
			logger.error(e);
			res.status(httpStatus.BAD_GATEWAY).send(e);
		}
	};

	deleteRecord = async (req, res) => {
		try {
			const record = await this.tableService.deleteRecord(req.params.id);
			res.status(httpStatus.OK).send(record);
		} catch (e) {
			res.status(httpStatus.BAD_GATEWAY).send(e);
		}
	};

	updateProduct = async (req, res) => {
		try {
			console.log(req.body);
			const { id, ...data } = req.body;		
			const record = await this.tableService.updateProduct(data, id);
			res.status(httpStatus.OK).send("Product updated successfully");
		} catch (e) {
			console.log(e);
			res.status(httpStatus.BAD_GATEWAY).send(e);
		}
	};

	createProducts = async (req, res) => {
		try {
			console.log(req.body);
			console.log(req.body.doc);
			const record = await this.tableService.createProducts(req.body.doc, req.body.supplier, req.body.products);
			res.status(httpStatus.OK).send(record);
		} catch (e) {
			res.status(httpStatus.BAD_GATEWAY).send(e);
		}
	};

}

module.exports = TableController;