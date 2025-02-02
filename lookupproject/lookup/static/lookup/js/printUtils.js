export function setupDownloadButton() {
    const downloadButton = document.getElementById('download-button')
    const content = document.getElementById('downloadable-body')
    
    downloadButton.addEventListener('click', () => {
        console.log('click')
        triggerFileDownload(content)
    })
}

function triggerFileDownload(content) {
    html2pdf()
    .set({
        margin: 1,
        filename: 'participants.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    })
    .from(content)
    .save();
}