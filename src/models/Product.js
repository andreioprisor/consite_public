const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
    class Product extends Model {
        static associate(models) {
            Product.belongsTo(models.document, { foreignKey: 'doc_id', targetKey: 'id' });
            Product.belongsTo(models.supplier, { foreignKey: 'sup_id', targetKey: 'id' });
        }
    }

    Product.init({
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true,
        },
        denumire: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        doc_id: {
            type: DataTypes.INTEGER,
            allowNull: false,
        },
        cantitate: {
            type: DataTypes.INTEGER,
            allowNull: false,
        },
        pret: {
            type: DataTypes.FLOAT,
            allowNull: true,
        },
        unitate_masura: {
            type: DataTypes.STRING,
            allowNull: true,
        },
        sup_id: {
            type: DataTypes.INTEGER,
            allowNull: true,
        },
    }, {
        sequelize,
        modelName: 'product',
        underscored: true,
        timestamps: false, // Disable automatic timestamps if not needed
    });

    return Product;
};
