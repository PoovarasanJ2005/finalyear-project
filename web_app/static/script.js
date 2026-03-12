document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const scanZone = document.getElementById('scan-zone');
    const scanInput = document.getElementById('scan-input');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview-image');
    const removeBtn = document.getElementById('remove-btn');
    const predictBtn = document.getElementById('predict-btn');
    const loadingSpinner = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const bloodGroupEl = document.getElementById('blood-group');
    const confidenceEl = document.getElementById('confidence-score');

    // Drag & Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('active');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('active');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('active');
        handleFiles(e.dataTransfer.files);
    });

    // Click to upload
    dropZone.addEventListener('click', () => {
        if (!previewContainer.style.display || previewContainer.style.display === 'none') {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    // USB Scanner Simulation
    if (scanZone) {
        scanZone.addEventListener('click', () => {
            // Simulate connecting to external USB scanner
            const originalHtml = scanZone.innerHTML;
            scanZone.innerHTML = '<span class="upload-icon" style="font-size: 3.5rem;">🔄</span><h3 style="color:#22c55e;">Connecting scanner...</h3><p style="color:var(--text-main); opacity: 0.9;">Please wait.</p>';
            scanZone.style.pointerEvents = 'none';

            setTimeout(() => {
                scanZone.innerHTML = originalHtml;
                scanZone.style.pointerEvents = 'auto';
                if (!previewContainer.style.display || previewContainer.style.display === 'none') {
                    // Trigger the real file picker but pretend it's from the scanner device stream
                    scanInput.click();
                }
            }, 1500);
        });

        scanInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });
    }

    // Handle selected files
    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();

                reader.onload = (e) => {
                    previewImage.src = e.target.result;
                    previewContainer.style.display = 'flex';
                    if (dropZone) dropZone.style.display = 'none';
                    if (scanZone) {
                        scanZone.style.display = 'none';
                        scanZone.nextElementSibling.style.display = 'none'; // hide the "OR" text block
                    }
                    predictBtn.disabled = false;
                    resultContainer.style.display = 'none';
                };

                reader.readAsDataURL(file);
                // Store file for sending
                window.selectedFile = file;
            } else {
                alert('Please upload an image file (JPG, PNG, BMP).');
            }
        }
    }

    // Remove Image
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent triggering dropZone click
        previewImage.src = '';
        previewContainer.style.display = 'none';
        if (dropZone) dropZone.style.display = 'block';
        if (scanZone) {
            scanZone.style.display = 'block';
            scanZone.nextElementSibling.style.display = 'flex'; // show the "OR" text block
        }
        predictBtn.disabled = true;
        resultContainer.style.display = 'none';
        if (fileInput) fileInput.value = '';
        if (scanInput) scanInput.value = '';
        window.selectedFile = null;
    });

    // Predict
    predictBtn.addEventListener('click', async () => {
        if (!window.selectedFile) return;

        // UI Prep
        predictBtn.style.display = 'none';
        loadingSpinner.style.display = 'block';
        resultContainer.style.display = 'none';

        const formData = new FormData();
        formData.append('image', window.selectedFile);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                bloodGroupEl.textContent = result.blood_group;
                confidenceEl.textContent = `Confidence: ${result.confidence}`;
                resultContainer.style.display = 'block';
            } else {
                alert('Error: ' + (result.error || 'Unknown error occurred.'));
            }
        } catch (error) {
            console.error('Prediction failed:', error);
            alert('Failed to connect to the server.');
        } finally {
            predictBtn.style.display = 'block';
            loadingSpinner.style.display = 'none';
        }
    });
});
