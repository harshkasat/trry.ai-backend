from table_orm import Session
session = Session()

# Insert a new record into a table
def insert_record(session, record):
    try:
        session.add(record)
        session.commit()
        print("Record added successfully!")
        return record.url_id # return primary key
    except Exception as e:
        session.rollback()
        print(f"Error adding record: {e}")

# Delete a record from a table
def delete_record(session, table_class, record_id):
    try:
        record = session.query(table_class).get(record_id)
        if record:
            session.delete(record)
            session.commit()
            print("Record deleted successfully!")
        else:
            print("Record not found!")
    except Exception as e:
        session.rollback()
        print(f"Error deleting record: {e}")

# Update a record in a table
def update_record(session, table_class, record_id, update_data):
    try:
        record = session.query(table_class).get(record_id)
        if record:
            for key, value in update_data.items():
                setattr(record, key, value)
            session.commit()
            print("Record updated successfully!")
        else:
            print("Record not found!")
    except Exception as e:
        session.rollback()
        print(f"Error updating record: {e}")

# Select records from a table
def select_records(session, table_class, filters=None):
    try:
        query = session.query(table_class)
        if filters:
            query = query.filter_by(**filters)
        records = query.all()
        return records
    except Exception as e:
        print(f"Error selecting records: {e}")
        return []


if __name__ == "__main__":
    from table_orm import URLTable, ExtraURLTable
    session = Session()
    new_url = URLTable(url_website="https://example.com")
    insert_record(session, new_url)
    extra_urls = select_records(session, ExtraURLTable, {"url_id": 1})
    print(extra_urls)