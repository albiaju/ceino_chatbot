import React, { useState, useRef } from 'react';

function PDFUploader() {
  const [pdfFile, setPdfFile] = useState(null);
  const [filename, setFilename] = useState('');
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
    } else {
      alert('Please select a PDF file');
    }
  };

  const handleUpload = async () => {
    if (!pdfFile) {
      alert('Please select a PDF file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', pdfFile);

    try {
      console.log('Uploading file:', pdfFile.name);

      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      });

      console.log('Response status:', response.status);

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Upload failed');
      }

      const data = await response.json();
      setFilename(data.filename);
      alert('PDF uploaded successfully!');
    } catch (error) {
      console.error('Upload error:', error);
      alert(`Upload failed: ${error.message}`);
    }
  };

  return (
    <div className="pdf-uploader">
      <h2>PDF Chat Assistant</h2>

      <div className="upload-section">
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          ref={fileInputRef}
          style={{ display: 'none' }}
        />
        <button onClick={() => fileInputRef.current.click()}>
          Select PDF
        </button>

        {pdfFile && (
          <div className="file-info">
            <p>Selected: {pdfFile.name}</p>
            <p>Size: {(pdfFile.size / 1024).toFixed(2)} KB</p>
          </div>
        )}

        <button onClick={handleUpload} disabled={!pdfFile}>
          Upload & Process
        </button>
      </div>

      {filename && (
        <div className="upload-success">
          <p>Ready to chat about: {filename}</p>
        </div>
      )}
    </div>
  );
}

export default PDFUploader;