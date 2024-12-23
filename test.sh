curl -X POST http://localhost:5000/api/tables/docs/add -H "Content-Type: application/json" -d '{
  "doc": {
    "furnizor": "Example Supplier",
    "data_intrare": "2023-10-01",
    "data_scadenta": "2023-12-01",
    "tip": 1,
    "document_number": "DOC12334"
  },
  "supplier": {
    "denumire": "Example Supplier",
    "cod_fiscal": "EX123456",
    "reg_com": "RC123456",
    "adresa": "123 Example St, City",
    "banca": "Example Bank",
    "cont_bancar": "RO49AAAA1B31007593840000",
    "persoana_contact": "John Doe",
    "telefon": "1234567890",
    "email": "contact@example.com"
  },
  "products": [
    {
      "denumire": "Product 1",
      "cantitate": 100,
      "pret": 15.50,
      "unitate_masura": "kg"
    },
    {
      "denumire": "Product 2",
      "cantitate": 200,
      "pret": 25.00,
      "unitate_masura": "kg"
    }
  ]
}' -v

