package domain

import (
	"bytes"
	"fmt"
	"io"
	"strings"

	"github.com/ledongthuc/pdf"
)

// ExtractTextFromPDF extracts text content from a PDF file
func ExtractTextFromPDF(pdfData []byte) (string, error) {
	// Create a reader from the PDF data
	reader := bytes.NewReader(pdfData)

	// Open the PDF
	pdfReader, err := pdf.NewReader(reader, int64(len(pdfData)))
	if err != nil {
		return "", fmt.Errorf("failed to open PDF: %w", err)
	}

	// Extract text from all pages
	var extractedText strings.Builder
	numPages := pdfReader.NumPage()

	for pageNum := 1; pageNum <= numPages; pageNum++ {
		page := pdfReader.Page(pageNum)
		if page.V.IsNull() {
			continue
		}

		// Extract text from the page
		text, err := page.GetPlainText(nil)
		if err != nil {
			// Log error but continue with other pages
			continue
		}

		extractedText.WriteString(text)
		extractedText.WriteString("\n")
	}

	// Get the final text
	result := extractedText.String()

	// Clean up the text - remove excessive whitespace while preserving structure
	result = cleanPDFText(result)

	if result == "" {
		return "", fmt.Errorf("no text content found in PDF")
	}

	return result, nil
}

// cleanPDFText removes excessive whitespace while preserving document structure
func cleanPDFText(text string) string {
	// Split into lines
	lines := strings.Split(text, "\n")

	var cleaned []string
	for _, line := range lines {
		// Trim whitespace from each line
		trimmed := strings.TrimSpace(line)
		// Only include non-empty lines
		if trimmed != "" {
			cleaned = append(cleaned, trimmed)
		}
	}

	// Join with single newlines
	return strings.Join(cleaned, "\n")
}

// IsPDF checks if the given mime type indicates a PDF file
func IsPDF(mimeType string) bool {
	return strings.HasPrefix(mimeType, "application/pdf")
}

// ExtractTextFromPDFReader extracts text from a PDF using an io.Reader
func ExtractTextFromPDFReader(reader io.Reader) (string, error) {
	// Read all data from the reader
	data, err := io.ReadAll(reader)
	if err != nil {
		return "", fmt.Errorf("failed to read PDF data: %w", err)
	}

	return ExtractTextFromPDF(data)
}
