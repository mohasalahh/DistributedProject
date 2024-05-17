
function getOpName(opId) {
    if (opId == 1) {
        return "EDGE_DETECTION";
    } else if (opId == 2) {
        return "COLOR_INVERSION";
    } else if (opId == 3) {
        return "CONTRAST_ADJUSTMENT";
    }
}

function getStatusName(stateId) {
    if (stateId == 1) {
        return "STARTED";
    } else if (stateId == 2) {
        return "FAILED";
    } else if (stateId == 3) {
        return "PROGRESS";
    } else if (stateId == 4) {
        return "DONE";
    }
}

function addProcess(process_id, num_of_nodes, operation, state, node) {
    const statusContainer = document.getElementById('container');

    console.log(state)
    const statusItem = document.createElement('div');
    statusItem.className = 'container';
    statusItem.innerHTML = `
            <div id="status-container">
                <p><strong>Process id:</strong> ${process_id}</p>
                <p><strong>Operation:</strong> ${getOpName(operation)}</p>
                <p><strong>Status:</strong> ${getStatusName(state)}</p>
                <div class="progress-bar">
                    <div class="progress-bar-progress" id="progress-main-${process_id}" style="width: 0%">
                        <div class="progress-bar-text-progress">0%</div>
                    </div>
                </div>
                <div id="node-status-container">
                    <div class="node-status" id="node-status-${node}">
                        <div class="node-label in-progress" id="node-label-${node}-1">Node ${node}: In Progress</div>
                    </div>
                    <div class="node-status" id="node-status-${node}">
                        <div class="node-label in-progress" id="node-label-${node}-1">Node ${node}: In Progress</div>
                    </div>
                    <div class="node-status" id="node-status-${node}">
                        <div class="node-label in-progress" id="node-label-${node}-1">Node ${node}: In Progress</div>
                    </div>
                </div>

                <div class="done-state">
                    <div class="card">
                        <img src="your-image-url.jpg" alt="Image description">
                        <div class="card-text">Original Image</div>
                        <div class="download-icon">
                            <img src="download-icon-url.png" alt="Download">
                        </div>
                    </div>
                    <div class="card">
                        <img src="your-image-url.jpg" alt="Image description">
                        <div class="card-text">Original Image</div>
                        <div class="download-icon">
                            <img src="download-icon-url.png" alt="Download">
                        </div>
                    </div>
                </div>
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
