document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const images = document.getElementById('images').files;
    const operation = document.getElementById('operation').value;
    
    for (let i = 0; i < images.length; i++) {
        processImage(images[i], operation, i + 1); // Mock node assignment
    }
});

function processImage(image, operation, node) {
    const statusContainer = document.getElementById('status-container');

    const statusItem = document.createElement('div');
    statusItem.className = 'status-item';
    statusItem.innerHTML = `
        <p><strong>Image:</strong> ${image.name}</p>
        <p><strong>Operation:</strong> ${operation}</p>
        <div class="progress-bar"><div id="progress-main-${node}" style="width: 0%">0%</div></div>
        <p><strong>Status:</strong> In Progress</p>
        <div class="node-status" id="node-status-${node}">
            <div class="node-label in-progress" id="node-label-${node}-1">Node ${node}: In Progress</div>
        </div>
    `;
    statusContainer.appendChild(statusItem);

    // Simulate progress
    setTimeout(() => {
        updateProgress(node, 50);
    }, 1000);

    setTimeout(() => {
        updateProgress(node, 75);
    }, 2000);

    // Simulate completion
    setTimeout(() => {
        completeProcessing(node, image, true);
    }, 3000);

    // Uncomment to simulate a failure state
    // setTimeout(() => {
    //     completeProcessing(node, image, false);
    // }, 4000);
}

function updateProgress(node, percentage) {
    const mainProgressBar = document.getElementById(`progress-main-${node}`);
    const nodeLabel = document.getElementById(`node-label-${node}-1`);

    mainProgressBar.style.width = `${percentage}%`;
    mainProgressBar.textContent = `${percentage}%`;

    nodeLabel.textContent = `Node ${node}: In Progress (${percentage}%)`;
}

function completeProcessing(node, image, success) {
    const mainProgressBar = document.getElementById(`progress-main-${node}`);
    const nodeLabel = document.getElementById(`node-label-${node}-1`);
    const statusItem = mainProgressBar.closest('.status-item');

    if (success) {
        mainProgressBar.style.width = '100%';
        mainProgressBar.textContent = '100%';
        mainProgressBar.classList.add('success');

        nodeLabel.textContent = `Node ${node}: Completed`;
        nodeLabel.classList.remove('in-progress');
        nodeLabel.classList.add('completed');

        const doneState = document.createElement('div');
        doneState.className = 'done-state';
        doneState.innerHTML = `
            <img src="${URL.createObjectURL(image)}" alt="original">
            <img src="${URL.createObjectURL(image)}" alt="processed">
            <p><a href="${URL.createObjectURL(image)}" download="processed_${image.name}">Download Processed Image</a></p>
        `;
        statusItem.appendChild(doneState);
    } else {
        mainProgressBar.classList.add('failed');
        mainProgressBar.textContent = 'Failed';

        nodeLabel.textContent = `Node ${node}: Failed`;
        nodeLabel.classList.remove('in-progress');
        nodeLabel.classList.add('failed');

        const alert = document.createElement('div');
        alert.className = 'alert';
        alert.textContent = `Processing failed at node ${node}`;
        statusItem.appendChild(alert);
    }
}
