from flask import Flask, render_template, jsonify, request
import pyperclip

app = Flask(__name__)

# In-memory storage for copied data
copied_data = {
    'patient_name': '',
    'nhs_number': '',
    'history': '',
    'otoscopy': '',
    'pta': '',
    'imp': ''
}

@app.route('/')
def home():
    return render_template('index.html', copied_data=copied_data)

@app.route('/copy', methods=['POST'])
def copy_to_clipboard():
    field = request.form.get('field')
    text = request.form.get('text')

    if not field or not text:
        return jsonify({'error': 'Missing field or text'}), 400

    # Store the copied text in the relevant field
    copied_data[field] = text

    # Copy data to the clipboard
    try:
        pyperclip.copy(text)
    except Exception as e:
        return jsonify({'error': f'Failed to copy to clipboard: {str(e)}'}), 500

    return jsonify({'message': f'{field} copied to clipboard', 'text': text}), 200

@app.route('/paste', methods=['POST'])
def paste_from_clipboard():
    field = request.form.get('field')

    if field not in copied_data:
        return jsonify({'error': 'Invalid field'}), 400

    # Retrieve the copied text from clipboard
    try:
        clipboard_data = pyperclip.paste()
        copied_data[field] = clipboard_data
    except Exception as e:
        return jsonify({'error': f'Failed to paste from clipboard: {str(e)}'}), 500

    return jsonify({'message': f'{field} pasted from clipboard', 'text': clipboard_data}), 200

@app.route('/reset', methods=['POST'])
def reset_clipboard():
    # Reset the in-memory clipboard data
    for key in copied_data:
        copied_data[key] = ''

    # Also clear the system clipboard
    pyperclip.copy('')

    return jsonify({'message': 'Clipboard reset'}), 200

if __name__ == '__main__':
    app.run(debug=True)
