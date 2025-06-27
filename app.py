from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from fpdf import FPDF
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'your-secret-key'

# Resume Form
class ResumeForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone')
    address = TextAreaField('Address')
    education = TextAreaField('Education', validators=[DataRequired()])
    experience = TextAreaField('Work Experience', validators=[DataRequired()])
    skills = TextAreaField('Skills', validators=[DataRequired()])
    submit = SubmitField('Generate Resume')

# Generate PDF
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt=data['name'], ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Email: {data['email']} | Phone: {data['phone']}", ln=True, align='C')
    pdf.cell(200, 10, txt=data['address'], ln=True, align='C')
    pdf.ln(10)

    # Sections
    sections = [
        ("Education", data['education']),
        ("Work Experience", data['experience']),
        ("Skills", data['skills'])
    ]

    for title, content in sections:
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(200, 10, txt=title, ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=content)
        pdf.ln(5)

    # Save PDF
    pdf_path = "static/resume.pdf"
    pdf.output(pdf_path)
    return pdf_path

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    form = ResumeForm()
    if form.validate_on_submit():
        resume_data = {
            'name': form.name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'address': form.address.data,
            'education': form.education.data,
            'experience': form.experience.data,
            'skills': form.skills.data
        }
        pdf_path = generate_pdf(resume_data)
        return redirect(url_for('resume'))
    return render_template('index.html', form=form)

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/download')
def download():
    return send_file("static/resume.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)