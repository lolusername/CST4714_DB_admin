const books = [
  {
    _id: 1,
    product_id: 34538756,
    title: 'MongoDB: The Definitive Guide: Powerful and Scalable Data Storage',
    details: 'MongoDB explained by MongoDB champions',
    authors: [ 'Shannon Bradshaw', 'Eoin Brazil', 'Christina Chodorow' ],
    publisher: "O'Reilly",
    language: 'English',
    pages: 514,
    catalogues: { isbn10: '1491954469', isbn13: '978-1491954461' }
  },
  {
    _id: 2,
    title: 'MongoDB: The Definitive Guide: Powerful and Scalable Data Storage',
    desc: 'MongoDB explained by MongoDB champions',
    authors: 'Shannon Bradshaw, Eoin Brazil, and Christina Chodorow',
    publisher: "O'Reilly",
    language: 'English',
    eformats: { epub: { pages: 774 }, pdf: { pages: 502 } },
    isbn10: '1491954469'
  },
  {
    _id: 3,
    product_id: 54538756,
    title: 'MongoDB: The Definitive Guide: Powerful and Scalable Data Storage',
    desc: 'The complete book of MongoDB by its employees',
    author: 'Eoin Brazil',
    narrator: 'Eoin Brazil',
    publisher: "O'Reilly",
    language: 'English',
    length_minutes: 1200
  }
]

print(books)