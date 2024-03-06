from app import app,database_model,db

with app.app_context():
    #book1 = database_model("Book 2", "Harry Potter")

    #db.session.add(book1)
    #db.session.commit()
    # Query all records from the database_model
    all_records = database_model.query.all()

    # Print the retrieved records
    for record in all_records:
        print(record)

    