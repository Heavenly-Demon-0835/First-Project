const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('file');
const submitBtn = document.getElementById('submitBtn');
const uploadForm = document.getElementById('uploadForm');
const selectedFile = document.createElement('div');

selectedFile.className = 'selected-file';
uploadArea.appendChild(selectedFile);

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => {
        uploadArea.classList.add('dragover');
    }, false);
});

['dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => {
        uploadArea.classList.remove('dragover');
    }, false);
});

uploadArea.addEventListener('drop', (e) => {
    let dt = e.dataTransfer;
    let files = dt.files;
    fileInput.files = files;
    updateFileName();
});

fileInput.addEventListener('change', updateFileName);

function updateFileName() {
    if (fileInput.files.length > 0) {
        selectedFile.style.display = 'block';
        selectedFile.textContent = 'Selected: ' + fileInput.files[0].name;
    } else {
        selectedFile.style.display = 'none';
    }
}

uploadForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (fileInput.files.length > 0) {
        submitBtn.classList.add('loading');
        submitBtn.querySelector('span').textContent = 'Uploading...';
        submitBtn.disabled = true;
        
        const progressText = document.getElementById('progressText');
        progressText.style.display = 'block';
        progressText.textContent = 'Starting process...';

        const formData = new FormData(uploadForm);
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if(data.error) {
                alert(data.error);
                resetUI();
                return;
            }
            pollStatus(data.task_id);
        })
        .catch(err => {
            alert('Upload failed.');
            resetUI();
        });
    }
});

function pollStatus(taskId) {
    const progressText = document.getElementById('progressText');
    const interval = setInterval(() => {
        fetch(`/status/${taskId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'processing') {
                submitBtn.querySelector('span').textContent = 'Processing...';
                if(data.total > 0) {
                    progressText.textContent = `Processing song: ${data.current} of ${data.total}`;
                }
            } else if (data.status === 'completed') {
                clearInterval(interval);
                progressText.textContent = 'Completed! Downloading...';
                submitBtn.querySelector('span').textContent = 'Done';
                submitBtn.classList.remove('loading');
                window.location.href = `/download/${taskId}`;
                setTimeout(resetUI, 3000);
            } else if (data.status === 'error') {
                clearInterval(interval);
                alert('Error: ' + data.error);
                resetUI();
            }
        });
    }, 1000);
}

function resetUI() {
    submitBtn.disabled = false;
    submitBtn.classList.remove('loading');
    submitBtn.querySelector('span').textContent = 'Process File';
    const progressText = document.getElementById('progressText');
    if(progressText) progressText.style.display = 'none';
    fileInput.value = '';
    selectedFile.style.display = 'none';
    uploadArea.classList.remove('dragover');
}
