from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# Function to write entries to CSV file
def write_to_csv(data):
    with open('entries.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Function to read entries from CSV file
def read_from_csv():
    entries = []
    with open('entries.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            entries.append(row)
    return entries

# Route for home page
@app.route('/')
def home():
    entries = read_from_csv()
    return render_template('index.html', entries=entries)

# Route for form submission
@app.route('/add_entry', methods=['POST'])
def add_entry():
    name = request.form['name']
    quote = request.form['quote']
    
    if not name or not quote:
        return "Name and Quote fields cannot be empty. Please go back and fill in all fields.", 400

    write_to_csv([name, quote])
    return redirect(url_for('home'))

# Route for deleting an entry
@app.route('/delete_entry/<int:index>', methods=['POST'])
def delete_entry(index):
    entries = read_from_csv()
    
    if 0 < index <= len(entries):
        del entries[index - 1]
        with open('entries.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(entries)
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
