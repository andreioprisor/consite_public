const Joi = require('joi');
const httpStatus = require('http-status');
const ApiError = require('../helper/ApiError');
const e = require('express');
const { error } = require('winston');

class TableValidator {
    constructor() {
        // Schema for validating documents
       this.productUpdateValidator = this.productUpdateValidator.bind(this);
       this.productsCreateValidator = this.productsCreateValidator.bind(this);
       this.docSchema = Joi.object({
            furnizor: Joi.string().max(100).required(),
            data_intrare: Joi.date().iso().required(),
            data_scadenta: Joi.date().iso().greater(Joi.ref('data_intrare')),
            tip: Joi.number().integer().required(),
            document_number: Joi.string().max(100).optional(),
            sup_id: Joi.number().integer().optional(),
        });

        // Schema for validating suppliers
        this.supplierSchema = Joi.object({
            denumire: Joi.string().max(100).required(),
            cod_fiscal: Joi.string().max(20).required(),
            reg_com: Joi.string().max(50).optional(),
            adresa: Joi.string().max(200).optional(),
            banca: Joi.string().max(50).optional(),
            cont_bancar: Joi.string().max(50).optional(),
            telefon: Joi.string().max(20).optional(),
            email: Joi.string().email().optional(),
            persoana_contact: Joi.string().max(100).optional(),
        });

        // Schema for validating products
        this.productSchema = Joi.object({
            id: Joi.number().integer().optional(),
            denumire: Joi.string().max(100).required(),
            doc_id: Joi.number().integer().optional(),
            cantitate: Joi.number().integer().min(1).required(),
            pret: Joi.number().precision(2).min(0).required(),
            unitate_masura: Joi.string().max(20).required(),
        });

        this.productUpdateSchema = Joi.object({
            id: Joi.number().integer().required(),
            denumire: Joi.string().max(100).optional(),
            doc_id: Joi.number().integer().optional(),
            cantitate: Joi.number().integer().min(1).optional(),
            pret: Joi.number().precision(2).min(0).optional(),
            unitate_masura: Joi.string().max(20).optional(),
        });
    }

	async productsCreateValidator(req, res, next) {
        const options = {
            abortEarly: false, // include all errors
            allowUnknown: true, // ignore unknown props
            stripUnknown: true, // remove unknown props
        };

        try {
            // Validate the products array
            console.log(req.body);
			const supplier = req.body.supplier || {};
			const doc = req.body.doc || {};
			const products = req.body.products || [];

			// Validate the document
			const { error: docError, value: docValue } = this.docSchema.validate(doc, options);
            console.log(doc);
			if (docError) {
                console.log(docError);
				const errorMessage = docError.details.map((details) => details.message).join(', ');
				throw new ApiError(httpStatus.BAD_REQUEST, `Document validation error: ${errorMessage}`);
			}
			req.body.doc = docValue; // Update the validated document

			// Validate the supplier
			const { error: supplierError, value: supplierValue } = this.supplierSchema.validate(supplier, options);
			if (supplierError) {
                console.log(supplierError);
				const errorMessage = supplierError.details.map((details) => details.message).join(', ');
				throw new ApiError(httpStatus.BAD_REQUEST, `Supplier validation error: ${errorMessage}`);
			}
			req.body.supplier = supplierValue; // Update the validated supplier

			// Validate the products
            for (let product of products) {
                console.log(product);
                const { error, value } = this.productSchema.validate(product, options);
                if (error) {
                    const errorMessage = error.details.map(details => details.message).join(', ');
                    throw new ApiError(httpStatus.BAD_REQUEST, `Products validation error: ${errorMessage}`);
                }
                product = value; // Update the validated product
            }

            // On success, replace req.body with validated values and call the next middleware function
            req.body.doc = doc;
            req.body.suppliers = supplier;
            req.body.products = products;
            console.log(doc);
            console.log(supplier);
            console.log(products);
            return next();
        } catch (error) {
            next(error);
        }
    }

	async productUpdateValidator(req, res, next) {
		const options = {
			abortEarly: false, // include all errors
			allowUnknown: true, // ignore unknown props
			stripUnknown: true, // remove unknown props
		};
		try {
			// Validate the product
			const { error, value } = this.productUpdateSchema.validate(req.body, options);
			if (error) {
                console.log("error");
				const errorMessage = error.details.map(details => details.message).join(', ');
				throw new ApiError(httpStatus.BAD_REQUEST, `Product validation error: ${errorMessage}`);
			}

			// On success, replace req.body with validated values and call the next middleware function
			req.body = value;
			return next();
		} catch (error) {
            console.log(error);
			next(error);
		}
	}
}

module.exports = TableValidator;