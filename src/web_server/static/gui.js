
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
        for (var i = 0; i < num_of_nodes - succeeded_nodes_count; i++) {
            html += `
                <div class="node-label failed" id="node-label-${i}-${process_id}">Node ${i}: Failed</div>
                `;
        }
    } else {
        for (var i = 0; i < num_of_nodes - succeeded_nodes_count; i++) {
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
                <div id="node-status-container-${process_id}">
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

function processProgress(process_id, progress, num_of_nodes, num_of_succeeded_nodes) {
    const statusP = document.getElementById(`status-${process_id}`);
    statusP.innerHTML = `<strong>Status:</strong> ${getStatusName(3)}`;

    console.log(num_of_nodes, num_of_succeeded_nodes)
    const node_status = document.getElementById(`node-status-container-${process_id}`);
    node_status.innerHTML = getNodesStatus(process_id, num_of_nodes, num_of_succeeded_nodes, 3)

    const progress_text = document.getElementById(`progress-${process_id}`);
    progress_text.textContent = `${progress}%`;

    const progress_track = document.getElementById(`progress-main-${process_id}`)
    progress_track.style.width = progress + "%"
}

function processCompletion(process_id, downloadLink) {
    const statusP = document.getElementById(`status-${process_id}`);
    statusP.innerHTML = `<strong>Status:</strong> ${getStatusName(4)}`;

    const node_status = document.getElementById(`node-status-container-${process_id}`);
    node_status.innerHTML = getNodesStatus(process_id, node_status.querySelectorAll('div').length, node_status.querySelectorAll('div').length, 4)

    const progress_track = document.getElementById(`progress-main-${process_id}`)
    progress_track.remove()

    const processed_img = document.getElementById(`processed-img-${process_id}`);
    processed_img.src = downloadLink;

    const processed_img_card = document.getElementById(`processed-img-card-${process_id}`);
    processed_img_card.style.display = "";
}