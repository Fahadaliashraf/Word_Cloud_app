import streamlit as st
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import PyPDF2
from docx import Document
import base64
from io import BytesIO

# Function for file reading
def read_txt(file):
    return file.getvalue().decode("utf-8")

def read_docx(file):
    doc = Document(file)
    return "".join([para.text for para in doc.paragraphs])

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() if page.extract_text() else ''
    return text

# Function to filter out stopwords
def filter_stopwords(text, additional_stopwords=[]):
    words = text.split()
    all_stopwords = STOPWORDS.union(set(additional_stopwords))
    filtered_words = [word for word in words if word.lower() not in all_stopwords]
    return " ".join(filtered_words)

# Function to generate a download link for a DataFrame
def get_table_download_link(df, filename, file_label):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{file_label}</a>'

# Streamlit application setup
st.title("🌌 Word Cloud Generator")
st.markdown("""
This application allows you to create word clouds from text files, PDFs, and Word documents. Upload your file, customize your inputs, and generate your visualization.
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📁 Choose a file", type=["pdf", "docx", "txt"], help="Upload a PDF, DOCX, or TXT file only.")

if uploaded_file:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.write(file_details)

    # Check the file type and read the file
    if uploaded_file.type == "text/plain":
        text = read_txt(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        text = read_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = read_docx(uploaded_file)
    else:
        st.error("File type not supported. Please upload a txt, pdf or docx file.")
        st.stop()

    # Filtering stopwords
    st.subheader("Filter out stop words")
    additional_stopwords = st.text_input("Enter additional stop words (comma-separated):", "")
    additional_stopwords = set(word.strip() for word in additional_stopwords.split(",") if word.strip())
    filtered_text = filter_stopwords(text, additional_stopwords)

    # Generate word cloud
    st.subheader("Generate Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(filtered_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot()  # Display the plot

    # Display word count
    st.subheader("Word Count")
    word_count = len(filtered_text.split())
    st.write(f"Total words: {word_count}")

    # Display word frequency
    st.subheader("Word Frequency")
    word_freq = pd.Series(filtered_text.split()).value_counts().reset_index()
    word_freq.columns = ["Word", "Frequency"]
    st.table(word_freq)

    # Download word frequency as CSV
    st.markdown(get_table_download_link(word_freq, "word_frequency.csv", "Download Word Frequency"), unsafe_allow_html=True)

# Sidebar content
import streamlit as st

# Custom CSS to inject for styling
st.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: #f1f3f6 !important;
}
</style>
""", unsafe_allow_html=True)



import streamlit as st

# Custom CSS to style the sidebar
st.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: #f1f3f6 !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar with application information and useful links
st.sidebar.title("📖 About the App")

# Introducing the app with an icon
st.sidebar.info(
    """
    🌐 **Word Cloud Generator** allows you to visualize the frequency of word usage in text files, PDFs, and Word documents.
    Simply upload your document, and the application will help you see the most predominant words, excluding common stopwords.
    """
)

# Step-by-step usage instructions with icons
st.sidebar.header("🛠 How to Use the App")
st.sidebar.text("📤 Upload your document.")
st.sidebar.text("⚙ Adjust settings if necessary.")
st.sidebar.text("🖼 View the generated word cloud.")
st.sidebar.text("📥 Download the results.")

# Providing additional resources with an icon
st.sidebar.header("📚 Learn More")
st.sidebar.write(
    "Discover more about natural language processing and data visualization by visiting our [GitHub repository](https://github.com/FahadAliAshraf)."
)

# Contact information with an icon
st.sidebar.header("📬 Contact Us")
st.sidebar.write("Questions or feedback? [Send us an email](mailto:fahadali614@gmail.com).")

# Interactive elements for user engagement with an icon
st.sidebar.header("📋 Participate in Our Survey")
if st.sidebar.button("📊 Take Survey"):
    st.sidebar.write("Thank you for your interest! Please, visit our website to take the survey.")

# Link to additional resources or tutorials with an icon
st.sidebar.header("🎥 Tutorials")
st.sidebar.write("For detailed tutorials on how to create word clouds, check out our [YouTube channel](https://youtube.com/).")

