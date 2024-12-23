const SuperDao = require('./SuperDao');
const models = require('../models');

const Document = models.document;

class DocumentDao extends SuperDao {
    constructor() {
        super(Document);
    }

    // Check if a document exists by its name, its supplier, and its date
    isDocumentExists = async (doc_nr, supplier) => {
        try {
            console.log('Checking if document exists:', doc_nr, supplier);
            // Define the condition for finding the document
            const condition = {
                document_number: doc_nr,
                furnizor: supplier
            };
            // Use the inherited findOneByWhere method to check if the document exists
            const document = await this.findOneByWhere(condition);
            console.log('Document:', document);
            // Return the id if the document exists, otherwise -1
            return document ? document.id : -1;
        } catch (error) {
            console.error('Error checking if document exists:', error);
            throw error;
        }
    }
}

module.exports = DocumentDao;