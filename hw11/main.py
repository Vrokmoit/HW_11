from fastapi import FastAPI, Request , HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from contactpr import models
from contactpr import schemas
from contactpr import database
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Добро пожаловать у мій FastAPI додаток!"}

# Створення сесії для роботи з базою даних
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Маршрут для створення нового контакту
@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Маршрут для отримання списку всіх контактів
@app.get("/contacts/", response_model=list[schemas.Contact])
def read_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts

# Маршрут для отримання одного контакту по його ідентифікатору
@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return contact

# Маршрут для оновлення контакту по його ідентифікатору
@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact_update: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    for key, value in contact_update.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Маршрут для видалення контакту по його ідентифікатору
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    db.delete(db_contact)
    db.commit()
    return {"message": "Контакт успішно видалено"}

# Маршрут для пошуку контактів за ім'ям, прізвищем або адресою електронної пошти
@app.get("/contacts/search/")
def search_contacts(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).filter(
        models.Contact.first_name.ilike(f"%{query}%") |
        models.Contact.last_name.ilike(f"%{query}%") |
        models.Contact.email.ilike(f"%{query}%")
    ).all()
    return contacts

# Маршрут для отримання списку контактів з днями народження в найближчі 7 днів
@app.get("/contacts/birthdays/")
def upcoming_birthdays(db: Session = Depends(get_db)):
    today = datetime.now().date()
    week_later = today + timedelta(days=7)
    upcoming_contacts = []

    # Отримання всіх контактів з бази даних
    all_contacts = db.query(models.Contact).all()

    # Ітерація через всі контакти для перевірки, чи має кожен контакт день народження в найближчій неділі
    for contact in all_contacts:
        if contact.birthday:
            birthday_this_year = datetime(today.year, contact.birthday.month, contact.birthday.day).date()
            if today <= birthday_this_year <= week_later:
                upcoming_contacts.append(contact)

    return upcoming_contacts