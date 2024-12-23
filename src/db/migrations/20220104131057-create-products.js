module.exports = {
    up: async (queryInterface, Sequelize) => {
        await queryInterface.createTable('products', {
            id: {
                allowNull: false,
                autoIncrement: true,
                primaryKey: true,
                type: Sequelize.INTEGER,
            },
            denumire: {
                type: Sequelize.STRING,
                allowNull: false,
            },
            doc_id: {
                type: Sequelize.INTEGER,
                allowNull: false,
                references: {
                    model: 'documents', // Table that this foreign key refers to
                    key: 'id',          // Column in the referenced table
                },
            },
            cantitate: {
                type: Sequelize.INTEGER,
                allowNull: false,
            },
            pret: {
                type: Sequelize.FLOAT,
                allowNull: true,
            },
            unitate_masura: {
                type: Sequelize.STRING,
                allowNull: true,
            },
            sup_id: {
                type: Sequelize.INTEGER,
                allowNull: true,
                references: {
                    model: 'suppliers', // Table that this foreign key refers to
                    key: 'id',          // Column in the referenced table
                },
            },
        });
    },

    down: async (queryInterface, Sequelize) => {
        await queryInterface.dropTable('products');
    },
};
