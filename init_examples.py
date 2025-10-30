from db_examples import ExampleDB
import os

def init_db_from_txt(txt_path="examples/sample.txt"):
    # Check if the text file exists
    if not os.path.exists(txt_path):
        print(f"[ERROR] {txt_path} not found.")
        return

    # Initialize the database
    db = ExampleDB("examples.db")

    # Read the text file line by line and insert non-empty lines into the DB
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
        for line in lines:
            db.insert_example(line)

    # Print how many lines were inserted
    print(f"[OK] {len(lines)} examples have been registered in the database.")

    # Close the database connection
    db.close()

if __name__ == "__main__":
    init_db_from_txt()
