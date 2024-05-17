
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
        return "In Queue";
    } else if (stateId == 2) {
        return "FAILED";
    } else if (stateId == 3) {
        return "PROGRESS";
    } else if (stateId == 4) {
        return "DONE";
    }
}

function getNodesStatus(process_id, num_of_nodes, succeeded_nodes_count, state) {
    let html = "";

    for (var i = 0; i < succeeded_nodes_count; i++) {
        html += `
            <div class="node-label completed" id="node-label-${i}-${process_id}">Node ${i}: Completed</div>
            `;
    }

    if (state == 2) {
        for (var i = succeeded_nodes_count - 1; i < num_of_nodes - succeeded_nodes_count; i++) {
            html += `
                <div class="node-label failed" id="node-label-${i}-${process_id}">Node ${i}: Failed</div>
                `;
        }
    } else {
        for (var i = succeeded_nodes_count - 1; i < num_of_nodes - succeeded_nodes_count; i++) {
            html += `
                <div class="node-label in-progress" id="node-label-${i}-${process_id}">Node ${i}: In Progress</div>
                `;
        }
    }
    return html;
}

function addProcess(process_id, num_of_nodes, operation, state, file_name, num_of_succeeded_nodes) {
    const statusContainer = document.getElementById('container');

    const statusItem = document.createElement('div');
    statusItem.className = 'container';
    statusItem.innerHTML = `
            <div id="status-container">
                <p><strong>Process id:</strong> ${process_id}</p>
                <p><strong>Operation:</strong> ${getOpName(operation)}</p>
                <p id="status-${process_id}"><strong>Status:</strong> ${getStatusName(state)}</p>
                <div class="progress-bar" style="${state == 1 || state == 3 ? "" : "display: none;"}">
                    <div class="progress-bar-progress" id="progress-main-${process_id}" style="width: 0%">
                        <div class="progress-bar-text-progress" id="progress-${process_id}">0%</div>
                    </div>
                </div>
                <div id="node-status-container">
                ${getNodesStatus(process_id, num_of_nodes, num_of_succeeded_nodes, state)}
                </div>

                <div class="done-state">
                    <div class="card">
                        <img src="../uploaded_imgs/${file_name}" alt="Original Image">
                        <div class="card-text">Original Image</div>
                        <a href="../uploaded_imgs/${file_name}" download="original-image-${process_id}.png">
                        <div class="download-icon">
                            <i class="fa-solid fa-download"></i>
                        </div>
                        </a>
                    </div>
                    <div class="card" id="processed-img-card-${process_id}" style="${state == 4 ? "" : "display: none;"}">
                        <img id="processed-img-${process_id}" src="../processed_imgs/${process_id}.png" alt="Processed Image">
                        <div class="card-text">Processed Image</div>
                        <a href="../processed_imgs/${process_id}.png" download="processed-image-${process_id}.png">
                        <div class="download-icon">
                            <i class="fa-solid fa-download"></i>
                        </div>
                        </a>
                    </div>
                </div>
            </div>
    `;
    statusContainer.appendChild(statusItem);
}

function processStarted(process_id) {
    const statusP = document.getElementById(`status-${process_id}`);
    statusP.innerHTML = `<strong>Status:</strong> ${getStatusName(1)}`;
}

function processProgress(process_id, progress) {
    const statusP = document.getElementById(`status-${process_id}`);
    statusP.innerHTML = `<strong>Status:</strong> ${getStatusName(3)}`;

    const progress_text = document.getElementById(`progress-${process_id}`);
    progress_text.textContent = `${progress}%`;

    const progress_track = document.getElementById(`progress-main-${process_id}`)
    progress_track.style.width = progress + "%"
}

function processCompletion(process_id, downloadLink) {
    const statusP = document.getElementById(`status-${process_id}`);
    statusP.innerHTML = `<strong>Status:</strong> ${getStatusName(4)}`;

    const progress_track = document.getElementById(`progress-main-${process_id}`)
    progress_track.remove()

    const processed_img = document.getElementById(`processed-img-${process_id}`);
    processed_img.src = downloadLink;

    const processed_img_card = document.getElementById(`processed-img-card-${process_id}`);
    processed_img_card.style.display = "";
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
